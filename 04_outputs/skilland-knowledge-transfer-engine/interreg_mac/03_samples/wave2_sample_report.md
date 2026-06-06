# wave2 sample report

Fecha: 2026-06-01T04:31:57.141Z

## Metodo

- Source discovery con `/api/available-filters-v2/`.
- Search API oficial de keep.eu via `/api/search/projects/`.
- Export oficial XLSX por grupo via `response_type=excel`.
- Descarga paralela de fichas HTML de proyecto con concurrencia 8.
- Modelo de registro final: `partner_in_project`.

## Cobertura de la wave

- Proyectos tomados: 150
- Registros partner_in_project scored: 1380
- Objetivo minimo de partner rows: 500
- Perfil ejecutado: broad

## Grupos ejecutados

- Interreg MAC 2021-2027: 0/20 proyectos tomados; 0 disponibles; 1 paginas
- Atlantic Area 2021-2027: 40/40 proyectos tomados; 52 disponibles; 8 paginas
- NEXT MED 2021-2027: 40/40 proyectos tomados; 59 disponibles; 8 paginas
- EURO MED 2021-2027: 25/25 proyectos tomados; 89 disponibles; 6 paginas
- Interreg MAC 2014-2020: 15/15 proyectos tomados; 123 disponibles; 4 paginas
- Atlantic Area 2014-2020: 15/15 proyectos tomados; 71 disponibles; 4 paginas
- Mediterranean 2014-2020: 15/15 proyectos tomados; 142 disponibles; 4 paginas

## Distribucion por programa

- 2021 - 2027 Interreg VI-B Atlantic Area: 648 registros
- 2021 - 2027 Interreg VI-B NEXT Mediterranean Sea Basin (NEXT MED): 261 registros
- 2021 - 2027 Interreg VI-B EURO Mediterranean (EURO MED): 221 registros
- 2014 - 2020 INTERREG VB Atlantic Area: 143 registros
- 2014 - 2020 INTERREG VB Mediterranean: 92 registros
- 2014 - 2020 INTERREG V-A Spain - Portugal (Madeira - Açores - Canarias (MAC)): 15 registros

## Distribucion por pais de partner

- Spain: 373 registros
- France: 201 registros
- Portugal: 193 registros
- Ireland: 126 registros
- Italy: 121 registros
- Greece: 75 registros
- Lebanon: 33 registros
- Tunisia: 25 registros
- Croatia: 25 registros
- United Kingdom: 25 registros
- Slovenia: 23 registros
- Cyprus: 22 registros
- Jordan: 22 registros
- Egypt: 20 registros
- Turkey: 20 registros

## Top scores

- 5 | University eCampus | GREENOLIVE~A_T_2.1_0213 | 2021 - 2027 Interreg VI-B NEXT Mediterranean Sea Basin (NEXT MED)
- 5 | Next Technology Tecnotessile Società Nazionale di Ricerca r.l. | Waste2Fashion~A_T_2.4_... | 2021 - 2027 Interreg VI-B NEXT Mediterranean Sea Basin (NEXT MED)
- 5 | CUEIM Consorzio Universitario di Economia Industriale e Manageriale | BIOSTARS | 2021 - 2027 Interreg VI-B EURO Mediterranean (EURO MED)
- 5 | Fundación Corporación Tecnológica De Andalucía | BIOSTARS | 2021 - 2027 Interreg VI-B EURO Mediterranean (EURO MED)
- 5 | t2i - trasferimento tecnologico e innovazione | RECONNECT | 2021 - 2027 Interreg VI-B EURO Mediterranean (EURO MED)
- 5 | Università Iuav di Venezia | MED4REGEN | 2021 - 2027 Interreg VI-B EURO Mediterranean (EURO MED)
- 5 | Università degli Studi di Ferrara | Sole MED | 2021 - 2027 Interreg VI-B EURO Mediterranean (EURO MED)
- 4.9 | Sapienza University of Rome | DIEM~A_T_3.1_0118 | 2021 - 2027 Interreg VI-B NEXT Mediterranean Sea Basin (NEXT MED)
- 4.9 | National Technological Centre for the Food and Canning Industry | HEEFTA~A_Y_3.1_0232 | 2021 - 2027 Interreg VI-B NEXT Mediterranean Sea Basin (NEXT MED)
- 4.9 | REGIONE DEL VENETO | MED4REGEN | 2021 - 2027 Interreg VI-B EURO Mediterranean (EURO MED)
- 4.9 | Empresa Municipal de Iniciativas y Actividades Empresariales de Málaga, S.A. | MED4REGEN | 2021 - 2027 Interreg VI-B EURO Mediterranean (EURO MED)
- 4.9 | Ayuntamiento de Lleida | Sole MED | 2021 - 2027 Interreg VI-B EURO Mediterranean (EURO MED)
- 4.8 | La Palma Research Centre (La Palma Office) | Impact4Mar | 2021 - 2027 Interreg VI-B Atlantic Area
- 4.8 | Asociación de Industrias de Conocimiento y Tecnología - GAIA - Euskal Herriko Ezagutza eta Teknologia Industrien Elkartea (Servicios Cluster) | BEACon | 2021 - 2027 Interreg VI-B Atlantic Areano 
- 4.8 | Asociación de Empresas Tecnológicas Innovalia (Research and development) | UPWELLING | 2021 - 2027 Interreg VI-B Atlantic Area

## Limitaciones

- keep.eu no expone emails directos de partner en abierto sin login.
- MAC 2021 sigue apareciendo en filtros pero no devolvio proyectos publicos en esta wave.
- El scoring sigue siendo heuristico y sirve para triage, no como decision final.
