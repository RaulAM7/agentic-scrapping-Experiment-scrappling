# Wave 1 scraping report

Fecha: 2026-05-31T20:49:35.393Z

## Fuente y vias usadas

- API interna del frontend: `https://keep.eu/api/search/projects/`
- Export oficial XLSX: `response_type=excel`
- HTML publico de ficha de proyecto: `https://keep.eu/projects/{id}/`

## Rutas de output generadas

### raw_exports

- 01_data_sources/raw_exports/20260531_keep_eu_mac_2021_projects_export.xlsx
- 01_data_sources/raw_exports/20260531_keep_eu_atlantic_2021_projects_export.xlsx
- 01_data_sources/raw_exports/20260531_keep_eu_mac_2014_projects_export.xlsx
- 01_data_sources/raw_exports/20260531_keep_eu_next_med_2021_projects_export.xlsx

### raw_api

- 01_data_sources/raw_api/20260531_keep_eu_available_filters.json
- 01_data_sources/raw_api/20260531_keep_eu_mac_2021_payload.json
- 01_data_sources/raw_api/20260531_keep_eu_mac_2021_projects_page_001.json
- 01_data_sources/raw_api/20260531_keep_eu_atlantic_2021_payload.json
- 01_data_sources/raw_api/20260531_keep_eu_atlantic_2021_projects_page_001.json
- 01_data_sources/raw_api/20260531_keep_eu_mac_2014_payload.json
- 01_data_sources/raw_api/20260531_keep_eu_mac_2014_projects_page_001.json
- 01_data_sources/raw_api/20260531_keep_eu_next_med_2021_payload.json
- 01_data_sources/raw_api/20260531_keep_eu_next_med_2021_projects_page_001.json

### raw_html

- 18 fichas de proyecto guardadas en `01_data_sources/raw_html/projects/`

## Decisiones de ejecucion

- Priorizacion real: MAC 2021-2027, Atlantic Area 2021-2027, MAC 2014-2020 y NEXT MED 2021-2027.
- Extraccion controlada por cuotas de proyecto por grupo para no sobrerrecoger datos irrelevantes.
- Enriquecimiento por ficha HTML solo para la muestra Wave 1, con delay de 400 ms entre fichas.

## Gaps pendientes

- Afinar payloads de busqueda por keywords si hace falta una Wave 2 mas focalizada.
- Añadir parser de adjuntos/documentos cuando el proyecto publica documentos descargables.
- Enriquecer contactos y webs oficiales fuera de keep.eu en una wave posterior.
