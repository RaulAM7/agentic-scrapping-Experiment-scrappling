# 001 — Plan Maestro: Experimento de Scraping Inteligente Orientado a ICP

> Documento operativo de referencia. Cada fase se ejecutara por separado desde este mismo hilo.
> Fecha: 2026-03-07

---

## Objetivo del experimento

Evaluar Scrapling como capa de smart scraping dentro de un workflow agentico que parte de un ICP definido y llega hasta hallazgos estructurados y accionables.

La pregunta que este experimento debe responder:

**Puede Scrapling convertirse en una capa de scraping inteligente fiable dentro de un sistema agentico de negocio que va de ICP a activacion comercial?**

---

## Estructura del experimento: 6 fases

### FASE 0 — Setup e instalacion
**Objetivo**: Tener Scrapling funcionando en el repo con todas las dependencias necesarias.

**Tareas**:
1. Crear entorno virtual Python (>=3.10)
2. Instalar Scrapling con extras: `pip install "scrapling[all]"`
3. Instalar browsers: `scrapling install`
4. Verificar instalacion con un fetch trivial (ej: `quotes.toscrape.com`)
5. Documentar: version instalada, tiempo de setup, problemas encontrados, tamano del entorno
6. Configurar MCP server de Scrapling en Claude Code (`claude mcp add`)
7. Actualizar `01_harness/STACK.md` con la info del runtime

**Entregable**: `05_scratch/fase-0_setup-log.md`

**Criterios de exito**:
- [ ] `Fetcher.get()` devuelve pagina correcta
- [ ] `StealthyFetcher.fetch()` funciona con headless
- [ ] MCP server responde desde Claude Code
- [ ] Setup documentado con tiempos y friccion

---

### FASE 1 — Reconocimiento del terreno (Target Discovery)
**Objetivo**: Identificar y catalogar las fuentes de datos publicas relevantes para el ICP (asesorias fiscales/contables en Canarias).

**Tareas**:
1. Mapear fuentes de datos candidatas:
   - Google Maps / Google Business (busqueda: "asesoria fiscal Las Palmas", "gestoria contable Tenerife", etc.)
   - Directorios colegiales: Colegio de Economistas de Las Palmas, Colegio de Gestores Administrativos
   - Paginas Amarillas / QDQ / directorios locales
   - LinkedIn (busquedas de perfiles y empresas)
   - Webs propias de despachos encontrados
2. Para cada fuente evaluar:
   - Accesibilidad (publica, requiere login, tiene API)
   - Tipo de proteccion anti-bot (ninguna, basica, Cloudflare, captcha)
   - Estructura del HTML (estatica vs dinamica)
   - Que datos aporta al ICP (nombre, direccion, telefono, servicios, resenas, tamano)
3. Hacer pruebas rapidas con los tres fetchers de Scrapling (Fetcher, DynamicFetcher, StealthyFetcher) para clasificar cada fuente segun el fetcher optimo
4. Documentar que senales del ICP (bloque 4) son alcanzables desde cada fuente

**Entregable**: `05_scratch/fase-1_reconocimiento-fuentes.md` — mapa de fuentes con clasificacion

**Criterios de exito**:
- [ ] Minimo 3 fuentes de datos identificadas y probadas
- [ ] Cada fuente clasificada por fetcher necesario y datos disponibles
- [ ] Conexion explicita entre fuentes y senales del ICP

---

### FASE 2 — Extraccion estructurada (Data Extraction)
**Objetivo**: Construir scripts de extraccion que obtengan datos reales de despachos profesionales desde las fuentes identificadas.

**Tareas**:
1. Para cada fuente viable de la Fase 1, escribir un script de extraccion:
   - Selector CSS/XPath para los campos clave (nombre, direccion, telefono, servicios, resenas)
   - Manejo de paginacion si aplica
   - Formato de salida: JSON estructurado
2. Probar la feature de adaptive scraping (`auto_save=True`, `adaptive=True`) cambiando selectores para simular cambio de estructura
3. Probar el CLI `scrapling extract` como alternativa rapida sin codigo
4. Evaluar el MCP server: pedirle a Claude que extraiga datos via MCP y comparar con scripts manuales
5. Recopilar datos reales de al menos 20-30 despachos

**Entregable**:
- Scripts en `05_scratch/scripts/`
- Datos extraidos en `05_scratch/data/`
- Log de evaluacion: `05_scratch/fase-2_extraccion-log.md`

**Criterios de exito**:
- [ ] Al menos 20 registros de despachos extraidos con datos estructurados
- [ ] Scripts reproducibles y documentados
- [ ] Evaluacion de adaptive scraping con hallazgos concretos
- [ ] Comparativa MCP vs script manual documentada

---

### FASE 3 — Spider de descubrimiento (Crawl + Discovery)
**Objetivo**: Probar el framework de Spiders para descubrimiento en profundidad — partiendo de un listado de despachos, rastrear sus webs para recopilar senales adicionales del ICP.

**Tareas**:
1. Disenar un Spider que:
   - Parta de los URLs de webs de despachos recopilados en Fase 2
   - Rastree cada web (1-2 niveles de profundidad)
   - Extraiga senales: servicios ofrecidos, equipo/tamano, tecnologia visible, presencia de portal cliente, blog/noticias
2. Usar multi-sesion si alguna web tiene proteccion (sesion HTTP normal + sesion stealth)
3. Probar pause/resume con `crawldir`
4. Probar streaming mode para monitoreo en tiempo real
5. Exportar resultados a JSON/JSONL
6. Evaluar: velocidad, estabilidad, facilidad de desarrollo, calidad de datos

**Entregable**:
- Spider en `05_scratch/scripts/discovery_spider.py`
- Datos en `05_scratch/data/discovery/`
- Log: `05_scratch/fase-3_spider-log.md`

**Criterios de exito**:
- [ ] Spider funcional que rastrea al menos 10 webs de despachos
- [ ] Multi-sesion probada (HTTP + stealth en mismo spider)
- [ ] Pause/resume probado
- [ ] Datos exportados en JSON estructurado

---

### FASE 4 — Scoring y enriquecimiento ICP
**Objetivo**: Aplicar la heuristica de scoring del ICP a los datos recopilados para producir un ranking de prospectos.

**Tareas**:
1. Cruzar los datos extraidos (Fases 2-3) con las senales del ICP (bloque 4 y bloque 6)
2. Asignar puntuacion a cada despacho segun la heuristica de scoring
3. Generar un ranking de prospectos ordenado por puntuacion
4. Identificar patrones: que senales resultaron mas discriminantes? Cuales fueron ruido?
5. Refinar el ICP si los datos sugieren ajustes (usar modo refinamiento de la skill icp-definer)

**Entregable**:
- `04_outputs/2026-XX-XX_icp-prospect-ranking_v1.md` — ranking con justificacion
- Actualizacion del ICP si procede

**Criterios de exito**:
- [ ] Ranking de al menos 15 prospectos con puntuacion
- [ ] Al menos 3 senales del ICP validadas con datos reales
- [ ] Conclusiones sobre que senales funcionan y cuales no

---

### FASE 5 — Evaluacion final y conclusiones
**Objetivo**: Producir el entregable definitivo del experimento — evaluacion completa de Scrapling con recomendacion.

**Tareas**:
1. Compilar hallazgos de todas las fases en un informe estructurado
2. Evaluar Scrapling segun los criterios del WHAT-IS-THIS-REPO:
   - **Friccion de adopcion**: dificultad de instalacion y setup
   - **Claridad del modelo mental**: facilidad para entender como funciona
   - **Flexibilidad**: adaptabilidad a distintos tipos de fuentes y protecciones
   - **Orquestacion por Claude**: facilidad para que un agente LLM lo use (MCP, scripts, CLI)
   - **Fit para research estructurado**: capacidad de producir datos utiles para ICP
   - **Escalabilidad futura**: potencial para un sistema de lead research mas serio
3. Documentar fortalezas, debilidades y tradeoffs concretos
4. Emitir recomendacion: merece Scrapling un lugar en el stack agentico de negocio?
5. Documentar que faltaria probar en el stack alternativo para que la comparacion sea justa

**Entregable**: `04_outputs/2026-XX-XX_scrapling-evaluation-report_v1.md`

**Criterios de exito**:
- [ ] Cada criterio de evaluacion tiene evidencia concreta de las fases anteriores
- [ ] Recomendacion clara (si/no/condicional) con justificacion
- [ ] Documento util para comparacion con el repo del stack alternativo
- [ ] Lista de gaps y siguientes pasos

---

## Principios operativos transversales

1. **Cada fase produce un entregable antes de pasar a la siguiente.** No se avanza sin documentar.
2. **Respetar robots.txt y rate limits.** Scraping etico. Delays razonables entre requests.
3. **Datos reales, no mocks.** El experimento solo vale si toca fuentes reales.
4. **Documentar fricciones, no solo exitos.** Los problemas son hallazgos tan valiosos como los datos.
5. **Conectar siempre con el ICP.** Cada prueba tecnica debe justificarse desde el caso de uso.
6. **Comparabilidad.** Documentar de forma que sirva para comparar con el otro stack.

---

## Mapa de herramientas Scrapling por fase

| Fase | Fetcher | StealthyFetcher | DynamicFetcher | Spider | CLI extract | MCP Server |
|------|---------|-----------------|----------------|--------|-------------|------------|
| 0 Setup | x | x | | | | x |
| 1 Reconocimiento | x | x | x | | x | |
| 2 Extraccion | x | x | x | | x | x |
| 3 Spider | | | | x | | |
| 4 Scoring | | | | | | |
| 5 Evaluacion | | | | | | |

---

## Estimacion de dependencias entre fases

```
Fase 0 (Setup)
  |
  v
Fase 1 (Reconocimiento)
  |
  v
Fase 2 (Extraccion) <--- puede retroalimentar Fase 1 si se descubren nuevas fuentes
  |
  v
Fase 3 (Spider) <--- usa URLs de Fase 2 como input
  |
  v
Fase 4 (Scoring) <--- usa datos de Fases 2+3
  |
  v
Fase 5 (Evaluacion) <--- sintetiza todo
```

---

## Riesgos identificados

| Riesgo | Impacto | Mitigacion |
|--------|---------|------------|
| Google Maps bloquea scraping directo | Alto — fuente principal del ICP | Probar StealthyFetcher; evaluar Google Maps API como alternativa; documentar como hallazgo |
| Directorios colegiales con poca info publica | Medio — reduce senales disponibles | Complementar con busquedas Google + webs propias |
| Scrapling no maneja bien sitios en espanol con acentos/encoding | Bajo | Verificar en Fase 0; unlikely pero facil de detectar |
| Volumen de despachos en Canarias es limitado | Bajo — es un experimento, no produccion | 20-30 registros es suficiente para evaluar |
| MCP server no disponible o inestable | Medio — afecta evaluacion de orquestacion | Probar temprano en Fase 0; tener scripts como fallback |

---

## Changelog del plan

| Fecha | Cambio | Razon |
|-------|--------|-------|
| 2026-03-07 | Creacion inicial del plan maestro | Primera iteracion tras analisis de Scrapling + contexto ICP |
