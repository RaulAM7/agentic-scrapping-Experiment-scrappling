# ROUND_STATUS - ICP2 Autonomous Execution

Fecha inicial: 2026-06-13

## Estado por ronda

| Ronda | Estado | Permitida en proxima `/goal` | Gate para avanzar | Notas |
|---|---|---:|---|---|
| Ronda 1 - Canarias alta calidad | planned_not_started | yes | reviewer PASS o PASS_WITH_WARNINGS sin errores criticos | Primera ronda obligatoria. |
| Ronda 2 - Canarias volumen | blocked_until_round_1_passes | conditional | Ronda 1 canonizada, deduplicada y QA PASS | No contaminar Ronda 1. |
| Ronda 3 - Espana nacional alta calidad | backlog_only | no | aprobacion humana posterior | Solo preparar planning_backlog. |
| Ronda 4 - Espana nacional alto volumen | backlog_only | no | aprobacion humana posterior | Alto ruido; no outbound directo. |
| Ronda 5 - CCAA / escalado territorial | backlog_only | no | aprobacion humana por CCAA | Comunidad por comunidad. |
| Enriquecimiento | conditional | yes, solo sobre R1/R2 | fuente primaria existente y evidencia trazable | No crea contactos por si solo. |
| Manual review / descartes | planned | yes, documentacion | no aplica | No exportar a CRM. |

## Ronda 1 fuentes

| Fuente | Estado | Accion futura |
|---|---|---|
| ICI - Asociaciones y colectivos de mujeres | planned_not_started | extract_controlled |
| Tenerife Violeta - Entidades comprometidas | planned_not_started | extract_controlled |
| Tenerife Isla Solidaria - Asociaciones | planned_not_started | extract_controlled |
| Red Anagos | planned_not_started | extract_controlled |
| EAPN Canarias - Red de entidades | planned_not_started | extract_controlled |
| Plena Inclusion Canarias - Entidades | planned_not_started | extract_controlled |
| Coordinadora ONGD Canarias | planned_not_started | extract_controlled |

## Ronda 2 fuentes

| Fuente | Estado | Accion futura |
|---|---|---|
| Datos Abiertos - Asociaciones de Canarias | blocked_until_round_1_passes | filter_then_extract |
| Datos Abiertos - Fundaciones Canarias | blocked_until_round_1_passes | filter_then_extract |
| Registro Regional de Entidades Colaboradoras de Servicios Sociales Canarias | blocked_until_round_1_passes | extract_controlled |
| La Palma Smart - Directorio de Voluntariado | blocked_until_round_1_passes | extract_controlled |
| Gobierno de Canarias - Voluntariado | blocked_until_round_1_passes | extract_controlled |

## Espana V2

| Bloque | Estado | Accion futura |
|---|---|---|
| Ronda 3 - alta calidad | backlog_only | prepare_planning_backlog |
| Ronda 4 - alto volumen | backlog_only | prepare_planning_backlog |
| Ronda 5 - CCAA | backlog_only | prepare_planning_backlog_by_ccaa |
