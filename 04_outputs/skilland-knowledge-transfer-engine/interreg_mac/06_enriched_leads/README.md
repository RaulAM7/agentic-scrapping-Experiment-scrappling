# Interreg MAC - Enriched Leads

Generated: 2026-06-07T16:47:14Z
QA status: PASS

Pause handoff: `04_outputs/skilland-knowledge-transfer-engine/interreg_mac/2026-06-07_interreg-pause-handoff_v1.md`

## Files

| File | Rows | Description |
|------|------|-------------|
| interreg_partner_leads_normalized.csv | 2415 | Canonical org table (deduped) |
| interreg_partner_leads_email_enrichment_log.csv | 2415 | Full enrichment log |
| interreg_partner_leads_outreach_ready.csv | 1667 | Orgs with email found |
| interreg_partner_leads_not_ready.csv | 748 | Orgs without email, with reason |

## Coverage

- `baseline_ready`: 360
- `wave1_ready`: 1506
- `ready_for_outreach`: 1667
- `delta_ready_wave2`: 161
- `delta_ready_vs_baseline`: 1307
- `email_not_found_no_website`: 30
- `email_not_found_form_only`: 588
- `email_not_found_no_contact_channel`: 68
- `email_not_found_scrape_blocked`: 22
- `email_not_found_manual_review`: 40

## Contact Quality

- `official_programme_proxy_email`: 1092
- `direct_partner_email`: 308
- `official_generic_partner_email`: 191
- `official_external_published_email`: 64
- `official_gateway_email`: 12

## Email Status Breakdown

- **email_found**: 1667 (69.0%)
- **email_not_found_form_only**: 588 (24.3%)
- **email_not_found_manual_review**: 40 (1.7%)
- **email_not_found_no_contact_channel**: 68 (2.8%)
- **email_not_found_no_website**: 30 (1.2%)
- **email_not_found_scrape_blocked**: 22 (0.9%)

## Wave 2 Notes

- Esta ola preserva los `1506` ready previos y re-crawlea la cola residual con homepage y paginas internas de contacto/equipo/about del dominio oficial.
- La mejora incremental fue de `+161` (`117` desde `form_only`, `25` desde `no_contact_channel`, `19` desde `manual_review`).
- La discovery con Bing quedo limitada al bloque sin website o con website rota; no fue el motor principal de esta pasada.
