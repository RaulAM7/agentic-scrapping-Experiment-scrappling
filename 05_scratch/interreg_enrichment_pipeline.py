#!/usr/bin/env python3
"""
Interreg MAC Email Enrichment Pipeline
Pasos: canonizar -> enriquecer -> exportar -> QA
Spec: 04_outputs/.../2026-06-07_email-enrichment-backfill-spec_v1.md
"""

import csv
import hashlib
import re
import unicodedata
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from functools import lru_cache
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

BASE = Path("/home/reboot/Escritorio/agentic-scrapping-Experiment-scrappling")
PROCESSED = BASE / "04_outputs/skilland-knowledge-transfer-engine/interreg_mac/04_processed_outputs"
RAW_HTML = BASE / "04_outputs/skilland-knowledge-transfer-engine/interreg_mac/01_data_sources/raw_html/projects"
OUT = BASE / "04_outputs/skilland-knowledge-transfer-engine/interreg_mac/06_enriched_leads"
OUT.mkdir(parents=True, exist_ok=True)

WAVE_FILES = [
    PROCESSED / "wave1_keep_eu_processed_scored.csv",
    PROCESSED / "wave2_keep_eu_processed_scored.csv",
    PROCESSED / "wave3_keep_eu_processed_scored.csv",
]

ENRICHED_AT = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# ---------------------------------------------------------------------------
# Email regex and helpers
# ---------------------------------------------------------------------------

EMAIL_RE = re.compile(r'\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b')
_BAD_EMAIL_DOMAINS = {
    "example.com",
    "example.org",
    "sentry.io",
    "domain.com",
    "email.com",
    "yourdomain",
    "yourcompany",
    "test.com",
}
_BAD_PREFIXES = {
    "noreply",
    "no-reply",
    "donotreply",
    "bounce",
    "mailer-daemon",
    "postmaster",
    "webmaster",
}
_SKIP_EXTS = re.compile(r'\.(png|jpg|jpeg|gif|svg|webp|bmp|ico|pdf|zip|docx?)$', re.I)
_CLEARLY_BAD_DOMAIN_MARKERS = {"sentry.wixpress.com", "wixpress.com", "osm.org"}
_GATEWAY_DOMAIN_MARKERS = (
    "legalmail.it",
    ".legalmail.it",
    "pec.it",
    ".pec.",
    ".pec",
    "hs01.kep.tr",
    ".kep.tr",
    "cert.",
)
_FORM_MARKERS = ("<form", "contact-form", "g-recaptcha", "type=\"submit\"", "type='submit'")
_KNOWN_FALSE_POSITIVES = {
    "default@osm.org",
    "8eb368c655b84e029ed79ad7a5c1718e@sentry.wixpress.com",
}


def extract_domain(url: str) -> str:
    if not url:
        return ""
    try:
        host = urlparse(url).netloc.lower().strip()
        if host.startswith("www."):
            host = host[4:]
        return host
    except Exception:
        return ""


def is_keep_eu(url: str) -> bool:
    return "keep.eu" in (url or "")


def homepage_from_url(url: str) -> str:
    if not url:
        return ""
    try:
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"
    except Exception:
        return ""


def normalize_name(name: str) -> str:
    if not name:
        return ""
    name = name.strip().lower()
    name = unicodedata.normalize("NFKC", name)
    name = re.sub(r'\s+', ' ', name)
    name = re.sub(r'[.,;:!?()\[\]{}"\']+$', '', name)
    return name


def org_id_from_key(key: str) -> str:
    digest = hashlib.md5(key.encode()).hexdigest()[:8]
    slug = re.sub(r'[^a-z0-9]+', '_', key.lower())[:40].strip('_')
    return f"org_{slug}_{digest}"


def split_pipe(value: str) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.split('|') if part.strip()]


def slug_tokens(value: str) -> set[str]:
    text = unicodedata.normalize("NFKD", value or "")
    text = text.encode("ascii", "ignore").decode("ascii").lower()
    return {token for token in re.split(r'[^a-z0-9]+', text) if len(token) >= 4}


def domain_root_tokens(domain: str) -> set[str]:
    pieces = [p for p in domain.split('.') if p and p not in {'www', 'com', 'org', 'net', 'gov', 'edu'}]
    return {piece for piece in pieces if len(piece) >= 4}


def domain_matches(org_domain: str, email_domain: str) -> bool:
    if not org_domain or not email_domain:
        return False
    return (
        email_domain == org_domain
        or email_domain.endswith('.' + org_domain)
        or org_domain.endswith('.' + email_domain)
    )


def is_gateway_domain(email_domain: str) -> bool:
    return any(marker in email_domain for marker in _GATEWAY_DOMAIN_MARKERS)


def is_clearly_bad_email(email: str) -> bool:
    domain = email.partition('@')[2].lower()
    return any(marker in domain for marker in _CLEARLY_BAD_DOMAIN_MARKERS)


def filter_emails(emails: list[str]) -> list[str]:
    out = []
    seen = set()
    for email in emails:
        email = email.lower().strip()
        if email in seen:
            continue
        local, _, domain = email.partition('@')
        if not domain:
            continue
        if domain in _BAD_EMAIL_DOMAINS or any(marker in domain for marker in _BAD_EMAIL_DOMAINS):
            continue
        if is_clearly_bad_email(email):
            continue
        if local in _BAD_PREFIXES:
            continue
        if _SKIP_EXTS.search(email):
            continue
        if len(local) < 2 or len(domain) < 4:
            continue
        out.append(email)
        seen.add(email)
    return out


def rank_email(email: str, org_domain: str) -> int:
    local = email.split('@')[0].lower()
    email_domain = email.split('@')[1].lower() if '@' in email else ''
    score = 0
    if not domain_matches(org_domain, email_domain):
        score += 100
    generic = {
        'info', 'contact', 'contacto', 'contatti', 'hello', 'hola', 'mail', 'email',
        'admin', 'support', 'office', 'enquiries', 'enquiry', 'query', 'general',
    }
    if local in generic:
        score += 10
    return score


def select_best_email(emails: list[str], org_domain: str) -> str:
    if not emails:
        return ""
    return sorted(emails, key=lambda email: rank_email(email, org_domain))[0]


def classify_email_candidate(email: str, org_domain: str, organization_name: str) -> tuple[str, str]:
    local, _, email_domain = email.lower().partition('@')
    if is_clearly_bad_email(email):
        return 'reject', 'rejected_third_party_or_telemetry_domain'
    if domain_matches(org_domain, email_domain):
        if email_domain == org_domain:
            return 'accept', 'accepted_same_domain'
        return 'accept', 'accepted_subdomain_or_related_org_domain'

    org_tokens = slug_tokens(organization_name) | domain_root_tokens(org_domain)
    local_tokens = slug_tokens(local)
    email_domain_tokens = domain_root_tokens(email_domain)

    if is_gateway_domain(email_domain):
        if org_tokens & (local_tokens | email_domain_tokens):
            return 'accept', 'accepted_gateway_domain_with_org_signal'
        return 'manual_review', 'gateway_domain_without_clear_org_signal'

    return 'manual_review', 'off_domain_email_requires_manual_review'


def classify_source_type(url: str) -> str:
    path = urlparse(url).path.lower()
    if 'contact' in path or 'contacto' in path or 'contatt' in path:
        return 'website_contact_page'
    if 'team' in path or 'equipo' in path or 'staff' in path:
        return 'website_team_page'
    if 'about' in path or 'about-us' in path or 'quienes' in path:
        return 'website_about_page'
    return 'website_footer'


def parse_keep_project_id(url: str) -> str:
    match = re.search(r'/projects/(\d+)/', url or '')
    return match.group(1) if match else ''


def get_keep_html_path(project_id: str) -> Path | None:
    matches = sorted(RAW_HTML.glob(f"*project_{project_id}.html"))
    return matches[0] if matches else None


@lru_cache(maxsize=None)
def extract_keep_html_candidate_urls(project_id: str) -> list[str]:
    html_path = get_keep_html_path(project_id)
    if not html_path:
        return []

    html = html_path.read_text(encoding='utf-8', errors='ignore')
    website_match = re.search(
        r'<strong>\s*Website:\s*</strong><a\s+href="([^"]+)"',
        html,
        flags=re.I,
    )
    if not website_match:
        return []

    url = website_match.group(1).strip()
    domain = extract_domain(url)
    if not domain or is_keep_eu(url) or _SKIP_EXTS.search(url):
        return []
    if domain.endswith('interact.eu') or domain.endswith('interreg.eu'):
        return []
    return [url]


# ---------------------------------------------------------------------------
# HTML email extractor
# ---------------------------------------------------------------------------


class EmailExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.emails: list[str] = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'a':
            href = attrs_dict.get('href', '')
            if href.lower().startswith('mailto:'):
                email = href[7:].split('?')[0].strip()
                if email:
                    self.emails.append(email)

    def handle_data(self, data):
        for email in EMAIL_RE.findall(data):
            self.emails.append(email)


def extract_emails_from_html(html: str) -> list[str]:
    parser = EmailExtractor()
    try:
        parser.feed(html[:500_000])
    except Exception:
        pass
    found = EMAIL_RE.findall(html[:500_000])
    combined = list(set(parser.emails + found))
    return filter_emails(combined)


def looks_like_form_only_page(html: str) -> bool:
    lower = html.lower()
    return any(marker in lower for marker in _FORM_MARKERS)


# ---------------------------------------------------------------------------
# HTTP fetch
# ---------------------------------------------------------------------------

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    ),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'es,en;q=0.8',
}
TIMEOUT = 15


def fetch_html(url: str) -> tuple[str, str]:
    req = Request(url, headers=HEADERS)
    with urlopen(req, timeout=TIMEOUT) as resp:
        charset = 'utf-8'
        content_charset = resp.headers.get_content_charset()
        if content_charset:
            charset = content_charset
        raw = resp.read(600_000)
        try:
            html = raw.decode(charset, errors='replace')
        except Exception:
            html = raw.decode('utf-8', errors='replace')
        return html, resp.url


@lru_cache(maxsize=4096)
def fetch_html_cached(url: str) -> tuple[str, str]:
    return fetch_html(url)


def make_result(org: dict) -> dict:
    return {
        'organization_id': org['organization_id'],
        'organization_name': org['organization_name'],
        'website_url': org.get('website_url', ''),
        'contact_url': org.get('contact_url', ''),
        'fetch_target_url': '',
        'fetch_status': '',
        'emails_found_raw': '',
        'selected_email': '',
        'email_status': '',
        'email_source_url': '',
        'email_source_type': '',
        'contact_name': org.get('contact_name', ''),
        'contact_role': org.get('contact_role', ''),
        'lead_readiness': '',
        'enriched_at_utc': ENRICHED_AT,
        'notes': '',
    }


def build_targets(org: dict) -> list[tuple[str, str]]:
    targets = []
    contact_url = org.get('contact_url', '')
    if contact_url and not is_keep_eu(contact_url):
        targets.append((contact_url, 'own_contact_url'))
        home = homepage_from_url(contact_url)
        if home and home.rstrip('/') != contact_url.rstrip('/'):
            targets.append((home, 'own_homepage_fallback'))
        return targets

    for project_url in split_pipe(org.get('source_project_urls', '')):
        project_id = parse_keep_project_id(project_url)
        for candidate_url in extract_keep_html_candidate_urls(project_id):
            targets.append((candidate_url, f'keep_eu_html_project_{project_id}'))
    return targets


def enrich_one(org: dict) -> dict:
    org_domain = extract_domain(org.get('website_url') or org.get('contact_url') or '')
    result = make_result(org)
    targets = build_targets(org)

    if not targets:
        result['fetch_status'] = 'skipped_no_own_url'
        result['email_status'] = 'email_not_found_no_website'
        result['lead_readiness'] = 'not_outreach_ready'
        return result

    candidate_results = []
    last_status = ''
    last_url = targets[0][0]

    for target, target_source in targets:
        try:
            html, final_url = fetch_html_cached(target)
            last_status = 'ok'
            last_url = final_url
            source_type = classify_source_type(target)
            if target_source.startswith('keep_eu_html_project_'):
                source_type = 'keep_eu_project_page'

            emails = extract_emails_from_html(html)
            for email in emails:
                decision, note = classify_email_candidate(email, org_domain, org['organization_name'])
                candidate_results.append({
                    'email': email,
                    'decision': decision,
                    'note': note,
                    'source_url': final_url,
                    'source_type': source_type,
                    'target_source': target_source,
                })

            accepted = [c for c in candidate_results if c['decision'] == 'accept']
            if accepted:
                break

            if emails:
                continue
            if looks_like_form_only_page(html):
                result['fetch_target_url'] = final_url
                result['fetch_status'] = last_status
                result['email_status'] = 'email_not_found_form_only'
                result['lead_readiness'] = 'not_outreach_ready'
                result['notes'] = f'page_fetched_form_only | candidate_source={target_source}'
                return result
        except HTTPError as exc:
            last_status = f'http_error_{exc.code}'
        except URLError:
            last_status = 'url_error'
        except Exception:
            last_status = 'error'

    result['fetch_target_url'] = last_url
    result['fetch_status'] = last_status or 'error'

    all_seen = sorted({candidate['email'] for candidate in candidate_results})
    accepted = [candidate for candidate in candidate_results if candidate['decision'] == 'accept']
    manual = [candidate for candidate in candidate_results if candidate['decision'] == 'manual_review']
    rejected = [candidate for candidate in candidate_results if candidate['decision'] == 'reject']

    if all_seen:
        result['emails_found_raw'] = ' | '.join(all_seen)

    if accepted:
        best = select_best_email([candidate['email'] for candidate in accepted], org_domain)
        chosen = next(candidate for candidate in accepted if candidate['email'] == best)
        result['selected_email'] = chosen['email']
        result['email_status'] = 'email_found'
        result['email_source_url'] = chosen['source_url']
        result['email_source_type'] = chosen['source_type']
        result['lead_readiness'] = 'ready_for_outreach'
        result['fetch_target_url'] = chosen['source_url']
        notes = [chosen['note'], f"candidate_source={chosen['target_source']}"]
        if manual:
            notes.append(f"manual_review_candidates={len(manual)}")
        if rejected:
            notes.append(f"rejected_candidates={len(rejected)}")
        result['notes'] = ' | '.join(notes)
    elif 'http_error_403' in last_status or 'http_error_429' in last_status:
        result['email_status'] = 'email_not_found_scrape_blocked'
        result['lead_readiness'] = 'manual_review_needed'
        result['notes'] = last_status
    elif manual:
        result['email_status'] = 'email_not_found_manual_review'
        result['lead_readiness'] = 'manual_review_needed'
        result['notes'] = ' | '.join(
            ['manual_review_only_candidates'] +
            [f"{candidate['email']}=>{candidate['note']}" for candidate in manual[:3]]
        )
    elif last_status == 'ok':
        result['email_status'] = 'email_not_found_no_contact_channel'
        result['lead_readiness'] = 'not_outreach_ready'
        result['notes'] = 'page_fetched but no email found'
    elif last_status in ('url_error', 'error') or 'http_error' in last_status:
        result['email_status'] = 'email_not_found_manual_review'
        result['lead_readiness'] = 'manual_review_needed'
        result['notes'] = last_status
    else:
        result['email_status'] = 'email_not_found_manual_review'
        result['lead_readiness'] = 'manual_review_needed'

    return result


# ---------------------------------------------------------------------------
# STEP 1 - Canonize
# ---------------------------------------------------------------------------


def infer_org_type(partner_name: str, notes: str) -> str:
    match = re.search(r'partner_org_type=([^|]+)', notes or '')
    if match:
        value = match.group(1).strip()
        if value and value.lower() not in ('n.a.', 'na', '', 'null'):
            return value

    name = partner_name.lower()
    if any(key in name for key in ('universit', 'college', 'escola', 'escuela', 'istitut', 'polytechni', 'academia', 'akademi')):
        return 'University / Research'
    if any(key in name for key in ('chamber', 'cámara', 'camara', 'chambre', 'camera')):
        return 'Chamber of Commerce'
    if any(key in name for key in ('municipio', 'ayuntamiento', 'commune', 'município', 'municipality', 'city of', 'town of', 'comune')):
        return 'Municipal Authority'
    if any(key in name for key in ('region', 'región', 'regional', 'province', 'provincia', 'prefect', 'prefettura')):
        return 'Regional Authority'
    if any(key in name for key in ('agency', 'agencia', 'agence', 'agenzia', 'agência')):
        return 'Agency'
    if any(key in name for key in ('fundacion', 'fundació', 'fundação', 'foundation', 'fondation', 'fondazione', 'fundacja')):
        return 'Foundation / NGO'
    if any(key in name for key in ('association', 'asociacion', 'associació', 'associação', 'associazione', 'vereniging', 'verein', 'junta')):
        return 'Association'
    if any(key in name for key in ('cluster', 'network', 'red ', 'réseau', 'rete')):
        return 'Cluster / Network'
    if any(key in name for key in ('s.l.', 's.a.', 's.p.a.', 'ltd', 'gmbh', 'bv ', ' inc', 's.r.l.', 'srl', 'sl ', 's.l ', 'sa ', ' s.a.')):
        return 'Private Company'
    if any(key in name for key in ('minister', 'ministry', 'ministerio', 'ministère', 'governo', 'gobierno', 'government')):
        return 'Government / Ministry'
    return 'Unknown'


def canonize(wave_files: list[Path]) -> tuple[list[dict], dict]:
    all_rows = []
    for wave_file in wave_files:
        wave_label = wave_file.stem.split('_')[0]
        with wave_file.open(newline='', encoding='utf-8') as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                row['_wave'] = wave_label
                all_rows.append(row)

    print(f"  Loaded {len(all_rows)} total rows from {len(wave_files)} waves")

    groups: dict[str, list[dict]] = {}
    for row in all_rows:
        partner_name = row.get('partner_name', '')
        country = row.get('partner_country', '')
        contact_url = row.get('contact_url', '')
        domain = extract_domain(contact_url) if not is_keep_eu(contact_url) else ''
        normalized_name = normalize_name(partner_name)
        if domain:
            key = f"{normalized_name}::{country}::{domain}"
        else:
            key = f"{normalized_name}::{country}"
        groups.setdefault(key, []).append(row)

    print(f"  Unique org keys after dedup: {len(groups)}")

    normalized = []
    org_map = {}

    for key, rows in groups.items():
        best_row = max(rows, key=lambda row: float(row.get('score', 0) or 0))
        max_score = float(best_row.get('score', 0) or 0)

        project_ids = list(dict.fromkeys(row.get('project_id', '') for row in rows if row.get('project_id')))
        project_names = list(dict.fromkeys(row.get('project_name', '') for row in rows if row.get('project_name')))
        source_urls = list(dict.fromkeys(row.get('source_url', '') for row in rows if row.get('source_url')))
        documents_urls = []
        for row in rows:
            documents_urls.extend(split_pipe(row.get('documents_url', '')))
        documents_urls = list(dict.fromkeys(doc for doc in documents_urls if doc))
        waves = list(dict.fromkeys(row.get('_wave', '') for row in rows))

        own_urls = [row.get('contact_url', '') for row in rows if not is_keep_eu(row.get('contact_url', ''))]
        contact_url = own_urls[0] if own_urls else (rows[0].get('contact_url', '') or '')
        website_url = homepage_from_url(contact_url) if not is_keep_eu(contact_url) else ''

        partner_name = best_row.get('partner_name', '')
        country = best_row.get('partner_country', '')
        org_type = infer_org_type(partner_name, best_row.get('notes', ''))
        org_id = org_id_from_key(key)

        notes_parts = []
        if len(rows) > 1:
            notes_parts.append(f"merged_from={len(rows)}_rows")
        if any(is_keep_eu(row.get('contact_url', '')) and not is_keep_eu(contact_url) for row in rows):
            notes_parts.append("contact_url_upgraded_to_own_domain")

        normalized_row = {
            'organization_id': org_id,
            'organization_name': partner_name,
            'organization_type': org_type,
            'partner_country': country,
            'partner_region': best_row.get('partner_region', ''),
            'source_dataset': 'interreg_mac',
            'source_wave': ' | '.join(waves),
            'source_project_ids': ' | '.join(project_ids),
            'source_project_names': ' | '.join(project_names),
            'source_project_urls': ' | '.join(source_urls),
            'website_url': website_url,
            'contact_url': contact_url,
            'documents_url': ' | '.join(documents_urls),
            'score': str(max_score),
            'score_reason': best_row.get('score_reason', ''),
            'suggested_angle': best_row.get('suggested_angle', ''),
            'dedupe_key': key,
            'normalization_notes': ' | '.join(notes_parts),
            '_contact_name': best_row.get('contact_name', ''),
            '_contact_role': best_row.get('contact_role', ''),
        }
        normalized.append(normalized_row)
        org_map[org_id] = normalized_row

    return normalized, org_map


# ---------------------------------------------------------------------------
# STEP 2 - Enrich
# ---------------------------------------------------------------------------


def enrich(normalized: list[dict], max_workers: int = 15) -> list[dict]:
    print(f"  Orgs to enrich: {len(normalized)}")
    results = []
    done = 0
    total = len(normalized)

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {
            pool.submit(
                enrich_one,
                {**row, 'contact_name': row.get('_contact_name', ''), 'contact_role': row.get('_contact_role', '')},
            ): row
            for row in normalized
        }
        for future in as_completed(futures):
            done += 1
            if done % 50 == 0 or done == total:
                print(f"    enriched {done}/{total}...")
            try:
                results.append(future.result())
            except Exception as exc:
                row = futures[future]
                results.append({
                    **make_result({**row, 'contact_name': row.get('_contact_name', ''), 'contact_role': row.get('_contact_role', '')}),
                    'fetch_status': f'exception: {exc}',
                    'email_status': 'email_not_found_manual_review',
                    'lead_readiness': 'manual_review_needed',
                    'notes': str(exc),
                })
    return results


# ---------------------------------------------------------------------------
# STEP 3 - Export
# ---------------------------------------------------------------------------

NORM_FIELDS = [
    'organization_id', 'organization_name', 'organization_type',
    'partner_country', 'partner_region', 'source_dataset', 'source_wave',
    'source_project_ids', 'source_project_names', 'source_project_urls',
    'website_url', 'contact_url', 'documents_url',
    'score', 'score_reason', 'suggested_angle',
    'dedupe_key', 'normalization_notes',
]

LOG_FIELDS = [
    'organization_id', 'organization_name', 'website_url', 'contact_url',
    'fetch_target_url', 'fetch_status',
    'emails_found_raw', 'selected_email',
    'email_status', 'email_source_url', 'email_source_type',
    'contact_name', 'contact_role',
    'lead_readiness', 'enriched_at_utc', 'notes',
]

READY_FIELDS = [
    'organization_id', 'organization_name', 'organization_type',
    'partner_country', 'website_url', 'contact_url',
    'contact_name', 'contact_role',
    'email', 'email_source_url', 'source_project_urls',
    'score', 'suggested_angle',
]

NOT_READY_FIELDS = [
    'organization_id', 'organization_name', 'organization_type',
    'partner_country', 'website_url', 'contact_url',
    'email_status', 'lead_readiness', 'fetch_status', 'notes',
    'source_project_urls', 'score',
]


def write_csv(path: Path, rows: list[dict], fields: list[str]):
    with path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Written: {path.name} ({len(rows)} rows)")


def export(normalized: list[dict], enrichment_log: list[dict]):
    log_by_id = {row['organization_id']: row for row in enrichment_log}
    normalized_clean = [{key: value for key, value in row.items() if not key.startswith('_')} for row in normalized]
    write_csv(OUT / "interreg_partner_leads_normalized.csv", normalized_clean, NORM_FIELDS)
    write_csv(OUT / "interreg_partner_leads_email_enrichment_log.csv", enrichment_log, LOG_FIELDS)

    ready_rows = []
    not_ready_rows = []
    for row in normalized:
        log_row = log_by_id.get(row['organization_id'], {})
        if log_row.get('lead_readiness') == 'ready_for_outreach' and log_row.get('selected_email'):
            ready_rows.append({
                'organization_id': row['organization_id'],
                'organization_name': row['organization_name'],
                'organization_type': row['organization_type'],
                'partner_country': row['partner_country'],
                'website_url': row['website_url'],
                'contact_url': row['contact_url'],
                'contact_name': log_row.get('contact_name', ''),
                'contact_role': log_row.get('contact_role', ''),
                'email': log_row.get('selected_email', ''),
                'email_source_url': log_row.get('email_source_url', ''),
                'source_project_urls': row['source_project_urls'],
                'score': row['score'],
                'suggested_angle': row['suggested_angle'],
            })
        else:
            not_ready_rows.append({
                'organization_id': row['organization_id'],
                'organization_name': row['organization_name'],
                'organization_type': row['organization_type'],
                'partner_country': row['partner_country'],
                'website_url': row['website_url'],
                'contact_url': row['contact_url'],
                'email_status': log_row.get('email_status', 'email_not_found_manual_review'),
                'lead_readiness': log_row.get('lead_readiness', 'manual_review_needed'),
                'fetch_status': log_row.get('fetch_status', ''),
                'notes': log_row.get('notes', ''),
                'source_project_urls': row['source_project_urls'],
                'score': row['score'],
            })

    write_csv(OUT / "interreg_partner_leads_outreach_ready.csv", ready_rows, READY_FIELDS)
    write_csv(OUT / "interreg_partner_leads_not_ready.csv", not_ready_rows, NOT_READY_FIELDS)
    return ready_rows, not_ready_rows


# ---------------------------------------------------------------------------
# STEP 4 - QA
# ---------------------------------------------------------------------------


def qa(normalized: list[dict], enrichment_log: list[dict], ready_rows: list[dict], not_ready_rows: list[dict]):
    errors = []
    warnings = []

    org_ids = [row['organization_id'] for row in normalized]
    if len(org_ids) != len(set(org_ids)):
        errors.append("FAIL: duplicate organization_id in normalized table")

    empty_email_ready = [row for row in ready_rows if not row.get('email', '').strip()]
    if empty_email_ready:
        errors.append(f"FAIL: {len(empty_email_ready)} ready rows have empty email")

    missing_status = [row for row in not_ready_rows if not row.get('email_status', '').strip()]
    if missing_status:
        errors.append(f"FAIL: {len(missing_status)} not_ready rows have no email_status")

    found_no_source = [
        row for row in enrichment_log
        if row.get('email_status') == 'email_found' and not row.get('email_source_url')
    ]
    if found_no_source:
        errors.append(f"FAIL: {len(found_no_source)} email_found rows missing email_source_url")

    total_out = len(ready_rows) + len(not_ready_rows)
    if total_out != len(normalized):
        errors.append(
            f"FAIL: ready({len(ready_rows)}) + not_ready({len(not_ready_rows)}) "
            f"= {total_out} != normalized({len(normalized)})"
        )

    bad_ready = [row for row in ready_rows if row.get('email', '').lower() in _KNOWN_FALSE_POSITIVES]
    if bad_ready:
        errors.append(f"FAIL: {len(bad_ready)} known false positives remain in outreach_ready")

    off_domain_ready = []
    for row in ready_rows:
        email_domain = row.get('email', '').partition('@')[2].lower()
        org_domain = extract_domain(row.get('website_url') or row.get('contact_url') or '')
        if not domain_matches(org_domain, email_domain) and not is_gateway_domain(email_domain):
            off_domain_ready.append(row)
    if off_domain_ready:
        errors.append(f"FAIL: {len(off_domain_ready)} ready rows use non-whitelisted off-domain emails")

    status_counts = Counter(row['email_status'] for row in enrichment_log)
    keep_recovered = [
        row for row in enrichment_log
        if 'candidate_source=keep_eu_html_project_' in row.get('notes', '')
    ]

    print("\n--- QA Summary ---")
    print(f"  Unique orgs (normalized): {len(normalized)}")
    print(f"  Outreach ready:           {len(ready_rows)}")
    print(f"  Not ready:                {len(not_ready_rows)}")
    print(f"  keep.eu HTML recoveries:  {len(keep_recovered)}")
    print("\n  Email status breakdown:")
    for status, count in sorted(status_counts.items()):
        pct = count / len(enrichment_log) * 100
        print(f"    {status:<45} {count:>4} ({pct:.1f}%)")

    if errors:
        print("\n  ERRORS:")
        for error in errors:
            print(f"    {error}")
    else:
        print("\n  All QA checks passed.")

    if warnings:
        print("\n  Warnings:")
        for warning in warnings:
            print(f"    {warning}")

    return len(errors) == 0


# ---------------------------------------------------------------------------
# README
# ---------------------------------------------------------------------------


def write_readme(normalized, ready_rows, not_ready_rows, enrichment_log, qa_passed: bool):
    status_counts = Counter(row['email_status'] for row in enrichment_log)
    keep_recovered = [
        row for row in enrichment_log
        if 'candidate_source=keep_eu_html_project_' in row.get('notes', '')
    ]

    lines = [
        "# Interreg MAC - Enriched Leads",
        "",
        f"Generated: {ENRICHED_AT}",
        f"QA status: {'PASS' if qa_passed else 'FAIL'}",
        "",
        "## Files",
        "",
        "| File | Rows | Description |",
        "|------|------|-------------|",
        f"| interreg_partner_leads_normalized.csv | {len(normalized)} | Canonical org table (deduped) |",
        f"| interreg_partner_leads_email_enrichment_log.csv | {len(enrichment_log)} | Full enrichment log |",
        f"| interreg_partner_leads_outreach_ready.csv | {len(ready_rows)} | Orgs with email found |",
        f"| interreg_partner_leads_not_ready.csv | {len(not_ready_rows)} | Orgs without email, with reason |",
        "",
        "## Coverage",
        "",
        f"- `ready_for_outreach`: {len(ready_rows)}",
        f"- `email_not_found_no_website`: {status_counts.get('email_not_found_no_website', 0)}",
        f"- `email_not_found_form_only`: {status_counts.get('email_not_found_form_only', 0)}",
        f"- `email_not_found_no_contact_channel`: {status_counts.get('email_not_found_no_contact_channel', 0)}",
        f"- `email_not_found_scrape_blocked`: {status_counts.get('email_not_found_scrape_blocked', 0)}",
        f"- `email_not_found_manual_review`: {status_counts.get('email_not_found_manual_review', 0)}",
        f"- `keep.eu_html_recoveries`: {len(keep_recovered)}",
        "",
        "## Email Status Breakdown",
        "",
    ]
    for status, count in sorted(status_counts.items()):
        pct = count / len(enrichment_log) * 100
        lines.append(f"- **{status}**: {count} ({pct:.1f}%)")

    lines += ["", "## Sources", "", "Input waves:", ""]
    for wave_file in WAVE_FILES:
        lines.append(f"- `{wave_file.relative_to(BASE)}`")

    with (OUT / "README.md").open('w', encoding='utf-8') as handle:
        handle.write('\n'.join(lines) + '\n')
    print("  Written: README.md")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("=== Step 1: Canonize ===")
    normalized, _ = canonize(WAVE_FILES)

    print("\n=== Step 2: Enrich (parallel fetch) ===")
    enrichment_log = enrich(normalized)

    print("\n=== Step 3: Export ===")
    ready_rows, not_ready_rows = export(normalized, enrichment_log)

    print("\n=== Step 4: QA ===")
    qa_passed = qa(normalized, enrichment_log, ready_rows, not_ready_rows)

    write_readme(normalized, ready_rows, not_ready_rows, enrichment_log, qa_passed)
    print(f"\nDone. Output: {OUT}")


if __name__ == '__main__':
    main()
