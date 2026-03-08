# Escalado Google Basic Curated - Experimento 1

- Fecha: 2026-03-07
- Fuente: `google_basic_live_serp` curada para emailing
- Registros raw: `47`
- Registros curados: `31`
- Registros descartados: `16`
- `source_quality_score`: `95`
- Gate de escalado: `True`

## Scorecard curado

- `% P0 contactable`: `100.0`
- `% email real`: `90.3`
- `% canal alternativo`: `9.7`
- `% emails unicos`: `100.0`
- `% ruido`: `0.0`
- `% duplicados`: `0.0`
- `% señales ICP útiles`: `100.0`
- `% queries con discovery live valido`: `100.0`

## Curacion aplicada

- `non_target_domain_or_entity`: `14`
- `non_target_url_pattern`: `2`

## Top ranking orientado a emailing

| Company | Geography | Email/Canal | SERP rank | Contactability |
|---|---|---|---:|---:|
| Weeks & Co | santa cruz de tenerife|tenerife | administración@weeksasesores.com | 6 | 95 |
| Tengo Asesor | santa cruz de tenerife|tenerife | taco@tengoasesor.com | 6 | 95 |
| Macrosuma asesores | las palmas de gran canaria|gran canaria | asesores@macrosuma.es | 1 | 95 |
| Asesoría Santa Cruz de Tenerife Tax | santa cruz de tenerife|tenerife | vic@tax.es | 4 | 95 |
| Armas y Asociados | las palmas de gran canaria|gran canaria | manuel@armas-asociados.com | 3 | 95 |
| A.T. ASESORES TENERIFE | santa cruz de tenerife|tenerife | atasesores@atasesores.net | 8 | 95 |
| Carlos Mantilla | multiple|canarias | contabilidad@mantillaasociados.com | 2 | 85 |
| Lafuente Asesores | santa cruz de tenerife|tenerife | contacto@lafuenteasesores.es | 4 | 80 |
| Gómez Asesores | santa cruz de tenerife|tenerife | administracion@gomezasesores.com | 8 | 80 |
| Ferrera Asesores Y CONSULTORES | santa cruz de tenerife|tenerife | info@ferreraasesores.com | 5 | 80 |
| Cabrera Rodríguez | las palmas de gran canaria|gran canaria | info@cabrerarodriguez.com | 2 | 80 |
| Asesoría Fiscal y Abogados en Las Palmas de Gran Canaria | las palmas de gran canaria|gran canaria | info@fiscaltaxcanarias.com | 3 | 80 |
| Asesores Tenerife | santa cruz de tenerife|tenerife | info@eximasesores.com | 5 | 80 |
| ah asesores | santa cruz de tenerife|tenerife | info@ahasesores.com | 4 | 80 |
| Advixy | santa cruz de tenerife|tenerife | info@advixy.com | 5 | 80 |

## Lectura operativa

- `google_basic` queda validado tecnicamente con discovery live en Google usando Scrapling.
- El dataset util para emailing exige una capa de curacion comercial explicita: Google por si solo mezcla webs propias, agregadores y ruido editorial.
- El output que debe escalar es este dataset curado, no el raw completo.
