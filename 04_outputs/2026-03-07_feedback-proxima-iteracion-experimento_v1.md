# Feedback de trabajo para la proxima iteracion del experimento

> Fecha: 2026-03-07
> Base: contexto del repo + ICP + guia visual + evaluation report + feedback explicito de usuario
> Objetivo: puente operativo entre experimento ejecutado y siguiente iteracion

---

## 1) Material revisado

- `02_context/BRIEF.md`
- `02_context/FACTS.md`
- `02_context/CONSTRAINTS.md`
- `03_specs/now/001_now.md`
- `04_outputs/icp-asesoria-fiscal-contable-canarias.md`
- `04_outputs/experimento_0/guia-visual-srappling-experimento-0.md`
- `04_outputs/2026-03-07_scrapling-evaluation-report_v1.md`
- `04_outputs/2026-03-07_icp-prospect-ranking_v1.md`
- `05_scratch/fase-1_reconocimiento-fuentes.md`
- scripts y datos de `04_outputs/experimento_0/`
- feedback del usuario incluido en este hilo

---

## 2) Diagnostico critico del experimento actual

## 2.1 Que salio bien

1. Se ejecuto un flujo completo y documentado de punta a punta (fases 0-5).
2. La ejecucion tecnica con Scrapling fue estable para las fuentes finalmente usadas.
3. Se obtuvo volumen util para analisis exploratorio (137 despachos, 49 colegiados, 77 prospectos con score).
4. Se validaron senales ICP relevantes para discovery inicial (presencia en directorios, geografia, ausencia de web propia en muestra rastreada).
5. El resultado permitio evaluar la herramienta (Scrapling) con evidencia real, no con ejemplos sinteticos.

## 2.2 Que salio mal

1. Hubo desalineacion entre salida del experimento y objetivo comercial final de la cadena (`ICP -> scraping -> outreach/emailing -> CRM`): no se priorizo email como dato critico.
2. El mapping de fuentes no fue suficientemente inteligente ni estructurado por tipo de fuente; se mezclo discovery sin separar estrategia de captura por canal.
3. La fase de keywords quedo corta en combinatorias derivadas del ICP (servicio x geografia x variaciones de intencion x sinonimos).
4. Se extrajo informacion util pero de menor valor para activacion directa (telefono, direccion, actividad) frente al dato mas sensible para emailing (correo).
5. Parte del set quedo demasiado apoyado en directorio generalista, afectando calidad percibida de la base final.

## 2.3 Que falto en el diseno (gap de arquitectura experimental)

1. Falto un **data contract** inicial que definiera campos P0/P1 antes de scrapear.
2. Falto un **gate de calidad de fuentes** (criterios de entrada/salida por cada fuente).
3. Falto separar formalmente discovery en al menos 3 carriles:
   - Google basico
   - Google Maps
   - directorios especializados
4. Falto un checkpoint interactivo temprano con usuario para confirmar:
   - objetivo operativo de la iteracion
   - dato critico de exito
   - umbral minimo de calidad aceptable
5. Faltaron metricas de evaluacion orientadas a campana (cobertura de email, tasa de contacto util, ruido por fuente).

---

## 3) Traduccion explicita del feedback del usuario

| Feedback usuario | Diagnostico sobre experimento actual | Implicacion para siguiente iteracion |
|---|---|---|
| Faltaron combinatorias creativas de keywords desde ICP | Discovery se centro en consultas validas pero limitadas y poco sistematizadas | Crear matriz de queries ICP-driven antes de tocar fuentes |
| Faltaron inteligencia y estructura en busqueda de fuentes | No hubo separacion formal por tipo de fuente ni evaluacion comparativa robusta por carril | Disenar framework por carriles (Google, Maps, directorios especializados) |
| Falto mapear desde el principio que datos queriamos scrapear | Campos se definieron durante ejecucion tecnica, no como criterio de negocio previo | Introducir data contract obligatorio en Fase 0/1 |
| El objetivo real era emailing y el dato critico eran correos | Datos finales tienen valor de research, pero no maximizan accionabilidad para emailing | Definir email como campo P0 y eje de priorizacion de fuentes |
| Se scrapeo mucho dato util pero no el principal | Hubo exito tecnico sin exito completo de activacion | Medir exito por readiness de campana, no solo por volumen |
| Tiene sentido proceso iterativo/interactivo antes de scrapear | No existio un gate formal de confirmacion con usuario antes de extraccion masiva | Incluir checkpoint de preguntas y aprobacion previa |
| Preocupacion por calidad de fuentes (directorio generalista degrada) | Alta dependencia de una fuente generalista para volumen | Introducir score de calidad de fuente y umbral minimo para inclusion |

---

## 4) Recomendaciones accionables para el proximo experimento

## 4.1 Antes de scrapear (obligatorio)

1. Crear un documento `data-contract` con prioridades:
   - P0 (criticos): `email`, `nombre_empresa`, `url_fuente`, `tipo_fuente`, `geografia`.
   - P1 (enriquecimiento): `telefono`, `web`, `servicio`, `tamano_aprox`, `senal_icp`.
2. Definir regla de exito de iteracion: no cerrar experimento si cobertura de email P0 no supera umbral acordado.
3. Ejecutar checkpoint interactivo con usuario para aprobar:
   - definicion de "email util"
   - umbral minimo de calidad
   - fuentes permitidas/no permitidas

## 4.2 Agentic mapping sources 2.0

1. Generar matriz de keywords desde ICP con estructura:
   - vertical (asesoria fiscal, contable, gestoria, asesoria empresas)
   - geo (Las Palmas, Tenerife, resto islas target)
   - intencion (despacho, asesoria, consultoria fiscal, etc.)
   - variante de consulta (marca local, barrio, combinacion larga)
2. Separar exploracion en tres carriles:
   - Carril A: Google basico
   - Carril B: Google Maps
   - Carril C: directorios especializados
3. Para cada fuente medir de forma uniforme:
   - probabilidad de email
   - calidad del dato
   - ruido/duplicidad
   - costo tecnico de scraping
   - riesgo de bloqueo/legal operativo

## 4.3 Extraccion y evaluacion por etapas (sin sistema gigante)

1. Hacer piloto corto por fuente (10-15 registros por carril) antes de escalar.
2. Escalar solo fuentes que superen el gate de calidad.
3. Registrar motivo de descarte de cada fuente (transparencia comparativa).
4. Evaluar resultado con metricas orientadas a activacion:
   - `% registros con email P0`
   - `% emails unicos`
   - `% registros provenientes de fuentes especializadas`
   - `% ruido/no accionable`

---

## 5) Propuesta de rediseño del Experimento 1 (siguiente iteracion)

## Alcance

Iteracion acotada para mejorar calidad y accionabilidad. No construir sistema final.

## Fases propuestas

### Fase 0 — Alineacion operativa (nueva)
- Output: `04_outputs/YYYY-MM-DD_experimento-1_data-contract_v1.md`
- Contenido minimo:
  - objetivo de negocio de la iteracion
  - campos P0/P1
  - definicion de calidad de fuente
  - criterios de exito
- Gate: aprobacion explicita del usuario antes de scrapear.

### Fase 1 — Discovery estructurado por carriles
- Output: `04_outputs/YYYY-MM-DD_experimento-1_source-map_v1.md`
- Requisitos:
  - matriz de queries ICP-driven
  - Google basico vs Maps vs directorios especializados evaluados por separado
  - score comparativo por fuente
- Gate: lista corta de fuentes permitidas.

### Fase 2 — Piloto de extraccion email-first
- Output: `05_scratch/experimento_1_piloto-extraccion.md` + JSON piloto
- Requisitos:
  - muestra pequena por fuente
  - medicion de cobertura email y ruido
- Gate: solo pasan a escala las fuentes que cumplan umbral.

### Fase 3 — Extraccion focalizada y scoring para outreach
- Output: dataset consolidado + ranking orientado a emailing
- Requisitos:
  - deduplicacion por empresa/email
  - trazabilidad de fuente por registro
  - scoring ICP + score de contactabilidad

### Fase 4 — Evaluation report de iteracion
- Output: `04_outputs/YYYY-MM-DD_experimento-1-evaluation-report_v1.md`
- Requisitos:
  - comparativa contra experimento 0
  - que mejoro / que no mejoro
  - decision de siguiente paso

---

## 6) Criterios de exito recomendados para la siguiente iteracion

1. El campo `email` pasa de dato opcional a criterio central de exito.
2. Cada registro final tiene trazabilidad de fuente y tipo de fuente.
3. Se reduce dependencia de directorio generalista en favor de fuentes mejor calificadas.
4. El reporte final distingue claramente:
   - rendimiento tecnico de scraping
   - utilidad real para activacion comercial
5. El diseno incorpora al menos un checkpoint interactivo usuario-IA antes de extraccion masiva.

---

## 7) Riesgos y mitigaciones para la iteracion

| Riesgo | Impacto | Mitigacion |
|---|---|---|
| Baja disponibilidad publica de emails en algunas fuentes | Alto | Priorizar fuentes por `email yield` y no por volumen bruto |
| Fuentes de alto volumen con baja calidad | Alto | Gate de calidad + descarte temprano |
| Sobre-diseno del experimento | Medio | Mantener piloto corto y criterios de paso simples |
| Confundir exito tecnico con exito comercial | Alto | KPI de outreach desde el inicio |

---

## 8) Unknowns que deben cerrarse al inicio de la siguiente iteracion

1. Definicion exacta de "email valido para campana" en este contexto.
2. Umbral minimo de cobertura email para considerar la iteracion exitosa.
3. Lista inicial de fuentes especializadas preferidas por el equipo de negocio.

---

## 9) Cierre

El experimento 0 fue util para validar Scrapling y demostrar capacidad de ejecucion end-to-end.  
La siguiente iteracion debe corregir un gap de diseno: pasar de **research util** a **dataset accionable para emailing**, con foco explicito en email, calidad de fuente y decisiones por gates.
