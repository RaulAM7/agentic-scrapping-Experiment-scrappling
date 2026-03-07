# Evaluacion de Scrapling como Capa de Smart Scraping para Workflow Agentico

> Fecha: 2026-03-07
> Version: v1
> Stack evaluado: Scrapling 0.4.1 (https://github.com/D4Vinci/Scrapling)
> Contexto: Experimento de scraping orientado a ICP — asesorias fiscales/contables en Canarias

---

## Resumen ejecutivo

Scrapling es una libreria solida, rapida y bien disenada para scraping web en Python. Demostro ser capaz de soportar un flujo completo de investigacion orientado a ICP: desde el descubrimiento de fuentes hasta la extraccion estructurada y el crawl en profundidad. Su principal fortaleza es la combinacion de tres fetchers (HTTP, Dynamic, Stealthy) en una API unificada con un framework de Spiders funcional. Su principal debilidad para un uso agentico es que el CLI y el MCP server estan por detras de la API Python en madurez.

**Recomendacion: SI, condicional** — Scrapling merece un lugar en el stack agentico como capa de scraping, pero el operador (humano o agente) necesita usar la API Python para obtener resultados fiables. El CLI y el MCP no son sustitutos todavia.

---

## Evaluacion por criterios

### 1. Friccion de adopcion
**Nota: 7/10**

| Aspecto | Resultado |
|---------|-----------|
| `pip install` | Limpio, sin conflictos |
| Instalacion browsers | Fallo con `scrapling install` (requiere sudo no documentado). Workaround facil: `playwright install chromium` + `patchright install chromium` |
| Primer fetch funcional | < 2 minutos tras instalacion |
| Tiempo total de setup | ~10 minutos incluyendo troubleshooting |

**Friccion real**: La instalacion de browsers es el unico punto de friccion. El README no explica claramente que `scrapling install` necesita sudo para dependencias del sistema. Un usuario sin experiencia con Playwright se atascaria aqui.

### 2. Claridad del modelo mental
**Nota: 9/10**

El modelo mental de Scrapling es claro y coherente:
- **Fetcher** = HTTP puro, rapido, sin JS
- **DynamicFetcher** = browser real (Playwright), para contenido dinamico
- **StealthyFetcher** = browser real (Patchright), para anti-bot
- **Spider** = crawl concurrente con multiples sesiones

La API es familiar (CSS selectors, XPath, estilo BeautifulSoup/Scrapy). Un desarrollador Python con experiencia minima en scraping entiende la libreria en minutos.

### 3. Flexibilidad
**Nota: 8/10**

| Escenario probado | Fetcher usado | Resultado |
|-------------------|---------------|-----------|
| Paginas Amarillas (HTML estatico) | Fetcher | Perfecto |
| Colegio Economistas (tabla JS) | DynamicFetcher | Perfecto |
| QDQ (problema TLS) | Fetcher | Fallo (TLS error) |
| Infocif (certificado invalido) | Fetcher | Fallo (SSL error) |

Scrapling cubrio 2/2 fuentes viables. Los fallos fueron por problemas SSL/TLS del sitio objetivo, no de Scrapling. La transicion entre fetchers es trivial (cambiar la clase, misma API de selectores).

### 4. Orquestacion por Claude (facilidad de uso agentico)
**Nota: 6/10**

| Canal | Resultado | Notas |
|-------|-----------|-------|
| API Python (scripts) | Excelente | Facil de generar, ejecutar y parsear por un agente |
| CLI `scrapling extract` | Pobre | Resultado vacio con CSS selector; sin selector devuelve bloqueo Incapsula. No usa impersonacion TLS por defecto. |
| MCP Server | Configurado, no verificado en sesion | Requiere reinicio de Claude Code. Limitacion para evaluacion en misma sesion. |

**Hallazgo critico**: La API Python es el canal fiable. El CLI no aplica las mismas estrategias anti-deteccion que el Fetcher de Python (no impersona TLS). Para uso agentico, un agente LLM que genere y ejecute scripts Python tendra mejores resultados que uno que intente usar el CLI.

### 5. Fit para research estructurado orientado a ICP
**Nota: 8/10**

El experimento completo produjo:
- 137 despachos unicos extraidos de 6 busquedas
- 49 colegiados del directorio profesional
- 77 prospectos scored contra heuristica ICP
- 30 fichas rastreadas en profundidad con Spider

Scrapling soporto todo el flujo sin bloqueos ni errores criticos. Los datos extraidos fueron suficientes para generar un ranking de prospectos accionable.

**Limitacion**: Las senales ICP mas ricas (resenas Google, presencia LinkedIn) requieren fuentes que no se probaron en este experimento. Scrapling podria manejarlas pero habria que evaluar el comportamiento contra Google Maps y LinkedIn (protecciones fuertes).

### 6. Escalabilidad futura
**Nota: 8/10**

| Feature | Disponible | Probada |
|---------|:----------:|:-------:|
| Concurrencia configurable | Si | Si (3 concurrent) |
| Multi-sesion (HTTP + Stealth) | Si | No (solo HTTP en spider) |
| Pause/resume | Si | Si (crawldir, checkpoint limpio) |
| Streaming | Si | No |
| Proxy rotation | Si | No |
| Export JSON/JSONL | Si | Si |
| Adaptive scraping | Si | Parcial (warning sobre configuracion) |
| MCP server | Si | Configurado, no probado en sesion |

El framework de Spiders es production-ready para crawls medianos. Para un sistema serio de lead research, las features de proxy rotation y multi-sesion (HTTP rapido + Stealth para sitios protegidos) serian clave.

---

## Fortalezas concretas

1. **Tres fetchers en una API unificada** — transicion trivial entre HTTP, Dynamic y Stealthy
2. **Spider framework solido** — concurrencia, rate limiting, pause/resume, estadisticas detalladas, export limpio
3. **Rendimiento** — 30 fichas en 19 segundos con rate limiting; 0 fallos, 0 bloqueos
4. **API familiar** — CSS selectors, XPath, estilo Scrapy/BS4. Curva de aprendizaje minima
5. **Schema.org parsing** — los selectores de itemprop funcionan perfectamente para datos estructurados

## Debilidades concretas

1. **CLI extract no aplica impersonacion TLS** — inutil contra sitios con proteccion minima (Incapsula)
2. **Adaptive scraping requiere configuracion no intuitiva** — el warning sobre `auto_save` sin `adaptive` en init es confuso
3. **Documentacion de instalacion de browsers** — no explica el requerimiento de sudo ni la necesidad de instalar tanto Playwright como Patchright
4. **MCP server no verificable en misma sesion** — requiere reinicio, lo que limita evaluacion fluida

## Hallazgos sobre el ICP

El experimento valido 3 senales del ICP con datos reales:
- **"Sin web propia"**: 100% confirmada (0/30 despachos rastreados tenian web propia)
- **"Ficha Google Business / PA como asesoria fiscal"**: funciona como senal primaria de descubrimiento
- **"Registro colegial"**: util para enriquecer, pero el cruce por apellido es impreciso

Senal no validada: resenas Google mencionando trato personal (requiere acceso a Google Maps, no probado).

---

## Que faltaria probar en el stack alternativo

Para que la comparacion sea justa, el otro stack deberia evaluarse contra:
1. Los mismos sitios (PA, Colegio Economistas) con los mismos selectores
2. El mismo flujo: busqueda → extraccion → crawl → scoring
3. Las mismas metricas: tiempo de setup, errores, rendimiento, facilidad de uso agentico
4. Adicionalmente: CLI y MCP si los ofrece, para comparar canales de orquestacion

---

## Conclusion

Scrapling puede ser la capa de smart scraping de un sistema agentico de negocio. No es perfecto: el CLI es debil, el MCP esta verde, y la documentacion de setup tiene lagunas. Pero donde importa — la API Python, los fetchers, y el Spider framework — funciona bien, es rapido, y produce datos utiles.

Para el caso de uso especifico (ICP → scraping → lead research → activacion comercial), Scrapling cubre las fases de descubrimiento y extraccion. Las fases de enriquecimiento avanzado (Google Maps, LinkedIn) requieren evaluacion adicional y probablemente proxy rotation.

**Veredicto: incorporar al stack, usar via API Python, no depender del CLI ni del MCP por ahora.**
