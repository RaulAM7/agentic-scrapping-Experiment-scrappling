# Evaluation Report - Experimento 1 vs Experimento 0

> Fecha: 2026-03-08
> Scope: comparativa de Fase 5 entre el Experimento 0 y el Experimento 1 email-first
> Stack: Scrapling via API Python
> ICP: asesorias fiscales/contables en Canarias

## Resumen ejecutivo

El Experimento 1 mejora de forma clara la accionabilidad comercial respecto al Experimento 0. El cambio no viene de "scrapear mas", sino de redisenar el experimento para producir un dataset contactable y trazable para emailing.

Resultado final de Experimento 1:
- `101` registros consolidados y contactables
- `98` emails reales y `3` canales alternativos
- `AAFC` escalado con `70` registros y `100%` email real
- `google_basic` validado end-to-end con discovery live en Google y `31` registros curados para emailing

Veredicto comparativo:
- **Si** mejoro el yield util de contacto
- **Si** se redujo de forma drastica la dependencia del directorio generalista
- **Si** Scrapling se mantuvo viable como stack unico
- **No del todo** queda resuelto `google_maps`
- **Unknown** el uplift porcentual exacto frente a Experimento 0 en email yield, porque el Experimento 0 no instrumentaba ese dato como metrica principal

## Comparativa directa

| Dimension | Experimento 0 | Experimento 1 | Lectura |
|---|---|---|---|
| Objetivo | research ICP y validacion de fuentes | dataset accionable para emailing | El pivote de objetivo cambia la calidad del output |
| Fuente principal | Paginas Amarillas + Colegio Economistas | `AAFC` + `google_basic` curado | Se pasa de directorio generalista a mezcla de directorio sectorial + web propia |
| Dependencia de directorio generalista | Alta: `137/186` registros raw (`73.7%`) venian de Paginas Amarillas | `0%` en el dataset final escalado | Reduccion material de dependencia |
| Output final | `137` despachos + `49` colegiados + `77` prospectos scored | `101` registros consolidados, todos P0 contactables | E1 produce menos volumen bruto pero mucho mas valor de activacion |
| Web propia visible | En muestra profunda: `0/30` fichas con web propia | `google_basic` aporta `31` registros desde web propia real | Mejora fuerte en trazabilidad y capacidad de enrichment |
| Cobertura de contacto | Telefono/direccion desde PA; email yield no instrumentado | `101/101` contactables, `98/101` email real (`97.0%`) | La comparacion exacta de porcentaje es `Unknown`, pero la utilidad comercial mejora claramente |
| Ruido | Estimacion PA raw: `14/137` off-target (`10.2%`) en directorio generalista | `google_basic` raw trae ruido, pero el dataset curado queda en `0%` ruido y `0%` duplicados | E1 introduce una capa de curacion explicita que E0 no tenia |
| Accionabilidad para emailing | Baja-media; research util, outreach poco directo | Alta; ranking por `contactability_score` e `icp_score` | Este es el cambio mas importante |

## Que mejoro exactamente

### 1. Yield de contacto

En el Experimento 0 el flujo estaba orientado a discovery y scoring ICP. El output principal eran fichas, directorios y señales de mercado. El email no era el centro del contrato de datos y por eso no existe una metrica limpia comparable de `% email real`.

En el Experimento 1:
- `AAFC`: `70/70` con email real
- `google_basic` curado: `28/31` con email real, `2` formularios, `1` canal directo alternativo
- consolidado: `98/101` con email real

Inferencia: el salto de utilidad para outreach es grande, aunque el uplift porcentual exacto frente a E0 quede como `Unknown` por falta de instrumentacion simetrica.

### 2. Calidad de fuente

`AAFC` demuestra el mejor perfil operativo:
- `70` registros
- `100%` email real
- `0%` ruido
- `0%` duplicados
- `source_quality_score=95`

`google_basic` demuestra el mejor perfil comercial por registro:
- `31` registros curados desde web propia
- `90.3%` email real
- `avg_contactability_score=78.7`
- `avg_icp_score=91.6`

Comparativa por rentabilidad con Scrapling:
- **Carril mas rentable operativamente**: `AAFC`
- **Carril mas valioso por calidad y enrichment**: `google_basic` curado

### 3. Reduccion de dependencia del directorio generalista

El Experimento 0 se apoyaba de forma dominante en Paginas Amarillas. Eso dio volumen y estructura, pero tambien:
- mezcla de categorias no ICP
- poca web propia
- poco valor directo para emailing

El Experimento 1 deja Paginas Amarillas como benchmark/control y construye el dataset final sin depender de ella. El cambio es estructural, no cosmetico.

### 4. Accionabilidad real

El Experimento 0 respondia bien a preguntas como:
- donde estan los despachos
- que categorias aparecen
- hay señal de "sin web propia"

El Experimento 1 ya responde a preguntas de activacion:
- a quien escribimos primero
- que email usamos
- que fuente fue mas rentable
- que registros tienen mejor combinacion de ICP + contactabilidad

## Hallazgos por carril

### `specialized_directory`

Es el carril mas robusto del experimento. `AAFC` fue el mejor compromiso entre volumen, limpieza y viabilidad tecnica con Scrapling. Su limitacion es que muchos registros salen sin `website_url`, asi que para enrichment comercial profundo sigue siendo inferior a una web propia.

### `google_basic`

Queda validado tecnicamente. Scrapling puede hacer discovery live en Google usando `StealthySession`, pero el raw live no es suficiente por si solo: la SERP mezcla webs propias con agregadores, institucional y ruido editorial. Por eso la unidad escalable no es el raw, sino el dataset curado.

### `google_maps`

Sigue abierto. No esta descartado, pero tampoco esta validado como carril integral dentro del stack actual. Antes de ampliar el stack, este es uno de los huecos tecnicos mas claros.

## Riesgos y gaps abiertos

- `google_basic` es viable, pero su estabilidad en corridas largas sigue siendo variable
- `google_maps` no queda resuelto en esta iteracion
- `AAFC` da mucho volumen, pero pobre `website_url`
- falta decidir si merece la pena abrir un segundo `specialized_directory`
- algunas comparativas contra E0 solo pueden hacerse por evidencia indirecta, no por metrica homologa

## Conclusion

El Experimento 1 supera al Experimento 0 en lo que importaba para el pivot email-first: contacto util, trazabilidad y accionabilidad comercial.

La lectura final es:
- `AAFC` debe escalarse ya
- `google_basic` debe escalarse tambien, pero solo con curacion comercial explicita
- `google_maps` queda para una validacion posterior
- Scrapling sigue siendo viable como stack unico si se usa via API Python

En otras palabras: el Experimento 0 demostro que Scrapling servia para research ICP; el Experimento 1 demostro que tambien puede llevarnos a un dataset operativo para emailing.

## Propuestas para el siguiente experimento

### 1. Escalado bulk `curated google_basic + AAFC`

Objetivo:
- pasar de validacion controlada a generacion sostenida de volumen util para emailing

Alcance sugerido:
- mantener `AAFC` como carril base de volumen limpio
- mantener `google_basic` solo en modo `curated business-only`
- consolidar ambos carriles en lotes repetibles con dedupe y trazabilidad
- fijar una cadencia de corrida y QA de ruido por lote

Hipotesis:
- la combinacion `AAFC + google_basic curated` puede producir bulk util sin ampliar stack

Gate sugerido:
- mantener `>=90%` de registros P0 contactables
- mantener ruido + duplicados `<=10%` en el dataset curado final
- sostener estabilidad tecnica en varias corridas consecutivas

### 2. Validacion `google_maps`

Objetivo:
- decidir si `google_maps` merece entrar como tercer carril operativo o seguir en `watch`

Alcance sugerido:
- microvalidacion tecnica con Scrapling sobre un set pequeno de fichas
- medir si el carril permite llegar de forma estable a `categoria -> geografia -> web enlazada -> contacto`
- comparar su coste tecnico y su yield contra `google_basic`

Hipotesis:
- `google_maps` puede aportar mejor validacion local y categoria, pero no esta claro que sea mas rentable que `google_basic`

Gate sugerido:
- acceso estable a muestra de fichas sin degradacion severa por bloqueo
- handoff util a web propia o canal directo en una proporcion suficiente para emailing
- mejora real de precision local respecto a `google_basic`
