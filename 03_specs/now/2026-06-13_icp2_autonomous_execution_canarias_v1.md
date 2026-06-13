# Spec activa: ICP2 Autonomous Execution Controller

Fecha: 2026-06-13

## Outcome

Crear la capa documental y operativa de control para una futura ejecucion autonoma encadenada de ICP2. Esta spec no ejecuta scraping, no crea datasets finales y no toca CRM/GWS.

La ejecucion futura recomendada es:

1. Ronda 1 - Canarias alta calidad.
2. Reviewer interno y QA.
3. Ronda 2 - Canarias volumen solo si Ronda 1 pasa gates.
4. Preparacion de backlog Espana V2 sin scraping nacional.

## Inputs

- `04_outputs/skilland-ia-mujeres/icp2_asociaciones_ong_canarias/exploitation_plan/`
- `04_outputs/skilland-ia-mujeres/icp2_asociaciones_ong_canarias/source_discovery/source_inventory.csv`
- `04_outputs/skilland-ia-mujeres/icp2_asociaciones_ong_canarias/source_discovery/next_phase_recommendation.md`
- `03_specs/now/2026-06-12_icp2_exploitation_plan_from_source_discovery.md`

## Contexto operativo fijo

- `business_line = SkilLand IA Mujeres`
- `campaign = IA Mujeres 2026`
- `macro_icp = asociaciones_ong_mujeres_inclusion_tech`
- `icp_segment = ICP2 - Asociaciones/ONG - Mujeres e Inclusion Tech`

ICP2 no crea nueva business line, campaign, funnel, workflow, metricas, CRM ni GWS.

## Entregables

Crear bajo `04_outputs/skilland-ia-mujeres/icp2_asociaciones_ong_canarias/autonomous_execution/`:

- `RUNBOOK.md`
- `STATE.md`
- `EXECUTION_LOG.md`
- `REVIEWER_GATES.md`
- `STOP_CONDITIONS.md`
- `ROUND_STATUS.md`
- `ERRORS_AND_BLOCKERS.md`
- `FINAL_SUMMARY.md`

## Scope

- Definir arquitectura de ejecucion autonoma.
- Definir rutas futuras por ronda.
- Definir reviewer interno.
- Definir gates y stop conditions.
- Definir limites de crawling/scraping.
- Definir estado vivo, logs, checkpoints y resumen.
- Definir que puede ejecutar una futura `/goal` sin supervision.
- Definir que queda bloqueado para humano.

## No Scope

No crear:

- `organizations_clean.csv`
- `contacts_clean.csv`
- leads finales
- scraping real
- crawling masivo
- scripts definitivos
- importacion CRM
- workflows
- envios
- GWS

No tocar:

- `04_outputs/skilland_ia_mujeres/data_prep/`
- CRM
- GWS
- otros repositorios

No inventar emails, cargos, nombres, actividad, foco mujeres, programas, alianzas ni senales de encaje. No deducir emails por patron.

## Acceptance

- Existen los ocho documentos de `autonomous_execution/`.
- `RUNBOOK.md` recomienda Opcion C y define secuencia Ronda 1 -> QA -> Ronda 2 -> QA -> backlog Espana V2.
- `STATE.md` queda en `planned_not_started`.
- `REVIEWER_GATES.md` incluye checks de emails, `source_url`, `sub_icp`, `copy_variant`, `Review`, `needs_manual_review`, duplicados, personalizacion, separacion Canarias/Espana y CRM/GWS.
- `STOP_CONDITIONS.md` incluye stops por ruido, bloqueo, datos dudosos, exceso de Review, falta de emails, datos personales, mezcla territorial, rutas historicas y QA fallido.
- `ROUND_STATUS.md` lista Rondas 1-5, enrichment y manual review.
- `ERRORS_AND_BLOCKERS.md` queda inicializado sin errores de ejecucion.
- `FINAL_SUMMARY.md` deja claro que no se ejecuto scraping ni se crearon datasets finales.
- Se ejecuta `git diff --check`.
- Se verifica que no se crearon nuevos `organizations_clean.csv` ni `contacts_clean.csv`.

## Riesgos

- Una futura `/goal` puede procesar fuentes de alto volumen sin limites si no sigue este controlador.
- Ronda 2 puede introducir ruido si se ejecuta antes de cerrar Ronda 1.
- Espana V2 puede mezclarse con Canarias si no se mantiene ruta separada.
- Datos personales publicados requieren revision humana antes de uso comercial.

## Unknowns

- `Unknown`: volumen real extraido por fuente hasta ejecutar scraping.
- `Unknown`: tasa real de `Review` por fuente.
- `Unknown`: disponibilidad real de emails trazables en cada directorio.
