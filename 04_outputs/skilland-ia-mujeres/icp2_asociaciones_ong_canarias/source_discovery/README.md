# ICP2 Source Discovery - Canarias V1 + Espana V2

Fecha: 2026-06-12

## Que es esta fase

Esta carpeta documenta una fase amplia de `Source Discovery` para el nuevo ICP2 de SkilLand IA Mujeres:

`ICP2 - Asociaciones / ONG - Mujeres e Inclusion Tech`

El objetivo no es crear leads finales. El objetivo es mapear y evaluar caladeros, fuentes, listados, registros y directorios para decidir donde conviene hacer extraccion en la siguiente fase.

## Que es ICP2

ICP2 amplia el funnel IA Mujeres hacia entidades sociales, asociaciones, fundaciones y ONG que trabajan con mujeres, igualdad, talento femenino, STEAM, inclusion digital, empleabilidad, formacion, juventud, migracion, vulnerabilidad, emprendimiento, desarrollo comunitario e innovacion social.

Mantiene:

- `business_line = SkilLand IA Mujeres`
- `campaign = IA Mujeres 2026`
- el mismo buyer journey, estados de funnel, secuencia, seguimiento, metricas y handoff CRM/GWS que IA Mujeres.

Diferencia:

- `macro_icp`
- `sub_icp`
- `copy_variant`
- `priority`
- `source_confidence`
- `high_confidence`
- `personalizacion_1`
- criterios de calidad/fuente
- revision humana obligatoria

## Canarias V1 vs Espana V2

Canarias V1 es el frente operativo inmediato. Evalua fuentes canarias con suficiente detalle para decidir una extraccion controlada posterior.

Espana V2 es un mapa nacional, sectorial y autonomico para escalado futuro. No mezcla leads nacionales con Canarias y no prepara una extraccion masiva inmediata.

## Archivos

- `source_inventory.csv`: inventario fuente a fuente con volumen, calidad outbound, esfuerzo, prioridad, ronda recomendada y fase recomendada.
- `source_discovery_report.md`: lectura ejecutiva de caladeros canarios, nacionales y autonomicos.
- `source_evaluation_matrix.md`: clasificacion por cuadrantes de volumen y calidad outbound, mas enriquecimiento, manual review y descartes.
- `next_phase_recommendation.md`: estrategia por rondas para ejecutar la siguiente fase.

## Que no hace

Esta fase no crea:

- `organizations_clean.csv`
- `contacts_clean.csv`
- leads finales
- importaciones CRM
- workflows
- envios
- GWS
- scraping masivo final

Tampoco inventa emails, cargos, nombres, actividad, senales de encaje ni foco de mujeres. No deduce emails por patron.

## Como usar estos entregables

Usar `source_inventory.csv` para seleccionar fuentes por `extraction_priority`, `recommended_round` y `recommended_phase`.

Usar `source_evaluation_matrix.md` para comparar volumen y calidad outbound sin caer en una lista corta arbitraria.

Usar `next_phase_recommendation.md` como plan operativo para la siguiente fase: empezar por Canarias alta calidad, seguir por Canarias volumen, y dejar Espana V2 como escalado nacional/autonomico planificado.
