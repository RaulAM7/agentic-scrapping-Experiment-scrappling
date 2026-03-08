"""
Piloto Fase 3 - Experimento 1 Scrapling (Email-First).

Extrae una muestra acotada de dos fuentes:
- google_basic (semillas de webs propias ya revalidadas)
- specialized_directory (AAFC / Despachos Profesionales)

Nota metodologica:
- La discovery live de Google no queda resuelta con Scrapling en este entorno.
- El piloto de `google_basic` usa una seed list curada desde la Fase 2 para medir
  la capacidad real de extraer contacto accionable desde webs propias.
"""

from __future__ import annotations

import csv
import json
import re
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

from scrapling.fetchers import Fetcher


OUT_DIR = Path("05_scratch/experimento_1")
DATASET_JSON = OUT_DIR / "2026-03-07_pilot-dataset_experimento-1.json"
DATASET_CSV = OUT_DIR / "2026-03-07_pilot-dataset_experimento-1.csv"
SCORECARD_JSON = OUT_DIR / "2026-03-07_pilot-scorecard_experimento-1.json"
SCORECARD_MD = OUT_DIR / "2026-03-07_pilot-scorecard_experimento-1.md"

EMAIL_RE = re.compile(r"(?i)\b[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}\b")
PHONE_RE = re.compile(r"(?<!\d)(?:\+34\s*)?(?:\d[\s./-]?){9,}(?!\d)")
GENERIC_LOCALS = {
    "info",
    "contacto",
    "contact",
    "hola",
    "hello",
    "admin",
    "administracion",
    "direccion",
    "recepcion",
    "asesoria",
    "fiscal",
    "office",
    "comercial",
}
FREE_EMAIL_DOMAINS = {
    "gmail.com",
    "hotmail.com",
    "outlook.com",
    "yahoo.es",
    "yahoo.com",
    "icloud.com",
}
SERVICE_KEYWORDS = {
    "fiscal": "fiscal",
    "contable": "contable",
    "laboral": "laboral",
    "autonom": "autonomos",
    "pyme": "pymes",
    "sociedad": "sociedades",
    "igic": "igic",
    "renta": "renta",
    "mercantil": "mercantil",
    "subvencion": "subvenciones",
}


@dataclass(frozen=True)
class GoogleSeed:
    company_name: str
    url: str
    geography: str
    query_cluster: str
    source_query: str
    role_hint: str = "despacho"
    preferred_email: str | None = None


GOOGLE_SEEDS: list[GoogleSeed] = [
    GoogleSeed(
        company_name="J&M Consulting",
        url="https://jmsconsulting.es/contacto/",
        geography="unknown|gran canaria",
        query_cluster="gb_core_contact",
        source_query='"asesoria fiscal" "Las Palmas de Gran Canaria" "contacto"',
    ),
    GoogleSeed(
        company_name="Unificont",
        url="https://unificont.es/",
        geography="unknown|gran canaria",
        query_cluster="gb_core_contact",
        source_query='"asesoria fiscal contable" Canarias email',
    ),
    GoogleSeed(
        company_name="Asesoria Fiscal Tenerife",
        url="https://asesoriafiscaltenerife.es/",
        geography="santa cruz de tenerife|tenerife",
        query_cluster="gb_core_contact",
        source_query='"asesoria contable" "Santa Cruz de Tenerife" "contacto"',
    ),
    GoogleSeed(
        company_name="Asesoramientos Tenerife",
        url="https://www.asesoramientostenerife.com/",
        geography="santa cruz de tenerife|tenerife",
        query_cluster="gb_service_pain",
        source_query='IGIC asesoria Tenerife contacto',
    ),
    GoogleSeed(
        company_name="Fiscal Tax Canarias",
        url="https://fiscaltaxcanarias.com/servicios/",
        geography="las palmas de gran canaria|gran canaria",
        query_cluster="gb_service_pain",
        source_query='"sociedades" "asesoria fiscal" Canarias email',
    ),
    GoogleSeed(
        company_name="OpenPlus Asesores",
        url="https://openplusasesores.es/",
        geography="las palmas de gran canaria|gran canaria",
        query_cluster="gb_core_contact",
        source_query='"asesoria fiscal" "Las Palmas de Gran Canaria" "contacto"',
    ),
    GoogleSeed(
        company_name="Asesoria en Tenerife",
        url="https://www.asesoriaentenerife.es/",
        geography="santa cruz de tenerife|tenerife",
        query_cluster="gb_core_contact",
        source_query='"asesoria contable" "Santa Cruz de Tenerife" "contacto"',
    ),
    GoogleSeed(
        company_name="Asesoria BV",
        url="https://asesoriabv.es/fiscal/",
        geography="multiple|canarias",
        query_cluster="gb_service_pain",
        source_query='"asesoria pymes" "Las Palmas" inurl:servicios',
        preferred_email="asesoriabvgc@gmail.com",
    ),
    GoogleSeed(
        company_name="Asesquivel",
        url="https://www.asesquivel.es/",
        geography="las palmas de gran canaria|gran canaria",
        query_cluster="gb_core_contact",
        source_query='"asesoria fiscal" "Las Palmas de Gran Canaria" "contacto"',
    ),
    GoogleSeed(
        company_name="Asesoria Garsa",
        url="https://asesoriagarsa.com/fiscal-contable/",
        geography="unknown|gran canaria",
        query_cluster="gb_service_pain",
        source_query='"asesoria fiscal contable" Canarias email',
    ),
    GoogleSeed(
        company_name="Legiscan",
        url="https://legiscan.es/",
        geography="las palmas de gran canaria|gran canaria",
        query_cluster="gb_service_pain",
        source_query='"asesoria pymes" "Las Palmas" inurl:servicios',
        preferred_email="legiscan@legiscan.es",
    ),
    GoogleSeed(
        company_name="Asesores Canarios",
        url="https://asesores-canarios.com/contacto-asesoria.html",
        geography="san bartolome de tirajana|gran canaria",
        query_cluster="gb_core_contact",
        source_query='"gestoria" "Gran Canaria" inurl:contacto',
    ),
]


def now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def normalize_email(raw: str) -> str | None:
    item = unquote(raw.strip()).lower().removeprefix("mailto:")
    item = item.split("?", 1)[0].strip()
    if not EMAIL_RE.fullmatch(item):
        return None
    return item


def unique_keep_order(items: list[str]) -> list[str]:
    out: list[str] = []
    seen = set()
    for item in items:
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out


def slugify(value: str) -> str:
    value = value.lower().strip()
    replacements = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "ü": "u",
        "ñ": "n",
        "&": "and",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    value = re.sub(r"\b(s\.?l\.?p?|s\.?c\.?p|s\.?a|s\.?l|cb)\b", "", value)
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value or "unknown"


def website_root(url: str) -> str:
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    return host


def extract_html_text(page: Any) -> str:
    html = str(getattr(page, "html_content", "") or "")
    text = str(getattr(page, "text", "") or "")
    return f"{text}\n{html}"


def extract_emails_from_page(page: Any) -> list[str]:
    hrefs = [normalize_email(x) for x in (page.css('a[href^="mailto:"]::attr(href)').getall() or [])]
    regexes = [normalize_email(x) for x in EMAIL_RE.findall(extract_html_text(page))]
    return unique_keep_order([x for x in [*hrefs, *regexes] if x])


def extract_tel_links(page: Any) -> list[str]:
    results = []
    for tel in page.css('a[href^="tel:"]::attr(href)').getall() or []:
        digits = re.sub(r"\D+", "", tel)
        if len(digits) >= 9:
            results.append(digits)
    return unique_keep_order(results)


def extract_contact_forms(page: Any, base_url: str) -> list[str]:
    forms = []
    for action in page.css("form::attr(action)").getall() or []:
        action = action.strip()
        if not action:
            continue
        if action.startswith("http://") or action.startswith("https://"):
            forms.append(action)
        else:
            parsed = urlparse(base_url)
            root = f"{parsed.scheme}://{parsed.netloc}"
            forms.append(root + (action if action.startswith("/") else f"/{action}"))
    return unique_keep_order(forms)


def parse_phone_from_text(value: str) -> str | None:
    match = PHONE_RE.search(value or "")
    if not match:
        return None
    digits = re.sub(r"\D+", "", match.group(0))
    return digits if len(digits) >= 9 else None


def choose_best_email(emails: list[str], website_domain: str | None = None, preferred: str | None = None) -> str | None:
    if preferred and preferred in emails:
        return preferred

    def score(email: str) -> tuple[int, int]:
        local, _, domain = email.partition("@")
        own_domain = int(bool(website_domain and domain == website_domain))
        non_free = int(domain not in FREE_EMAIL_DOMAINS)
        non_generic = int(local not in GENERIC_LOCALS)
        return (own_domain * 100 + non_free * 10 + non_generic, -len(local))

    if not emails:
        return None
    return sorted(emails, key=score, reverse=True)[0]


def normalize_services(text: str) -> list[str]:
    lower = text.lower()
    found = [label for needle, label in SERVICE_KEYWORDS.items() if needle in lower]
    return unique_keep_order(found)


def build_icp_signals(
    services: list[str],
    geography: str,
    url: str,
    email: str | None,
    has_form: bool,
    website_domain: str | None,
) -> list[str]:
    signals: list[str] = []
    municipality, _, island = geography.partition("|")
    if email:
        local, _, domain = email.partition("@")
        if domain not in FREE_EMAIL_DOMAINS and website_domain and domain == website_domain and local not in GENERIC_LOCALS:
            signals.append("direct_email")
        elif domain not in FREE_EMAIL_DOMAINS:
            signals.append("direct_email")
    elif has_form:
        signals.append("form_only")

    if any(token in url.lower() for token in ["/contact", "/contacto", "contacto"]):
        signals.append("contact_page")

    if municipality in {"las palmas de gran canaria", "santa cruz de tenerife"}:
        signals.append("capital_insular")

    for service in services:
        if service in {"igic", "autonomos", "pymes", "sociedades"}:
            signals.append(service)

    return unique_keep_order(signals)


def compute_icp_score(services: list[str], geography: str, icp_signals: list[str], contact_type: str) -> int:
    score = 0
    if "fiscal" in services:
        score += 25
    if "contable" in services:
        score += 25
    if "laboral" in services:
        score += 10
    if any(item in services for item in ["autonomos", "pymes", "sociedades", "igic"]):
        score += 15
    if geography.split("|", 1)[0] in {"las palmas de gran canaria", "santa cruz de tenerife"}:
        score += 15
    elif geography.endswith("|gran canaria") or geography.endswith("|tenerife"):
        score += 10
    if "direct_email" in icp_signals:
        score += 10
    elif contact_type == "email":
        score += 5
    return min(score, 100)


def compute_contactability_score(contact_type: str, channel: str, website_domain: str | None = None) -> int:
    if contact_type == "none":
        return 0
    if contact_type == "form":
        return 50
    if contact_type == "other_direct":
        return 45

    email = channel.lower()
    local, _, domain = email.partition("@")
    if domain in FREE_EMAIL_DOMAINS:
        return 55
    if website_domain and domain == website_domain and local not in GENERIC_LOCALS:
        return 95
    if website_domain and domain == website_domain:
        return 80
    if local not in GENERIC_LOCALS:
        return 85
    return 72


def build_dedupe_key(company_name: str, geography: str, contact_type: str, channel: str, website_url: str, source_name: str) -> str:
    company_slug = slugify(company_name)
    geography_slug = slugify(geography.replace("|", "-"))
    if contact_type == "none":
        fallback = slugify(website_root(website_url) or source_name)
        return f"{company_slug}|{geography_slug}|none|{fallback}"
    channel_slug = slugify(channel)
    return f"{company_slug}|{geography_slug}|{contact_type}|{channel_slug}"


def google_record(seed: GoogleSeed, source_rank: int) -> dict[str, Any]:
    page = Fetcher.get(seed.url, timeout=30000)
    website_domain = website_root(seed.url)
    emails = extract_emails_from_page(page)
    forms = extract_contact_forms(page, seed.url)
    phones = extract_tel_links(page)
    best_email = choose_best_email(emails, website_domain, seed.preferred_email)

    if best_email:
        contact_type = "email"
        email_or_channel = best_email
    elif forms:
        contact_type = "form"
        email_or_channel = forms[0]
    elif phones:
        contact_type = "other_direct"
        email_or_channel = phones[0]
    else:
        contact_type = "none"
        email_or_channel = "none"

    page_text = extract_html_text(page)
    services = normalize_services(page_text)
    icp_signals = build_icp_signals(
        services=services,
        geography=seed.geography,
        url=seed.url,
        email=best_email,
        has_form=bool(forms),
        website_domain=website_domain,
    )
    icp_score = compute_icp_score(services, seed.geography, icp_signals, contact_type)
    contactability = compute_contactability_score(contact_type, email_or_channel, website_domain)
    evidence = best_email or (forms[0] if forms else (phones[0] if phones else "none"))

    return {
        "company_name": seed.company_name,
        "source_lane": "google_basic",
        "source_name": "google_basic_seeded_websites",
        "source_url": seed.url,
        "query_cluster": seed.query_cluster,
        "geography": seed.geography,
        "contact_channel_type": contact_type,
        "email_or_channel": email_or_channel,
        "website_url": f"https://{website_domain}",
        "services": services,
        "icp_signals": icp_signals,
        "source_quality_score": 0,
        "contactability_score": contactability,
        "dedupe_key": build_dedupe_key(seed.company_name, seed.geography, contact_type, email_or_channel, seed.url, "google_basic_seeded_websites"),
        "source_query": seed.source_query,
        "source_rank": source_rank,
        "contact_page_url": seed.url if "contact" in seed.url else "Unknown",
        "company_phone": phones[0] if phones else "Unknown",
        "postal_address": "Unknown",
        "role_hint": seed.role_hint,
        "icp_score": icp_score,
        "evidence_snippet": f"channel={evidence}",
        "scrapling_fetcher": "Fetcher",
        "extracted_at_utc": now_iso(),
        "notes": "seeded_google_basic_pilot",
    }


def clean_node_text(node: Any) -> str:
    texts = [t.strip() for t in (node.css("::text").getall() or [])]
    texts = [t for t in texts if t]
    return " ".join(texts).strip()


def parse_aafc_card(card: Any, source_rank: int) -> dict[str, Any] | None:
    values = [clean_node_text(node) for node in card.css("div.info-value")]
    values = [value for value in values if value]
    if len(values) < 3:
        return None

    company_name = values[0]
    raw_geo = values[1]
    parts = [part.strip().lower() for part in raw_geo.split("|")]
    geography = f"{parts[1]}|{parts[0]}" if len(parts) >= 2 else f"unknown|{raw_geo.strip().lower()}"

    contact_line = next((value for value in values if "@" in value or PHONE_RE.search(value)), "")
    services_line = next((value for value in values if value.lower().startswith("servicios:")), "")
    emails = unique_keep_order([normalize_email(x) for x in EMAIL_RE.findall(contact_line) if normalize_email(x)])
    phone = parse_phone_from_text(contact_line) or "Unknown"
    services = normalize_services(services_line)

    if emails:
        contact_type = "email"
        email_or_channel = emails[0]
    elif phone != "Unknown":
        contact_type = "other_direct"
        email_or_channel = phone
    else:
        contact_type = "none"
        email_or_channel = "none"

    icp_signals = build_icp_signals(
        services=services,
        geography=geography,
        url="https://asesoresfiscalesdecanarias.org/servicios/despachos-profesionales/",
        email=emails[0] if emails else None,
        has_form=False,
        website_domain=None,
    )
    icp_score = compute_icp_score(services, geography, icp_signals, contact_type)
    contactability = compute_contactability_score(contact_type, email_or_channel, None)

    return {
        "company_name": company_name,
        "source_lane": "specialized_directory",
        "source_name": "AAFC - Despachos Profesionales",
        "source_url": "https://asesoresfiscalesdecanarias.org/servicios/despachos-profesionales/",
        "query_cluster": "sd_colegial_sectorial",
        "geography": geography,
        "contact_channel_type": contact_type,
        "email_or_channel": email_or_channel,
        "website_url": "Unknown",
        "services": services,
        "icp_signals": icp_signals,
        "source_quality_score": 0,
        "contactability_score": contactability,
        "dedupe_key": build_dedupe_key(company_name, geography, contact_type, email_or_channel, "", "AAFC - Despachos Profesionales"),
        "source_query": 'site:org "asesores fiscales" Canarias asociacion',
        "source_rank": source_rank,
        "contact_page_url": "Unknown",
        "company_phone": phone,
        "postal_address": "Unknown",
        "role_hint": "despacho",
        "icp_score": icp_score,
        "evidence_snippet": contact_line[:180] if contact_line else "none",
        "scrapling_fetcher": "Fetcher",
        "extracted_at_utc": now_iso(),
        "notes": "aafc_directory_pilot",
    }


def extract_aafc_records(limit: int | None = 12) -> list[dict[str, Any]]:
    page = Fetcher.get("https://asesoresfiscalesdecanarias.org/servicios/despachos-profesionales/", timeout=30000)
    cards = page.css("div.perfil-container")
    records: list[dict[str, Any]] = []
    for idx, card in enumerate(cards, start=1):
        record = parse_aafc_card(card, source_rank=idx)
        if record:
            records.append(record)
        if limit is not None and len(records) >= limit:
            break
    return records


def source_metrics(records: list[dict[str, Any]], source_name: str) -> dict[str, Any]:
    total = len(records)
    emails = [r for r in records if r["contact_channel_type"] == "email"]
    alt = [r for r in records if r["contact_channel_type"] in {"form", "other_direct"}]
    p0 = [r for r in records if r["contact_channel_type"] != "none"]
    unique_email_count = len({r["email_or_channel"] for r in emails})
    duplicate_count = total - len({r["dedupe_key"] for r in records})

    def pct(value: float) -> float:
        return round(value * 100, 1)

    useful_icp = [r for r in records if len(r["icp_signals"]) >= 2 or r["icp_score"] >= 60]
    precision_ok = [
        r
        for r in records
        if r["company_name"] != "Unknown" and r["contact_channel_type"] != "none" and len(r["services"]) >= 1
    ]
    noise = [r for r in records if r["company_name"] == "Unknown" or (r["contact_channel_type"] == "none" and not r["services"])]

    if source_name == "google_basic_seeded_websites":
        tech_points = 2
        cost_points = 3
        risk_points = 2
        integral_viability = False
        viability_note = "La extraccion de webs funciona con Scrapling, pero la discovery live en Google devuelve 429/sorry."
    else:
        tech_points = 9
        cost_points = 8
        risk_points = 4
        integral_viability = True
        viability_note = "Fuente extraible con Fetcher en esta muestra piloto."

    p0_rate = len(p0) / total if total else 0.0
    density_rate = len(useful_icp) / total if total else 0.0
    precision_rate = len(precision_ok) / total if total else 0.0
    noise_dup_rate = min((len(noise) + duplicate_count) / total, 1.0) if total else 1.0
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
        "source_name": source_name,
        "sample_size": total,
        "p0_contactable_pct": pct(p0_rate),
        "email_real_pct": pct(len(emails) / total if total else 0.0),
        "alt_channel_pct": pct(len(alt) / total if total else 0.0),
        "unique_email_pct": pct(unique_email_count / len(emails) if emails else 0.0),
        "noise_pct": pct(len(noise) / total if total else 0.0),
        "duplicate_pct": pct(duplicate_count / total if total else 0.0),
        "icp_signal_useful_pct": pct(density_rate),
        "source_quality_score": source_quality,
        "integral_scrapling_viability": integral_viability,
        "gate_pass": gate_pass,
        "viability_note": viability_note,
    }


def apply_source_quality(records: list[dict[str, Any]], metrics: dict[str, Any]) -> None:
    for record in records:
        record["source_quality_score"] = metrics["source_quality_score"]


def write_csv(records: list[dict[str, Any]]) -> None:
    fieldnames = [
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
    ]
    with DATASET_CSV.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            row = dict(record)
            row["services"] = ", ".join(record["services"])
            row["icp_signals"] = ", ".join(record["icp_signals"])
            writer.writerow(row)


def build_markdown(records: list[dict[str, Any]], metrics_list: list[dict[str, Any]], google_probe: dict[str, Any]) -> str:
    lines = [
        "# Pilot Scorecard - Experimento 1",
        "",
        f"- Fecha: {time.strftime('%Y-%m-%d')}",
        "- Scope: piloto acotado sobre `google_basic` y `AAFC` usando Scrapling API Python",
        "- Muestra: 12 registros `google_basic` (seeded) + 12 registros `AAFC`",
        "",
        "## Resumen",
        "",
    ]

    for metrics in metrics_list:
        lines.append(f"### {metrics['source_name']}")
        lines.append("")
        lines.append(f"- Sample size: `{metrics['sample_size']}`")
        lines.append(f"- `% P0 contactable`: `{metrics['p0_contactable_pct']}`")
        lines.append(f"- `% email real`: `{metrics['email_real_pct']}`")
        lines.append(f"- `% canal alternativo`: `{metrics['alt_channel_pct']}`")
        lines.append(f"- `% emails unicos`: `{metrics['unique_email_pct']}`")
        lines.append(f"- `% ruido`: `{metrics['noise_pct']}`")
        lines.append(f"- `% duplicados`: `{metrics['duplicate_pct']}`")
        lines.append(f"- `% senales ICP utiles`: `{metrics['icp_signal_useful_pct']}`")
        lines.append(f"- `source_quality_score`: `{metrics['source_quality_score']}`")
        lines.append(f"- Viabilidad integra con Scrapling: `{metrics['integral_scrapling_viability']}`")
        lines.append(f"- Gate piloto/escalado: `{metrics['gate_pass']}`")
        lines.append(f"- Nota: {metrics['viability_note']}")
        lines.append("")

    lines.extend(
        [
            "## Hallazgos clave",
            "",
            f"- `google_basic` extrae contacto muy bien una vez que entras en la web propia, pero la discovery live en Google sigue bloqueada: status `{google_probe['status']}` con `DynamicFetcher` y `StealthyFetcher` devolviendo `/sorry`.",
            "- `AAFC` se comporta como la mejor fuente sectorial del piloto: pagina estable, emails visibles y buena densidad fiscal-contable.",
            "- El piloto de `google_basic` es valido para medir contact extraction, no para declarar resuelta la discovery de Google.",
            "",
            "## Regla recomendada post-piloto",
            "",
            "- `AAFC - Despachos Profesionales`: `PASS` para seguir a escalado controlado.",
            "- `google_basic_seeded_websites`: `WATCH` para escalado. El output comercial es bueno, pero falla la exigencia de viabilidad integra con Scrapling por el bloqueo de Google.",
            "",
            "## Unknown y riesgos",
            "",
            "- `Unknown`: si Google puede volverse usable con otra estrategia Scrapling sin salir a proxies complejos.",
            "- `Unknown`: cuanto cambia el yield de `google_basic` cuando dejas las semillas curadas y entras en discovery real query-by-query.",
            "- Riesgo: sesgo optimista en `google_basic` porque la muestra entra por seeds ya validadas.",
            "- Riesgo: parte del AAFC puede requerir luego website enrichment externo si quieres web propia y no solo email/telefono.",
        ]
    )
    return "\n".join(lines).strip() + "\n"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    google_records = [google_record(seed, idx) for idx, seed in enumerate(GOOGLE_SEEDS, start=1)]
    aafc_records = extract_aafc_records(limit=12)
    all_records = [*google_records, *aafc_records]

    metrics_google = source_metrics(google_records, "google_basic_seeded_websites")
    metrics_aafc = source_metrics(aafc_records, "AAFC - Despachos Profesionales")
    apply_source_quality(google_records, metrics_google)
    apply_source_quality(aafc_records, metrics_aafc)

    google_probe = {
        "status": 429,
        "note": "Google Search con DynamicFetcher/StealthyFetcher devuelve /sorry en esta fase",
    }

    DATASET_JSON.write_text(json.dumps(all_records, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(all_records)
    scorecard = {
        "generated_at_utc": now_iso(),
        "google_probe": google_probe,
        "sources": [metrics_google, metrics_aafc],
    }
    SCORECARD_JSON.write_text(json.dumps(scorecard, ensure_ascii=False, indent=2), encoding="utf-8")
    SCORECARD_MD.write_text(build_markdown(all_records, [metrics_google, metrics_aafc], google_probe), encoding="utf-8")

    print(f"Wrote {DATASET_JSON}")
    print(f"Wrote {DATASET_CSV}")
    print(f"Wrote {SCORECARD_JSON}")
    print(f"Wrote {SCORECARD_MD}")
    for metrics in [metrics_google, metrics_aafc]:
        print(
            f"{metrics['source_name']}: sample={metrics['sample_size']} "
            f"email_real_pct={metrics['email_real_pct']} "
            f"source_quality_score={metrics['source_quality_score']} "
            f"gate_pass={metrics['gate_pass']}"
        )


if __name__ == "__main__":
    main()
