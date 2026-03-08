"""
Microvalidacion tecnica con Scrapling para Fase 2 del Experimento 1.

Valida tres fuentes candidatas:
- google_basic -> webs propias con email visible
- AAFC -> directorio/despachos profesionales
- Gestores Tenerife -> localizador + PDF de colegiados
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

from scrapling.fetchers import DynamicFetcher, Fetcher


EMAIL_RE = re.compile(r"(?i)\b[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}\b")
PHONE_RE = re.compile(r"(?<!\d)(?:\+34\s*)?(?:\d[\s.-]?){9,}(?!\d)")

ROOT = Path("05_scratch/experimento_1")
JSON_OUT = ROOT / "2026-03-07_scrapling-source-validation.json"
MD_OUT = ROOT / "2026-03-07_scrapling-source-validation.md"


def page_status(page: Any) -> int | None:
    return getattr(page, "status", None)


def page_reason(page: Any) -> str | None:
    return getattr(page, "reason", None)


def page_headers(page: Any) -> dict[str, Any]:
    return dict(getattr(page, "headers", {}) or {})


def page_text(page: Any) -> str:
    try:
        return str(page.text or "")
    except Exception:
        return ""


def page_html(page: Any) -> str:
    try:
        return str(page.html_content or "")
    except Exception:
        return ""


def normalize_emails(values: list[str]) -> list[str]:
    clean = []
    seen = set()
    for value in values:
        item = value.strip().lower().removeprefix("mailto:")
        item = item.split("?", 1)[0].strip()
        if not EMAIL_RE.fullmatch(item):
            continue
        if item and item not in seen:
            seen.add(item)
            clean.append(item)
    return clean


def extract_emails(page: Any) -> list[str]:
    href_emails = page.css('a[href^="mailto:"]::attr(href)').getall() or []
    blob = page_text(page) + "\n" + page_html(page)
    regex_emails = EMAIL_RE.findall(blob)
    return normalize_emails([*href_emails, *regex_emails])


def extract_phones(page: Any) -> list[str]:
    blob = page_text(page) + "\n" + page_html(page)
    seen = set()
    phones = []
    for match in PHONE_RE.findall(blob):
        digits = re.sub(r"\D+", "", match)
        if len(digits) >= 9 and digits not in seen:
            seen.add(digits)
            phones.append(digits)
    return phones


def fetch_static(url: str) -> dict[str, Any]:
    started = time.time()
    try:
        page = Fetcher.get(url, timeout=30000)
        elapsed = round(time.time() - started, 2)
        return summarize_page(url, "Fetcher", page, elapsed)
    except Exception as exc:
        elapsed = round(time.time() - started, 2)
        return {
            "url": url,
            "fetcher": "Fetcher",
            "status": None,
            "reason": None,
            "content_type": "",
            "elapsed_seconds": elapsed,
            "title": "",
            "emails": [],
            "phones": [],
            "link_count": 0,
            "html_length": 0,
            "text_length": 0,
            "keywords": {"contacto": 0, "despachos": 0, "buscador": 0, "colegiados": 0},
            "sample_links": [],
            "error": repr(exc),
        }


def fetch_dynamic(url: str) -> dict[str, Any]:
    started = time.time()
    try:
        page = DynamicFetcher.fetch(url, headless=True, network_idle=True, timeout=30000)
        elapsed = round(time.time() - started, 2)
        return summarize_page(url, "DynamicFetcher", page, elapsed)
    except Exception as exc:
        elapsed = round(time.time() - started, 2)
        return {
            "url": url,
            "fetcher": "DynamicFetcher",
            "status": None,
            "reason": None,
            "content_type": "",
            "elapsed_seconds": elapsed,
            "title": "",
            "emails": [],
            "phones": [],
            "link_count": 0,
            "html_length": 0,
            "text_length": 0,
            "keywords": {"contacto": 0, "despachos": 0, "buscador": 0, "colegiados": 0},
            "sample_links": [],
            "error": repr(exc),
        }


def summarize_page(url: str, fetcher: str, page: Any, elapsed: float) -> dict[str, Any]:
    headers = page_headers(page)
    title = page.css("title::text").get("").strip()
    text_blob = page_text(page)
    html_blob = page_html(page)
    pdf_blob = ""
    content_type = headers.get("content-type", "")
    if "pdf" in str(content_type).lower():
        body = getattr(page, "body", b"") or b""
        if isinstance(body, bytes):
            pdf_blob = body.decode("latin-1", errors="ignore")
        else:
            pdf_blob = str(body)

    all_emails = normalize_emails(EMAIL_RE.findall("\n".join([text_blob, html_blob, pdf_blob])))
    href_emails = normalize_emails(page.css('a[href^="mailto:"]::attr(href)').getall() or [])
    all_emails = normalize_emails([*href_emails, *all_emails])

    return {
        "url": url,
        "fetcher": fetcher,
        "final_url": getattr(page, "url", url),
        "status": page_status(page),
        "reason": page_reason(page),
        "content_type": content_type,
        "elapsed_seconds": elapsed,
        "title": title,
        "emails": all_emails,
        "phones": extract_phones(page),
        "link_count": len(page.css("a")),
        "html_length": len(html_blob),
        "text_length": len(text_blob),
        "keywords": {
            "contacto": int("contacto" in (text_blob + html_blob).lower()),
            "despachos": int("despach" in (text_blob + html_blob).lower()),
            "buscador": int("buscador" in (text_blob + html_blob).lower()),
            "colegiados": int("colegiad" in (text_blob + html_blob).lower()),
        },
        "sample_links": [
            {
                "text": anchor.css("::text").get("").strip(),
                "href": anchor.attrib.get("href", ""),
            }
            for anchor in page.css("a")[:10]
        ],
    }


def validate_google_basic() -> dict[str, Any]:
    urls = [
        "https://jmsconsulting.es/contacto/",
        "https://unificont.es/",
        "https://asesoriafiscaltenerife.es/",
    ]
    pages = []
    for url in urls:
        pages.append(fetch_static(url))

    ok_pages = [p for p in pages if p["status"] == 200]
    pages_with_email = [p for p in ok_pages if p["emails"]]

    status = "PASS_TECH" if len(pages_with_email) >= 2 else "WATCH"
    verdict = (
        "Fetcher carga varias webs propias y extrae emails visibles sin necesitar browser."
        if status == "PASS_TECH"
        else "La carga es parcial o el email visible no aparece de forma estable."
    )
    return {
        "source_id": "google_basic_webs_propias",
        "source_name": "Google Basic -> webs propias con email visible",
        "status": status,
        "recommended_fetcher": "Fetcher",
        "verdict": verdict,
        "pages_tested": pages,
    }


def find_first_link(page_result: dict[str, Any], contains: str) -> str | None:
    contains = contains.lower()
    for item in page_result["sample_links"]:
        href = (item.get("href") or "").strip()
        text = (item.get("text") or "").lower()
        if contains in href.lower() or contains in text:
            return href
    return None


def absolutize(base_url: str, maybe_relative: str | None) -> str | None:
    if not maybe_relative:
        return None
    return urljoin(base_url, maybe_relative)


def validate_aafc() -> dict[str, Any]:
    home_url = "https://asesoresfiscalesdecanarias.org/"
    home = fetch_static(home_url)

    candidate_urls = [home_url]
    guessed = "https://asesoresfiscalesdecanarias.org/despachos-profesionales/"
    if guessed not in candidate_urls:
        candidate_urls.append(guessed)

    discovered = find_first_link(home, "despach")
    if discovered:
        try:
            joined = absolutize(home_url, discovered)
            if joined and joined not in candidate_urls:
                candidate_urls.append(joined)
        except Exception:
            pass

    pages = [home]
    for url in candidate_urls[1:]:
        pages.append(fetch_static(url))

    ok_pages = [p for p in pages if p.get("status") == 200]
    directory_markers = [
        p
        for p in ok_pages
        if p["keywords"].get("despachos") or p["keywords"].get("buscador") or p["emails"] or p["phones"]
    ]
    if not directory_markers:
        dynamic = fetch_dynamic(guessed)
        pages.append(dynamic)
        if dynamic.get("status") == 200 and (
            dynamic["keywords"].get("despachos")
            or dynamic["keywords"].get("buscador")
            or dynamic["emails"]
            or dynamic["phones"]
        ):
            directory_markers.append(dynamic)

    status = "PASS_TECH" if directory_markers else "WATCH"
    verdict = (
        "Scrapling localiza el directorio o al menos un entrypoint usable del buscador/despachos."
        if status == "PASS_TECH"
        else "No queda demostrado todavia que el directorio sea extraible con estabilidad usando Scrapling."
    )
    return {
        "source_id": "aafc_despachos_profesionales",
        "source_name": "AAFC / Despachos Profesionales",
        "status": status,
        "recommended_fetcher": "Fetcher" if any(p.get("fetcher") == "Fetcher" and p.get("status") == 200 for p in pages) else "DynamicFetcher",
        "verdict": verdict,
        "pages_tested": pages,
    }


def validate_gestores_tenerife() -> dict[str, Any]:
    landing_url = "https://gestorestenerife.org/localiza-ga/"
    landing = fetch_static(landing_url)

    pdf_links = []
    for item in landing["sample_links"]:
        href = item.get("href", "")
        if href.lower().endswith(".pdf"):
            pdf_links.append(href)

    if not pdf_links:
        try:
            page = Fetcher.get(landing_url, timeout=30000)
            for link in page.css('a[href$=".pdf"]::attr(href)').getall() or []:
                if link not in pdf_links:
                    pdf_links.append(link)
        except Exception:
            pass

    pdf_pages = []
    for link in pdf_links[:2]:
        pdf_url = absolutize(landing_url, link)
        if not pdf_url:
            continue
        pdf_pages.append(fetch_static(pdf_url))

    pages = [landing, *pdf_pages]
    landing_ok = landing.get("status") == 200
    pdf_with_email = [
        p
        for p in pdf_pages
        if p.get("status") == 200 and ("pdf" in str(p.get("content_type", "")).lower()) and (p["emails"] or p["phones"])
    ]

    status = "PASS_TECH" if landing_ok and pdf_with_email else "WATCH"
    verdict = (
        "Scrapling carga el localizador y puede descargar/leer al menos un PDF con contacto reutilizable."
        if status == "PASS_TECH"
        else "El entrypoint carga, pero el listado reusable no queda suficientemente demostrado."
    )
    return {
        "source_id": "gestores_tenerife_localizador_pdf",
        "source_name": "Gestores Tenerife / Localiza tu GA + PDF",
        "status": status,
        "recommended_fetcher": "Fetcher",
        "verdict": verdict,
        "pages_tested": pages,
    }


def build_markdown(results: list[dict[str, Any]]) -> str:
    lines = [
        "# Scrapling Validation - Experimento 1",
        "",
        f"- Fecha: {time.strftime('%Y-%m-%d')}",
        "- Scope: microvalidacion tecnica con Scrapling API Python sobre las 3 fuentes `pass` de Fase 2",
        "",
        "## Veredicto",
        "",
    ]
    for result in results:
        lines.append(f"### {result['source_name']}")
        lines.append("")
        lines.append(f"- Status tecnico: `{result['status']}`")
        lines.append(f"- Fetcher recomendado: `{result['recommended_fetcher']}`")
        lines.append(f"- Veredicto: {result['verdict']}")
        lines.append("")
        for page in result["pages_tested"]:
            url = page.get("url", "Unknown")
            status = page.get("status", "Unknown")
            fetcher = page.get("fetcher", "Unknown")
            emails = ", ".join(page.get("emails", [])[:4]) or "none"
            phones = ", ".join(page.get("phones", [])[:3]) or "none"
            error = page.get("error")
            lines.append(f"- `{fetcher}` `{url}` -> status `{status}`, emails `{emails}`, phones `{phones}`")
            if error:
                lines.append(f"  error: `{error}`")
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)

    results = [
        validate_google_basic(),
        validate_aafc(),
        validate_gestores_tenerife(),
    ]

    JSON_OUT.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    MD_OUT.write_text(build_markdown(results), encoding="utf-8")

    print(f"Wrote {JSON_OUT}")
    print(f"Wrote {MD_OUT}")
    for result in results:
        print(f"{result['source_name']}: {result['status']} ({result['recommended_fetcher']})")


if __name__ == "__main__":
    main()
