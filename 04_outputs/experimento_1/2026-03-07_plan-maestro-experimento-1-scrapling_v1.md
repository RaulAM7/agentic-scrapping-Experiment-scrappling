# Plan Maestro - Experimento 1 Scrapling (Email-First)

> Fecha: 2026-03-07
> Version: v1
> Estado: Fase 0 cerrada; Fase 1 propuesta lista para Checkpoint 1
> Stack operativo: Scrapling via API Python

## 1. North Star

- Objetivo: pasar de research util a dataset accionable para emailing sin salir del stack Scrapling
- Unidad de exito: registro contactable y trazable, no solo empresa encontrada
- Benchmark/control: Paginas Amarillas queda como referencia comparativa, no como fuente principal de diseño
- Regla de lectura del experimento: primero contacto, despues enriquecimiento

## 2. Lo que arrastramos del Experimento 0

- La API Python de Scrapling si funciono como nucleo operativo
- CLI y MCP quedaron por detras; no entran en el core de esta iteracion
- La ausencia de web propia fue una senal ICP real
- Google Maps quedo sin validar; se trata como carril de alto potencial y alto riesgo
- El discovery previo estuvo poco disenado y mezclo logicas de fuente distintas
- La dependencia de directorio generalista degrado la calidad comercial del output

## 3. Alcance y no alcance

### Alcance

- Iteracion acotada, fase por fase
- Carriles cerrados: `google_basic`, `google_maps`, `specialized_directory`
- Reporte siempre separado entre email real y canal alternativo
- Carril C limitado a colegios, asociaciones y directorios sectoriales del vertical fiscal-contable en Canarias

### No alcance

- LinkedIn como carril activo
- Proxies complejos
- Sistema final de outreach
- Automatizacion grande antes de validar piloto

## 4. Definiciones operativas cerradas

### 4.1 Email util

Para piloto y escalado, "email util" se interpreta de forma flexible solo para no perder cobertura inicial:

- `email`: direccion real de correo, directa o generica
- `form`: formulario de contacto verificable
- `other_direct`: canal directo distinto de email, por ejemplo WhatsApp o telefono visible
- `none`: no existe via de contacto accionable

El reporte nunca mezcla `email` con `form` u `other_direct`. Email real se reporta siempre por separado.

### 4.2 P0 contactable

Un registro cuenta como `P0 contactable` si `contact_channel_type` es `email`, `form` u `other_direct`.

### 4.3 Carriles

| source_lane | Objetivo | Output esperado |
|-------------|----------|-----------------|
| `google_basic` | Descubrir webs propias, paginas de contacto y listados organicos | Email visible, pagina contacto, website propia |
| `google_maps` | Validar categoria local y detectar web enlazada o canal directo | Categoria, localizacion, web enlazada, telefono u otro canal |
| `specialized_directory` | Encontrar actores del vertical con mayor densidad ICP | Directorio sectorial, colegio, asociacion, email o canal publicado |

## 5. Data Contract congelado

### 5.1 Campos P0 obligatorios

| Campo | Tipo | Regla |
|-------|------|-------|
| `company_name` | `string` | Nombre comercial o profesional normalizado |
| `source_lane` | `enum` | `google_basic` \| `google_maps` \| `specialized_directory` |
| `source_name` | `string` | Nombre legible de la fuente concreta |
| `source_url` | `string` | URL absoluta de la pagina origen del registro |
| `query_cluster` | `string` | ID estable del pack o cluster de busqueda |
| `geography` | `string` | Formato normalizado `municipio|isla` o `capital|isla` |
| `contact_channel_type` | `enum` | `email` \| `form` \| `other_direct` \| `none` |
| `email_or_channel` | `string` | Email, URL de formulario, telefono/canal o literal `none` |
| `website_url` | `string` | Dominio o URL propia; si no existe, `Unknown` |
| `services` | `array[string]` | Servicios detectados y normalizados |
| `icp_signals` | `array[string]` | Senales ICP observables capturadas en la extraccion |
| `source_quality_score` | `integer` | `0-100`, heredado de la evaluacion de la fuente |
| `contactability_score` | `integer` | `0-100`, calculado a nivel registro |
| `dedupe_key` | `string` | Clave canonica de deduplicacion |

### 5.2 Campos P1 recomendados

| Campo | Tipo | Uso |
|-------|------|-----|
| `source_query` | `string` | Query exacta usada para encontrar el registro |
| `source_rank` | `integer` | Posicion en SERP, mapa o directorio |
| `contact_page_url` | `string` | URL de la pagina de contacto si difiere de `source_url` |
| `company_phone` | `string` | Telefono visible normalizado |
| `postal_address` | `string` | Direccion visible si existe |
| `role_hint` | `string` | Titular, economista, gestor, despacho, Unknown |
| `icp_score` | `integer` | `0-100`, scoring de ajuste al ICP para ranking final |
| `evidence_snippet` | `string` | Texto corto que justifica el canal o la senal ICP |
| `scrapling_fetcher` | `string` | `Fetcher`, `DynamicFetcher`, `StealthyFetcher`, Unknown |
| `extracted_at_utc` | `string` | Timestamp ISO-8601 |

### 5.3 Semantica de campos criticos

- `services` debe quedarse en vocabulario util para outreach: `fiscal`, `contable`, `laboral`, `autonomos`, `pymes`, `sociedades`, `igic`, `renta`, `mercantil`, `subvenciones`
- `icp_signals` debe recoger solo senales accionables: `no_website`, `web_basica`, `contact_page`, `direct_email`, `form_only`, `colegiado`, `capital_insular`, `igic`, `autonomos`, `pymes`, `sociedades`
- `website_url` no puede apuntar a una ficha de directorio salvo que no exista otra web; en ese caso el valor correcto es `Unknown`

## 6. Deduplicacion y merge

### 6.1 Normalizacion

Antes de generar `dedupe_key`:

1. `company_name`: lowercase, trim, colapsar espacios, eliminar puntuacion trivial y sufijos legales frecuentes (`sl`, `s.l.`, `slp`, `scp`, `cb`, `sa`) si aparecen al final
2. `website_url`: lowercase, quitar `http://`, `https://`, `www.` y slash final
3. `email_or_channel`:
   - email: lowercase y sin `mailto:`
   - form: host + path sin querystring
   - other_direct: solo digitos para telefono o URL canonica del canal
   - none: literal `none`
4. `geography`: lowercase, formato `municipio|isla`

### 6.2 Regla de clave

`dedupe_key = company_slug + "|" + geography_slug + "|" + contact_channel_type + "|" + channel_slug`

Fallback cuando `contact_channel_type = none`:

`dedupe_key = company_slug + "|" + geography_slug + "|none|" + website_slug_or_source_name`

### 6.3 Politica de merge

Si dos registros chocan por `dedupe_key`, se conserva el mejor segun este orden:

1. Mayor `contactability_score`
2. `email` por encima de `form`, `other_direct` y `none`
3. `website_url` propia por encima de directorio o `Unknown`
4. Mayor `source_quality_score`
5. Mayor numero de `icp_signals`

## 7. Scorecard de fuentes

### 7.1 Gate de paso a piloto y escalado

Cada fuente necesita una muestra de 10-15 registros y solo pasa si cumple todos estos minimos:

- `>= 30%` de cobertura `P0 contactable`
- `<= 25%` de ruido o duplicados
- `source_quality_score >= 60/100`
- Viabilidad integra con Scrapling via API Python

### 7.2 Rubrica de `source_quality_score`

| Componente | Peso | Pregunta de evaluacion |
|------------|------|------------------------|
| P0/contact yield | 30 | Cuantos registros terminan con contacto accionable |
| Densidad ICP | 20 | Cuantos registros encajan con el vertical y la geografia objetivo |
| Calidad/precision | 15 | Que tan correctos y utilizables son nombre, canal y servicios |
| Ruido/duplicados | 10 | Cuanto trabajo de limpieza genera la fuente |
| Viabilidad tecnica con Scrapling | 10 | Que tan estable es la extraccion sin salir de Scrapling |
| Coste operativo | 10 | Tiempo, paginacion y complejidad por registro util |
| Riesgo operativo/legal | 5 | Riesgo de bloqueo, ambiguedad legal o fragilidad operacional |

### 7.3 Escala de `contactability_score`

| Rango | Lectura operativa |
|-------|-------------------|
| `90-100` | Email directo o nominal en dominio propio |
| `70-89` | Email generico util en dominio propio |
| `40-69` | Formulario verificable o canal directo alternativo util |
| `1-39` | Canal ambiguo, indirecto o de baja confianza |
| `0` | Sin canal accionable |

### 7.4 Hipotesis inicial por carril

| Carril/Fuente | Yield de email | Densidad ICP | Riesgo tecnico | Rol en experimento |
|---------------|----------------|--------------|----------------|--------------------|
| `google_basic` | Alto potencial | Medio-alto | Medio | Carril prioritario para encontrar webs propias y contacto visible |
| `google_maps` | Medio potencial | Alto | Alto | Carril de validacion local y enlace hacia web/canal |
| `specialized_directory` | Medio | Alto | Medio-bajo | Carril de precision vertical y enrichment inicial |
| `Paginas Amarillas` | Bajo | Medio | Bajo | Benchmark/control comparativo, no driver de diseño |

## 8. Roadmap por fases

| Fase | Entregable | Decision gate |
|------|------------|---------------|
| 0. Encadre operativo y data contract | Este documento maestro | Cerrada |
| 1. Smart agentic mapping ICP-driven | Keyword-angle map aprobado | Checkpoint 1 |
| 2. Discovery por carriles separados | Source-map por carril con pass/watch/drop | Checkpoint 2 |
| 3. Piloto email-first acotado | Pilot scorecard + dataset piloto en `05_scratch/experimento_1/` | Checkpoint 3 |
| 4. Escalado controlado | Dataset consolidado + ranking orientado a emailing | Solo fuentes que pasen gates |
| 5. Evaluation report | Comparativa contra Experimento 0 | Cierre del experimento |

## 9. Keyword-angle map ICP-driven

### 9.1 Ejes de busqueda

| Eje | Variantes activas |
|-----|-------------------|
| Servicio | `asesoria fiscal`, `asesoria contable`, `gestoria`, `autonomos`, `pymes`, `sociedades`, `igic` |
| Geografia | `Las Palmas de Gran Canaria`, `Santa Cruz de Tenerife`, `Gran Canaria`, `Telde`, `Arrecife`, `Canarias` |
| Rol/titulo | `asesor fiscal`, `economista`, `gestor administrativo`, `despacho`, `asesoria` |
| Cliente/pain | `autonomos`, `pymes`, `sociedades`, `igic`, `impuestos`, `contabilidad` |
| Operador/intencion | `contacto`, `email`, `inurl:contacto`, `inurl:servicios`, `site:`, busqueda nativa en Maps |

### 9.2 Packs propuestos

| Pack | Carril | Query cluster | Hipotesis |
|------|--------|---------------|-----------|
| `GB-01` | `google_basic` | `gb_core_contact` | Detecta webs propias con pagina de contacto y mejor probabilidad de email visible |
| `GB-02` | `google_basic` | `gb_service_pain` | Fuerza lenguaje mas cercano al ICP y puede sacar paginas de servicios mas accionables |
| `GM-01` | `google_maps` | `gm_local_category` | Sirve para validar categoria local y detectar web enlazada, telefono o formulario |
| `SD-01` | `specialized_directory` | `sd_colegial_sectorial` | Prioriza directorios de precision vertical con mayor autoridad y menor ruido |

### 9.3 Queries por pack

| # | Pack | Query | Por que puede encontrar mejor contacto |
|---|------|-------|----------------------------------------|
| 1 | `GB-01` | `"asesoria fiscal" "Las Palmas de Gran Canaria" "contacto"` | Cruza servicio + capital + intencion de contacto; deberia priorizar paginas propias |
| 2 | `GB-01` | `"asesoria contable" "Santa Cruz de Tenerife" "contacto"` | Replica el patron para la otra capital prioritaria |
| 3 | `GB-01` | `"gestoria" "Gran Canaria" inurl:contacto` | Empuja resultados con URL de contacto ya expuesta |
| 4 | `GB-01` | `"asesoria fiscal contable" Canarias email` | Busca paginas o snippets con correo visible |
| 5 | `GB-02` | `"asesoria autonomos" Canarias "contacto"` | Captura firmas enfocadas en autonomos, pain alineado con el ICP |
| 6 | `GB-02` | `"asesoria pymes" "Las Palmas" inurl:servicios` | Puede sacar paginas de servicios donde suele aparecer CTA o email |
| 7 | `GB-02` | `IGIC asesoria Tenerife contacto` | Mete especificidad Canarias/IGIC para filtrar ruido no local |
| 8 | `GB-02` | `"sociedades" "asesoria fiscal" Canarias email` | Busca lenguaje de servicio util para priorizar despachos mas comerciales |
| 9 | `GM-01` | `asesoria fiscal Las Palmas de Gran Canaria` | Query nativa para Maps centrada en categoria + localidad |
| 10 | `GM-01` | `gestoria Santa Cruz de Tenerife` | Variante de categoria adyacente con alta presencia local |
| 11 | `GM-01` | `asesoria contable Telde` | Testea municipio secundario con menor competencia y posible mejor precision |
| 12 | `GM-01` | `asesoria autonomos Arrecife` | Busca mezcla de nicho + isla menos saturada |
| 13 | `SD-01` | `site:org "colegio de economistas" "Las Palmas" directorio` | Prioriza autoridad colegial con ruido bajo |
| 14 | `SD-01` | `site:org "gestores administrativos" Tenerife directorio` | Busca el equivalente colegial para otra profesion cercana |
| 15 | `SD-01` | `site:org "asesores fiscales" Canarias asociacion` | Abre carril de asociaciones sin caer en directorio generalista |
| 16 | `SD-01` | `"directorio" "asesoria fiscal" Canarias "colegiado"` | Mezcla vertical + senal profesional para encontrar listados sectoriales |

### 9.4 Recomendacion inicial para Checkpoint 1

- Mantener: `GB-01`, `GB-02`, `GM-01`, `SD-01`
- Eliminar: ninguno todavia; no hay evidencia local suficiente para descartar antes del discovery
- Ampliar solo si quieres mas cobertura insular desde el inicio: `La Laguna`, `Puerto del Rosario`, `Vecindario`

No se pasa a Fase 2 hasta recibir feedback explicito sobre estos packs: mantener, eliminar o ampliar.

## 10. Criterios de aceptacion del experimento

- Existe un data contract aprobado antes de scrapear y no cambia durante la iteracion
- El mapping incluye propuestas creativas derivadas del ICP y pasa por checkpoint dialogado antes del discovery
- Los tres carriles se analizan con logicas y metricas distintas
- Ninguna fuente escala sin superar gates de contactabilidad y calidad
- El dataset final distinguira email real frente a canal alternativo y conservara trazabilidad `query -> fuente -> registro`
- El reporte final comparara Experimento 1 contra Experimento 0 en cobertura de contacto, calidad de fuente, ruido y accionabilidad para emailing

## 11. Unknown, riesgos y siguiente paso

### Unknown

- `Unknown`: cobertura real de email directo en `google_basic` frente a formulario/telefono
- `Unknown`: nivel de bloqueo de `google_maps` en ejecucion real con Scrapling sin proxies complejos
- `Unknown`: que directorios sectoriales concretos de Canarias ofreceran mejor equilibrio entre precision y contactabilidad

### Riesgos

- Confundir un canal alternativo con exito email-first
- Volver a sobrerrepresentar fuentes generalistas por comodidad operativa
- Generar demasiados duplicados si `google_basic` y `google_maps` convergen en los mismos negocios

### Siguiente paso inmediato

Cerrar Checkpoint 1 sobre los packs `GB-01`, `GB-02`, `GM-01` y `SD-01`. Con esa aprobacion, la siguiente ejecucion debe producir el `source-map` por carril con shortlist `pass/watch/drop` y preparar el piloto.
