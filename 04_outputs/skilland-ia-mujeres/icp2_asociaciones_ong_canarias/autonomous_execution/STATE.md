# STATE - ICP2 Autonomous Execution

Fecha inicial: 2026-06-13

## Estado actual

- `status = planned_not_started`
- `current_round = none`
- `current_source = none`
- `last_completed_round = none`
- `last_completed_source = none`
- `next_action = wait_for_goal_instruction`
- `scraping_executed = false`
- `datasets_created = false`
- `crm_touched = false`
- `gws_touched = false`

## Alcance autorizado para futura `/goal`

- Ronda 1 Canarias alta calidad.
- Ronda 2 Canarias volumen solo si Ronda 1 pasa gates.
- Preparacion Espana V2 solo como backlog/planning.

## Alcance bloqueado

- Ronda 3 scraping Espana nacional alta calidad.
- Ronda 4 scraping Espana nacional alto volumen.
- Ronda 5 scraping CCAA.
- CRM.
- GWS.
- Envios.

## Ultimo checkpoint

No hay ejecucion. Controller documental creado para futura `/goal`.

## Invariantes

- `business_line = SkilLand IA Mujeres`
- `campaign = IA Mujeres 2026`
- `macro_icp = asociaciones_ong_mujeres_inclusion_tech`
- `icp_segment = ICP2 - Asociaciones/ONG - Mujeres e Inclusion Tech`
- Canarias V1 separado de Espana V2.
- No deducir emails por patron.
- No inventar emails, cargos, nombres, actividad ni senales de encaje.

## Proxima accion permitida

Recibir una instruccion `/goal` explicita que autorice ejecutar segun `RUNBOOK.md`.
