# ERRORS_AND_BLOCKERS - ICP2 Autonomous Execution

Fecha inicial: 2026-06-13

## Estado actual

No hay errores de ejecucion. No se ha ejecutado scraping.

## Bloqueos iniciales

| Bloqueo | Estado | Accion |
|---|---|---|
| Ronda 3 Espana alta calidad | blocked_for_future_human_approval | Preparar backlog solamente. |
| Ronda 4 Espana alto volumen | blocked_for_future_human_approval | No ejecutar scraping nacional. |
| Ronda 5 CCAA | blocked_for_future_human_approval | No ejecutar scraping autonomico. |
| CRM | prohibited | No tocar. |
| GWS | prohibited | No tocar. |
| Ruta historica `04_outputs/skilland_ia_mujeres/data_prep/` | prohibited | No modificar. |

## Formato para errores futuros

```text
## YYYY-MM-DD HH:MM - [round] - [source]

- Error type:
- Severity:
- What happened:
- Affected outputs:
- Records affected:
- Stop condition triggered:
- Recovery attempted:
- Decision:
- Human review needed:
```

## Severidades

- `info`: evento documentado, no afecta avance.
- `warning`: avance permitido con reviewer warning.
- `blocker`: fuente se detiene, ronda puede continuar si no contamina.
- `critical`: detener ronda o ejecucion completa.

## Decisiones permitidas

- `continue`
- `continue_with_warning`
- `skip_source`
- `mark_manual_review`
- `pause_round`
- `stop_needs_human_review`
