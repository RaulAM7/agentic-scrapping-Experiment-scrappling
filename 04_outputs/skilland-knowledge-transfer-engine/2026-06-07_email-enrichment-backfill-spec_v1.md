# Email Enrichment Backfill Spec

Fecha: 2026-06-07
Estado: execution-ready spec para la siguiente ola

## Summary

Objetivo: convertir las organizaciones ya extraidas en el carril `Knowledge Transfer / Interreg` en una capa canonica de leads con `email` o `email_status`, sin abrir nuevas fuentes aleatorias y sin repetir scraping discovery fuera de las entidades ya identificadas.

Resultado esperado:

- conservar la capa fuente scored de Interreg;
- construir una capa canonica de organizaciones;
- ejecutar enrichment de contacto sobre webs ya detectadas;
- exportar dos salidas finales: leads listos para outreach y leads no listos pero cerrados con motivo.

## Inputs y outputs

Input canonico obligatorio:

- `04_outputs/skilland-knowledge-transfer-engine/interreg_mac/04_processed_outputs/wave1_keep_eu_processed_scored.csv`
- `04_outputs/skilland-knowledge-transfer-engine/interreg_mac/04_processed_outputs/wave2_keep_eu_processed_scored.csv`
- `04_outputs/skilland-knowledge-transfer-engine/interreg_mac/04_processed_outputs/wave3_keep_eu_processed_scored.csv`

Inputs de apoyo permitidos:

- `01_data_sources/raw_html/projects/`
- `01_data_sources/raw_api/`
- `01_data_sources/raw_exports/`
- `05_reports/*`

No usar como input operativo independiente:

- `03_samples/*_sample_scored.csv` porque son duplicados exactos de `04_processed_outputs/*`
- cualquier fuente nueva no vinculada a las entidades ya extraidas

Carpeta de salida de la ola:

- `04_outputs/skilland-knowledge-transfer-engine/interreg_mac/06_enriched_leads/`

Archivos a generar:

- `interreg_partner_leads_normalized.csv`
- `interreg_partner_leads_email_enrichment_log.csv`
- `interreg_partner_leads_outreach_ready.csv`
- `interreg_partner_leads_not_ready.csv`
- `README.md`

## Data contract

`interreg_partner_leads_normalized.csv` debe contener, como minimo:

- `organization_id`
- `organization_name`
- `organization_type`
- `partner_country`
- `partner_region`
- `source_dataset`
- `source_wave`
- `source_project_ids`
- `source_project_names`
- `source_project_urls`
- `website_url`
- `contact_url`
- `documents_url`
- `score`
- `score_reason`
- `suggested_angle`
- `dedupe_key`
- `normalization_notes`

`interreg_partner_leads_email_enrichment_log.csv` debe contener:

- `organization_id`
- `organization_name`
- `website_url`
- `contact_url`
- `fetch_target_url`
- `fetch_status`
- `emails_found_raw`
- `selected_email`
- `email_status`
- `email_source_url`
- `email_source_type`
- `contact_name`
- `contact_role`
- `lead_readiness`
- `enriched_at_utc`
- `notes`

`interreg_partner_leads_outreach_ready.csv` debe contener solo filas con:

- `lead_readiness = ready_for_outreach`
- `selected_email` no vacio

Campos minimos:

- `organization_id`
- `organization_name`
- `organization_type`
- `partner_country`
- `website_url`
- `contact_url`
- `contact_name`
- `contact_role`
- `email`
- `email_source_url`
- `source_project_urls`
- `score`
- `suggested_angle`

`interreg_partner_leads_not_ready.csv` debe contener solo filas con:

- `lead_readiness != ready_for_outreach`
- `email_status` obligatorio

## Normalizacion obligatoria

Paso 1. Unificar las tres waves processed en una sola tabla de staging.

Paso 2. Canonizar por organizacion usando estas reglas:

- clave primaria provisional: `normalized_name + partner_country + normalized_contact_domain`
- si no existe dominio, usar `normalized_name + partner_country`
- `normalized_name` = lowercase, trim, espacios colapsados, sin puntuacion terminal obvia
- `normalized_contact_domain` se deriva de `contact_url` si apunta a website de partner; si `contact_url` solo apunta a keep.eu, dejarlo vacio

Paso 3. Consolidar duplicados:

- agrupar proyectos repetidos de la misma organizacion en arrays concatenados con separador ` | `
- conservar el `score` maximo observado
- conservar `suggested_angle` del registro con mayor `score`
- conservar `contact_url` no-keep.eu si existe; si no, usar `source_url` keep.eu como fallback trazable

Paso 4. Inferir `organization_type` desde estas fuentes por orden:

- `notes` (`partner_org_type=`)
- keywords en `partner_name`
- fallback `Unknown`

## Precedencia de enrichment

No abrir discovery general. Solo seguir este orden:

1. `contact_url` cuando no sea `keep.eu`
2. `website_url` derivada del dominio de `contact_url`
3. URLs publicadas en `documents_url` si ayudan a confirmar email o website
4. `source_project_urls` keep.eu solo para recuperar enlaces visibles en la ficha si faltara website

Si una organizacion solo conserva `keep.eu` y no se puede derivar web propia, cerrar con:

- `email_status = email_not_found_no_website`
- `lead_readiness = not_outreach_ready`

## Seleccion de email

Regla de prioridad para `selected_email`:

1. email nominal o funcional en dominio propio de la organizacion
2. email generico de departamento en dominio propio
3. email corporativo de holding o entidad matriz si la web lo presenta como contacto oficial
4. no usar emails de terceros, directorios, marketplaces o dominios no trazables

Si aparecen varios emails validos, conservar todos en `emails_found_raw` y elegir el mejor con esta prioridad:

- nominal no generico en dominio propio
- departamento / area relevante
- `info@` o `contact@` como ultimo recurso valido

## Enum obligatorio

`email_status` permitido:

- `email_found`
- `email_not_found_no_website`
- `email_not_found_no_contact_channel`
- `email_not_found_form_only`
- `email_not_found_scrape_blocked`
- `email_not_found_manual_review`

`email_source_type` permitido:

- `website_contact_page`
- `website_footer`
- `website_team_page`
- `website_about_page`
- `website_document`
- `keep_eu_project_page`
- `manual_review`

`lead_readiness` permitido:

- `ready_for_outreach`
- `not_outreach_ready`
- `manual_review_needed`

Reglas:

- si `email_status = email_found`, entonces `lead_readiness = ready_for_outreach`
- si solo hay formulario sin email visible, entonces `email_status = email_not_found_form_only` y `lead_readiness = not_outreach_ready`
- si el fetch falla o queda ambiguo, usar `manual_review_needed`

## QA y acceptance criteria

La ola se considera terminada solo si:

- existe una sola capa canonica deduped por organizacion
- `03_samples/*_sample_scored.csv` no se usa como segundo input operativo
- cada fila final tiene `email` o `email_status`
- cada email seleccionado tiene `email_source_url`
- `outreach_ready` y `not_ready` quedan separados en archivos distintos
- se documenta el coverage final de:
  - organizaciones con email
  - organizaciones sin website
  - organizaciones con formulario pero sin email
  - organizaciones en manual review

Tests minimos:

- validar que no haya duplicados por `organization_id` en la capa normalizada
- validar que `outreach_ready` no contenga emails vacios
- validar que `not_ready` no contenga `email_status` vacio
- validar que `email_source_url` exista cuando `email_status = email_found`
- validar que el total de `outreach_ready + not_ready` coincida con la capa normalizada

## Assumptions

- No se usaran fuentes privadas, LinkedIn scraping ni deduccion de emails no publicados.
- `04_processed_outputs/` es la base canonica de entrada para Interreg, aunque hoy siga siendo una capa intermedia.
- La capa `skilland_ia_mujeres/data_prep` se toma como referencia interna para flags, trazabilidad y shape canonico.
