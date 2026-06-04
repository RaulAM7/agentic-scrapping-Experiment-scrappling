# Dataset Inventory - SkilLand IA Mujeres

- Date: 2026-06-04
- Scope: datasets and traceability files located in the existing repo and evaluated for CRM data prep.
- Note: no structured association dataset was found in the inspected CSV/XLSX/JSON sources; the usable tabular data is concentrated in cabildos and ayuntamientos.

| file_path | file_type | apparent_content | likely_target | record_count_if_known | usable_for_import | notes |
|---|---|---|---|---:|---|---|
| 04_outputs/skilland-ia-mujeres/Directorio_Igualdad_Empleo_Cabildos_Canarias.xlsx | xlsx | Legacy cabildos spreadsheet focused on igualdad/empleo contacts in Canarias. | cabildos | Unknown | partial | Legacy spreadsheet at project root; treated as precursor source, not final normalized dataset. |
| 04_outputs/skilland-ia-mujeres/cabildos_contactos_igualdad_social/directorio_cabildos_igualdad_social.csv | csv | Final tabular directory of cabildo contacts across igualdad, accion social and empleo. | cabildos | 16 | yes | Primary structured source used for cabildo normalization. |
| 04_outputs/skilland-ia-mujeres/cabildos_contactos_igualdad_social/directorio_cabildos_igualdad_social.xlsx | xlsx | Excel version of the final cabildo directory. | cabildos | Unknown | partial | Likely export of the final CSV; not used directly because CSV is easier to normalize reproducibly. |
| 04_outputs/skilland-ia-mujeres/cabildos_contactos_igualdad_social/directorio_cabildos_igualdad_social.md | md | Narrative report and tabular summary for the cabildo directory. | cabildos | Unknown | no | Used as contextual validation only. |
| 04_outputs/skilland-ia-mujeres/cabildos_contactos_igualdad_social/scraping_notes.md | md | Cabildo source methodology, source URLs and quality notes. | cabildos | Unknown | no | Useful for traceability, not for direct import. |
| 04_outputs/skilland-ia-mujeres/ayuntamientos_contactos_igualdad_social/municipios_canarias_seed.csv | csv | Seed list of the 88 municipalities with official websites and transparency URLs. | ayuntamientos | 88 | partial | Used to canonicalize municipality websites. |
| 04_outputs/skilland-ia-mujeres/ayuntamientos_contactos_igualdad_social/directorio_ayuntamientos_igualdad_social.csv | csv | Final tabular directory of municipal contacts across igualdad, servicios sociales and related areas. | ayuntamientos | 88 | yes | Primary structured source used for ayuntamiento normalization. |
| 04_outputs/skilland-ia-mujeres/ayuntamientos_contactos_igualdad_social/directorio_ayuntamientos_igualdad_social.xlsx | xlsx | Excel version of the final ayuntamiento directory. | ayuntamientos | Unknown | partial | Likely export of the final CSV; not used directly because CSV is easier to normalize reproducibly. |
| 04_outputs/skilland-ia-mujeres/ayuntamientos_contactos_igualdad_social/directorio_ayuntamientos_igualdad_social.md | md | Narrative report and summary table for the ayuntamiento directory. | ayuntamientos | Unknown | no | Used as contextual validation only. |
| 04_outputs/skilland-ia-mujeres/ayuntamientos_contactos_igualdad_social/fuentes_ayuntamientos.json | json | JSON traceability map of municipalities and official sources consulted. | ayuntamientos | 88 | partial | Useful for traceability and source audits, not for direct CRM import. |
| 04_outputs/skilland-ia-mujeres/ayuntamientos_contactos_igualdad_social/coverage_report.md | md | Coverage summary by island for municipal directory production. | ayuntamientos | Unknown | no | Coverage QA summary only. |
| 04_outputs/skilland-ia-mujeres/ayuntamientos_contactos_igualdad_social/scraping_notes_ayuntamientos.md | md | Municipal methodology and data quality notes. | ayuntamientos | Unknown | no | Useful for traceability, not for direct import. |
| 05_scratch/ayuntamientos_contactos_igualdad_social/directorio_ayuntamientos_igualdad_social_raw.csv | csv | Scratch raw directory for ayuntamientos before final export. | ayuntamientos | 88 | partial | Intermediate scratch dataset; final CSV in 04_outputs takes precedence. |
| 05_scratch/ayuntamientos_contactos_igualdad_social/local_curated_rows.csv | csv | Partial locally curated municipal rows used during assembly. | ayuntamientos | 15 | no | Intermediate partial file with incomplete coverage. |
