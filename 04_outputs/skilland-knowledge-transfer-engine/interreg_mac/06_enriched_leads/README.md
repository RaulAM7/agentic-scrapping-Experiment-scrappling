# Interreg MAC - Enriched Leads

Generated: 2026-06-07T16:20:17Z
QA status: PASS

## Files

| File | Rows | Description |
|------|------|-------------|
| interreg_partner_leads_normalized.csv | 2415 | Canonical org table (deduped) |
| interreg_partner_leads_email_enrichment_log.csv | 2415 | Full enrichment log |
| interreg_partner_leads_outreach_ready.csv | 1506 | Orgs with email found |
| interreg_partner_leads_not_ready.csv | 909 | Orgs without email, with reason |

## Coverage

- `baseline_ready`: 360
- `ready_for_outreach`: 1506
- `delta_ready_wave1`: 1146
- `promoted_from_existing_evidence`: 1146
- `email_not_found_no_website`: 30
- `email_not_found_form_only`: 705
- `email_not_found_no_contact_channel`: 93
- `email_not_found_scrape_blocked`: 22
- `email_not_found_manual_review`: 59

## Contact Quality

- `official_programme_proxy_email`: 1092
- `direct_partner_email`: 199
- `official_generic_partner_email`: 161
- `official_external_published_email`: 43
- `official_gateway_email`: 11

## Email Status Breakdown

- **email_found**: 1506 (62.4%)
- **email_not_found_form_only**: 705 (29.2%)
- **email_not_found_manual_review**: 59 (2.4%)
- **email_not_found_no_contact_channel**: 93 (3.9%)
- **email_not_found_no_website**: 30 (1.2%)
- **email_not_found_scrape_blocked**: 22 (0.9%)

## Wave 1 Notes

- Esta ola promociona contactos ya publicados y trazables en la evidencia actual.
- La discovery oficial de website y el crawl profundo quedan pendientes para `wave 2` sobre la cola residual.
