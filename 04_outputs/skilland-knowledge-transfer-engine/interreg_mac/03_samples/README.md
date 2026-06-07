# Samples

Esta carpeta alojara muestras pequenas de datos extraidos.

Objetivo:

- validar estructura;
- validar campos;
- probar scoring;
- revisar calidad;
- detectar duplicados;
- ajustar scraping antes de escalar.

Importante:

- `03_samples/` es una capa de validacion, no la exportacion final de outreach;
- si la muestra no conserva website/contact trace, no esta lista para enrichment;
- si no hay email ni `email_status`, el registro sigue incompleto.

Ejemplos esperados:

- `wave1_keep_eu_sample_raw.csv`
- `wave1_keep_eu_sample_scored.csv`
- `wave1_sample_report.md`
