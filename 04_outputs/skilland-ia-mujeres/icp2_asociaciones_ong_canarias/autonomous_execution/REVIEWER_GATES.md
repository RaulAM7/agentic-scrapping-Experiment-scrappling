# REVIEWER_GATES - ICP2 Autonomous Execution

Fecha inicial: 2026-06-13

## Objetivo

El reviewer interno evita que una futura `/goal` cierre una fuente, una ronda o un dataset sin controles minimos de seguridad, trazabilidad y separacion territorial.

## Estados de reviewer

- `PASS`: cumple todos los gates criticos.
- `PASS_WITH_WARNINGS`: cumple gates criticos pero deja gaps documentados.
- `FAIL`: incumple uno o mas gates criticos; parar y pedir revision humana.

## Gate por fuente

Ejecutar al terminar cada fuente.

Checklist critico:

- [ ] La fuente procesada coincide con la ronda autorizada.
- [ ] La fuente conserva `source_url` en cada registro.
- [ ] No se crearon emails inventados.
- [ ] No se dedujeron emails por patron.
- [ ] No se inventaron cargos, nombres, actividad ni senales de encaje.
- [ ] Los contactos personales publicados quedan marcados para revision si hay duda.
- [ ] Los registros sin contacto usable quedan `organization_only=true`.
- [ ] `sub_icp` se asigna solo con evidencia.
- [ ] `copy_variant` coincide con `sub_icp`.
- [ ] `personalizacion_1` no afirma nada no publicado.
- [ ] `needs_manual_review=true` se usa ante duda.
- [ ] `quality_flags` documenta riesgos.
- [ ] No se mezclo Canarias con Espana.
- [ ] No se toco CRM/GWS.
- [ ] No se modifico `04_outputs/skilland_ia_mujeres/data_prep/`.

Resultado por fuente:

- PASS si no hay incumplimientos criticos.
- PASS_WITH_WARNINGS si faltan emails, hay organization_only o quedan gaps no criticos.
- FAIL si falta `source_url`, hay inferencias, hay mezcla territorial, hay patrones de email, o se toca ruta prohibida.

## Gate Ronda 1

Ronda 1 solo pasa si:

- [ ] Existen outputs de ronda en ruta permitida.
- [ ] `organizations_clean.csv` existe o se justifica formalmente que no hubo datos suficientes.
- [ ] `contacts_clean.csv` existe o se justifica formalmente que no hubo contactos trazables.
- [ ] Cada fila tiene `source_url`.
- [ ] Todas las filas tienen valores fijos:
  - `business_line = SkilLand IA Mujeres`
  - `campaign = IA Mujeres 2026`
  - `macro_icp = asociaciones_ong_mujeres_inclusion_tech`
  - `icp_segment = ICP2 - Asociaciones/ONG - Mujeres e Inclusion Tech`
- [ ] `sub_icp` y `copy_variant` coinciden.
- [ ] `priority=Review` queda fuera de cualquier envio.
- [ ] `needs_manual_review=true` queda fuera de cualquier envio.
- [ ] `duplicate_possible=true` esta marcado y no se promociona sin resolver.
- [ ] `personalizacion_1` es segura o queda vacia.
- [ ] Existe `data_quality_report.md`.
- [ ] Existe `gaps_and_manual_review.md`.
- [ ] Existe `reviewer_report.md`.
- [ ] `git diff --check` pasa.

Umbrales Ronda 1:

- FAIL si cualquier fila carece de `source_url`.
- FAIL si se detecta email deducido.
- FAIL si se mezclan entidades Espana V2.
- FAIL si `Review` supera 40% de registros conservados.
- PASS_WITH_WARNINGS si hay pocos contactos pero registros trazables `organization_only`.

## Gate Ronda 2

Ronda 2 solo puede empezar si Ronda 1 paso gate.

Ronda 2 solo pasa si:

- [ ] Dedupe contra Ronda 1 ejecutado.
- [ ] Registros de volumen sin contacto estan en `organization_only.csv`.
- [ ] Registros dudosos estan en `manual_review.csv`.
- [ ] No se asigna `mujeres_igualdad_steam` por keyword ambigua.
- [ ] Registros sin web/contacto no van a CRM.
- [ ] Ruido documentado por fuente.
- [ ] Cada fila tiene `source_url`.
- [ ] No se contamina Ronda 1.

Umbrales Ronda 2:

- FAIL si no existe canon Ronda 1.
- FAIL si duplicados R1/R2 no estan marcados.
- FAIL si `Review` supera 50% de candidatos filtrados.
- FAIL si una fuente de volumen introduce mas de 50% ruido en muestra.
- PASS_WITH_WARNINGS si el volumen es util pero mayoritariamente `organization_only`.

## Gate Espana V2 backlog

Permitido solo planning/backlog, sin scraping.

Checklist:

- [ ] Ruta separada `icp2_asociaciones_ong_espana_v2/planning_backlog/`.
- [ ] No se crean CSVs de extraccion Espana.
- [ ] No se mezcla con Canarias.
- [ ] Fuentes Ronda 3/4/5 quedan como backlog.
- [ ] CCAA quedan comunidad por comunidad.

FAIL si se extraen registros Espana o se mezclan con Canarias.

## Gate CRM/GWS

Debe ser siempre PASS porque no se toca CRM/GWS.

FAIL inmediato si:

- se crea importacion CRM;
- se toca repo CRM;
- se crea workflow;
- se toca GWS;
- se preparan envios;
- se generan drafts de email.

## Gate de rutas

Permitidas:

- `04_outputs/skilland-ia-mujeres/icp2_asociaciones_ong_canarias/autonomous_execution/`
- `04_outputs/skilland-ia-mujeres/icp2_asociaciones_ong_canarias/ronda_1_canarias_alta_calidad/`
- `04_outputs/skilland-ia-mujeres/icp2_asociaciones_ong_canarias/ronda_2_canarias_volumen/`
- `04_outputs/skilland-ia-mujeres/icp2_asociaciones_ong_espana_v2/planning_backlog/`

Prohibida:

- `04_outputs/skilland_ia_mujeres/data_prep/`

FAIL si se modifica una ruta prohibida.

## Reporte obligatorio

Cada `reviewer_report.md` debe incluir:

- total organizaciones;
- total contactos;
- total `organization_only`;
- total `manual_review`;
- total `duplicate_possible`;
- total sin email;
- total con contacto nominal;
- fuentes fallidas;
- gates PASS/WARN/FAIL;
- decision: continue, continue_with_warnings, stop_needs_human_review.
