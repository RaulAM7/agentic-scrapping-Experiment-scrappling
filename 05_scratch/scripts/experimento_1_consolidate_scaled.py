"""
Consolida AAFC escalado + google_basic curado en un dataset unico.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import experimento_1_pilot_extract as pilot


SCRATCH_DIR = Path("05_scratch/experimento_1")
OUTPUT_DIR = Path("04_outputs/experimento_1")

AAFC_JSON = SCRATCH_DIR / "2026-03-07_aafc-scaled-dataset_experimento-1.json"
GOOGLE_JSON = SCRATCH_DIR / "2026-03-07_google-basic-curated-dataset_experimento-1.json"

OUT_JSON = SCRATCH_DIR / "2026-03-07_consolidated-scaled-dataset_experimento-1.json"
OUT_CSV = SCRATCH_DIR / "2026-03-07_consolidated-scaled-dataset_experimento-1.csv"
SUMMARY_MD = OUTPUT_DIR / "2026-03-07_dataset-consolidado-experimento-1_v1.md"


def write_csv(records: list[dict]) -> None:
    with OUT_CSV.open("w", newline="", encoding="utf-8") as fh:
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


def consolidation_key(record: dict) -> str:
    return pilot.build_dedupe_key(
        record["company_name"],
        record["geography"],
        record["contact_channel_type"],
        record["email_or_channel"],
        record["website_url"],
        "consolidated",
    )


def preferred_record(left: dict, right: dict) -> dict:
    left_score = (
        left["contactability_score"],
        left["source_quality_score"],
        left["icp_score"],
        int(left["website_url"] != "Unknown"),
    )
    right_score = (
        right["contactability_score"],
        right["source_quality_score"],
        right["icp_score"],
        int(right["website_url"] != "Unknown"),
    )
    return left if left_score >= right_score else right


def merge_records(left: dict, right: dict) -> dict:
    primary = preferred_record(left, right)
    secondary = right if primary is left else left
    merged = dict(primary)

    services = pilot.unique_keep_order(primary["services"] + secondary["services"])
    icp_signals = pilot.unique_keep_order(primary["icp_signals"] + secondary["icp_signals"])
    source_name = pilot.unique_keep_order([primary["source_name"], secondary["source_name"]])
    source_lane = pilot.unique_keep_order([primary["source_lane"], secondary["source_lane"]])
    source_query = pilot.unique_keep_order([primary["source_query"], secondary["source_query"]])

    merged["services"] = services
    merged["icp_signals"] = icp_signals
    merged["source_name"] = " + ".join(source_name)
    merged["source_lane"] = " + ".join(source_lane)
    merged["source_query"] = " || ".join(source_query)
    merged["notes"] = f"{primary['notes']}, merged_from={secondary['source_name']}"
    merged["source_quality_score"] = max(primary["source_quality_score"], secondary["source_quality_score"])
    merged["contactability_score"] = max(primary["contactability_score"], secondary["contactability_score"])
    merged["icp_score"] = max(primary["icp_score"], secondary["icp_score"])
    merged["dedupe_key"] = consolidation_key(merged)
    return merged


def main() -> None:
    SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    aafc_records = json.loads(AAFC_JSON.read_text(encoding="utf-8"))
    google_records = json.loads(GOOGLE_JSON.read_text(encoding="utf-8"))

    merged: dict[str, dict] = {}
    overlaps = 0
    for record in [*aafc_records, *google_records]:
        key = consolidation_key(record)
        if key in merged:
            overlaps += 1
            merged[key] = merge_records(merged[key], record)
        else:
            item = dict(record)
            item["dedupe_key"] = key
            merged[key] = item

    consolidated = sorted(
        merged.values(),
        key=lambda row: (row["contactability_score"], row["source_quality_score"], row["icp_score"], row["company_name"].lower()),
        reverse=True,
    )

    OUT_JSON.write_text(json.dumps(consolidated, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(consolidated)

    source_breakdown: dict[str, int] = {}
    for record in consolidated:
        for source in [item.strip() for item in record["source_name"].split("+")]:
            source_breakdown[source] = source_breakdown.get(source, 0) + 1

    top_rows = [
        f"| {record['company_name']} | {record['source_name']} | {record['geography']} | {record['email_or_channel']} | {record['contactability_score']} |"
        for record in consolidated[:20]
    ]

    summary = "\n".join(
        [
            "# Dataset Consolidado - Experimento 1",
            "",
            "- Fecha: 2026-03-07",
            f"- Registros `AAFC`: `{len(aafc_records)}`",
            f"- Registros `google_basic` curados: `{len(google_records)}`",
            f"- Overlaps deduplicados: `{overlaps}`",
            f"- Dataset consolidado final: `{len(consolidated)}`",
            "",
            "## Mix de fuentes",
            "",
            *[f"- `{source}`: `{count}`" for source, count in sorted(source_breakdown.items())],
            "",
            "## Top ranking orientado a emailing",
            "",
            "| Company | Source | Geography | Email/Canal | Contactability |",
            "|---|---|---|---|---:|",
            *top_rows,
            "",
            "## Lectura operativa",
            "",
            "- `AAFC` aporta volumen limpio y estructura colegial.",
            "- `google_basic` aporta webs propias y mejor enrichment comercial para emailing.",
            "- El dataset consolidado ya permite ordenar por `contactability_score` y `icp_score` con trazabilidad de origen.",
        ]
    ) + "\n"

    SUMMARY_MD.write_text(summary, encoding="utf-8")

    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {SUMMARY_MD}")
    print(f"aafc={len(aafc_records)} google_basic={len(google_records)} overlaps={overlaps} consolidated={len(consolidated)}")


if __name__ == "__main__":
    main()
