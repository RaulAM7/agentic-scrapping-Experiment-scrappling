"""
Fase 4 - Escalado controlado de google_basic con discovery live en Google.

Usa Scrapling en dos pasos:
- discovery live con StealthySession sobre Google
- extraccion de contacto en las webs descubiertas con Fetcher
"""

from __future__ import annotations

import csv
import json
import re
import time
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
from urllib.parse import urljoin, urlparse, urlunparse

from scrapling.fetchers import Fetcher, StealthySession

import experimento_1_pilot_extract as pilot


SCRATCH_DIR = Path("05_scratch/experimento_1")
OUTPUT_DIR = Path("04_outputs/experimento_1")

DATA_JSON = SCRATCH_DIR / "2026-03-07_google-basic-scaled-dataset_experimento-1.json"
DATA_CSV = SCRATCH_DIR / "2026-03-07_google-basic-scaled-dataset_experimento-1.csv"
RESULTS_JSON = SCRATCH_DIR / "2026-03-07_google-basic-live-serp-results.json"
SUMMARY_MD = OUTPUT_DIR / "2026-03-07_escalado-google-basic_experimento-1_v1.md"

HOME_URLS = [
    "https://www.google.com/?hl=es&gl=ES",
    "https://www.google.es/?hl=es",
]

QUERY_DEFS = [
    {
        "query": '"asesoria fiscal" "Las Palmas de Gran Canaria" "contacto"',
        "query_cluster": "gb_core_contact",
        "fallback_geography": "las palmas de gran canaria|gran canaria",
    },
    {
        "query": '"asesoria contable" "Santa Cruz de Tenerife" "contacto"',
        "query_cluster": "gb_core_contact",
        "fallback_geography": "santa cruz de tenerife|tenerife",
    },
    {
        "query": '"gestoria" "Gran Canaria" inurl:contacto',
        "query_cluster": "gb_core_contact",
        "fallback_geography": "unknown|gran canaria",
    },
    {
        "query": '"asesoria fiscal contable" Canarias email',
        "query_cluster": "gb_core_contact",
        "fallback_geography": "multiple|canarias",
    },
    {
        "query": '"asesoria autonomos" Canarias "contacto"',
        "query_cluster": "gb_service_pain",
        "fallback_geography": "multiple|canarias",
    },
    {
        "query": '"asesoria pymes" "Las Palmas" inurl:servicios',
        "query_cluster": "gb_service_pain",
        "fallback_geography": "las palmas de gran canaria|gran canaria",
    },
    {
        "query": "IGIC asesoria Tenerife contacto",
        "query_cluster": "gb_service_pain",
        "fallback_geography": "unknown|tenerife",
    },
    {
        "query": '"sociedades" "asesoria fiscal" Canarias email',
        "query_cluster": "gb_service_pain",
        "fallback_geography": "multiple|canarias",
    },
]

BLOCKED_DOMAINS = {
    "agenciatributaria.gob.es",
    "asesoresfiscalesdecanarias.org",
    "ayudatpymes.com",
    "clubdelasesor.com",
    "cotime.es",
    "cronoshare.com",
    "cronoshare.com.mx",
    "deustoformacion.com",
    "einforma.com",
    "factorial.es",
    "glassdoor.es",
    "gobiernodecanarias.org",
    "google.com",
    "google.es",
    "holded.com",
    "iberinform.es",
    "laspalmasgc.es",
    "linkedin.com",
    "lajanda.legal",
    "modelosdeplandenegocios.com",
    "openges.es",
    "taxdown.es",
    "todosbiz.es",
    "trustlocal.es",
    "ufv.es",
    "webnode.es",
    "youtube.com",
}

DISCARD_HINTS = {
    "blog",
    "cuanto cuesta",
    "diferencias",
    "funciones",
    "master",
    "precio",
    "preguntas",
    "salario",
    "vs.",
    "vs ",
}

URL_DISCARD_HINTS = {
    "/ayuntamiento/",
    "/cuanto-cuesta",
    "/empresa/",
    "/informes-empresas/",
    "/procedimientoini/",
    "/sueldo",
    "/tributos/",
}

NON_TARGET_HINTS = {
    "agencia tributaria",
    "ayuntamiento",
    "ciudadania",
    "contacto y ayuda",
    "deusto",
    "einforma",
    "glassdoor",
    "gobierno de canarias",
    "holded",
    "iberinform",
    "todosbiz",
    "tributaria",
}

CONTACT_HINTS = (
    "contact",
    "contacto",
    "escribenos",
    "escribenos",
    "oficina",
)

GEO_HINTS = [
    ("las palmas de gran canaria", "las palmas de gran canaria|gran canaria"),
    ("santa cruz de tenerife", "santa cruz de tenerife|tenerife"),
    ("san cristobal de la laguna", "san cristobal de la laguna|tenerife"),
    ("la laguna", "san cristobal de la laguna|tenerife"),
    ("san bartolome de tirajana", "san bartolome de tirajana|gran canaria"),
    ("maspalomas", "san bartolome de tirajana|gran canaria"),
    ("arrecife", "arrecife|lanzarote"),
    ("telde", "telde|gran canaria"),
    ("gran canaria", "unknown|gran canaria"),
    ("tenerife", "unknown|tenerife"),
    ("lanzarote", "unknown|lanzarote"),
    ("fuerteventura", "unknown|fuerteventura"),
    ("canarias", "multiple|canarias"),
]


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def strip_fragment(url: str) -> str:
    parsed = urlparse(url)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, parsed.query, ""))


def page_action_search(page: Any, query: str) -> None:
    for selector in [
        'button:has-text("Aceptar todo")',
        'button:has-text("Aceptar")',
        'button:has-text("Accept all")',
        'button:has-text("I agree")',
        "form button",
    ]:
        try:
            locator = page.locator(selector)
            if locator.count():
                locator.first.click(timeout=2500)
                page.wait_for_timeout(1200)
                break
        except Exception:
            continue

    for selector in ["textarea[name='q']", "input[name='q']"]:
        try:
            locator = page.locator(selector)
            if locator.count():
                locator.first.click(timeout=3000)
                locator.first.fill("")
                locator.first.type(query, delay=55)
                page.keyboard.press("Enter")
                page.wait_for_timeout(3500)
                try:
                    page.wait_for_load_state("networkidle", timeout=8000)
                except Exception:
                    pass
                return
        except Exception:
            continue


def organic_anchor_text(anchor: Any) -> str:
    text = " ".join(part.strip() for part in (anchor.css("::text").getall() or []) if part.strip())
    return clean_text(text)


def is_allowed_result(url: str, text: str) -> bool:
    lower = f"{url} {text}".lower()
    host = pilot.website_root(url)
    if not url.startswith(("http://", "https://")):
        return False
    if text == "Unknown":
        return False
    if url.lower().endswith(".pdf"):
        return False
    if any(hint in url.lower() for hint in URL_DISCARD_HINTS):
        return False
    if host in BLOCKED_DOMAINS:
        return False
    if any(host.endswith(f".{item}") for item in BLOCKED_DOMAINS):
        return False
    if any(token in host for token in ["facebook.", "instagram.", "x.com"]):
        return False
    if any(hint in lower for hint in DISCARD_HINTS):
        return False
    return True


def page_has_results(page: Any) -> bool:
    external_links = [
        a.attrib.get("href", "")
        for a in page.css('a[href^="http"]')
        if is_allowed_result(a.attrib.get("href", ""), organic_anchor_text(a))
    ]
    return len(page.css("h3")) >= 3 and len(external_links) >= 3


def parse_search_results(page: Any, query_def: dict[str, str]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    seen_urls: set[str] = set()
    rank = 0
    for anchor in page.css('a[href^="http"]'):
        href = strip_fragment(anchor.attrib.get("href", ""))
        if not href:
            continue
        title = organic_anchor_text(anchor)
        if not is_allowed_result(href, title):
            continue
        if href in seen_urls:
            continue
        seen_urls.add(href)
        rank += 1
        records.append(
            {
                "query": query_def["query"],
                "query_cluster": query_def["query_cluster"],
                "fallback_geography": query_def["fallback_geography"],
                "serp_rank": rank,
                "url": href,
                "serp_title": title or "Unknown",
                "domain": pilot.website_root(href),
            }
        )
        if len(records) >= 8:
            break
    return records


def search_google(query_def: dict[str, str]) -> dict[str, Any]:
    attempts: list[dict[str, Any]] = []
    for home_url in HOME_URLS:
        with TemporaryDirectory(prefix="google-basic-live-") as tmpdir:
            with StealthySession(
                user_data_dir=tmpdir,
                headless=True,
                locale="es-ES",
                disable_resources=False,
                retries=1,
                hide_canvas=True,
                block_webrtc=True,
            ) as session:
                page = session.fetch(
                    home_url,
                    google_search=False,
                    network_idle=True,
                    wait=2500,
                    page_action=lambda page: page_action_search(page, query_def["query"]),
                )
                status = getattr(page, "status", None)
                attempt = {
                    "query": query_def["query"],
                    "home_url": home_url,
                    "status": status,
                    "final_url": getattr(page, "url", None),
                    "title": page.css("title::text").get("").strip(),
                    "h3_count": len(page.css("h3")),
                    "results": parse_search_results(page, query_def),
                }
                attempt["results_count"] = len(attempt["results"])
                attempts.append(attempt)
                if status == 200 and page_has_results(page):
                    return {
                        "query": query_def["query"],
                        "query_cluster": query_def["query_cluster"],
                        "fallback_geography": query_def["fallback_geography"],
                        "status": "pass",
                        "attempts": attempts,
                        "results": attempt["results"],
                    }
        time.sleep(1.5)
    return {
        "query": query_def["query"],
        "query_cluster": query_def["query_cluster"],
        "fallback_geography": query_def["fallback_geography"],
        "status": "watch",
        "attempts": attempts,
        "results": attempts[-1]["results"] if attempts else [],
    }


def same_domain(url: str, domain: str) -> bool:
    return pilot.website_root(url) == domain


def candidate_contact_urls(page: Any, source_url: str) -> list[str]:
    domain = pilot.website_root(source_url)
    root = f"{urlparse(source_url).scheme}://{urlparse(source_url).netloc}"
    candidates = [root]
    for anchor in page.css("a[href]"):
        href = anchor.attrib.get("href", "").strip()
        if not href:
            continue
        absolute = strip_fragment(urljoin(source_url, href))
        if not absolute.startswith(("http://", "https://")):
            continue
        if not same_domain(absolute, domain):
            continue
        lower = f"{absolute} {organic_anchor_text(anchor).lower()}"
        if any(hint in lower for hint in CONTACT_HINTS):
            candidates.append(absolute)
    return pilot.unique_keep_order(candidates)[:4]


def derive_company_name(page: Any, serp_title: str, domain: str) -> str:
    for selector in [
        'meta[property="og:site_name"]::attr(content)',
        'meta[name="application-name"]::attr(content)',
        "header img[alt]::attr(alt)",
        ".site-title::text",
        "h1::text",
        "title::text",
    ]:
        value = clean_text(page.css(selector).get(""))
        if value and len(value) <= 120:
            value = re.split(r"\s+[|\-]\s+", value, maxsplit=1)[0].strip()
            if value:
                return value

    if serp_title and serp_title != "Unknown":
        value = re.split(r"\s+https?://|\s+[|\-]\s+", serp_title, maxsplit=1)[0].strip()
        if value:
            return value

    host = domain.replace(".es", "").replace(".com", "")
    host = host.replace("www.", "")
    return host.replace("-", " ").replace(".", " ").title()


def infer_geography(text: str, fallback: str) -> tuple[str, bool]:
    lower = text.lower()
    for needle, geography in GEO_HINTS:
        if needle in lower:
            return geography, True
    return fallback, False


def fetch_page(url: str) -> Any | None:
    try:
        page = Fetcher.get(url, timeout=30000)
    except Exception:
        return None
    if getattr(page, "status", 0) and int(getattr(page, "status", 0)) >= 400:
        return None
    return page


def collect_contact_bundle(candidate: dict[str, Any]) -> dict[str, Any] | None:
    primary_page = fetch_page(candidate["url"])
    if primary_page is None:
        return None

    domain = candidate["domain"]
    visited_pages = []
    emails: list[str] = []
    forms: list[str] = []
    phones: list[str] = []
    combined_text_parts: list[str] = []
    contact_page_url = "Unknown"

    for idx, url in enumerate(candidate_contact_urls(primary_page, candidate["url"])):
        page = primary_page if idx == 0 and strip_fragment(candidate["url"]) == strip_fragment(url) else fetch_page(url)
        if page is None:
            continue
        visited_pages.append(url)
        combined_text_parts.append(pilot.extract_html_text(page))
        emails.extend(pilot.extract_emails_from_page(page))
        forms.extend(pilot.extract_contact_forms(page, url))
        phones.extend(pilot.extract_tel_links(page))
        if contact_page_url == "Unknown" and ("contact" in url.lower() or "contacto" in url.lower()):
            contact_page_url = url

    emails = pilot.unique_keep_order(emails)
    forms = pilot.unique_keep_order(forms)
    phones = pilot.unique_keep_order(phones)
    combined_text = "\n".join(combined_text_parts)
    company_name = derive_company_name(primary_page, candidate["serp_title"], domain)
    geography, geography_from_page = infer_geography(combined_text, candidate["fallback_geography"])
    best_email = pilot.choose_best_email(emails, domain)

    if best_email:
        contact_type = "email"
        channel = best_email
    elif forms:
        contact_type = "form"
        channel = forms[0]
    elif phones:
        contact_type = "other_direct"
        channel = phones[0]
    else:
        contact_type = "none"
        channel = "none"

    services = pilot.normalize_services(combined_text)
    icp_signals = pilot.build_icp_signals(
        services=services,
        geography=geography,
        url=candidate["url"],
        email=best_email,
        has_form=bool(forms),
        website_domain=domain,
    )
    icp_score = pilot.compute_icp_score(services, geography, icp_signals, contact_type)
    contactability = pilot.compute_contactability_score(contact_type, channel, domain)

    notes = ["google_live_discovery"]
    if len(visited_pages) > 1:
        notes.append("contact_path_followup")
    if candidate["url"] != f"https://{domain}":
        notes.append("serp_landing_not_root")
    notes.append("geo_from_page" if geography_from_page else "geo_from_query_fallback")

    return {
        "company_name": company_name or "Unknown",
        "source_lane": "google_basic",
        "source_name": "google_basic_live_serp",
        "source_url": candidate["url"],
        "query_cluster": candidate["query_cluster"],
        "geography": geography,
        "contact_channel_type": contact_type,
        "email_or_channel": channel,
        "website_url": f"https://{domain}",
        "services": services,
        "icp_signals": icp_signals,
        "source_quality_score": 0,
        "contactability_score": contactability,
        "dedupe_key": pilot.build_dedupe_key(company_name or "Unknown", geography, contact_type, channel, candidate["url"], "google_basic_live_serp"),
        "source_query": candidate["query"],
        "source_rank": candidate["serp_rank"],
        "contact_page_url": contact_page_url,
        "company_phone": phones[0] if phones else "Unknown",
        "postal_address": "Unknown",
        "role_hint": "despacho",
        "icp_score": icp_score,
        "evidence_snippet": f"serp={candidate['serp_title'][:100]} | channel={channel}",
        "scrapling_fetcher": "StealthySession + Fetcher",
        "extracted_at_utc": pilot.now_iso(),
        "notes": ", ".join(notes),
    }


def record_is_target(record: dict[str, Any]) -> bool:
    haystack = " ".join(
        [
            record["company_name"],
            record["website_url"],
            record["source_url"],
            " ".join(record["services"]),
            record["source_query"],
            record["notes"],
        ]
    ).lower()
    if record["contact_channel_type"] == "none":
        return False
    if any(token in haystack for token in NON_TARGET_HINTS):
        return False
    if not any(token in haystack for token in ["asesor", "asesoria", "gestor", "gestoria", "consult", "fiscal", "contable"]):
        return False
    if not any(token in record["geography"] for token in ["gran canaria", "tenerife", "lanzarote", "fuerteventura", "canarias"]):
        return False
    if "geo_from_query_fallback" in record["notes"] and not any(
        token in haystack for token in ["canarias", "tenerife", "gran canaria", "las palmas", "lanzarote", "fuerteventura"]
    ):
        return False
    return True


def source_metrics(records: list[dict[str, Any]], query_runs: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(records)
    emails = [r for r in records if r["contact_channel_type"] == "email"]
    alt = [r for r in records if r["contact_channel_type"] in {"form", "other_direct"}]
    p0 = [r for r in records if r["contact_channel_type"] != "none"]
    unique_email_count = len({r["email_or_channel"] for r in emails})
    duplicate_count = total - len({r["dedupe_key"] for r in records})
    useful_icp = [r for r in records if len(r["icp_signals"]) >= 2 or r["icp_score"] >= 60]
    precision_ok = [
        r for r in records if r["company_name"] != "Unknown" and r["contact_channel_type"] != "none" and len(r["services"]) >= 1
    ]
    noise = [r for r in records if r["company_name"] == "Unknown" or (r["contact_channel_type"] == "none" and not r["services"])]
    passed_queries = [run for run in query_runs if run["status"] == "pass"]

    def pct(value: float) -> float:
        return round(value * 100, 1)

    p0_rate = len(p0) / total if total else 0.0
    density_rate = len(useful_icp) / total if total else 0.0
    precision_rate = len(precision_ok) / total if total else 0.0
    noise_dup_rate = min((len(noise) + duplicate_count) / total, 1.0) if total else 1.0
    query_pass_rate = len(passed_queries) / len(query_runs) if query_runs else 0.0

    tech_points = 9 if query_pass_rate >= 0.5 else 6 if query_pass_rate >= 0.25 else 3
    cost_points = 7 if total >= 20 else 5 if total >= 10 else 3
    risk_points = 4 if query_pass_rate >= 0.5 else 3 if query_pass_rate >= 0.25 else 2
    integral_viability = query_pass_rate >= 0.5 and total >= 12
    viability_note = (
        "Discovery live en Google validado con StealthySession; aun existe fragilidad parcial por query."
        if integral_viability
        else "Discovery live parcialmente funcional; la tasa de queries con resultados aun es insuficiente."
    )

    source_quality = round(
        30 * p0_rate
        + 20 * density_rate
        + 15 * precision_rate
        + 10 * (1 - noise_dup_rate)
        + tech_points
        + cost_points
        + risk_points
    )
    gate_pass = (
        p0_rate >= 0.30
        and ((len(noise) + duplicate_count) / total if total else 1.0) <= 0.25
        and source_quality >= 60
        and integral_viability
    )

    return {
        "source_name": "google_basic_live_serp",
        "sample_size": total,
        "p0_contactable_pct": pct(p0_rate),
        "email_real_pct": pct(len(emails) / total if total else 0.0),
        "alt_channel_pct": pct(len(alt) / total if total else 0.0),
        "unique_email_pct": pct(unique_email_count / len(emails) if emails else 0.0),
        "noise_pct": pct(len(noise) / total if total else 0.0),
        "duplicate_pct": pct(duplicate_count / total if total else 0.0),
        "icp_signal_useful_pct": pct(density_rate),
        "query_pass_pct": pct(query_pass_rate),
        "source_quality_score": source_quality,
        "integral_scrapling_viability": integral_viability,
        "gate_pass": gate_pass,
        "viability_note": viability_note,
    }


def write_csv(records: list[dict[str, Any]]) -> None:
    with DATA_CSV.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "company_name",
                "source_lane",
                "source_name",
                "source_url",
                "query_cluster",
                "geography",
                "contact_channel_type",
                "email_or_channel",
                "website_url",
                "services",
                "icp_signals",
                "source_quality_score",
                "contactability_score",
                "dedupe_key",
                "source_query",
                "source_rank",
                "contact_page_url",
                "company_phone",
                "postal_address",
                "role_hint",
                "icp_score",
                "evidence_snippet",
                "scrapling_fetcher",
                "extracted_at_utc",
                "notes",
            ],
        )
        writer.writeheader()
        for record in records:
            row = dict(record)
            row["services"] = ", ".join(record["services"])
            row["icp_signals"] = ", ".join(record["icp_signals"])
            writer.writerow(row)


def main() -> None:
    SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    query_runs = []
    candidate_pool: list[dict[str, Any]] = []
    seen_domains: set[str] = set()

    for query_def in QUERY_DEFS:
        run = search_google(query_def)
        query_runs.append(run)
        for item in run["results"]:
            if item["domain"] in seen_domains:
                continue
            seen_domains.add(item["domain"])
            candidate_pool.append(item)
        time.sleep(2)

    records: list[dict[str, Any]] = []
    for candidate in candidate_pool:
        record = collect_contact_bundle(candidate)
        if record and record_is_target(record):
            records.append(record)
        time.sleep(0.8)

    deduped = list({record["dedupe_key"]: record for record in records}.values())
    deduped.sort(
        key=lambda row: (row["contactability_score"], row["icp_score"], row["company_name"].lower()),
        reverse=True,
    )

    metrics = source_metrics(deduped, query_runs)
    pilot.apply_source_quality(deduped, metrics)

    RESULTS_JSON.write_text(json.dumps(query_runs, ensure_ascii=False, indent=2), encoding="utf-8")
    DATA_JSON.write_text(json.dumps(deduped, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(deduped)

    top_rows = [
        f"| {record['company_name']} | {record['geography']} | {record['email_or_channel']} | {record['source_rank']} | {record['contactability_score']} |"
        for record in deduped[:15]
    ]
    query_lines = []
    for run in query_runs:
        attempts = run["attempts"]
        first_attempt = attempts[0] if attempts else {}
        query_lines.append(
            f"- `{run['query']}` -> `{run['status']}` | results `{len(run['results'])}` | first status `{first_attempt.get('status')}`"
        )

    summary = "\n".join(
        [
            "# Escalado Google Basic - Experimento 1",
            "",
            "- Fecha: 2026-03-07",
            "- Fuente: `google_basic_live_serp`",
            f"- Registros extraidos: `{len(deduped)}`",
            f"- `source_quality_score`: `{metrics['source_quality_score']}`",
            f"- Gate de escalado: `{metrics['gate_pass']}`",
            "",
            "## Scorecard",
            "",
            f"- `% P0 contactable`: `{metrics['p0_contactable_pct']}`",
            f"- `% email real`: `{metrics['email_real_pct']}`",
            f"- `% canal alternativo`: `{metrics['alt_channel_pct']}`",
            f"- `% emails unicos`: `{metrics['unique_email_pct']}`",
            f"- `% ruido`: `{metrics['noise_pct']}`",
            f"- `% duplicados`: `{metrics['duplicate_pct']}`",
            f"- `% señales ICP útiles`: `{metrics['icp_signal_useful_pct']}`",
            f"- `% queries con discovery live valido`: `{metrics['query_pass_pct']}`",
            "",
            "## Resultado por query",
            "",
            *query_lines,
            "",
            "## Top ranking orientado a emailing",
            "",
            "| Company | Geography | Email/Canal | SERP rank | Contactability |",
            "|---|---|---|---:|---:|",
            *top_rows,
            "",
            "## Lectura operativa",
            "",
            f"- {metrics['viability_note']}",
            "- Este dataset ya no depende de seeds manuales: la discovery nace en Google y la extraccion de contacto se resuelve despues en la web propia.",
            "- Si la fuente pasa gate, `google_basic` ya puede tratarse como candidato real a bulk dentro del stack actual.",
        ]
    ) + "\n"

    SUMMARY_MD.write_text(summary, encoding="utf-8")

    print(f"Wrote {RESULTS_JSON}")
    print(f"Wrote {DATA_JSON}")
    print(f"Wrote {DATA_CSV}")
    print(f"Wrote {SUMMARY_MD}")
    print(
        f"records={len(deduped)} query_pass_pct={metrics['query_pass_pct']} "
        f"source_quality_score={metrics['source_quality_score']} gate_pass={metrics['gate_pass']}"
    )


if __name__ == "__main__":
    main()
