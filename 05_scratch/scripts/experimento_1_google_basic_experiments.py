"""
Bateria tecnica para rescatar `google_basic` con Scrapling.

Prueba multiples estrategias:
- fetch directo
- browser fetch directo
- sesiones persistentes con home -> query
- cookies/consentimiento
- CDP opcional contra Chromium local
"""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Callable

from scrapling.fetchers import DynamicFetcher, DynamicSession, StealthyFetcher, StealthySession


OUT_DIR = Path("05_scratch/experimento_1")
JSON_OUT = OUT_DIR / "2026-03-07_google-basic-rescue-attempts.json"
MD_OUT = OUT_DIR / "2026-03-07_google-basic-rescue-attempts.md"

QUERY = '"asesoria fiscal" "Las Palmas de Gran Canaria" "contacto"'
SEARCH_URL = "https://www.google.com/search?q=%22asesoria+fiscal%22+%22Las+Palmas+de+Gran+Canaria%22+%22contacto%22&hl=es&gl=ES&num=10&pws=0"
HOME_URL = "https://www.google.com/?hl=es&gl=ES"
HOME_URL_ES = "https://www.google.es/?hl=es"
CONSENT_COOKIE = {
    "name": "CONSENT",
    "value": "YES+cb.20210328-17-p0.es+FX+917",
    "domain": ".google.com",
    "path": "/",
}


def classify_page(page: Any) -> str:
    status = getattr(page, "status", None)
    title = page.css("title::text").get("").strip().lower()
    text = str(getattr(page, "text", "") or "").lower()
    links = page.css("a")
    external_links = [
        a.attrib.get("href", "")
        for a in links
        if a.attrib.get("href", "").startswith("http") and "google." not in a.attrib.get("href", "")
    ]
    if status == 429 or "sorry" in getattr(page, "url", "").lower():
        return "google_sorry_429"
    if "antes de ir a la búsqueda de google" in title or "before you continue" in title:
        return "google_consent"
    if len(page.css("h3")) >= 3 and len(external_links) >= 3:
        return "results_like"
    if "google search" in title and len(links) <= 3:
        return "google_enablejs_shell"
    if any("/url?" in (a.attrib.get("href", "")) for a in links):
        return "results_like"
    if "why did this happen" in text:
        return "google_blocked"
    return "unknown"


def summarize(label: str, page: Any | None = None, error: Exception | None = None, extra: dict[str, Any] | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {
        "label": label,
        "status": None,
        "final_url": None,
        "title": None,
        "link_count": 0,
        "classification": "error" if error else "unknown",
        "sample_links": [],
    }
    if page is not None:
        result.update(
            {
                "status": getattr(page, "status", None),
                "final_url": getattr(page, "url", None),
                "title": page.css("title::text").get("").strip(),
                "link_count": len(page.css("a")),
                "classification": classify_page(page),
                "sample_links": [
                    {
                        "text": a.css("::text").get("").strip(),
                        "href": a.attrib.get("href", ""),
                    }
                    for a in page.css("a")[:8]
                ],
            }
        )
    if error is not None:
        result["error"] = repr(error)
    if extra:
        result.update(extra)
    return result


def accept_consent_and_search(page: Any, query: str) -> None:
    for selector in [
        'button:has-text("Aceptar todo")',
        'button:has-text("Aceptar")',
        'button:has-text("Accept all")',
        'button:has-text("I agree")',
        'form button',
    ]:
        try:
            locator = page.locator(selector)
            if locator.count():
                locator.first.click(timeout=2500)
                page.wait_for_timeout(1500)
                break
        except Exception:
            continue

    for selector in ["textarea[name='q']", "input[name='q']"]:
        try:
            locator = page.locator(selector)
            if locator.count():
                locator.first.click(timeout=3000)
                locator.first.fill("")
                locator.first.type(query, delay=70)
                page.keyboard.press("Enter")
                page.wait_for_timeout(4000)
                try:
                    page.wait_for_load_state("networkidle", timeout=8000)
                except Exception:
                    pass
                return
        except Exception:
            continue


def run_with_session(session_factory: Callable[..., Any], home_url: str, label: str, **session_kwargs: Any) -> dict[str, Any]:
    with TemporaryDirectory(prefix="google-basic-") as tmpdir:
        try:
            with session_factory(user_data_dir=tmpdir, **session_kwargs) as session:
                page = session.fetch(
                    home_url,
                    google_search=False,
                    network_idle=True,
                    wait=2500,
                    page_action=lambda page: accept_consent_and_search(page, QUERY),
                )
                return summarize(label, page, extra={"strategy": "home_then_search", "home_url": home_url})
        except Exception as exc:
            return summarize(label, error=exc, extra={"strategy": "home_then_search", "home_url": home_url})


def run_cdp_attempt(cdp_url: str) -> dict[str, Any]:
    try:
        page = StealthyFetcher.fetch(
            SEARCH_URL,
            cdp_url=cdp_url,
            google_search=False,
            network_idle=True,
            wait=2500,
            locale="es-ES",
            disable_resources=False,
        )
        return summarize("stealth_cdp_direct", page, extra={"strategy": "cdp_direct", "cdp_url": cdp_url})
    except Exception as exc:
        return summarize("stealth_cdp_direct", error=exc, extra={"strategy": "cdp_direct", "cdp_url": cdp_url})


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, Any]] = []

    attempts: list[tuple[str, Callable[[], Any]]] = [
        (
            "dynamic_direct",
            lambda: DynamicFetcher.fetch(
                SEARCH_URL,
                google_search=False,
                network_idle=True,
                wait=1500,
                locale="es-ES",
            ),
        ),
        (
            "stealth_direct",
            lambda: StealthyFetcher.fetch(
                SEARCH_URL,
                google_search=False,
                network_idle=True,
                wait=1500,
                locale="es-ES",
                disable_resources=False,
            ),
        ),
        (
            "dynamic_direct_with_cookie",
            lambda: DynamicFetcher.fetch(
                SEARCH_URL,
                google_search=False,
                network_idle=True,
                wait=1500,
                locale="es-ES",
                cookies=[CONSENT_COOKIE],
            ),
        ),
        (
            "stealth_direct_with_cookie",
            lambda: StealthyFetcher.fetch(
                SEARCH_URL,
                google_search=False,
                network_idle=True,
                wait=1500,
                locale="es-ES",
                cookies=[CONSENT_COOKIE],
                disable_resources=False,
            ),
        ),
    ]

    for label, fn in attempts:
        try:
            results.append(summarize(label, page=fn(), extra={"strategy": "direct"}))
        except Exception as exc:
            results.append(summarize(label, error=exc, extra={"strategy": "direct"}))

    results.append(
        run_with_session(
            DynamicSession,
            HOME_URL,
            "dynamic_session_home_search",
            headless=True,
            locale="es-ES",
            disable_resources=False,
            retries=1,
        )
    )
    results.append(
        run_with_session(
            StealthySession,
            HOME_URL,
            "stealth_session_home_search",
            headless=True,
            locale="es-ES",
            disable_resources=False,
            retries=1,
            hide_canvas=True,
            block_webrtc=True,
        )
    )
    results.append(
        run_with_session(
            StealthySession,
            HOME_URL_ES,
            "stealth_session_home_search_google_es",
            headless=True,
            locale="es-ES",
            disable_resources=False,
            retries=1,
            hide_canvas=True,
            block_webrtc=True,
        )
    )

    cdp_hint = Path("/tmp/chromium-google-basic.ws")
    if cdp_hint.exists():
        cdp_url = cdp_hint.read_text(encoding="utf-8").strip()
        if cdp_url:
            results.append(run_cdp_attempt(cdp_url))

    JSON_OUT.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    md_lines = [
        "# Google Basic Rescue Attempts",
        "",
        "- Fecha: 2026-03-07",
        "- Scope: bateria tecnica para desbloquear `google_basic` con Scrapling",
        f"- Query objetivo: `{QUERY}`",
        "",
    ]
    for result in results:
        md_lines.append(f"## {result['label']}")
        md_lines.append("")
        md_lines.append(f"- Classification: `{result['classification']}`")
        md_lines.append(f"- Status: `{result['status']}`")
        md_lines.append(f"- Final URL: `{result['final_url']}`")
        md_lines.append(f"- Title: `{result['title']}`")
        if result.get("error"):
            md_lines.append(f"- Error: `{result['error']}`")
        md_lines.append(f"- Link count: `{result['link_count']}`")
        if result.get("sample_links"):
            md_lines.append("- Sample links:")
            for item in result["sample_links"]:
                md_lines.append(f"  - `{item['text']}` -> `{item['href']}`")
        md_lines.append("")

    success = [r for r in results if r["classification"] == "results_like"]
    md_lines.extend(
        [
            "## Verdict",
            "",
            f"- Results-like attempts: `{len(success)}`",
            "- Si este valor sigue en `0`, Google continua bloqueado en discovery live dentro del stack actual y sin proxy externo.",
            "",
        ]
    )
    MD_OUT.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"Wrote {JSON_OUT}")
    print(f"Wrote {MD_OUT}")
    for result in results:
        print(
            f"{result['label']}: classification={result['classification']} "
            f"status={result['status']} title={result['title']}"
        )


if __name__ == "__main__":
    main()
