# Escalado Google Basic - Experimento 1

- Fecha: 2026-03-07
- Fuente: `google_basic_live_serp`
- Registros extraidos: `47`
- `source_quality_score`: `94`
- Gate de escalado: `True`

## Scorecard

- `% P0 contactable`: `100.0`
- `% email real`: `83.0`
- `% canal alternativo`: `17.0`
- `% emails unicos`: `100.0`
- `% ruido`: `0.0`
- `% duplicados`: `0.0`
- `% señales ICP útiles`: `97.9`
- `% queries con discovery live valido`: `100.0`

## Resultado por query

- `"asesoria fiscal" "Las Palmas de Gran Canaria" "contacto"` -> `pass` | results `8` | first status `200`
- `"asesoria contable" "Santa Cruz de Tenerife" "contacto"` -> `pass` | results `8` | first status `200`
- `"gestoria" "Gran Canaria" inurl:contacto` -> `pass` | results `8` | first status `200`
- `"asesoria fiscal contable" Canarias email` -> `pass` | results `8` | first status `200`
- `"asesoria autonomos" Canarias "contacto"` -> `pass` | results `8` | first status `200`
- `"asesoria pymes" "Las Palmas" inurl:servicios` -> `pass` | results `4` | first status `200`
- `IGIC asesoria Tenerife contacto` -> `pass` | results `8` | first status `429`
- `"sociedades" "asesoria fiscal" Canarias email` -> `pass` | results `8` | first status `200`

## Top ranking orientado a emailing

| Company | Geography | Email/Canal | SERP rank | Contactability |
|---|---|---|---:|---:|
| Weeks & Co | santa cruz de tenerife|tenerife | administraci%c3%b3n@weeksasesores.com | 6 | 95 |
| Tengo Asesor | santa cruz de tenerife|tenerife | taco@tengoasesor.com | 6 | 95 |
| Macrosuma asesores | las palmas de gran canaria|gran canaria | asesores@macrosuma.es | 1 | 95 |
| Asesoría Santa Cruz de Tenerife Tax | santa cruz de tenerife|tenerife | vic@tax.es | 4 | 95 |
| Armas y Asociados | las palmas de gran canaria|gran canaria | manuel@armas-asociados.com | 3 | 95 |
| A.T. ASESORES TENERIFE | santa cruz de tenerife|tenerife | atasesores@atasesores.net | 8 | 95 |
| Horario de Atención a la Ciudadanía | las palmas de gran canaria|gran canaria | webmaster@laspalmasgc.es | 5 | 95 |
| Iberinform | santa cruz de tenerife|tenerife | clientes@iberinform.es | 7 | 95 |
| EINFORMA. Información de empresas | unknown|gran canaria | clientes@einforma.com | 1 | 95 |
| Carlos Mantilla | multiple|canarias | contabilidad@mantillaasociados.com | 2 | 85 |
| Contacto | multiple|canarias | consultas.atc@gobiernodecanarias.org | 3 | 85 |
| Lafuente Asesores | santa cruz de tenerife|tenerife | contacto@lafuenteasesores.es | 4 | 80 |
| Gómez Asesores | santa cruz de tenerife|tenerife | administracion@gomezasesores.com | 8 | 80 |
| Gestorías en Santa Cruz De Tenerife | santa cruz de tenerife|tenerife | hello@holded.com | 3 | 80 |
| Ferrera Asesores Y CONSULTORES | santa cruz de tenerife|tenerife | info@ferreraasesores.com | 5 | 80 |

## Lectura operativa

- Discovery live en Google validado con StealthySession; aun existe fragilidad parcial por query.
- Este dataset ya no depende de seeds manuales: la discovery nace en Google y la extraccion de contacto se resuelve despues en la web propia.
- Si la fuente pasa gate, `google_basic` ya puede tratarse como candidato real a bulk dentro del stack actual.
