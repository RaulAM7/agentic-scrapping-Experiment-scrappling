# wave2 scraping report

Fecha: 2026-06-01T04:31:57.141Z

## Fuente y vias usadas

- API interna del frontend: `https://keep.eu/api/search/projects/`
- Export oficial XLSX: `response_type=excel`
- HTML publico de ficha de proyecto: `https://keep.eu/projects/{id}/`

## Volumen de la wave

- Proyectos: 150
- Registros partner_in_project: 1380
- Fichas HTML guardadas: 150

## Rutas de output generadas

### raw_exports

- 01_data_sources/raw_exports/20260601_wave2_keep_eu_mac_2021_projects_export.xlsx
- 01_data_sources/raw_exports/20260601_wave2_keep_eu_atlantic_2021_projects_export.xlsx
- 01_data_sources/raw_exports/20260601_wave2_keep_eu_next_med_2021_projects_export.xlsx
- 01_data_sources/raw_exports/20260601_wave2_keep_eu_euro_med_2021_projects_export.xlsx
- 01_data_sources/raw_exports/20260601_wave2_keep_eu_mac_2014_projects_export.xlsx
- 01_data_sources/raw_exports/20260601_wave2_keep_eu_atlantic_2014_projects_export.xlsx
- 01_data_sources/raw_exports/20260601_wave2_keep_eu_med_2014_projects_export.xlsx

### raw_api

- 01_data_sources/raw_api/20260601_wave2_keep_eu_available_filters.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_mac_2021_payload.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_mac_2021_projects_page_001.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_atlantic_2021_payload.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_atlantic_2021_projects_page_001.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_atlantic_2021_projects_page_002.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_atlantic_2021_projects_page_003.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_atlantic_2021_projects_page_004.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_atlantic_2021_projects_page_005.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_atlantic_2021_projects_page_006.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_atlantic_2021_projects_page_007.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_atlantic_2021_projects_page_008.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_next_med_2021_payload.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_next_med_2021_projects_page_001.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_next_med_2021_projects_page_002.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_next_med_2021_projects_page_003.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_next_med_2021_projects_page_004.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_next_med_2021_projects_page_005.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_next_med_2021_projects_page_006.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_next_med_2021_projects_page_007.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_next_med_2021_projects_page_008.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_euro_med_2021_payload.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_euro_med_2021_projects_page_001.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_euro_med_2021_projects_page_002.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_euro_med_2021_projects_page_003.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_euro_med_2021_projects_page_004.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_euro_med_2021_projects_page_005.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_euro_med_2021_projects_page_006.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_mac_2014_payload.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_mac_2014_projects_page_001.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_mac_2014_projects_page_002.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_mac_2014_projects_page_003.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_mac_2014_projects_page_004.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_atlantic_2014_payload.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_atlantic_2014_projects_page_001.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_atlantic_2014_projects_page_002.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_atlantic_2014_projects_page_003.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_atlantic_2014_projects_page_004.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_med_2014_payload.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_med_2014_projects_page_001.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_med_2014_projects_page_002.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_med_2014_projects_page_003.json
- 01_data_sources/raw_api/20260601_wave2_keep_eu_med_2014_projects_page_004.json

### raw_html

- 150 fichas de proyecto guardadas en `01_data_sources/raw_html/projects/`

## Decisiones de ejecucion

- Priorizacion amplia sobre Atlantic, MAC y MED para subir volumen.
- Se compenso la ausencia publica de MAC 2021 con programas adyacentes de mayor densidad.
- Se uso detalle paralelo con caché local para acelerar sin hacer scraping ciego.
