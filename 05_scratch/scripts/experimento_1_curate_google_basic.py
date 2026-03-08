"""
Curacion comercial del escalado google_basic.

Parte del dataset live ya extraido y elimina:
- instituciones publicas
- directorios/listados
- clasificados y contenido editorial
- proveedores no alineados con el ICP local
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from urllib.parse import unquote

import experimento_1_scale_google_basic as google_basic


SCRATCH_DIR = Path("05_scratch/experimento_1")
OUTPUT_DIR = Path("04_outputs/experimento_1")

RAW_DATA_JSON = SCRATCH_DIR / "2026-03-07_google-basic-scaled-dataset_experimento-1.json"
QUERY_RESULTS_JSON = SCRATCH_DIR / "2026-03-07_google-basic-live-serp-results.json"

CURATED_JSON = SCRATCH_DIR / "2026-03-07_google-basic-curated-dataset_experimento-1.json"
CURATED_CSV = SCRATCH_DIR / "2026-03-07_google-basic-curated-dataset_experimento-1.csv"
SUMMARY_MD = OUTPUT_DIR / "2026-03-07_escalado-google-basic-curated_experimento-1_v1.md"

BLOCKED_HINTS = {
    "agencia tributaria",
    "agenciatributaria",
    "allianz",
    "ayudatpymes",
    "ayuntamiento",
    "casasapo",
    "ciudadania",
    "contacto y ayuda",
    "cotime",
    "cylex",
    "deusto",
    "einforma",
    "fundae",
    "gobiernodecanarias",
    "glassdoor",
    "helvetia",
    "holded",
    "iberinform",
    "laspalmasgc",
    "milanuncios",
    "paginasamarillas",
    "qdq",
    "todosbiz",
    "tributaria",
    "webnode",
}

BLOCKED_URL_HINTS = {
    "/ayuntamiento/",
    "/cuanto-cuesta",
    "/empresa/",
    "/informes-empresas/",
    "/procedimientoini/",
    "/sueldo",
    "/tributos/",
}


def write_csv(records: list[dict]) -> None:
    with CURATED_CSV.open("w", newline="", encoding="utf-8") as fh:
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


def clean_record(record: dict) -> dict:
    cleaned = dict(record)
    if cleaned["contact_channel_type"] == "email":
        cleaned["email_or_channel"] = unquote(cleaned["email_or_channel"]).lower()
        cleaned["evidence_snippet"] = unquote(cleaned["evidence_snippet"])
    cleaned["notes"] = f"{cleaned['notes']}, curated_google_basic_v1"
    return cleaned


def drop_reason(record: dict) -> str | None:
    haystack = " ".join(
        [
            record["company_name"],
            record["source_url"],
            record["website_url"],
            record["notes"],
            record["evidence_snippet"],
        ]
    ).lower()
    if any(token in haystack for token in BLOCKED_HINTS):
        return "non_target_domain_or_entity"
    if any(token in record["source_url"].lower() for token in BLOCKED_URL_HINTS):
        return "non_target_url_pattern"
    return None


def main() -> None:
    SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw_records = json.loads(RAW_DATA_JSON.read_text(encoding="utf-8"))
    query_runs = json.loads(QUERY_RESULTS_JSON.read_text(encoding="utf-8"))

    kept: list[dict] = []
    dropped: dict[str, int] = {}
    for raw in raw_records:
        reason = drop_reason(raw)
        if reason:
            dropped[reason] = dropped.get(reason, 0) + 1
            continue
        kept.append(clean_record(raw))

    kept.sort(
        key=lambda row: (row["contactability_score"], row["icp_score"], row["company_name"].lower()),
        reverse=True,
    )

    metrics = google_basic.source_metrics(kept, query_runs)
    for record in kept:
        record["source_quality_score"] = metrics["source_quality_score"]

    CURATED_JSON.write_text(json.dumps(kept, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(kept)

    top_rows = [
        f"| {record['company_name']} | {record['geography']} | {record['email_or_channel']} | {record['source_rank']} | {record['contactability_score']} |"
        for record in kept[:15]
    ]

    summary = "\n".join(
        [
            "# Escalado Google Basic Curated - Experimento 1",
            "",
            "- Fecha: 2026-03-07",
            "- Fuente: `google_basic_live_serp` curada para emailing",
            f"- Registros raw: `{len(raw_records)}`",
            f"- Registros curados: `{len(kept)}`",
            f"- Registros descartados: `{len(raw_records) - len(kept)}`",
            f"- `source_quality_score`: `{metrics['source_quality_score']}`",
            f"- Gate de escalado: `{metrics['gate_pass']}`",
            "",
            "## Scorecard curado",
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
            "## Curacion aplicada",
            "",
            *[f"- `{reason}`: `{count}`" for reason, count in sorted(dropped.items())],
            "",
            "## Top ranking orientado a emailing",
            "",
            "| Company | Geography | Email/Canal | SERP rank | Contactability |",
            "|---|---|---|---:|---:|",
            *top_rows,
            "",
            "## Lectura operativa",
            "",
            "- `google_basic` queda validado tecnicamente con discovery live en Google usando Scrapling.",
            "- El dataset util para emailing exige una capa de curacion comercial explicita: Google por si solo mezcla webs propias, agregadores y ruido editorial.",
            "- El output que debe escalar es este dataset curado, no el raw completo.",
        ]
    ) + "\n"

    SUMMARY_MD.write_text(summary, encoding="utf-8")

    print(f"Wrote {CURATED_JSON}")
    print(f"Wrote {CURATED_CSV}")
    print(f"Wrote {SUMMARY_MD}")
    print(
        f"raw={len(raw_records)} curated={len(kept)} dropped={len(raw_records) - len(kept)} "
        f"source_quality_score={metrics['source_quality_score']} gate_pass={metrics['gate_pass']}"
    )


if __name__ == "__main__":
    main()
