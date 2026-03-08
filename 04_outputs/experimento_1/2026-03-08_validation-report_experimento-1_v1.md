# Validation Report - Experimento 1 Scrapling (Email-First)

> Fecha: 2026-03-08
> Version: v1
> Scope: validacion formal de la iteracion `experimento_1`
> Stack validado: Scrapling via API Python

## Resumen ejecutivo

El Experimento 1 queda **validado** como iteracion email-first util y operable dentro del stack actual.

Lo que queda validado:
- `AAFC` funciona como fuente sectorial escalable
- `google_basic` funciona end-to-end con Scrapling si se escala en modo curado
- el dataset final distingue email real vs canal alternativo
- la trazabilidad `query -> fuente -> registro` queda preservada
- el output ya es accionable para emailing, no solo para research

Lo que no queda validado:
- `google_maps` como carril operativo
- estabilidad de `google_basic` en corridas largas sin curacion posterior
- uplift exacto de email yield frente a Experimento 0 por falta de metrica homologa

## Validacion contra criterios de aceptacion

| Criterio | Estado | Evidencia | Lectura |
|---|---|---|---|
| Existe data contract estable para la iteracion | `PASS` | Plan maestro y datasets de Fase 3-4 | Los campos P0/P1 y los cierres de canal/fuente se mantuvieron |
| El mapping ICP-driven paso por checkpoint antes del discovery | `PASS` | Checkpoint 1 aprobado y source-map ejecutado despues | El discovery no se lanzo a ciegas |
| Los tres carriles se analizaron con logica distinta | `PASS` | `google_basic`, `google_maps`, `specialized_directory` separados en source-map | No se mezclaron como una sola fuente |
| Ninguna fuente escala sin gates de contactabilidad y calidad | `PASS` | `AAFC` y `google_basic curated` pasan; `google_maps` queda fuera | La disciplina de gates se mantuvo |
| El dataset final distingue email real de canal alternativo | `PASS` | consolidado: `98` emails reales y `3` canales alternativos | El objetivo email-first no se diluye |
| El dataset final conserva trazabilidad y ranking | `PASS` | consolidado con `source_query`, `source_name`, `contactability_score`, `icp_score` | El output es usable para activacion |
| Comparativa explicita con Experimento 0 | `PASS` | evaluation report de Fase 5 | El cierre ya responde mejora, rentabilidad y gaps |

## Validacion por fuente

### 1. `AAFC - Despachos Profesionales`

Estado: `PASS`

Metricas validadas:
- `70` registros escalados
- `100%` email real
- `0%` ruido
- `0%` duplicados
- `source_quality_score=95`
- `gate_pass=True`

Lectura:
- es la mejor fuente por limpieza y estabilidad
- su debilidad no es el contacto, sino la falta de `website_url` en muchos registros

### 2. `google_basic`

Estado: `PASS`, con restriccion

Validacion tecnica:
- Scrapling logra discovery live en Google con `StealthySession`
- el raw live produjo `47` registros
- el curado comercial deja `31` registros utiles

Metricas validadas del curado:
- `90.3%` email real
- `0%` ruido
- `0%` duplicados
- `source_quality_score=95`
- `gate_pass=True`

Restriccion validada:
- el raw live no debe escalarse tal cual
- la unidad operativa valida es `google_basic curated business-only`

### 3. `google_maps`

Estado: `WATCH`

Lectura:
- no queda descartado
- no existe validacion suficiente para meterlo en el escalado actual
- requiere microvalidacion dedicada en siguiente iteracion

## Validacion del dataset final

Dataset consolidado:
- total: `101`
- emails reales: `98`
- canales alternativos: `3`
- overlaps en consolidacion: `0`

Composicion:
- `AAFC`: `70`
- `google_basic curated`: `31`

Valor de negocio validado:
- ya permite priorizar outreach
- ya permite separar volumen limpio vs enrichment comercial
- ya permite decidir por fuente y por carril

## Validacion comparativa frente a Experimento 0

Lo validado:
- mejora clara de accionabilidad comercial
- reduccion fuerte de dependencia del directorio generalista
- paso de research util a dataset P0 contactable

Lo no homologable:
- `% email real` exacto contra E0
- porque E0 no instrumentaba el email como salida principal

## Riesgos residuales

- `google_basic` puede degradarse por variabilidad de SERP o bloqueo
- el curado comercial de `google_basic` no debe relajarse
- `AAFC` sigue necesitando enrichment adicional si se quiere mas contexto de web propia

## Decision final de validacion

Decision: **VALIDADO CON CONDICIONES**

Condiciones:
1. Escalar `AAFC` sin reservas dentro del stack actual.
2. Escalar `google_basic` solo en modo curado.
3. Mantener `google_maps` fuera del bulk hasta validacion especifica.
4. Mantener Scrapling via API Python como canal oficial del experimento.
