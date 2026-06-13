# RUNBOOK - ICP2 Autonomous Execution Controller

Fecha: 2026-06-13

## Proposito

Este runbook controla una futura ejecucion `/goal` de ICP2 con autonomia limitada y gates internos fuertes.

No ejecuta scraping por si mismo. Define como debe trabajar una futura sesion larga sin supervison continua.

## Decision de autonomia

Opcion recomendada: **Opcion C**.

La futura `/goal` puede ejecutar:

1. Ronda 1 - Canarias alta calidad.
2. Reviewer interno y QA.
3. Ronda 2 - Canarias volumen solo si Ronda 1 pasa gates.
4. Preparacion de backlog Espana V2 sin scraping nacional.

No debe ejecutar todas las rondas. Rondas 3, 4 y 5 quedan bloqueadas para ejecucion posterior con aprobacion humana.

## Inputs obligatorios

Leer antes de ejecutar:

- `04_outputs/skilland-ia-mujeres/icp2_asociaciones_ong_canarias/exploitation_plan/README.md`
- `04_outputs/skilland-ia-mujeres/icp2_asociaciones_ong_canarias/exploitation_plan/exploitation_master_plan.md`
- `04_outputs/skilland-ia-mujeres/icp2_asociaciones_ong_canarias/exploitation_plan/rounds_execution_plan.md`
- `04_outputs/skilland-ia-mujeres/icp2_asociaciones_ong_canarias/exploitation_plan/source_exploitation_playbook.md`
- `04_outputs/skilland-ia-mujeres/icp2_asociaciones_ong_canarias/exploitation_plan/data_contracts_and_quality_gates.md`
- `04_outputs/skilland-ia-mujeres/icp2_asociaciones_ong_canarias/exploitation_plan/dedupe_and_enrichment_strategy.md`
- `04_outputs/skilland-ia-mujeres/icp2_asociaciones_ong_canarias/exploitation_plan/crm_handoff_planning.md`
- `04_outputs/skilland-ia-mujeres/icp2_asociaciones_ong_canarias/source_discovery/source_inventory.csv`
- `04_outputs/skilland-ia-mujeres/icp2_asociaciones_ong_canarias/source_discovery/next_phase_recommendation.md`

## Rutas permitidas

Control autonomo:

- `04_outputs/skilland-ia-mujeres/icp2_asociaciones_ong_canarias/autonomous_execution/`

Ronda 1:

- `04_outputs/skilland-ia-mujeres/icp2_asociaciones_ong_canarias/ronda_1_canarias_alta_calidad/`

Ronda 2:

- `04_outputs/skilland-ia-mujeres/icp2_asociaciones_ong_canarias/ronda_2_canarias_volumen/`

Backlog Espana V2 sin extraccion:

- `04_outputs/skilland-ia-mujeres/icp2_asociaciones_ong_espana_v2/planning_backlog/`

## Rutas prohibidas

No tocar:

- `04_outputs/skilland_ia_mujeres/data_prep/`
- cualquier ruta CRM;
- cualquier ruta GWS;
- otros repositorios.

## Outputs futuros por ronda

Cada ronda ejecutada debe crear:

- `README.md`
- `source_notes.md`
- `extraction_log.md`
- `data_quality_report.md`
- `gaps_and_manual_review.md`
- `reviewer_report.md`
- `data_prep/organizations_clean.csv`
- `data_prep/contacts_clean.csv`
- `data_prep/organization_only.csv`
- `data_prep/manual_review.csv`
- `data_prep/rejected_or_deferred.csv`

Nota: esta fase de controller no crea esos CSVs. Solo una futura `/goal` aprobada puede crearlos en las rutas nuevas de ronda.

## Secuencia obligatoria

1. Verificar que el repo esta en ruta correcta.
2. Verificar que no se trabajara en `04_outputs/skilland_ia_mujeres/data_prep/`.
3. Actualizar `STATE.md` a `running_round_1`.
4. Ejecutar Ronda 1 fuente por fuente.
5. Tras cada fuente, actualizar:
   - `STATE.md`
   - `ROUND_STATUS.md`
   - `EXECUTION_LOG.md`
   - `ERRORS_AND_BLOCKERS.md` si aplica.
6. Ejecutar reviewer interno de Ronda 1.
7. Si Ronda 1 falla gates, parar.
8. Si Ronda 1 pasa gates, ejecutar Ronda 2.
9. Ejecutar dedupe Ronda 2 contra Ronda 1.
10. Ejecutar reviewer interno de Ronda 2.
11. Crear backlog Espana V2 sin scraping.
12. Actualizar `FINAL_SUMMARY.md`.
13. Ejecutar QA final.

## Ronda 1 - fuentes permitidas

- ICI - Asociaciones y colectivos de mujeres.
- Tenerife Violeta - Entidades comprometidas.
- Tenerife Isla Solidaria - Asociaciones.
- Red Anagos.
- EAPN Canarias - Red de entidades.
- Plena Inclusion Canarias - Entidades.
- Coordinadora ONGD Canarias.

## Ronda 2 - fuentes permitidas

Solo si Ronda 1 pasa gates:

- Datos Abiertos - Asociaciones de Canarias.
- Datos Abiertos - Fundaciones Canarias.
- Registro Regional de Entidades Colaboradoras de Servicios Sociales Canarias.
- La Palma Smart - Directorio de Voluntariado.
- Gobierno de Canarias - Voluntariado.

## Espana V2

Permitido:

- crear backlog/planning;
- preparar rutas;
- documentar fuentes;
- no extraer.

Prohibido:

- scraping nacional;
- crear CSVs Espana V2;
- mezclar Espana con Canarias.

## Limites de crawling y extraccion

Limites por defecto:

- No crawling recursivo.
- Maximo 1 pagina de listado + paginas de detalle necesarias por fuente.
- Enriquecimiento web oficial limitado a home, contacto, quienes somos/equipo, transparencia/memoria y programas.
- Maximo 3 paginas de enriquecimiento por organizacion.
- Si una fuente requiere mas profundidad, marcar `manual_review`.
- No intentar saltar bloqueos, captchas, logins ni rate limits.
- No usar fuentes privadas ni redes sociales cerradas.

Limites de volumen:

- Ronda 1: procesar directorios completos si son pequenos; parar si una fuente supera 300 entidades antes de filtros.
- Ronda 2 CSV: se puede leer el CSV completo, pero solo se exportan candidatos filtrados ICP2.
- Ronda 2 enrichment: maximo 100 organizaciones enriquecidas por fuente en una corrida autonoma.
- Si se alcanza limite, dejar remanente en backlog.

## Politica de emails

Permitido:

- emails publicados en fuente oficial;
- emails genericos institucionales;
- formularios publicados;
- emails de area si estan publicados.

Prohibido:

- deducir emails por patron;
- generar emails;
- usar emails no publicados;
- usar emails de terceros ambiguos;
- usar datos personales sin fuente clara.

## Reviewer interno

El reviewer interno debe cerrar cada fuente y cada ronda. Debe producir `reviewer_report.md` y actualizar `REVIEWER_GATES.md` con PASS, PASS_WITH_WARNINGS o FAIL.

## Estados permitidos

- `planned_not_started`
- `running_round_1`
- `reviewing_round_1`
- `blocked_round_1`
- `running_round_2`
- `reviewing_round_2`
- `blocked_round_2`
- `preparing_spain_v2_backlog`
- `completed_canarias_v1`
- `stopped_needs_human_review`

## QA final obligatorio

Antes de cerrar futura `/goal`:

- Ejecutar `git diff --check`.
- Verificar que no se modifico `04_outputs/skilland_ia_mujeres/data_prep/`.
- Verificar que no se toco CRM/GWS.
- Verificar que cada CSV nuevo esta en ruta de ronda permitida.
- Verificar que todas las filas tienen `source_url`.
- Verificar que `Review` y `needs_manual_review=true` quedan fuera de envio.
- Verificar que no se inventaron emails, cargos, personas ni actividad.
- Verificar que Canarias/Espana estan separados.

## Prompt recomendado para `/goal`

```text
/goal

Ejecuta autonomia segura ICP2 Canarias V1 segun:
04_outputs/skilland-ia-mujeres/icp2_asociaciones_ong_canarias/autonomous_execution/RUNBOOK.md

Alcance:
- Ejecutar Ronda 1 Canarias alta calidad.
- Ejecutar Ronda 2 Canarias volumen solo si Ronda 1 pasa reviewer gates.
- Preparar Espana V2 solo como backlog/planning.

No tocar:
- 04_outputs/skilland_ia_mujeres/data_prep/
- CRM
- GWS
- workflows
- envios

Reglas:
- No inventar emails, cargos, nombres, actividad ni senales de encaje.
- No deducir emails por patron.
- Conservar source_url.
- Separar Canarias V1 de Espana V2.
- Actualizar STATE.md y EXECUTION_LOG.md tras cada fuente.
- Parar si se activa cualquier stop condition.
```
