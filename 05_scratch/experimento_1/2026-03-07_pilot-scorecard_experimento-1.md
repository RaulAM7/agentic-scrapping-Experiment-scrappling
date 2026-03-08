# Pilot Scorecard - Experimento 1

- Fecha: 2026-03-07
- Scope: piloto acotado sobre `google_basic` y `AAFC` usando Scrapling API Python
- Muestra: 12 registros `google_basic` (seeded) + 12 registros `AAFC`

## Resumen

### google_basic_seeded_websites

- Sample size: `12`
- `% P0 contactable`: `100.0`
- `% email real`: `100.0`
- `% canal alternativo`: `0.0`
- `% emails unicos`: `100.0`
- `% ruido`: `0.0`
- `% duplicados`: `0.0`
- `% senales ICP utiles`: `100.0`
- `source_quality_score`: `82`
- Viabilidad integra con Scrapling: `False`
- Gate piloto/escalado: `False`
- Nota: La extraccion de webs funciona con Scrapling, pero la discovery live en Google devuelve 429/sorry.

### AAFC - Despachos Profesionales

- Sample size: `12`
- `% P0 contactable`: `100.0`
- `% email real`: `100.0`
- `% canal alternativo`: `0.0`
- `% emails unicos`: `100.0`
- `% ruido`: `0.0`
- `% duplicados`: `0.0`
- `% senales ICP utiles`: `91.7`
- `source_quality_score`: `93`
- Viabilidad integra con Scrapling: `True`
- Gate piloto/escalado: `True`
- Nota: Fuente extraible con Fetcher en esta muestra piloto.

## Hallazgos clave

- `google_basic` extrae contacto muy bien una vez que entras en la web propia, pero la discovery live en Google sigue bloqueada: status `429` con `DynamicFetcher` y `StealthyFetcher` devolviendo `/sorry`.
- `AAFC` se comporta como la mejor fuente sectorial del piloto: pagina estable, emails visibles y buena densidad fiscal-contable.
- El piloto de `google_basic` es valido para medir contact extraction, no para declarar resuelta la discovery de Google.

## Regla recomendada post-piloto

- `AAFC - Despachos Profesionales`: `PASS` para seguir a escalado controlado.
- `google_basic_seeded_websites`: `WATCH` para escalado. El output comercial es bueno, pero falla la exigencia de viabilidad integra con Scrapling por el bloqueo de Google.

## Unknown y riesgos

- `Unknown`: si Google puede volverse usable con otra estrategia Scrapling sin salir a proxies complejos.
- `Unknown`: cuanto cambia el yield de `google_basic` cuando dejas las semillas curadas y entras en discovery real query-by-query.
- Riesgo: sesgo optimista en `google_basic` porque la muestra entra por seeds ya validadas.
- Riesgo: parte del AAFC puede requerir luego website enrichment externo si quieres web propia y no solo email/telefono.
