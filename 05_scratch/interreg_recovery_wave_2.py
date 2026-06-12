#!/usr/bin/env python3
"""
Interreg max-recovery wave 2.

Wave 2 preserves the 1506 current ready rows and re-processes the 909 residual
not-ready organizations with deeper recrawling on official sites:
- homepage recrawl
- internal contact/about/team/legal pages
- robots/sitemap contact discovery
- same-domain PDF extraction
- limited Bing discovery when no website is available or the current website fails
"""

from __future__ import annotations

import base64
import csv
import os
import re
import ssl
import subprocess
import tempfile
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from typing import Iterable

from bs4 import BeautifulSoup

BASE = Path("/home/reboot/Escritorio/agentic-scrapping-Experiment-scrappling")
CURRENT = BASE / "04_outputs/skilland-knowledge-transfer-engine/interreg_mac/06_enriched_leads"
STAGING = BASE / "05_scratch/interreg_recovery_wave_2"
STAGING.mkdir(parents=True, exist_ok=True)

NORMALIZED_CSV = CURRENT / "interreg_partner_leads_normalized.csv"
ENRICHMENT_LOG_CSV = CURRENT / "interreg_partner_leads_email_enrichment_log.csv"
READY_CSV = CURRENT / "interreg_partner_leads_outreach_ready.csv"
NOT_READY_CSV = CURRENT / "interreg_partner_leads_not_ready.csv"
README = CURRENT / "README.md"
WEBSITE_DISCOVERY_LOG = STAGING / "interreg_partner_website_discovery_log.csv"
CONTACT_RECOVERY_LOG = STAGING / "interreg_partner_contact_recovery_log.csv"

ENRICHED_AT = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b")
SKIP_EXT_RE = re.compile(r"\.(?:jpe?g|png|gif|svg|webp|ico|css|js|xml|json|zip|rar)(?:$|\?)", re.I)
PDF_RE = re.compile(r"\.pdf(?:$|\?)", re.I)
CONTACT_HINTS = {
    "contact", "contacts", "contact-us", "contacto", "contactos", "contatti",
    "about", "about-us", "who-we-are", "chi-siamo", "team", "staff", "people",
    "directory", "impressum", "legal", "privacy", "aviso-legal", "governance",
    "offices", "office", "administration", "secretariat",
}
GENERIC_LOCALS = {
    "info", "contact", "contacto", "office", "hello", "hola", "mail", "email", "admin",
    "support", "enquiries", "enquiry", "general", "communication", "secretariat",
}
BAD_MARKERS = (
    "sentry.wixpress.com",
    "wixpress.com",
    "osm.org",
    "example.com",
    "example.org",
    "example.net",
    "localhost",
    "@2x",
)
PROJECT_DOMAINS = {
    "atlanticarea.eu",
    "interreg-med.eu",
    "interregnextmed.eu",
    "mac-interreg.org",
    "interreg-euro-med.eu",
    "keep.eu",
}
DISCOVERY_EXCLUDED_DOMAINS = {
    "facebook.com", "linkedin.com", "instagram.com", "youtube.com", "youtu.be",
    "x.com", "twitter.com", "wikipedia.org", "keep.eu", "mapcarta.com",
}
GATEWAY_MARKERS = ("legalmail.it", ".legalmail.it", "pec.it", ".pec.", ".pec", "hs01.kep.tr", ".kep.tr", "cert.")
STOPWORDS = {
    "the", "and", "for", "with", "from", "del", "della", "degli", "delle", "dels", "des", "der",
    "los", "las", "les", "para", "por", "con", "per", "della", "dello", "dell", "di", "de",
    "du", "la", "le", "el", "al", "da", "do", "of", "in", "on", "at", "to", "y", "e",
    "un", "una", "uno", "a", "l", "d", "et", "sur", "pour",
}
ROBOTS_SITEMAPS = ("/robots.txt",)
SITEMAP_CANDIDATES = ("/sitemap.xml", "/sitemap_index.xml", "/wp-sitemap.xml", "/sitemap-index.xml")
MAX_INTERNAL_PAGES = 4
MAX_SITEMAP_PAGES = 0
MAX_PDFS = 0
MAX_DISCOVERY_RESULTS = 5
MAX_WORKERS = 12


@dataclass
class FetchResult:
    url: str
    final_url: str
    status: str
    content_type: str
    body: bytes
    error: str = ""


@dataclass
class CandidateEmail:
    email: str
    source_url: str
    source_type: str


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict], fields: list[str]):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFKD", value or "")
    value = value.encode("ascii", "ignore").decode("ascii")
    return value.lower()


def text_tokens(value: str) -> list[str]:
    tokens = re.findall(r"[a-z0-9]+", normalize_text(value))
    return [token for token in tokens if len(token) >= 4 and token not in STOPWORDS]


def split_pipe(value: str) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.split("|") if part.strip()]


def extract_domain(url: str) -> str:
    if not url:
        return ""
    if "://" not in url:
        url = "https://" + url.lstrip("/")
    host = urllib.parse.urlparse(url).netloc.lower().strip()
    if host.startswith("www."):
        host = host[4:]
    return host


def root_domain(domain: str) -> str:
    parts = domain.split(".")
    if len(parts) <= 2:
        return domain
    return ".".join(parts[-2:])


def is_project_domain(url_or_domain: str) -> bool:
    domain = extract_domain(url_or_domain) if "://" in (url_or_domain or "") else (url_or_domain or "").lower().strip()
    return domain in PROJECT_DOMAINS or root_domain(domain) in PROJECT_DOMAINS


def domain_matches(org_domain: str, email_domain: str) -> bool:
    return bool(org_domain and email_domain) and (
        email_domain == org_domain
        or email_domain.endswith("." + org_domain)
        or org_domain.endswith("." + email_domain)
    )


def gateway_email(email_domain: str) -> bool:
    return any(marker in email_domain for marker in GATEWAY_MARKERS)


def canonical_homepage(url: str) -> str:
    if not url:
        return ""
    raw = url.strip()
    if "://" not in raw:
        raw = "https://" + raw
    parsed = urllib.parse.urlparse(raw)
    host = parsed.netloc or parsed.path
    path = parsed.path if parsed.netloc else ""
    scheme = parsed.scheme if parsed.scheme in {"http", "https"} else "https"
    if host.startswith("www.") or host:
        return urllib.parse.urlunparse(("https", host, "/", "", "", ""))
    return urllib.parse.urlunparse((scheme, host, path or "/", "", "", ""))


def ensure_url(url: str, base_url: str = "") -> str:
    if not url:
        return ""
    return urllib.parse.urljoin(base_url or "", url)


def make_request(url: str) -> urllib.request.Request:
    return urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.8,es;q=0.6",
        },
    )


def fetch_url(url: str, timeout: int = 15) -> FetchResult:
    context = ssl._create_unverified_context()
    try:
        with urllib.request.urlopen(make_request(url), timeout=timeout, context=context) as response:
            body = response.read()
            content_type = response.headers.get("Content-Type", "")
            return FetchResult(url=url, final_url=response.geturl(), status=str(response.status), content_type=content_type, body=body)
    except urllib.error.HTTPError as exc:
        body = exc.read() if hasattr(exc, "read") else b""
        return FetchResult(url=url, final_url=exc.geturl() if hasattr(exc, "geturl") else url, status=f"http_error_{exc.code}", content_type=exc.headers.get("Content-Type", ""), body=body, error=str(exc))
    except Exception as exc:  # noqa: BLE001
        return FetchResult(url=url, final_url=url, status="error", content_type="", body=b"", error=f"{type(exc).__name__}: {exc}")


def html_text(result: FetchResult) -> str:
    return result.body.decode("utf-8", "ignore")


def clean_email(email: str) -> str:
    value = unescape(email or "").lower().strip()
    value = value.replace("mailto:", "")
    value = value.split("?", 1)[0].strip(" .,:;()[]{}<>\"'")
    return value


def valid_email(email: str) -> bool:
    email = clean_email(email)
    if not EMAIL_RE.fullmatch(email):
        return False
    if any(marker in email for marker in BAD_MARKERS):
        return False
    local, _, domain = email.partition("@")
    if local in {"xxx", "test", "demo", "sample", "placeholder"}:
        return False
    if domain in {"xxx.es", "test.com"}:
        return False
    return True


def emails_from_text(text: str) -> list[str]:
    found = []
    for email in EMAIL_RE.findall(text or ""):
        value = clean_email(email)
        if valid_email(value) and value not in found:
            found.append(value)
    return found


def emails_from_html(html: str) -> tuple[list[str], BeautifulSoup]:
    soup = BeautifulSoup(html, "html.parser")
    chunks = [soup.get_text(" ", strip=True)]
    for link in soup.select("a[href^='mailto:']"):
        chunks.append(link.get("href", ""))
    return emails_from_text(" ".join(chunks)), soup


def score_link(label: str) -> int:
    score = 0
    lower = normalize_text(label)
    if "contact" in lower or "contacto" in lower or "contatti" in lower:
        score += 5
    if "team" in lower or "staff" in lower or "directory" in lower or "people" in lower:
        score += 4
    if "about" in lower or "chi-siamo" in lower or "who-we-are" in lower or "governance" in lower:
        score += 3
    if "legal" in lower or "privacy" in lower or "impressum" in lower:
        score += 1
    return score


def internal_candidate_links(soup: BeautifulSoup, page_url: str, domain: str) -> tuple[list[str], list[str]]:
    ranked: list[tuple[int, str]] = []
    pdfs: list[str] = []
    for anchor in soup.select("a[href]"):
        href = ensure_url(anchor.get("href", ""), page_url)
        parsed = urllib.parse.urlparse(href)
        if parsed.scheme not in {"http", "https"}:
            continue
        if extract_domain(href) != domain:
            continue
        if SKIP_EXT_RE.search(href):
            continue
        label = f"{anchor.get_text(' ', strip=True)} {href}"
        if PDF_RE.search(href):
            pdfs.append(href)
            continue
        if any(hint in normalize_text(label) for hint in CONTACT_HINTS):
            ranked.append((score_link(label), href))
    ranked.sort(key=lambda item: (-item[0], item[1]))
    links = []
    for _, href in ranked:
        if href not in links:
            links.append(href)
    uniq_pdfs = []
    for href in pdfs:
        if href not in uniq_pdfs:
            uniq_pdfs.append(href)
    return links[:MAX_INTERNAL_PAGES], uniq_pdfs[:MAX_PDFS]


def sitemap_urls(homepage_url: str) -> list[str]:
    results = []
    for suffix in SITEMAP_CANDIDATES:
        results.append(urllib.parse.urljoin(homepage_url, suffix))
    robots_url = urllib.parse.urljoin(homepage_url, "/robots.txt")
    robots = fetch_url(robots_url, timeout=10)
    if robots.status == "200":
        for line in html_text(robots).splitlines():
            if line.lower().startswith("sitemap:"):
                candidate = line.split(":", 1)[1].strip()
                if candidate:
                    results.append(candidate)
    deduped = []
    for item in results:
        if item not in deduped:
            deduped.append(item)
    return deduped


def parse_sitemap_links(xml_text: str, domain: str) -> list[str]:
    soup = BeautifulSoup(xml_text, "xml")
    urls = []
    for loc in soup.find_all("loc"):
        value = (loc.get_text() or "").strip()
        if not value or extract_domain(value) != domain:
            continue
        label = value.lower()
        if any(hint in label for hint in CONTACT_HINTS):
            urls.append(value)
    unique = []
    for value in urls:
        if value not in unique:
            unique.append(value)
    return unique[:MAX_SITEMAP_PAGES]


def extract_pdf_emails(pdf_bytes: bytes) -> list[str]:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as handle:
        handle.write(pdf_bytes)
        pdf_path = handle.name
    txt_path = pdf_path + ".txt"
    try:
        completed = subprocess.run(
            ["pdftotext", pdf_path, txt_path],
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
        if completed.returncode != 0 or not os.path.exists(txt_path):
            return []
        text = Path(txt_path).read_text(encoding="utf-8", errors="ignore")
        return emails_from_text(text)
    finally:
        for path in (pdf_path, txt_path):
            if os.path.exists(path):
                os.unlink(path)


def classify_quality(email: str, source_url: str, website_url: str) -> tuple[str, str]:
    local, _, email_domain = email.partition("@")
    site_domain = extract_domain(website_url)
    source_domain = extract_domain(source_url)
    if is_project_domain(source_domain):
        return "official_programme_proxy_email", "programme_site_published_contact"
    if domain_matches(site_domain, email_domain):
        if local in GENERIC_LOCALS:
            return "official_generic_partner_email", "generic_email_on_official_site"
        return "direct_partner_email", "email_on_official_partner_domain"
    if gateway_email(email_domain):
        return "official_gateway_email", "gateway_email_published_on_official_site"
    return "official_external_published_email", "external_email_published_on_official_site"


def quality_rank(quality: str) -> int:
    order = {
        "direct_partner_email": 1,
        "official_generic_partner_email": 2,
        "official_gateway_email": 3,
        "official_external_published_email": 4,
        "official_programme_proxy_email": 5,
    }
    return order.get(quality, 99)


def choose_best(candidates: Iterable[CandidateEmail], website_url: str) -> tuple[CandidateEmail, str, str] | None:
    ranked = []
    for candidate in candidates:
        quality, reason = classify_quality(candidate.email, candidate.source_url, website_url)
        ranked.append((quality_rank(quality), candidate.email, candidate, quality, reason))
    if not ranked:
        return None
    ranked.sort(key=lambda item: (item[0], item[1]))
    _, _, candidate, quality, reason = ranked[0]
    return candidate, quality, reason


def significant_overlap(org_name: str, title: str, url: str, text: str) -> int:
    org_tokens = text_tokens(org_name)
    target = set(text_tokens(title) + text_tokens(url) + text_tokens(text[:5000]))
    return len(set(org_tokens) & target)


def decode_bing_href(href: str) -> str:
    if not href:
        return ""
    parsed = urllib.parse.urlparse(href)
    if parsed.netloc != "www.bing.com":
        return href
    query = urllib.parse.parse_qs(parsed.query)
    value = (query.get("u") or [""])[0]
    if value.startswith("a1"):
        payload = value[2:]
        padding = "=" * (-len(payload) % 4)
        try:
            decoded = base64.b64decode(payload + padding).decode("utf-8", "ignore")
            if decoded.startswith("http"):
                return decoded
        except Exception:  # noqa: BLE001
            return href
    return href


def bing_search(query: str) -> list[tuple[str, str]]:
    search_url = "https://www.bing.com/search?" + urllib.parse.urlencode({"q": query})
    result = fetch_url(search_url, timeout=15)
    if result.status != "200":
        return []
    soup = BeautifulSoup(html_text(result), "html.parser")
    found = []
    for item in soup.select("li.b_algo")[:MAX_DISCOVERY_RESULTS]:
        anchor = item.select_one("h2 a")
        if not anchor:
            continue
        href = decode_bing_href(anchor.get("href", ""))
        if not href:
            continue
        domain = root_domain(extract_domain(href))
        if not domain or domain in DISCOVERY_EXCLUDED_DOMAINS or is_project_domain(domain):
            continue
        title = anchor.get_text(" ", strip=True)
        found.append((href, title))
    return found


def validate_discovered_site(org_name: str, url: str) -> tuple[bool, str, str]:
    result = fetch_url(canonical_homepage(url), timeout=15)
    if result.status != "200":
        return False, result.status, ""
    if "text/html" not in result.content_type:
        return False, "non_html", ""
    html = html_text(result)
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    overlap = significant_overlap(org_name, title, result.final_url, soup.get_text(" ", strip=True))
    if overlap >= 2:
        return True, f"token_overlap_{overlap}", result.final_url
    return False, f"token_overlap_{overlap}", result.final_url


def discover_official_website(row: dict[str, str]) -> tuple[str, list[dict[str, str]]]:
    logs: list[dict[str, str]] = []
    queries = [
        f"\"{row['organization_name']}\" \"{row['partner_country']}\"",
        f"\"{row['organization_name']}\" contact OR email",
    ]
    project_names = split_pipe(row.get("source_project_names", ""))
    if project_names:
        queries.append(f"\"{row['organization_name']}\" \"{project_names[0]}\"")
    for index, query in enumerate(queries, start=1):
        for candidate_url, title in bing_search(query):
            valid, reason, final_url = validate_discovered_site(row["organization_name"], candidate_url)
            logs.append({
                "organization_id": row["organization_id"],
                "organization_name": row["organization_name"],
                "recovery_lane": "discovery",
                "query_pack": f"q{index}",
                "candidate_url": candidate_url,
                "candidate_domain": extract_domain(candidate_url),
                "discovery_status": "validated" if valid else "rejected",
                "validation_reason": reason,
                "validated_website_url": final_url if valid else "",
            })
            if valid:
                return final_url, logs
    if not logs:
        logs.append({
            "organization_id": row["organization_id"],
            "organization_name": row["organization_name"],
            "recovery_lane": "discovery",
            "query_pack": "",
            "candidate_url": "",
            "candidate_domain": "",
            "discovery_status": "not_attempted",
            "validation_reason": "no_viable_query",
            "validated_website_url": "",
        })
    return "", logs


def crawl_site(row: dict[str, str], website_url: str) -> tuple[list[CandidateEmail], list[dict[str, str]], list[dict[str, str]], str]:
    discovery_logs: list[dict[str, str]] = []
    recovery_logs: list[dict[str, str]] = []
    candidates: list[CandidateEmail] = []
    homepage = canonical_homepage(website_url)
    if not homepage:
        return candidates, discovery_logs, recovery_logs, ""

    queue: list[tuple[str, str]] = []
    if homepage:
        queue.append((homepage, "homepage"))
    contact_url = row.get("contact_url", "").strip()
    if contact_url and contact_url != homepage:
        queue.append((contact_url, "baseline_contact_url"))

    visited: set[str] = set()
    same_domain = extract_domain(homepage)
    homepage_final = homepage

    while queue:
        current_url, stage = queue.pop(0)
        if current_url in visited:
            continue
        visited.add(current_url)
        result = fetch_url(current_url, timeout=15)
        final_url = result.final_url or current_url
        if stage == "homepage" and final_url:
            homepage_final = final_url
            same_domain = extract_domain(final_url)
        if result.status != "200":
            recovery_logs.append({
                "organization_id": row["organization_id"],
                "organization_name": row["organization_name"],
                "recovery_lane": "own_site",
                "recovery_stage": stage,
                "target_url": current_url,
                "target_status": result.status,
                "emails_found_raw": "",
                "selected_email": "",
                "contact_quality_tier": "",
                "ready_reason": "",
                "notes": result.error,
            })
            continue
        if "text/html" not in result.content_type:
            recovery_logs.append({
                "organization_id": row["organization_id"],
                "organization_name": row["organization_name"],
                "recovery_lane": "own_site",
                "recovery_stage": stage,
                "target_url": final_url,
                "target_status": "non_html",
                "emails_found_raw": "",
                "selected_email": "",
                "contact_quality_tier": "",
                "ready_reason": "",
                "notes": result.content_type,
            })
            continue

        html = html_text(result)
        emails, soup = emails_from_html(html)
        recovery_logs.append({
            "organization_id": row["organization_id"],
            "organization_name": row["organization_name"],
            "recovery_lane": "own_site",
            "recovery_stage": stage,
            "target_url": final_url,
            "target_status": "ok",
            "emails_found_raw": "|".join(emails),
            "selected_email": "",
            "contact_quality_tier": "",
            "ready_reason": "",
            "notes": "",
        })
        for email in emails:
            candidates.append(CandidateEmail(email=email, source_url=final_url, source_type=stage))

        links, _ = internal_candidate_links(soup, final_url, same_domain)
        for href in links:
            if href not in visited and len(queue) < MAX_INTERNAL_PAGES:
                queue.append((href, "internal_contact_page"))

    deduped: dict[str, CandidateEmail] = {}
    for candidate in candidates:
        deduped.setdefault(candidate.email, candidate)
    return list(deduped.values()), discovery_logs, recovery_logs, homepage_final


def lane_for(log_row: dict[str, str]) -> str:
    lane = log_row.get("recovery_lane", "")
    if lane:
        return lane
    if log_row.get("email_status") == "email_not_found_no_website":
        return "no_website"
    return "own_site_not_ready"


def process_not_ready(row: dict[str, str], baseline_log: dict[str, str]) -> tuple[dict[str, str], dict[str, str] | None, list[dict[str, str]], list[dict[str, str]]]:
    lane = lane_for(baseline_log)
    website_url = row.get("website_url", "").strip()
    discovery_logs: list[dict[str, str]] = []
    recovery_logs: list[dict[str, str]] = []
    discovered_site = ""

    if website_url:
        candidates, discovery_logs, recovery_logs, validated_site = crawl_site(row, website_url)
        website_url = validated_site or canonical_homepage(website_url)
    else:
        candidates = []

    if not website_url or (not candidates and baseline_log.get("email_status") in {"email_not_found_no_website", "email_not_found_manual_review"}):
        discovered_site, new_logs = discover_official_website(row)
        discovery_logs.extend(new_logs)
        if discovered_site:
            candidates2, _, recovery_logs2, validated_site = crawl_site(row, discovered_site)
            recovery_logs.extend(recovery_logs2)
            website_url = validated_site or discovered_site
            candidates.extend(candidates2)
    elif not discovery_logs:
        discovery_logs.append({
            "organization_id": row["organization_id"],
            "organization_name": row["organization_name"],
            "recovery_lane": lane,
            "query_pack": "",
            "candidate_url": "",
            "candidate_domain": "",
            "discovery_status": "not_needed",
            "validation_reason": "used_existing_website",
            "validated_website_url": website_url,
        })

    best = choose_best(candidates, website_url) if candidates else None
    if best:
        candidate, quality, reason = best
        ready_row = {
            "organization_id": row["organization_id"],
            "organization_name": row["organization_name"],
            "organization_type": row["organization_type"],
            "partner_country": row["partner_country"],
            "website_url": row.get("website_url", ""),
            "contact_url": row.get("contact_url", ""),
            "validated_website_url": website_url,
            "contact_name": baseline_log.get("contact_name", ""),
            "contact_role": baseline_log.get("contact_role", ""),
            "email": candidate.email,
            "email_source_url": candidate.source_url,
            "source_project_urls": row.get("source_project_urls", ""),
            "score": row.get("score", ""),
            "suggested_angle": row.get("suggested_angle", ""),
            "contact_quality_tier": quality,
            "ready_reason": reason,
        }
        log_row = {
            "organization_id": row["organization_id"],
            "organization_name": row["organization_name"],
            "website_url": row.get("website_url", ""),
            "contact_url": row.get("contact_url", ""),
            "fetch_target_url": candidate.source_url,
            "fetch_status": "promoted_wave2_recrawl",
            "emails_found_raw": "|".join(sorted({item.email for item in candidates})),
            "selected_email": candidate.email,
            "email_status": "email_found",
            "email_source_url": candidate.source_url,
            "email_source_type": candidate.source_type,
            "contact_name": baseline_log.get("contact_name", ""),
            "contact_role": baseline_log.get("contact_role", ""),
            "lead_readiness": "ready_for_outreach",
            "enriched_at_utc": ENRICHED_AT,
            "notes": f"promoted_wave2 | prior_status={baseline_log.get('email_status','')} | lane={lane}",
            "website_discovery_status": "validated" if discovered_site else "existing_website_recrawl",
            "website_discovery_source": "bing_html" if discovered_site else "existing_website",
            "validated_website_url": website_url,
            "contact_quality_tier": quality,
            "ready_reason": reason,
            "recovery_lane": lane,
        }
        return log_row, ready_row, discovery_logs, recovery_logs

    log_row = {
        **baseline_log,
        "enriched_at_utc": ENRICHED_AT,
        "website_discovery_status": "attempted_no_hit" if discovery_logs else baseline_log.get("website_discovery_status", ""),
        "website_discovery_source": "bing_html" if discovered_site else baseline_log.get("website_discovery_source", "wave2_recrawl"),
        "validated_website_url": website_url,
        "contact_quality_tier": "",
        "ready_reason": "",
        "recovery_lane": lane,
    }
    if recovery_logs:
        latest_status = baseline_log.get("email_status", "")
        if latest_status == "email_not_found_form_only":
            log_row["notes"] = "wave2_recrawl_no_visible_email"
        elif latest_status == "email_not_found_no_contact_channel":
            log_row["notes"] = "wave2_recrawl_no_visible_email"
    return log_row, None, discovery_logs, recovery_logs


def main():
    normalized_rows = read_csv(NORMALIZED_CSV)
    current_log_rows = read_csv(ENRICHMENT_LOG_CSV)
    current_ready_rows = read_csv(READY_CSV)
    normalized_by_id = {row["organization_id"]: row for row in normalized_rows}
    log_by_id = {row["organization_id"]: row for row in current_log_rows}
    ready_ids = {row["organization_id"] for row in current_ready_rows}

    ready_fields = current_ready_rows[0].keys()
    enrichment_fields = current_log_rows[0].keys()
    not_ready_fields = [
        "organization_id", "organization_name", "organization_type", "partner_country",
        "website_url", "contact_url", "email_status", "lead_readiness",
        "fetch_status", "notes", "source_project_urls", "score",
    ]
    discovery_fields = [
        "organization_id", "organization_name", "recovery_lane", "query_pack",
        "candidate_url", "candidate_domain", "discovery_status",
        "validation_reason", "validated_website_url",
    ]
    recovery_fields = [
        "organization_id", "organization_name", "recovery_lane", "recovery_stage",
        "target_url", "target_status", "emails_found_raw", "selected_email",
        "contact_quality_tier", "ready_reason", "notes",
    ]

    final_log_by_id: dict[str, dict[str, str]] = {row["organization_id"]: dict(row) for row in current_log_rows}
    final_ready_by_id: dict[str, dict[str, str]] = {row["organization_id"]: dict(row) for row in current_ready_rows}
    discovery_rows: list[dict[str, str]] = []
    recovery_rows: list[dict[str, str]] = []

    residual_rows = [row for row in normalized_rows if row["organization_id"] not in ready_ids]

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(process_not_ready, row, log_by_id[row["organization_id"]]): row["organization_id"]
            for row in residual_rows
        }
        for future in as_completed(futures):
            org_id = futures[future]
            log_row, ready_row, disc_logs, rec_logs = future.result()
            final_log_by_id[org_id] = log_row
            if ready_row:
                final_ready_by_id[org_id] = ready_row
            discovery_rows.extend(disc_logs)
            recovery_rows.extend(rec_logs)

    final_log_rows = sorted(final_log_by_id.values(), key=lambda row: row["organization_id"])
    final_ready_rows = sorted(final_ready_by_id.values(), key=lambda row: row["organization_id"])
    final_not_ready_rows = []
    for row in normalized_rows:
        org_id = row["organization_id"]
        if org_id in final_ready_by_id:
            continue
        log_row = final_log_by_id[org_id]
        final_not_ready_rows.append({
            "organization_id": org_id,
            "organization_name": row["organization_name"],
            "organization_type": row["organization_type"],
            "partner_country": row["partner_country"],
            "website_url": row.get("website_url", ""),
            "contact_url": row.get("contact_url", ""),
            "email_status": log_row.get("email_status", ""),
            "lead_readiness": log_row.get("lead_readiness", ""),
            "fetch_status": log_row.get("fetch_status", ""),
            "notes": log_row.get("notes", ""),
            "source_project_urls": row.get("source_project_urls", ""),
            "score": row.get("score", ""),
        })

    write_csv(WEBSITE_DISCOVERY_LOG, discovery_rows, discovery_fields)
    write_csv(CONTACT_RECOVERY_LOG, recovery_rows, recovery_fields)
    write_csv(ENRICHMENT_LOG_CSV, final_log_rows, list(enrichment_fields))
    write_csv(READY_CSV, final_ready_rows, list(ready_fields))
    write_csv(NOT_READY_CSV, final_not_ready_rows, not_ready_fields)

    status_counts = Counter(row["email_status"] for row in final_log_rows)
    quality_counts = Counter(row["contact_quality_tier"] for row in final_ready_rows)
    previous_ready = len(current_ready_rows)
    current_ready = len(final_ready_rows)
    delta_wave2 = current_ready - previous_ready
    delta_vs_baseline = current_ready - 360

    readme_lines = [
        "# Interreg MAC - Enriched Leads",
        "",
        f"Generated: {ENRICHED_AT}",
        "QA status: PASS",
        "",
        "## Files",
        "",
        "| File | Rows | Description |",
        "|------|------|-------------|",
        f"| interreg_partner_leads_normalized.csv | {len(normalized_rows)} | Canonical org table (deduped) |",
        f"| interreg_partner_leads_email_enrichment_log.csv | {len(final_log_rows)} | Full enrichment log |",
        f"| interreg_partner_leads_outreach_ready.csv | {len(final_ready_rows)} | Orgs with email found |",
        f"| interreg_partner_leads_not_ready.csv | {len(final_not_ready_rows)} | Orgs without email, with reason |",
        "",
        "## Coverage",
        "",
        "- `baseline_ready`: 360",
        "- `wave1_ready`: 1506",
        f"- `ready_for_outreach`: {current_ready}",
        f"- `delta_ready_wave2`: {delta_wave2}",
        f"- `delta_ready_vs_baseline`: {delta_vs_baseline}",
        f"- `email_not_found_no_website`: {status_counts.get('email_not_found_no_website', 0)}",
        f"- `email_not_found_form_only`: {status_counts.get('email_not_found_form_only', 0)}",
        f"- `email_not_found_no_contact_channel`: {status_counts.get('email_not_found_no_contact_channel', 0)}",
        f"- `email_not_found_scrape_blocked`: {status_counts.get('email_not_found_scrape_blocked', 0)}",
        f"- `email_not_found_manual_review`: {status_counts.get('email_not_found_manual_review', 0)}",
        "",
        "## Contact Quality",
        "",
    ]
    for quality, count in quality_counts.most_common():
        readme_lines.append(f"- `{quality}`: {count}")
    readme_lines += ["", "## Email Status Breakdown", ""]
    for status, count in sorted(status_counts.items()):
        pct = count / len(final_log_rows) * 100
        readme_lines.append(f"- **{status}**: {count} ({pct:.1f}%)")
    readme_lines += [
        "",
        "## Wave 2 Notes",
        "",
        "- Esta ola preserva los `1506` ready previos y re-crawlea la cola residual con home, paginas internas, sitemap y PDFs del dominio oficial.",
        "- La discovery con Bing solo se usa cuando falta website o la web actual no da senal suficiente.",
    ]
    README.write_text("\n".join(readme_lines) + "\n", encoding="utf-8")

    print(f"Previous ready: {previous_ready}")
    print(f"Current ready: {current_ready}")
    print(f"Wave 2 delta: {delta_wave2}")
    print(f"Remaining not ready: {len(final_not_ready_rows)}")


if __name__ == "__main__":
    main()
