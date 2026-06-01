# Wave 1 sample report

Fecha: 2026-05-31T20:49:35.393Z

## Metodo

- Source discovery con `/api/available-filters-v2/`.
- Search API oficial de keep.eu via `/api/search/projects/`.
- Export oficial XLSX por grupo via `response_type=excel`.
- Descarga de fichas HTML de proyecto para enriquecer fechas, estado, partners, outputs y objetivo especifico.
- Modelo de registro final: `partner_in_project`.

## Cobertura de la wave

- Proyectos tomados: 18
- Registros partner_in_project scored: 136
- Objetivo minimo de partner rows: 100

## Grupos ejecutados

- Interreg MAC 2021-2027: 0/8 proyectos tomados
- Atlantic Area 2021-2027: 8/8 proyectos tomados
- Interreg MAC 2014-2020: 5/5 proyectos tomados
- NEXT MED 2021-2027: 5/5 proyectos tomados

## Distribucion por programa

- 2021 - 2027 Interreg VI-B Atlantic Area: 101 registros
- 2021 - 2027 Interreg VI-B NEXT Mediterranean Sea Basin (NEXT MED): 30 registros
- 2014 - 2020 INTERREG V-A Spain - Portugal (Madeira - Açores - Canarias (MAC)): 5 registros

## Distribucion por pais de partner

- Spain: 38 registros
- Portugal: 29 registros
- France: 24 registros
- Ireland: 19 registros
- Italy: 5 registros
- Tunisia: 4 registros
- Lebanon: 4 registros
- Greece: 4 registros
- Palestine: 4 registros
- Jordan: 2 registros

## Top scores

- 4.9 | Sapienza University of Rome | DIEM~A_T_3.1_0118 | 2021 - 2027 Interreg VI-B NEXT Mediterranean Sea Basin (NEXT MED)
- 4.8 | La Palma Research Centre (La Palma Office) | Impact4Mar | 2021 - 2027 Interreg VI-B Atlantic Area
- 4.65 | Università degli Studi di Bari Aldo Moro | HERACLES~A_T_1.1_0235 | 2021 - 2027 Interreg VI-B NEXT Mediterranean Sea Basin (NEXT MED)
- 4.65 | Universidad de Huelva | HERACLES~A_T_1.1_0235 | 2021 - 2027 Interreg VI-B NEXT Mediterranean Sea Basin (NEXT MED)
- 4.65 | Associació Fons Català de Cooperació al Desenvolupament | EmpoweerNEET~A_T_3.1_0156 | 2021 - 2027 Interreg VI-B NEXT Mediterranean Sea Basin (NEXT MED)
- 4.6 | Aqualgae Sociedade Limitada (Research and Development) | SMACC+ | 2021 - 2027 Interreg VI-B Atlantic Area
- 4.55 | Universitat Politècnica de València | DIEM~A_T_3.1_0118 | 2021 - 2027 Interreg VI-B NEXT Mediterranean Sea Basin (NEXT MED)
- 4.55 | Fondazione MeNO ETS – Italy | DIEM~A_T_3.1_0118 | 2021 - 2027 Interreg VI-B NEXT Mediterranean Sea Basin (NEXT MED)
- 4.5 | Technological University of the Shannon: Midlands Midwest (Research Development and Innovation ) | Impact4Mar | 2021 - 2027 Interreg VI-B Atlantic Area
- 4.5 | South East Technological University (RIKON Research Centre - SETU) | Impact4Mar | 2021 - 2027 Interreg VI-B Atlantic Area

## Limitaciones

- keep.eu no expone emails directos de partner en abierto sin login, por eso `contact_email` queda vacio.
- No todos los proyectos muestran documentos adjuntos; `documents_url` solo se rellena cuando la ficha publica los expone.
- El scoring es heuristico y prioriza senales de training, capacity building, knowledge transfer y business-facing beneficiaries.
