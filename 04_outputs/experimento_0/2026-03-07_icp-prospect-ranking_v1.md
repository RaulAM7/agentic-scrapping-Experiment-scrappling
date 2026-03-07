# Ranking de Prospectos ICP — Asesorias Fiscales/Contables Canarias

> Generado: 2026-03-07
> Fuentes: Paginas Amarillas (6 busquedas) + Colegio de Economistas de Las Palmas
> Total prospectos en Canarias: 77
> Despachos en target ICP (asesoria fiscal/contable): 38

## Metodologia de scoring

Basada en la heuristica del ICP (`04_outputs/icp-asesoria-fiscal-contable-canarias.md`, bloque 6):

| Senal | Peso | Fuente |
|-------|------|--------|
| Asesoria fiscal/contable en Canarias | 4 | Paginas Amarillas |
| Sin web propia | 3 | Confirmado via fichas PA |
| Posible registro colegial (cruce apellidos) | 3 | Colegio Economistas LP |
| Ubicacion en capital insular | 2 | Paginas Amarillas |
| **Score maximo posible** | **12** | |

## Top 20 prospectos

| # | Score | Nombre | Actividad | Localidad |
|---|-------|--------|-----------|-----------|
| 1 | 12 | Sanchez Marichal Auditores | Asesorias fiscales | Las Palmas de GC |
| 2 | 12 | Asesoria Romero S.L. | Asesorias fiscales | Las Palmas de GC |
| 3 | 12 | Asesoria Artiles | Asesorias fiscales | Las Palmas de GC |
| 4 | 12 | Responsable Mario Alonso Alvarez | Asesorias de empresas | Santa Cruz de TF |
| 5 | 10 | Asesoria Fiscal Miguel Lopez Rosa | Asesorias fiscales | Arrecife |
| 6 | 10 | Asesoria Agustin J. Marrero | Asesorias de empresas | Telde |
| 7 | 10 | Agustin Ruiz Y Asociados S.L. | Asesorias fiscales | Puerto de la Cruz |
| 8 | 9 | Lujan Asesores S.L. | Asesorias fiscales | Las Palmas de GC |
| 9 | 9 | Elena Maria Gutierrez Suarez | Asesorias fiscales | Las Palmas de GC |
| 10 | 9 | Galvan & Martin Asesoria de empresas | Asesorias fiscales | Las Palmas de GC |
| 11 | 9 | Carmen Martin Consultores S.L.P. | Asesorias de empresas | Las Palmas de GC |
| 12 | 9 | ASESORIA SANCHEZ MARICHAL | Asesorias fiscales | Las Palmas de GC |
| 13 | 9 | Chesey Gestiones | Asesorias fiscales | Santa Cruz de TF |
| 14 | 9 | Asesoria Fiscal Mendez Roldan | Asesorias fiscales | Santa Cruz de la Palma |
| 15 | 9 | Asesoria EvMar Tenerife | Asesorias fiscales | Santa Cruz de TF |
| 16 | 9 | Gestoria Benitez Sarmiento | Gestorias administrativas | Las Palmas de GC |
| 17 | 9 | Asesoria Rdp Asociados | Asesorias de empresas | Las Palmas de GC |
| 18 | 9 | Asociacion Castro | Asesorias de empresas | Las Palmas de GC |
| 19 | 9 | HDN Asesores de Empresas | Asesorias de empresas | Las Palmas de GC |
| 20 | 9 | Asfico Asesores C.B. | Asesorias fiscales | Santa Cruz de TF |

## Distribucion de scores

| Score | Despachos |
|-------|-----------|
| 12 | 4 |
| 10 | 3 |
| 9 | 15 |
| 7 | 24 |
| 6 | 13 |
| 4 | 18 |

## Senales validadas con datos reales

| Senal | Cobertura | Veredicto |
|-------|-----------|-----------|
| Ficha PA como asesoria fiscal en Canarias | 38/77 (49%) | **Funciona bien** — discrimina claramente el target |
| Sin web propia | 77/77 (100%) | **Confirmada masivamente** — ninguno de los 30 rastreados tenia web propia |
| Registro colegial (cruce apellidos) | 15/77 (19%) | **Util pero limitado** — solo cruza por apellido, no por empresa |
| Capital insular | 32/77 (42%) | **Util** — concentra la mitad del target |

## Datos en bruto

- `05_scratch/data/paginas_amarillas_canarias.json` — 137 despachos (todas las islas)
- `05_scratch/data/colegio_economistas_lp.json` — 49 colegiados
- `05_scratch/data/icp_scored_prospects.json` — 77 prospectos con scoring
- `05_scratch/data/despachos_enriquecidos.json` — 30 fichas rastreadas en detalle
