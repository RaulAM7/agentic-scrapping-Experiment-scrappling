# Interreg Pause Handoff

Fecha: 2026-06-07
Estado: pausado
Motivo: el siguiente bloque de trabajo del repo se dedicara a scraping para otro proyecto

## Estado actual

- organizaciones canonizadas: `2415`
- `ready_for_outreach`: `1667`
- `not_ready`: `748`
- mejora acumulada vs baseline (`360 ready`): `+1307`
- mejora incremental de `wave 2`: `+161`

## Residual pendiente

- `588` `email_not_found_form_only`
- `68` `email_not_found_no_contact_channel`
- `40` `email_not_found_manual_review`
- `30` `email_not_found_no_website`
- `22` `email_not_found_scrape_blocked`

## Artefactos canonicos

- estado final y metricas: `04_outputs/skilland-knowledge-transfer-engine/interreg_mac/06_enriched_leads/README.md`
- tabla normalizada: `04_outputs/skilland-knowledge-transfer-engine/interreg_mac/06_enriched_leads/interreg_partner_leads_normalized.csv`
- log completo: `04_outputs/skilland-knowledge-transfer-engine/interreg_mac/06_enriched_leads/interreg_partner_leads_email_enrichment_log.csv`
- leads listos: `04_outputs/skilland-knowledge-transfer-engine/interreg_mac/06_enriched_leads/interreg_partner_leads_outreach_ready.csv`
- leads no listos: `04_outputs/skilland-knowledge-transfer-engine/interreg_mac/06_enriched_leads/interreg_partner_leads_not_ready.csv`

## Scripts usados

- hardening base: `05_scratch/interreg_enrichment_pipeline.py`
- max recovery wave 1: `05_scratch/interreg_recovery_wave_1.py`
- max recovery wave 2: `05_scratch/interreg_recovery_wave_2.py`

## Logs de trabajo

- `05_scratch/interreg_recovery_wave_1/interreg_partner_website_discovery_log.csv`
- `05_scratch/interreg_recovery_wave_1/interreg_partner_contact_recovery_log.csv`
- `05_scratch/interreg_recovery_wave_2/interreg_partner_website_discovery_log.csv`
- `05_scratch/interreg_recovery_wave_2/interreg_partner_contact_recovery_log.csv`

## Que hizo cada ola

- hardening:
  - convirtio el primer enrichment en una exportacion canonica conservadora
  - dejo `360` organizaciones en `ready_for_outreach`
- wave 1:
  - promociono evidencia ya publicada y trazable
  - subio de `360` a `1506`
- wave 2:
  - preservo los `1506` previos
  - recrawleo homepage y paginas internas claras en webs propias
  - subio de `1506` a `1667`

## Limitaciones conocidas

- el mayor bloque pendiente sigue siendo `form_only` en webs institucionales grandes
- parte del residual esta bloqueado por anti-bot o certificados rotos
- la discovery con Bing quedo minimizada porque el mejor ROI estuvo en recrawl de webs propias
- no se hizo inferencia de emails ni scraping de LinkedIn ni fuentes privadas

## Mejor punto de reentrada

Si se retoma Interreg, empezar por `wave 3` sobre el residual `748` con este orden:

1. `scrape_blocked` y `manual_review`
2. `no_website`
3. `form_only` institucional de alto valor

## Recomendacion tecnica para retomar

- no reejecutar `wave 1`
- usar `06_enriched_leads/` actual como baseline
- conservar el contrato actual de `contact_quality_tier` y `ready_reason`
- medir siempre delta contra `1667 ready / 748 not_ready`

## Criterio de exito para una futura wave 3

- mantener `ready + not_ready = 2415`
- no introducir falsos positivos tecnicos
- documentar delta incremental por carril y por tipo de contacto recuperado
