#!/usr/bin/env python3
"""
Interreg max-recovery wave 1.

Wave 1 prioriza lo mas rentable y trazable:
- preservar el baseline ready
- promocionar emails ya publicados en la evidencia actual
- etiquetar la calidad del contacto
- dejar logs claros de que se hizo y que quedo pendiente
"""

from __future__ import annotations

import csv
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

BASE = Path("/home/reboot/Escritorio/agentic-scrapping-Experiment-scrappling")
CURRENT = BASE / "04_outputs/skilland-knowledge-transfer-engine/interreg_mac/06_enriched_leads"
STAGING = BASE / "05_scratch/interreg_recovery_wave_1"
STAGING.mkdir(parents=True, exist_ok=True)

NORMALIZED_CSV = CURRENT / "interreg_partner_leads_normalized.csv"
ENRICHMENT_LOG_CSV = CURRENT / "interreg_partner_leads_email_enrichment_log.csv"
READY_CSV = CURRENT / "interreg_partner_leads_outreach_ready.csv"
NOT_READY_CSV = CURRENT / "interreg_partner_leads_not_ready.csv"
WEBSITE_DISCOVERY_LOG = STAGING / "interreg_partner_website_discovery_log.csv"
CONTACT_RECOVERY_LOG = STAGING / "interreg_partner_contact_recovery_log.csv"
README = CURRENT / "README.md"

ENRICHED_AT = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
PROJECT_DOMAINS = {
    "atlanticarea.eu",
    "interreg-med.eu",
    "interregnextmed.eu",
    "mac-interreg.org",
    "interreg-euro-med.eu",
}
EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b")
BAD_MARKERS = ("sentry.wixpress.com", "wixpress.com", "osm.org", "example.com", "example.org")
GATEWAY_MARKERS = ("legalmail.it", ".legalmail.it", "pec.it", ".pec.", ".pec", "hs01.kep.tr", ".kep.tr", "cert.")
GENERIC_LOCALS = {
    "info", "contact", "contacto", "office", "hello", "hola", "mail", "email", "admin",
    "support", "enquiries", "enquiry", "general", "communication", "secretariat",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict], fields: list[str]):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def split_pipe(value: str) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.split("|") if part.strip()]


def extract_domain(url: str) -> str:
    if not url:
        return ""
    host = urlparse(url).netloc.lower().strip()
    if host.startswith("www."):
        host = host[4:]
    return host


def root_domain(domain: str) -> str:
    if not domain:
        return ""
    parts = domain.split(".")
    if len(parts) <= 2:
        return domain
    return ".".join(parts[-2:])


def is_project_domain(url_or_domain: str) -> bool:
    domain = extract_domain(url_or_domain) if "://" in url_or_domain else url_or_domain.lower().strip()
    return domain in PROJECT_DOMAINS or root_domain(domain) in PROJECT_DOMAINS


def domain_matches(org_domain: str, email_domain: str) -> bool:
    if not org_domain or not email_domain:
        return False
    return (
        email_domain == org_domain
        or email_domain.endswith("." + org_domain)
        or org_domain.endswith("." + email_domain)
    )


def gateway_email(email_domain: str) -> bool:
    return any(marker in email_domain for marker in GATEWAY_MARKERS)


def clean_emails(raw_value: str) -> list[str]:
    seen = set()
    cleaned = []
    for email in split_pipe(raw_value):
        email = email.lower().strip().removeprefix("mailto:")
        email = email.split("?", 1)[0].strip()
        if email in seen or not EMAIL_RE.fullmatch(email):
            continue
        if any(marker in email for marker in BAD_MARKERS):
            continue
        seen.add(email)
        cleaned.append(email)
    return cleaned


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
    if source_domain and domain_matches(source_domain, email_domain):
        return "direct_partner_email", "email_on_source_domain"
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


def best_candidate(emails: list[str], source_url: str, website_url: str) -> tuple[str, str, str]:
    ranked = []
    for email in emails:
        quality, reason = classify_quality(email, source_url, website_url)
        ranked.append((quality_rank(quality), email, quality, reason))
    ranked.sort()
    _, email, quality, reason = ranked[0]
    return email, quality, reason


def lane_for(log_row: dict[str, str], normalized_row: dict[str, str]) -> str:
    if log_row.get("email_status") == "email_not_found_no_website":
        return "no_website"
    fetch_target = log_row.get("fetch_target_url", "")
    if is_project_domain(fetch_target) or (not normalized_row.get("website_url", "").strip() and is_project_domain(normalized_row.get("contact_url", ""))):
        return "programme_or_project_site"
    return "own_site_not_ready"


def main():
    normalized_rows = read_csv(NORMALIZED_CSV)
    ready_rows = read_csv(READY_CSV)
    baseline_log_rows = read_csv(ENRICHMENT_LOG_CSV)
    normalized_by_id = {row["organization_id"]: row for row in normalized_rows}
    baseline_log_by_id = {row["organization_id"]: row for row in baseline_log_rows}

    final_log_rows = []
    final_ready_rows = []
    final_not_ready_rows = []
    website_discovery_rows = []
    contact_recovery_rows = []

    baseline_ready_count = 0
    promoted_count = 0

    ready_fields = [
        "organization_id", "organization_name", "organization_type", "partner_country",
        "website_url", "contact_url", "validated_website_url", "contact_name", "contact_role",
        "email", "email_source_url", "source_project_urls", "score", "suggested_angle",
        "contact_quality_tier", "ready_reason",
    ]
    not_ready_fields = [
        "organization_id", "organization_name", "organization_type", "partner_country",
        "website_url", "contact_url", "email_status", "lead_readiness",
        "fetch_status", "notes", "source_project_urls", "score",
    ]
    enrichment_fields = [
        "organization_id", "organization_name", "website_url", "contact_url",
        "fetch_target_url", "fetch_status", "emails_found_raw", "selected_email",
        "email_status", "email_source_url", "email_source_type", "contact_name",
        "contact_role", "lead_readiness", "enriched_at_utc", "notes",
        "website_discovery_status", "website_discovery_source", "validated_website_url",
        "contact_quality_tier", "ready_reason", "recovery_lane",
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

    for row in normalized_rows:
        org_id = row["organization_id"]
        baseline = baseline_log_by_id[org_id]
        lane = lane_for(baseline, row)
        website_url = row.get("website_url", "")
        validated_website_url = website_url
        source_url = baseline.get("email_source_url") or baseline.get("fetch_target_url") or website_url

        if baseline.get("lead_readiness") == "ready_for_outreach" and baseline.get("selected_email"):
            baseline_ready_count += 1
            email = baseline["selected_email"]
            quality, reason = classify_quality(email, source_url, website_url or source_url)
            log_row = {
                **baseline,
                "enriched_at_utc": ENRICHED_AT,
                "website_discovery_status": "baseline_existing",
                "website_discovery_source": "baseline_existing",
                "validated_website_url": validated_website_url,
                "contact_quality_tier": quality,
                "ready_reason": reason,
                "recovery_lane": "baseline_ready",
            }
            final_log_rows.append(log_row)
            final_ready_rows.append({
                "organization_id": org_id,
                "organization_name": row["organization_name"],
                "organization_type": row["organization_type"],
                "partner_country": row["partner_country"],
                "website_url": row.get("website_url", ""),
                "contact_url": row.get("contact_url", ""),
                "validated_website_url": validated_website_url,
                "contact_name": baseline.get("contact_name", ""),
                "contact_role": baseline.get("contact_role", ""),
                "email": email,
                "email_source_url": baseline.get("email_source_url", ""),
                "source_project_urls": row.get("source_project_urls", ""),
                "score": row.get("score", ""),
                "suggested_angle": row.get("suggested_angle", ""),
                "contact_quality_tier": quality,
                "ready_reason": reason,
            })
            continue

        emails = clean_emails(baseline.get("emails_found_raw", ""))
        if emails:
            selected_email, quality, reason = best_candidate(emails, source_url, website_url or source_url)
            promoted_count += 1
            final_log_rows.append({
                "organization_id": org_id,
                "organization_name": row["organization_name"],
                "website_url": row.get("website_url", ""),
                "contact_url": row.get("contact_url", ""),
                "fetch_target_url": baseline.get("fetch_target_url", ""),
                "fetch_status": "promoted_from_existing_evidence",
                "emails_found_raw": baseline.get("emails_found_raw", ""),
                "selected_email": selected_email,
                "email_status": "email_found",
                "email_source_url": source_url,
                "email_source_type": "existing_evidence_promotion",
                "contact_name": baseline.get("contact_name", ""),
                "contact_role": baseline.get("contact_role", ""),
                "lead_readiness": "ready_for_outreach",
                "enriched_at_utc": ENRICHED_AT,
                "notes": f"promoted_from_existing_evidence | prior_status={baseline.get('email_status','')}",
                "website_discovery_status": "not_attempted_wave1",
                "website_discovery_source": "existing_evidence_only",
                "validated_website_url": validated_website_url,
                "contact_quality_tier": quality,
                "ready_reason": reason,
                "recovery_lane": lane,
            })
            final_ready_rows.append({
                "organization_id": org_id,
                "organization_name": row["organization_name"],
                "organization_type": row["organization_type"],
                "partner_country": row["partner_country"],
                "website_url": row.get("website_url", ""),
                "contact_url": row.get("contact_url", ""),
                "validated_website_url": validated_website_url,
                "contact_name": baseline.get("contact_name", ""),
                "contact_role": baseline.get("contact_role", ""),
                "email": selected_email,
                "email_source_url": source_url,
                "source_project_urls": row.get("source_project_urls", ""),
                "score": row.get("score", ""),
                "suggested_angle": row.get("suggested_angle", ""),
                "contact_quality_tier": quality,
                "ready_reason": reason,
            })
            website_discovery_rows.append({
                "organization_id": org_id,
                "organization_name": row["organization_name"],
                "recovery_lane": lane,
                "query_pack": "",
                "candidate_url": "",
                "candidate_domain": "",
                "discovery_status": "skipped_existing_evidence_sufficient",
                "validation_reason": "wave1_promoted_from_published_contact",
                "validated_website_url": validated_website_url,
            })
            contact_recovery_rows.append({
                "organization_id": org_id,
                "organization_name": row["organization_name"],
                "recovery_lane": lane,
                "recovery_stage": "existing_evidence_promotion",
                "target_url": source_url,
                "target_status": "promoted",
                "emails_found_raw": baseline.get("emails_found_raw", ""),
                "selected_email": selected_email,
                "contact_quality_tier": quality,
                "ready_reason": reason,
                "notes": "",
            })
            continue

        final_log_rows.append({
            **baseline,
            "enriched_at_utc": ENRICHED_AT,
            "website_discovery_status": "pending_wave2",
            "website_discovery_source": "wave1_existing_evidence_only",
            "validated_website_url": validated_website_url,
            "contact_quality_tier": "",
            "ready_reason": "",
            "recovery_lane": lane,
        })
        final_not_ready_rows.append({
            "organization_id": org_id,
            "organization_name": row["organization_name"],
            "organization_type": row["organization_type"],
            "partner_country": row["partner_country"],
            "website_url": row.get("website_url", ""),
            "contact_url": row.get("contact_url", ""),
            "email_status": baseline.get("email_status", ""),
            "lead_readiness": baseline.get("lead_readiness", ""),
            "fetch_status": baseline.get("fetch_status", ""),
            "notes": baseline.get("notes", ""),
            "source_project_urls": row.get("source_project_urls", ""),
            "score": row.get("score", ""),
        })
        website_discovery_rows.append({
            "organization_id": org_id,
            "organization_name": row["organization_name"],
            "recovery_lane": lane,
            "query_pack": "",
            "candidate_url": "",
            "candidate_domain": "",
            "discovery_status": "pending_wave2",
            "validation_reason": "no_published_email_in_current_evidence",
            "validated_website_url": validated_website_url,
        })
        contact_recovery_rows.append({
            "organization_id": org_id,
            "organization_name": row["organization_name"],
            "recovery_lane": lane,
            "recovery_stage": "existing_evidence_review",
            "target_url": source_url,
            "target_status": "not_promoted",
            "emails_found_raw": baseline.get("emails_found_raw", ""),
            "selected_email": "",
            "contact_quality_tier": "",
            "ready_reason": "",
            "notes": baseline.get("email_status", ""),
        })

    write_csv(WEBSITE_DISCOVERY_LOG, website_discovery_rows, discovery_fields)
    write_csv(CONTACT_RECOVERY_LOG, contact_recovery_rows, recovery_fields)
    write_csv(ENRICHMENT_LOG_CSV, final_log_rows, enrichment_fields)
    write_csv(READY_CSV, final_ready_rows, ready_fields)
    write_csv(NOT_READY_CSV, final_not_ready_rows, not_ready_fields)

    status_counts = Counter(row["email_status"] for row in final_log_rows)
    quality_counts = Counter(row["contact_quality_tier"] for row in final_ready_rows)
    delta_ready = len(final_ready_rows) - baseline_ready_count

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
        f"- `baseline_ready`: {baseline_ready_count}",
        f"- `ready_for_outreach`: {len(final_ready_rows)}",
        f"- `delta_ready_wave1`: {delta_ready}",
        f"- `promoted_from_existing_evidence`: {promoted_count}",
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
        "## Wave 1 Notes",
        "",
        "- Esta ola promociona contactos ya publicados y trazables en la evidencia actual.",
        "- La discovery oficial de website y el crawl profundo quedan pendientes para `wave 2` sobre la cola residual.",
    ]
    README.write_text("\n".join(readme_lines) + "\n", encoding="utf-8")

    print(f"Baseline ready: {baseline_ready_count}")
    print(f"Promoted from existing evidence: {promoted_count}")
    print(f"Final ready: {len(final_ready_rows)}")
    print(f"Final not ready: {len(final_not_ready_rows)}")


if __name__ == "__main__":
    main()
