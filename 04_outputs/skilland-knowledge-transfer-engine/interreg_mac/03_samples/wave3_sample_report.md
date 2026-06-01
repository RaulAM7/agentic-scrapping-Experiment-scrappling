# wave3 sample report

Fecha: 2026-06-01T04:44:04.607Z

## Metodo

- Source discovery con `/api/available-filters-v2/`.
- Search API oficial de keep.eu via `/api/search/projects/`.
- Export oficial XLSX por grupo via `response_type=excel`.
- Descarga paralela de fichas HTML de proyecto con concurrencia 10.
- Modelo de registro final: `partner_in_project`.

## Cobertura de la wave

- Proyectos tomados: 200
- Registros partner_in_project scored: 1676
- Objetivo minimo de partner rows: 1200
- Perfil ejecutado: deep

## Grupos ejecutados

- Interreg MAC 2021-2027: 0/20 proyectos tomados; 0 disponibles; 1 paginas
- Atlantic Area 2021-2027: 12/30 proyectos tomados; 52 disponibles; 9 paginas
- NEXT MED 2021-2027: 19/35 proyectos tomados; 59 disponibles; 10 paginas
- EURO MED 2021-2027: 60/60 proyectos tomados; 89 disponibles; 15 paginas
- Interreg MAC 2014-2020: 40/40 proyectos tomados; 123 disponibles; 11 paginas
- Atlantic Area 2014-2020: 30/30 proyectos tomados; 71 disponibles; 9 paginas
- Mediterranean 2014-2020: 60/60 proyectos tomados; 142 disponibles; 14 paginas

## Distribucion por programa

- 2021 - 2027 Interreg VI-B EURO Mediterranean (EURO MED): 593 registros
- 2014 - 2020 INTERREG VB Mediterranean: 384 registros
- 2014 - 2020 INTERREG VB Atlantic Area: 298 registros
- 2021 - 2027 Interreg VI-B Atlantic Area: 238 registros
- 2021 - 2027 Interreg VI-B NEXT Mediterranean Sea Basin (NEXT MED): 123 registros
- 2014 - 2020 INTERREG V-A Spain - Portugal (Madeira - Açores - Canarias (MAC)): 40 registros

## Distribucion por pais de partner

- Spain: 365 registros
- Italy: 220 registros
- France: 190 registros
- Portugal: 186 registros
- Greece: 163 registros
- Ireland: 81 registros
- Croatia: 78 registros
- United Kingdom: 64 registros
- Slovenia: 51 registros
- Cyprus: 44 registros
- Bosnia and Herzegovina: 34 registros
- Montenegro: 33 registros
- Albania: 30 registros
- Bulgaria: 25 registros
- Malta: 24 registros

## Top scores

- 5 | Catalan Fashion Cluster | MATRIX~A_T_2.4_0289 | 2021 - 2027 Interreg VI-B NEXT Mediterranean Sea Basin (NEXT MED)
- 5 | Next Technology Tecnotessile Società Nazionale di Ricerca r.l. | MATRIX~A_T_2.4_0289 | 2021 - 2027 Interreg VI-B NEXT Mediterranean Sea Basin (NEXT MED)
- 5 | Association of the Mediterranean Chambers of Commerce and Industry | SMAC~A_T_1.2_0523 | 2021 - 2027 Interreg VI-B NEXT Mediterranean Sea Basin (NEXT MED)
- 5 | Eticas Research and Consulting S.L | MEDAIGENCY()~A_T_3.2_0018 | 2021 - 2027 Interreg VI-B NEXT Mediterranean Sea Basin (NEXT MED)
- 5 | Consejo Superior de Investigaciones Cientificas - Instituto Geologico y Minero de España | Clepsydra | 2021 - 2027 Interreg VI-B EURO Mediterranean (EURO MED)
- 5 | Università degli Studi di Cassino e del Lazio Meridionale | Clepsydra | 2021 - 2027 Interreg VI-B EURO Mediterranean (EURO MED)
- 5 | Instituto Superior de Agronomia-Linking environment agriculture and forests | Clepsydra | 2021 - 2027 Interreg VI-B EURO Mediterranean (EURO MED)
- 5 | Fund de la Com. Valenciana para la investigación, promoción y estudios comerciales de Valenciaport | TOURISMO | 2021 - 2027 Interreg VI-B EURO Mediterranean (EURO MED)
- 5 | Fondazione per la Ricerca e l’Innovazione | TOURISMO | 2021 - 2027 Interreg VI-B EURO Mediterranean (EURO MED)
- 5 | Università degli Studi di Firenze | TOURISMO | 2021 - 2027 Interreg VI-B EURO Mediterranean (EURO MED)
- 5 | Università di Firenze | TOURISMO | 2021 - 2027 Interreg VI-B EURO Mediterranean (EURO MED)
- 5 | Università di Torino | CircleMED | 2021 - 2027 Interreg VI-B EURO Mediterranean (EURO MED)
- 5 | Confindustria Umbria | VERDEinMED | 2021 - 2027 Interreg VI-B EURO Mediterranean (EURO MED)
- 5 | Centro Tecnológico das Indústrias Têxtil e do Vestuário de Portugal | VERDEinMED | 2021 - 2027 Interreg VI-B EURO Mediterranean (EURO MED)
- 5 | Fundación Corporación Tecnológica De Andalucía | VERDEinMED | 2021 - 2027 Interreg VI-B EURO Mediterranean (EURO MED)

## Limitaciones

- keep.eu no expone emails directos de partner en abierto sin login.
- MAC 2021 sigue apareciendo en filtros pero no devolvio proyectos publicos en esta wave.
- El scoring sigue siendo heuristico y sirve para triage, no como decision final.
