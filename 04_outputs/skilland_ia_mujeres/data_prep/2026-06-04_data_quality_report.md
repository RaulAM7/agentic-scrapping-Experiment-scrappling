# Data Quality Report - SkilLand IA Mujeres

- Date: 2026-06-04
- Note: `high_confidence`, `needs_manual_review` and duplicate totals below are reported on the combined review dataset unless stated otherwise.

## 1. Resumen ejecutivo

- Total organizations: 95
- Total contacts: 166
- Cabildos: 7
- Ayuntamientos: 88
- Asociaciones u otras entidades: 0
- Emails personales: 45
- Emails genericos: 114
- Registros `high_confidence`: 164
- Registros `needs_manual_review`: 127
- Posibles duplicados: 17

## 2. Fuentes utilizadas

| source_file | source_type | records_used | notes |
|---|---|---:|---|
| 04_outputs/skilland-ia-mujeres/ayuntamientos_contactos_igualdad_social/directorio_ayuntamientos_igualdad_social.csv | spreadsheet | 88 | Primary municipal contact directory used for contacts and organizations. |
| 04_outputs/skilland-ia-mujeres/cabildos_contactos_igualdad_social/directorio_cabildos_igualdad_social.csv | spreadsheet | 16 | Primary cabildo contact directory used for contacts and organizations. |
| 04_outputs/skilland-ia-mujeres/ayuntamientos_contactos_igualdad_social/municipios_canarias_seed.csv | spreadsheet | 88 | Used only to canonicalize municipal organization websites. |

## 3. Distribucion por segmento

| icp_segment | organizations | contacts | emails | high_confidence | needs_manual_review |
|---|---:|---:|---:|---:|---:|
| Cabildo - Igualdad | 6 | 11 | 11 | 11 | 8 |
| Cabildo - Empleo | 4 | 6 | 6 | 6 | 6 |
| Cabildo - Politicas Sociales | 2 | 3 | 3 | 3 | 3 |
| Ayuntamiento - Igualdad | 61 | 110 | 105 | 109 | 34 |
| Ayuntamiento - Empleo | 1 | 1 | 1 | 1 | 0 |
| Ayuntamiento - Desarrollo Local | 1 | 2 | 2 | 2 | 0 |
| Entidad Publica - Igualdad/Empleo | 25 | 32 | 31 | 32 | 18 |
| Unknown | 0 | 1 | 1 | 0 | 1 |

## 4. Problemas detectados

### Datos incompletos

- Contact rows without email: 6.
- Contact rows without phone: 4.
- Contact rows without named person: 16.

### Emails genericos

- Generic email rows: 114.
- Generic institutional email rows: 47.
- Department emails are common and often more useful than personal emails, but they still need manual routing expectations.

### Duplicados

- Records flagged as possible duplicates: 17.
- Main duplicate driver is exact email reuse across multiple roles or shared central phones.

### Fuentes ambiguas

- Low source confidence rows: 2.
- Medium-confidence rows usually rely on generic institutional channels or missing direct role-level contact data.

### Campos no homologables

- Source files mix political areas, service units and directorios; `department_area` was normalized into CRM-friendly categories.
- Some source rows contained multiple emails in one field; they were split conservatively into one email per contact row.

### Registros que necesitan revision manual

- Combined rows flagged for manual review: 127.
- Review is concentrated in generic institutional emails, unknown named contacts, low-confidence sources and merged duplicate channels.

## 5. Recomendacion para importacion en CRM

- Import organizations from `04_outputs/skilland_ia_mujeres/data_prep/organizations_clean.csv`.
- Import contacts from `04_outputs/skilland_ia_mujeres/data_prep/contacts_clean.csv`.
- Map native fields first: organization/contact names, email, phone, website, municipality, notes.
- Create only the minimum custom campaign fields listed in the Twenty mapping document: `campaign_name`, `icp_segment`, `department_area`, `source_type`, `source_url`, `high_confidence`, `needs_manual_review`, `generic_email`.
- Manually review all rows marked `needs_manual_review=true` before production import; do not blind-import the generic institutional duplicates.
- Dataset readiness: yes for Phase 2 as a review-ready CRM import base, but not for zero-touch import.
