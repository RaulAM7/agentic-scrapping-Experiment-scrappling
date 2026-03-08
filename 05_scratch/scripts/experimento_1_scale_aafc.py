"""
Fase 4 - Escalado controlado de AAFC para Experimento 1.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import experimento_1_pilot_extract as pilot


SCRATCH_DIR = Path("05_scratch/experimento_1")
OUTPUT_DIR = Path("04_outputs/experimento_1")

DATA_JSON = SCRATCH_DIR / "2026-03-07_aafc-scaled-dataset_experimento-1.json"
DATA_CSV = SCRATCH_DIR / "2026-03-07_aafc-scaled-dataset_experimento-1.csv"
SUMMARY_MD = OUTPUT_DIR / "2026-03-07_escalado-aafc_experimento-1_v1.md"


def write_csv(records: list[dict]) -> None:
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

    records = pilot.extract_aafc_records(limit=None)
    metrics = pilot.source_metrics(records, "AAFC - Despachos Profesionales")
    pilot.apply_source_quality(records, metrics)
    records = sorted(
        records,
        key=lambda r: (r["contactability_score"], r["icp_score"], r["company_name"].lower()),
        reverse=True,
    )

    DATA_JSON.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(records)

    islands: dict[str, int] = {}
    for record in records:
        island = record["geography"].split("|", 1)[1] if "|" in record["geography"] else "unknown"
        islands[island] = islands.get(island, 0) + 1

    top_rows = []
    for record in records[:15]:
        top_rows.append(
            f"| {record['company_name']} | {record['geography']} | {record['email_or_channel']} | {record['icp_score']} | {record['contactability_score']} |"
        )

    summary = "\n".join(
        [
            "# Escalado AAFC - Experimento 1",
            "",
            "- Fecha: 2026-03-07",
            "- Fuente: `AAFC - Despachos Profesionales`",
            f"- Registros extraidos: `{len(records)}`",
            f"- `source_quality_score`: `{metrics['source_quality_score']}`",
            f"- Gate de escalado: `{metrics['gate_pass']}`",
            "",
            "## Scorecard",
            "",
            f"- `% P0 contactable`: `{metrics['p0_contactable_pct']}`",
            f"- `% email real`: `{metrics['email_real_pct']}`",
            f"- `% emails unicos`: `{metrics['unique_email_pct']}`",
            f"- `% ruido`: `{metrics['noise_pct']}`",
            f"- `% duplicados`: `{metrics['duplicate_pct']}`",
            f"- `% señales ICP útiles`: `{metrics['icp_signal_useful_pct']}`",
            "",
            "## Distribución por isla",
            "",
            *[f"- `{island}`: `{count}`" for island, count in sorted(islands.items())],
            "",
            "## Top ranking orientado a emailing",
            "",
            "| Company | Geography | Email | ICP | Contactability |",
            "|---|---|---|---:|---:|",
            *top_rows,
            "",
            "## Lectura operativa",
            "",
            "- `AAFC` queda aprobado para escalado controlado dentro del experimento.",
            "- El dataset es bueno para emailing, pero parte del valor futuro exigirá enriquecer `website_url`, porque hoy muchos registros salen sin web propia visible.",
            "- El siguiente paso razonable es consolidar este dataset como carril `specialized_directory` y compararlo contra cualquier rescate que logremos en `google_basic`.",
        ]
    ) + "\n"

    SUMMARY_MD.write_text(summary, encoding="utf-8")

    print(f"Wrote {DATA_JSON}")
    print(f"Wrote {DATA_CSV}")
    print(f"Wrote {SUMMARY_MD}")
    print(f"records={len(records)} source_quality_score={metrics['source_quality_score']} gate_pass={metrics['gate_pass']}")


if __name__ == "__main__":
    main()
