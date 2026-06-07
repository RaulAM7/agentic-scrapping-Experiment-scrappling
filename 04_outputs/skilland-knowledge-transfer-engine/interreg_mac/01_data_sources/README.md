# Data sources

Esta carpeta contiene fuentes de datos para el caladero Interreg MAC / keep.eu.

## Subcarpetas

- `raw_exports/`: exports manuales o descargados desde keep.eu.
- `raw_html/`: HTML raw guardado durante scraping.
- `raw_api/`: respuestas JSON/API si existen.

## Reglas

- No editar raw data.
- Guardar fecha de descarga.
- Guardar URL de origen.
- Mantener trazabilidad.
- Separar raw de processed.
- Recordar que `raw_*` no es un lead export; solo es evidencia para la siguiente fase de normalizacion y enrichment.
