# Email Enrichment Audit

Fecha: 2026-06-07
Alcance: auditoria de datasets, outputs, scripts y reportes del repo que contienen organizaciones o contactos utiles para prospeccion B2B, con foco prioritario en `04_outputs/skilland-knowledge-transfer-engine` y el caladero `Interreg / keep.eu`.

## Resumen ejecutivo

- El repo ya tiene dos precedentes validos de trabajo `email-first`: `Experimento 1` y `skilland_ia_mujeres/data_prep`. Ambos separan discovery de contactabilidad y ya llegan a emails utilizables.
- El principal gap estructural esta en `skilland-knowledge-transfer-engine/interreg_mac`: existen `368` proyectos raw y `3,192` filas `partner_in_project` scored, pero `0` emails reales poblados en `contact_email`.
- En Interreg hay duplicacion de payload a nivel de archivo: `03_samples/wave*_keep_eu_sample_scored.csv` y `04_processed_outputs/wave*_keep_eu_processed_scored.csv` son binariamente identicos en las tres waves.
- Los datasets historicos de `experimento_0` sirven como discovery y research de mercado, pero no conservan email y en general tampoco una web oficial lista para enrichment.
- A partir de ahora, una exportacion final de prospeccion debe incluir `email` o `email_status`. Todo lo demas es capa intermedia.

## Inventario por familia

### 1. Knowledge Transfer / Interreg MAC / keep.eu

| Artefacto | Ruta principal | Grano | Volumen real | URLs web / fuente | Emails | Estado |
|---|---|---|---:|---|---|---|
| Raw API provenance | `interreg_mac/01_data_sources/raw_api/` | payload / pagina | `121` JSON | si, trazabilidad por payload y respuesta | no | `supporting_only` |
| Raw exports | `interreg_mac/01_data_sources/raw_exports/` | export oficial | `18` XLSX | si, origen keep.eu | no | `supporting_only` |
| Raw HTML fichas | `interreg_mac/01_data_sources/raw_html/projects/` | proyecto | `368` HTML | si, fichas keep.eu cacheadas | no | `supporting_only` |
| Sample raw wave1 | `03_samples/wave1_keep_eu_sample_raw.csv` | proyecto | `18` | `source_url` | no | `normalization_first` |
| Sample raw wave2 | `03_samples/wave2_keep_eu_sample_raw.csv` | proyecto | `150` | `source_url` | no | `normalization_first` |
| Sample raw wave3 | `03_samples/wave3_keep_eu_sample_raw.csv` | proyecto | `200` | `source_url` | no | `normalization_first` |
| Sample scored wave1 | `03_samples/wave1_keep_eu_sample_scored.csv` | `partner_in_project` | `136` | `source_url`, `contact_url` | `0/136` | `duplicate_mirror` |
| Sample scored wave2 | `03_samples/wave2_keep_eu_sample_scored.csv` | `partner_in_project` | `1,380` | `source_url`, `contact_url`, `documents_url` en `122` filas | `0/1,380` | `duplicate_mirror` |
| Sample scored wave3 | `03_samples/wave3_keep_eu_sample_scored.csv` | `partner_in_project` | `1,676` | `source_url`, `contact_url`, `documents_url` en `486` filas | `0/1,676` | `duplicate_mirror` |
| Processed scored wave1 | `04_processed_outputs/wave1_keep_eu_processed_scored.csv` | `partner_in_project` | `136` | `source_url`, `contact_url` | `0/136` | `enrichment_ready_after_canonicalization` |
| Processed scored wave2 | `04_processed_outputs/wave2_keep_eu_processed_scored.csv` | `partner_in_project` | `1,380` | `source_url`, `contact_url`, `documents_url` parcial | `0/1,380` | `enrichment_ready_after_canonicalization` |
| Processed scored wave3 | `04_processed_outputs/wave3_keep_eu_processed_scored.csv` | `partner_in_project` | `1,676` | `source_url`, `contact_url`, `documents_url` parcial | `0/1,676` | `enrichment_ready_after_canonicalization` |

Campos relevantes observados en la capa scored / processed:

- proyecto: `project_id`, `project_name`, `project_acronym`, `programme`, `status`, `start_date`, `end_date`
- entidad: `partner_name`, `partner_role`, `lead_partner`, `partner_country`, `partner_region`
- trazabilidad: `source_url`, `documents_url`, `contact_url`
- scoring: `recency_score`, `geo_score`, `topic_score`, `training_transfer_score`, `beneficiary_score`, `entity_type_score`, `commercial_relevance_score`, `score`
- contacto actual: `contact_name`, `contact_role`, `contact_email` (presente en esquema, vacio en todas las filas)

Observaciones criticas:

- `03_samples/*_sample_scored.csv` y `04_processed_outputs/*_processed_scored.csv` son duplicados exactos por wave. Para enrichment solo debe sobrevivir una copia canonica.
- La granularidad actual es `partner_in_project`, no `organization`. Esto multiplica duplicados de entidad cuando el mismo partner aparece en varios proyectos o waves.
- Duplicados internos visibles por `(partner_name + partner_country)` en la capa processed: wave1=`5`, wave2=`194`, wave3=`353`.
- `contact_url` existe en el `100%` de las filas scored porque hoy cae en `partner_website` o, en su defecto, en la ficha de proyecto keep.eu. Eso permite enrichment posterior, pero no es equivalente a tener email.

### 2. Experimento 0 - discovery y scoring pre-email-first

| Dataset | Ruta | Grano | Volumen | URLs web | Emails | Estado |
|---|---|---|---:|---|---|---|
| `paginas_amarillas_canarias.json` | `04_outputs/experimento_0/datos/` | ficha de directorio | `137` | `url_ficha` si | no | `normalization_first` |
| `colegio_economistas_lp.json` | `04_outputs/experimento_0/datos/` | colegiado | `49` | no | no | `normalization_first` |
| `despachos_enriquecidos.json` | `04_outputs/experimento_0/datos/` | despacho | `30` | `url_ficha` si, `web_propia` vacia | no | `normalization_first` |
| `icp_scored_prospects.json` | `04_outputs/experimento_0/datos/` | prospecto scored | `77` | no | no | `supporting_only` |

Campos y diagnostico:

- `paginas_amarillas_canarias.json` guarda `nombre`, `actividad`, `direccion`, `telefono`, `url_ficha`; sirve como discovery base, pero no conserva web propia ni email.
- `colegio_economistas_lp.json` solo guarda `nombre`, `apellidos`, `nombre_completo`, `num_colegiado`; no esta listo para enrichment sin una fase previa de website matching.
- `despachos_enriquecidos.json` añade descripcion, horario y un flag `tiene_web_propia`, pero `web_propia` aparece vacia en la evidencia local. Tiene `30/30` `url_ficha` y `28/30` telefonos, pero `0` emails.
- `icp_scored_prospects.json` es una capa de ranking, no una capa de contacto.

### 3. Experimento 1 - precedente email-first validado

| Dataset | Ruta | Grano | Volumen | URLs web | Emails / canales | Estado |
|---|---|---|---:|---|---|---|
| `aafc-scaled-dataset_experimento-1.csv` | `05_scratch/experimento_1/` | empresa | `70` | `70/70` `website_url` | `70/70` | `already_enriched` |
| `google-basic-curated-dataset_experimento-1.csv` | `05_scratch/experimento_1/` | empresa | `31` | `31/31` `website_url` | `28/31` email real | `already_enriched` |
| `consolidated-scaled-dataset_experimento-1.csv` | `05_scratch/experimento_1/` | empresa deduped | `101` | `31/101` `website_url`, `26/101` `contact_page_url` | `98/101` email real | `already_enriched` |

Diagnostico:

- Es el mejor precedente interno de contrato `email-first` del repo.
- Usa `contact_channel_type`, `email_or_channel`, `website_url`, `contact_page_url` y `dedupe_key`.
- `dedupe_key` no presenta duplicados en el consolidado (`0`).

### 4. Skilland IA Mujeres - outreach institucional ya enriquecido

| Dataset | Ruta | Grano | Volumen | URLs fuente | Emails | Estado |
|---|---|---|---:|---|---|---|
| `directorio_ayuntamientos_igualdad_social.csv` | `04_outputs/skilland-ia-mujeres/ayuntamientos_contactos_igualdad_social/` | municipio recomendado | `88` | `88/88` fuente principal, `82/88` secundaria | patron email en `82/88` filas | `already_enriched` |
| `municipios_canarias_seed.csv` | misma carpeta | municipio seed | `88` | `88/88` URL oficial | no | `normalization_first` |
| `directorio_cabildos_igualdad_social.csv` | `04_outputs/skilland-ia-mujeres/cabildos_contactos_igualdad_social/` | contacto por cabildo | `16` | `16/16` principal, `16/16` secundaria | patron email en `16/16` filas | `already_enriched` |

Diagnostico:

- Los directorios finales ya cumplen la logica de contacto institucional con trazabilidad de fuente.
- `municipios_canarias_seed.csv` solo es un seed de discovery, no un lead export.
- En cabildos hay `9` duplicados por columna `Cabildo` porque el dataset tiene varias filas por institucion; eso es esperado a nivel de contacto, no de organizacion.

### 5. Skilland IA Mujeres - capa canonica data prep

| Dataset | Ruta | Grano | Volumen | Website / source URL | Emails | Estado |
|---|---|---|---:|---|---|---|
| `organizations_clean.csv` | `04_outputs/skilland_ia_mujeres/data_prep/` | organizacion | `95` | `79/95` `website`, `95/95` `source_url` | `89/95` `email_main` | `already_enriched` |
| `contacts_clean.csv` | misma carpeta | contacto | `166` | `166/166` `source_url` | `160/166` email | `already_enriched` |
| `import_ready_combined.csv` | misma carpeta | mixed import | `261` | `website` y `source_url` | patron email en `249/261` filas | `already_enriched` |
| `organizations_clean.json` | misma carpeta | espejo JSON | `95` | si | si | `mirror_export` |
| `contacts_clean.json` | misma carpeta | espejo JSON | `166` | si | si | `mirror_export` |

Diagnostico:

- Esta es la referencia mas cercana a una capa canonica de organizaciones + contactos dentro del repo.
- `organizations_clean.csv` y `contacts_clean.csv` no presentan duplicados en sus claves simples revisadas (`organization_name` y `organization_name + email`).
- Conviene reutilizar su contrato de trazabilidad (`source_url`, `source_file`, `source_type`, flags de calidad) en Interreg.

## Respuestas directas al encargo

### Que datasets existen

Existen cinco familias relevantes:

- `Interreg / keep.eu / Knowledge Transfer`: raw provenance, sample raw, sample scored, processed scored, reports y scripts.
- `Experimento 0`: discovery y scoring pre-email-first para despachos / directorios.
- `Experimento 1`: precedent interno email-first con datasets ya contactables.
- `Skilland IA Mujeres` directorios finales: ayuntamientos y cabildos con emails institucionales.
- `Skilland IA Mujeres` data prep: capa canonica de organizaciones y contactos lista para import.

### Cuantas organizaciones / entidades ya se han extraido

No es seguro sumar todas las filas del repo porque muchas capas son derivadas o duplicadas. Los volumenes utiles por familia son:

- Interreg raw proyecto: `18 + 150 + 200 = 368` proyectos.
- Interreg partner scored: `136 + 1,380 + 1,676 = 3,192` filas `partner_in_project` antes de dedupe cross-wave.
- Experimento 0: `137` fichas de directorio, `49` colegiados, `30` despachos enriquecidos, `77` prospectos scored.
- Experimento 1: `70` AAFC, `31` Google curated, `101` consolidado deduped.
- Skilland IA Mujeres: `88` municipios seed, `88` filas finales de ayuntamientos, `16` filas finales de cabildos, `95` organizaciones canonicas, `166` contactos canonicos.

### Que campos tienen actualmente

Patrones principales observados:

- discovery historico: `nombre`, `actividad`, `direccion`, `telefono`, `url_ficha`
- email-first comercial: `company_name`, `contact_channel_type`, `email_or_channel`, `website_url`, `contact_page_url`, `dedupe_key`
- institucional final: multiples columnas de email (`personal`, `area`, `generico`), telefonos, URLs fuente y notas de confianza
- Interreg scored: metadata de proyecto y partner, `source_url`, `documents_url`, `contact_url`, scores, pero `contact_email` vacio
- canonica data prep: `organization_name`, `website`, `email_main`, `source_url`, `source_file`, flags de calidad, `needs_manual_review`

### Contienen las URLs de sus sitios web

- Si, claramente: `Experimento 1`, directorios finales de IA Mujeres, `organizations_clean`, `Interreg scored` via `contact_url`, y `Interreg raw` via `source_url`.
- Parcialmente: `experimento_0` via `url_ficha`, pero no con web oficial util para enrichment en todos los casos.
- No: `colegio_economistas_lp.json` e `icp_scored_prospects.json`.

### Contienen correos electronicos

- Si: `Experimento 1`, directorios finales de IA Mujeres, `organizations_clean`, `contacts_clean`, `import_ready_combined`.
- No: toda la capa `Interreg scored / processed`, `Interreg raw`, `experimento_0` y `municipios_canarias_seed.csv`.

### Estan los emails presentes en las exportaciones finales

- Si en los carriles ya maduros: `Experimento 1` y `skilland_ia_mujeres/data_prep`, mas los directorios finales de ayuntamientos y cabildos.
- No en `skilland-knowledge-transfer-engine/interreg_mac/04_processed_outputs/`: esa carpeta hoy se presenta como processed final, pero en realidad sigue siendo pre-outreach porque `contact_email` = `0` en todas las waves.
- No en los outputs finales de `experimento_0`.

### Se conservan las URLs de origen del contacto

- Si, de forma fuerte: IA Mujeres y `data_prep` (`source_url`, URLs fuente principal/secundaria).
- Si, pero incompleto para email: Interreg (`source_url` y `contact_url` existen, pero no `email_source_url` ni una evidencia cerrada del hallazgo/ausencia del email).
- Parcial: Experimento 0 (`url_ficha` de directorio, no necesariamente web oficial del despacho).

### Existen organizaciones duplicadas

Si.

- Duplicado de archivo: `sample_scored` y `processed_scored` son espejos exactos en las tres waves Interreg.
- Duplicado de entidad en Interreg: al menos `5`, `194` y `353` duplicados por `(partner_name + partner_country)` en waves `1`, `2` y `3`.
- Duplicado esperado por multiconacto institucional: cabildos (`9` duplicados por columna `Cabildo`).
- No se observan duplicados en `Experimento 1` consolidado por `dedupe_key`, ni en `organizations_clean` / `contacts_clean` con las claves simples revisadas.

### Que datasets estan listos para el enriquecimiento

Prioridad real de enrichment futuro:

1. `04_outputs/skilland-knowledge-transfer-engine/interreg_mac/04_processed_outputs/wave*_keep_eu_processed_scored.csv`
   - Mejor input disponible para backfill.
   - Ya tiene partner, geografia, scoring y `contact_url` en `100%` de filas.
   - Requiere canonizacion previa y dedupe antes de enrichment web.
2. `03_samples/wave*_keep_eu_sample_scored.csv`
   - No enriquecer por separado.
   - Son espejo del punto 1 y solo sirven como evidencia de duplicacion.
3. `municipios_canarias_seed.csv`
   - Tecnicamente listo para una busqueda de contacto, pero no es prioridad porque ya existe un directorio final mucho mas rico.

### Que datasets necesitan normalizacion previa

Necesitan normalizacion antes de cualquier enrichment serio:

- `Interreg sample raw` (`wave*_keep_eu_sample_raw.csv`): grano proyecto, no grano organizacion/contacto.
- `experimento_0/datos/*.json`: discovery historico sin email y con preservacion debil de web oficial.
- `colegio_economistas_lp.json`: sin URLs y sin contacto web.
- toda la provenance raw de Interreg (`raw_api`, `raw_html`, `raw_exports`): sirven de evidencia, no de input directo a CRM.

## Recomendacion operativa

- Declarar `04_processed_outputs/wave*_keep_eu_processed_scored.csv` como unica base candidata de Interreg para la ola siguiente.
- Eliminar el doble trabajo sobre `03_samples/*_sample_scored.csv` en la fase de enrichment; conservarlos solo como muestra historica.
- Introducir una capa canonica de leads donde `score` y `lead_readiness` vivan separados.
- Usar `skilland_ia_mujeres/data_prep` como patron interno de contrato de datos: `source_url`, `source_file`, `source_type`, flags de calidad y trazabilidad de contacto.

## Unknowns / riesgos abiertos

- `Unknown`: cuantas entidades Interreg tendran web de partner accesible desde `contact_url` sin una segunda fase de discovery controlada.
- `Unknown`: cuantos partners compartiran un mismo email generico y exigiran consolidacion por organizacion.
- Riesgo: si se hace enrichment directamente sobre `partner_in_project` sin capa canonica, el CRM duplicara organizaciones entre waves y proyectos.
