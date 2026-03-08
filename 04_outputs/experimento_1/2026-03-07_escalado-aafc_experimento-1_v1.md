# Escalado AAFC - Experimento 1

- Fecha: 2026-03-07
- Fuente: `AAFC - Despachos Profesionales`
- Registros extraidos: `70`
- `source_quality_score`: `95`
- Gate de escalado: `True`

## Scorecard

- `% P0 contactable`: `100.0`
- `% email real`: `100.0`
- `% emails unicos`: `100.0`
- `% ruido`: `0.0`
- `% duplicados`: `0.0`
- `% señales ICP útiles`: `95.7`

## Distribución por isla

- ``: `1`
- `el hierro`: `1`
- `fuerteventura`: `6`
- `gran canaria`: `34`
- `la palma`: `1`
- `lanzarote`: `5`
- `tenerife`: `22`

## Top ranking orientado a emailing

| Company | Geography | Email | ICP | Contactability |
|---|---|---|---:|---:|
| SANTIAGO GRANADO ASESORES SL | las palmas de gran canaria|gran canaria | laurasantiago@bsvega.com | 85 | 85 |
| PAYA Y ASOCIADOS CONSULTORES, S.L.U. | santa cruz de tenerife|tenerife | paya@payaconsultores.com | 85 | 85 |
| MABRIBA SL | las palmas de gran canaria|gran canaria | informacion@mabriba.com | 85 | 85 |
| GALLEGO Y ASOCIADOS C.E.SLP | las palmas de gran canaria|gran canaria | amparo@gallegoyasociados.com | 85 | 85 |
| ASESORIA CANARIA GONZALEZ, S.L. | las palmas de gran canaria|gran canaria | gonzalezasesoria@canariasgonzalez.com | 85 | 85 |
| SOLVE IT SPAIN SCP | san bartolome de tirajana|gran canaria | welcome@solveitspain.com | 80 | 85 |
| REAL ASESORES Y ABOGADOS | la orotava|tenerife | real@realasesoresyabogados.com | 80 | 85 |
| GOYA ASESORES | arona|tenerife | asesores@goyaasesores.com | 80 | 85 |
| CONFIJULAB, S.L. | adeje|tenerife | informacion@confijulab.com | 80 | 85 |
| ASESORÍA LOMBARDI | arona|tenerife | juridico@asesorialombardi.es | 80 | 85 |
| ASESORÍA GONZÁLEZ VEGA SLPU | ingenio|gran canaria | pepa@asesoriagonzalezvega.es | 80 | 85 |
| ASESORIA SANTANA GONZALEZ- MARÍA ELISABETH DÉNIZ VALIDO | santa lucia de tirajana|gran canaria | elisabeth@asesoriasantanagonzalez.com | 80 | 85 |
| ASESORIA LABORAL ALEJANDRO | telde|gran canaria | asesoralejandro@telefonica.net | 80 | 85 |
| ASESORIA CONSULTING CRISTY PLASENCIA | guia de isora|tenerife | asesoriaconsulting@cristyplasencia.com | 80 | 85 |
| ALODAN ASESORES SL | granadilla de abona|tenerife | alodan@alodanasesores.es | 80 | 85 |

## Lectura operativa

- `AAFC` queda aprobado para escalado controlado dentro del experimento.
- El dataset es bueno para emailing, pero parte del valor futuro exigirá enriquecer `website_url`, porque hoy muchos registros salen sin web propia visible.
- El siguiente paso razonable es consolidar este dataset como carril `specialized_directory` y compararlo contra cualquier rescate que logremos en `google_basic`.
