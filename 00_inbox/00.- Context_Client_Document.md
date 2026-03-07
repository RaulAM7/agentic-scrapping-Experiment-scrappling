# Context Document — Yanira Leyva
<!-- SOURCE: IA 360 - Yanira Leyva _ Transcripcion cliente.md -->

## Document Purpose
This document captures Yanira's complete context through her voice, problems, requirements, beliefs, and desired transformation. The Context Document is the foundation for Offer Design and Proposal Development.

---

## 1️⃣ Transcripcion literal (destilada, en palabras del cliente)

⚠️ **Objetivo aqui**: capturar **como piensa**, **que le duele** y **que teme**, no resumir tecnicamente.

### Como vive hoy su negocio

- "Yo soy autonoma y trabajo por mi cuenta, pero despues colaboro con dos asesorias. Una es a nivel nacional y la otra es de aqui de Las Palmas."
- "Lo que llevo yo a modo personal son tanto nacionales como de aqui de Canarias."
- "Yo solo manejo la parte contable fiscal. Yo de la parte laboral no hago nada."
- "Ponle que sobre... entre 200 y 250" [clientes]
- "Tambien llevo un volumen grande de trabajo, o sea, no tengo pocos clientes, pero bueno, soy bastante organizada y mas o menos no tengo que trabajar mas de 8 o 9 horas al dia, pero al final hay cosas que tengo que sacar 3, 4 horas o 5 horas aqui para esto."

👉 **Insight clave**: Yanira opera como profesional independiente con una cartera masiva (200-250 clientes) en un modelo hibrido entre clientes propios y colaboracion con dos asesorias. Su capacidad organizativa es lo unico que sostiene un volumen de trabajo que estructuralmente excede su capacidad individual, compensando con horas extra y fines de semana.

### Dolor principal (real)

- "Eso es que parece una boberia, pero es a mi me quita una barbaridad de tiempo." [sobre organizar documentacion en Drive]
- "Un cliente medio, una hora y media, dos horas, no te las quitas." [solo para organizar facturas]
- "Si yo le subo 300 facturas, el me cobra esas 300 facturas, pero a lo mejor de esas 300 facturas, 80, no me las contabiliza. Tengo que volverlas a sacar y contabilizarlas yo."
- "Revisar 54 clientes todos los trimestres, pues si me lleva a dos, tres dias."
- "Al final a lo mejor un fin de semana, un sabado por la tarde, me dedico a reorganizar todas esas carpetas para que entre semana no tenga que estar trabajando 10 horas en vez de 8."

👉 **Insight clave**: El dolor real no es una sola tarea, sino la acumulacion de tareas manuales repetitivas que devoran aproximadamente 1,5 semanas al mes. La organizacion de documentos y la revision de contabilidad defectuosa del software son trabajo que no genera valor pero consume la mayor parte de su energia productiva. El resultado es una profesional altamente competente atrapada en trabajo operativo de bajo nivel.

### Miedos criticos

- "Si llega una inspeccion de la agencia tributaria, eso es lo que yo le tengo que enviar a la agencia tributaria. No puede estar de cualquier manera ni estar talado ni con errores."
- "Eso es dinero al fin y al cabo, que si yo lo presento mal..."
- "Yo no puedo esperar al ultimo dia para presentar 67 Impuestos sobre Sociedades, porque no... no, no, no, no, tiempo, no, no."
- "Me gusta revisar lo que me da el chat, no se, porque al final estamos hablando de leyes, y si pongo un articulo que no es, se me..."

👉 **Insight clave**: Los miedos de Yanira son fundamentalmente de responsabilidad profesional y legal. No teme perder clientes por mal servicio (sabe que su atencion es buena), sino que un error contable o fiscal derivado de la automatizacion defectuosa le genere consecuencias legales o economicas para sus clientes. Esto la obliga a un ciclo de doble revision que multiplica su carga de trabajo.

### Expectativas sobre la solucion

- "Cualquier cosa que automatice y me quite tiempo, me va bien."
- "Si yo tuviera un Excel, que yo le subo los modelos a la inteligencia artificial y me lo hace."
- "Que sea en la nube, que no me de tantos problemas a la hora de instalar..."
- "Uno pues que tenga ya, aprovechando ya todo esto, que tenga inteligencia artificial integrado para, yo que se, para lo que me pueda servir, para correos mismos o para respuestas a clientes o para que me suba las cosas al drive."
- "No tengo el mas minimo problema en cambiarme de programa."

👉 **Insight clave**: Yanira no busca una transformacion digital radical ni una solucion sofisticada. Quiere herramientas que funcionen de verdad, que le ahorren el trabajo manual que su software actual promete pero no cumple, y que esten en la nube para evitar los problemas de instalacion local. Su disposicion total al cambio de software revela que la lealtad al sistema actual es cero: solo lo mantiene porque no ha tenido tiempo de buscar alternativa.

### Vision de futuro

- "El proposito del dos mil veintiseis es poder automatizar todo lo que pueda."
- "Poderles ofrecer otro tipo de servicio adicional... por ejemplo, a mi no me da tiempo de revisar si hay subvenciones o no hay subvenciones."
- "Si puedo trabajar 6, mejor, sabes? Me gusta estudiar tambien y me gustaria hacer mas masteres de los que tengo."
- "Si puedo tener mas clientes, pues tambien, porque al final mi trabajo me gusta."
- "Yo quiero trabajar todo lo que puedo hasta que me lo permita la mente y el cuerpo. Pero porque me gusta, para mi el trabajo es como una aficion mas."

👉 **Insight clave**: Yanira no quiere menos trabajo, quiere trabajo de mayor valor. Su vision combina tres aspiraciones: ofrecer servicios premium (subvenciones, asesoramiento personalizado), reestructurar precios para reflejar el valor real, y recuperar tiempo personal para formacion y vida. Lo que realmente esta comprando no es software ni automatizacion, sino la capacidad de evolucionar de operaria contable a asesora estrategica.

---

## 2️⃣ Problemas reales (no soluciones, no features)

Aqui destilamos **los problemas estructurales**, no lo que el cliente "cree que necesita".

### Problema 1 — Trabajo manual de organizacion documental sin valor anadido

Los clientes suben documentacion a carpetas compartidas (Drive/iCloud) sin clasificar, obligando a Yanira a reorganizar manualmente cada archivo.

Cada cliente requiere:
- Revisar todos los documentos subidos sin orden
- Clasificar facturas en carpetas de ingresos vs gastos
- Separar por trimestre para facilitar revision posterior
- Renombrar o identificar facturas sin nombre descriptivo

El coste es temporal y cognitivo: un cliente medio consume 1,5-2 horas; clientes de alto volumen (300 facturas/mes) hasta 4 horas. Multiplicado por 200-250 clientes, esto representa semanas de trabajo no facturable.

👉 **Problema raiz**: *No existe un sistema de clasificacion automatica entre el punto de subida del cliente y el punto de consumo de la asesora. Toda la inteligencia de organizacion reside en la cabeza de Yanira y se ejecuta manualmente.*

### Problema 2 — Software contable (Dias Software/Cegid) que genera mas trabajo del que elimina

El programa promete automatizar la contabilizacion de facturas pero falla sistematicamente:

Dependencia extrema de:
- OCR que no procesa ~27% de las facturas (tickets, escaneos borrosos, facturas simplificadas)
- Contabilizacion que duplica bienes de inversion entre trimestres
- Soporte tecnico deficiente tras la adquisicion por Cegid
- Software local (no nube) que genera conflictos con actualizaciones en entorno Mac

Si el OCR falla → Yanira debe contabilizar manualmente las facturas rechazadas. Si los bienes de inversion se duplican → riesgo de presentar impuestos incorrectos. Si el soporte falla en periodo critico → 67 Impuestos sobre Sociedades manuales.

👉 **Problema raiz**: *La herramienta principal de trabajo no es fiable, obligando a un ciclo sistematico de doble revision que anula el beneficio de la automatizacion y genera riesgo fiscal.*

### Problema 3 — Modelo de precios plano que no refleja la carga de trabajo real

Yanira cobra tarifas fijas por tipo de cliente (autonomo) sin diferenciar la carga de trabajo real.

Hoy funciona porque:
- Yanira absorbe personalmente las diferencias de carga con mas horas
- Los clientes historicos (20 anos) mantienen tarifas antiguas sin cuestionar

Manana, con mas clientes o servicios adicionales:
- Clientes de alto volumen (cafeteria vs salon de belleza) subsidian a clientes de bajo volumen
- Servicios extras (notificaciones, solicitudes, proyectos) se realizan gratis por costumbre
- No existe contrato formal que delimite alcance, lo que impide cobrar suplementos

👉 **Problema raiz**: *No existe un sistema de medicion del tiempo/esfuerzo por cliente ni una estructura contractual que permita escalar precios de forma justa y defendible.*

### Problema 4 — Conciliacion trimestral manual con plataforma de colaboracion

Para los 54 clientes de la plataforma nacional, Yanira debe descargar el libro de ingresos y gastos, desconfiar de los datos, y unificar manualmente Excel trimestre a trimestre.

Cada trimestre requiere:
- Descargar datos de la plataforma
- Verificar que los datos sean correctos (bienes de inversion duplicados, IVA incorrecto, porcentajes mal calculados)
- Unificar Excel del Q1 + Q2 + Q3 + Q4 para el resumen anual
- Corregir errores antes de presentar a la Agencia Tributaria

El coste es 2-3 dias por trimestre, acumulandose en el Q4 cuando debe cuadrar todo el ano.

👉 **Problema raiz**: *La plataforma de colaboracion no genera datos fiables, forzando una capa de verificacion manual que convierte cada cierre trimestral en un cuello de botella critico.*

---

## 3️⃣ Requisitos funcionales (destilados a nivel estrategico)

No a nivel tecnico todavia, sino **que debe ser verdad para que esto funcione**.

### MUST — Imprescindibles

- Automatizacion real del escaneo/contabilizacion de facturas que funcione con tickets, facturas simplificadas y escaneos de calidad variable
- Clasificacion automatica de documentos subidos por clientes en carpetas correctas (ingresos, gastos, por trimestre)
- Software contable en la nube que no dependa de instalacion local ni genere conflictos con entorno Mac
- Fiabilidad del sistema: que lo que se automatice este bien hecho y no requiera doble revision sistematica
- Deteccion correcta de inversion del sujeto pasivo en facturas de peninsula a Canarias

### SHOULD — Muy importantes

- Automatizacion de envio de correos recurrentes (recordatorios mensuales de documentacion) sin tener que programarlos manualmente
- Conciliacion bancaria integrada en el software contable
- Capacidad de unificar y verificar datos trimestrales de forma automatica para los 54 clientes de la plataforma
- Inteligencia artificial integrada para asistencia en redaccion de correos y respuestas a clientes

### COULD — Deseables

- Sistema de medicion del tiempo/esfuerzo por cliente para fundamentar reestructuracion de precios
- Herramienta de busqueda automatica de subvenciones aplicables a cada cliente
- Mejora de respuestas automaticas de WhatsApp con IA para dudas recurrentes
- Definicion de niveles de servicio y plantilla de contrato para nuevos clientes

---

## ATERRIZADO PRE-OFFER -> DE TODOS SUS PROBLEMAS, QUE ELEGIMOS RESOLVER Y COMO?

Base: seccion Requisitos funcionales (MUST/SHOULD/COULD) del presente Context Document.

### PROBLEM 1 — Document Ops (Drive): caos de entrada → caos de salida

**Que engloba (del doc):**
- Clasificacion automatica de documentos en carpetas correctas por ingresos/gastos/trimestre (MUST).
- Parte del flujo de recordatorios, en tanto impacta directamente a la entrada de documentacion (SHOULD).

**Que tiene que ser verdad para que funcione:**
- Existe una estructura estandar (la metodologia de Yanira) que todos los clientes respetan sin friccion adicional.
- Lo que entra al sistema se auto-clasifica y queda listo para trabajar, no para ordenar.
- El sistema es tolerante al caos: nombres mal puestos, PDFs mezclados, fotos de tickets, etc.

**Lo que SI vamos a resolver:**
- Diseno de estructura de carpetas/subcarpetas alineada con la operativa real de Yanira.
- Clasificacion inteligente automatica de lo que suben los clientes hacia esa estructura.
- Minima friccion: que el cliente suba documentacion como siempre y el sistema ordene por el.

**Lo que NO vamos a resolver:**
- Cambiar habitos humanos por fuerza bruta ("educar a todos los clientes" como unica solucion).
- Construir un portal cliente complejo si no hace falta (evitar sobre-ingenieria).

**Como lo resolvemos (a nivel conceptual):**
- Sistema de Document Intelligence: reglas + IA para interpretar documento → ubicar → renombrar/etiquetar → logging.
- Principio rector: "diseno primero, automatizacion despues".

---

### PROBLEM 2 — Accounting Ops (OCR/contabilizacion): automatizacion que falla → doble revision

**Que engloba (del doc):**
- OCR/escaneo con tickets, factura simplificada y calidad variable (MUST).
- Fiabilidad: que no requiera doble revision sistematica (MUST).
- Deteccion de inversion del sujeto pasivo Peninsula → Canarias (MUST).

**Que tiene que ser verdad:**
- No basta con "leer": hay que extraer + validar + clasificar fiscalmente lo critico.
- Flujo de excepcion: lo que no es fiable se manda a revision puntual, no todo el volumen.

**Lo que SI vamos a resolver:**
- Pipeline tolerante a calidad variable de documentos de entrada.
- Capa de validacion + revision por excepciones (no revision sistematica de todo).
- Regla especifica para deteccion de inversion del sujeto pasivo.

**Lo que NO vamos a resolver:**
- ERP contable desde cero.
- Promesa de "0 errores" sin capa de revision.
- Integracion con cualquier sistema legacy si es inviable tecnicamente.

**Como lo resolvemos:**
- OCR + extraccion estructurada + validadores fiscales + cola de revision por excepcion.
- Definicion de un estandar de fiabilidad operativa medible.

---

### PROBLEM 3 — ERP / Software contable cloud: herramienta core que no estorbe

**Que engloba (del doc):**
- Software contable en la nube sin instalacion local ni conflictos Mac (MUST).
- Conciliacion bancaria integrada (SHOULD).

**Lo que SI vamos a hacer:**
- Research + shortlist + criterios de evaluacion + decision guiada con Yanira.
- Acompanamiento en la transicion a nivel estrategico-operativo (no desarrollo a medida).

**Lo que NO vamos a hacer:**
- ERP a medida.
- Migracion masiva completa como parte del alcance core.

**Como lo resolvemos:**
- "ERP Selection Sprint": requirements → shortlist → demos → decision → plan de migracion.

---

### PROBLEM 4 — Business Model & Monetizacion: tarifa plana que castiga a la mejor clienta

**Que engloba (del doc):**
- Medicion de tiempo/esfuerzo por cliente (COULD).
- Niveles de servicio + contrato para nuevos clientes (COULD).

**Lo que SI vamos a resolver:**
- Reestructurar pricing + scope defendible.
- Disenar niveles de servicio (tiering) y reglas claras de "que entra / que no entra".
- Plantillas y sistema para onboarding de nuevos clientes con marco contractual claro.

**Lo que NO vamos a resolver:**
- Control horario corporativo pesado.
- Cambiar precios a toda la base historica de clientes de golpe.

**Como lo resolvemos:**
- "Value Ladder + Offer Architecture": diseno de escalera de valor con niveles diferenciados.
- Medicion simple "minimo viable" de esfuerzo por cliente, si aplica.

---

### PROBLEM 5 — Communications Ops: correos + WhatsApp como palancas

**Que engloba (del doc):**
- Automatizacion de correos recurrentes (SHOULD).
- IA para redaccion/respuestas a clientes (SHOULD).
- WhatsApp con IA para dudas recurrentes (COULD).

**Lo que SI vamos a resolver:**
- Automatizacion de recordatorios por email (mensual/trimestral segun proceso). -> COMO APORTAR VALOR Y AUTOMATIZAR UN PROCESO QUE YA EXISTE PARA REBAJAR CARGA OPERATIVA + MUY IMPORTANTE APROVECHAR ESTE CANAL COMUNICATIVO COMO CANAL PARA ADQUISICION Y CONVERSION DE CLIENTE Y NO SOLO UN FYQ RESOLVEDOR DE DUDAS
- Playbook de comunicacion: mensajes tipo, timing, segmentacion por tipo de cliente. -> COMO CONVERTIR WHATSAPP EN UN CANAL DE ADQUISICION Y CONVERSION DE CLIENTE Y NO SOLO UN FYQ RESOLVEDOR DE DUDAS 

**Lo que NO vamos a resolver:**
- Rehacer WhatsApp desde cero.
- Bot avanzado si no es necesario para el volumen actual.

**Como lo resolvemos:**
- "Email Ops Automation": calendario + segmentos + plantillas + triggers automaticos.
- WhatsApp: mejoras ligeras dentro del mentoring, sin desarrollo a medida.

---

### Traduccion a "bloques grandes" de la offer (sin disenarla aun) -> QUE SI VAMOS A RESOLVER Y COMO AGRUPARLO EN LA OFFER

**STACK 1 — Implementacion tecnica (Done-for-you)**
- Document Ops AI (Problem 1)
- Email Ops Automation (parte de Problem 5)
- (Opcional / segun alcance) Accounting Ops AI (Problem 2) — core o fase 2 segun riesgo/tiempo.

**STACK 2 — Consultoria + mentoring (estrategico + tecnico)**
- Consultoria negocio (Problem 4): frameworks Hormozi + Russell para pricing y offer architecture.
- Mentoring tecnico-operativo (Problem 3 + WhatsApp del Problem 5): ERP selection + comunicaciones + adopcion.

**Formato propuesto:**
- 8 sesiones semanales (1h) + 2 sesiones de seguimiento (mes 3 y mes 6).

---

## 4️⃣ Creencias profundas del cliente (oro puro para la offer)

Esto es **material directo para copy, promesa y Big Domino** despues.

### Creencias explicitas

- "La atencion al cliente esta bastante bien y no tengo quejas en ese aspecto"
- "Me gusta revisar lo que me da el chat, porque al final estamos hablando de leyes"
- "Para mi el trabajo es como una aficion mas, lo que pasa es que es un poquito mas desgastante que el resto"
- "No tengo el mas minimo problema en cambiarme de programa"
- "Cualquier cosa que automatice y me quite tiempo, me va bien"

### Creencias implicitas

- "Prefiero invertir tiempo extra en revision antes que arriesgarme a un error fiscal" — La fiabilidad es mas importante que la velocidad
- "Si el software no funciona bien, prefiero hacerlo manual antes que confiar ciegamente" — La confianza en la tecnologia se gana con resultados, no con promesas
- "El tiempo que pierdo en tareas operativas es tiempo que me roban de crecer como profesional" — Su identidad es la de asesora estrategica, no de operaria contable
- "Los clientes antiguos son intocables en precio, pero los nuevos deben entrar con reglas claras" — Valora la lealtad pero reconoce que necesita un nuevo marco

---

## 5️⃣ Resultado deseado real (Day 90 implicito)

Aunque no lo dice asi, **esto es lo que realmente quiere**:

- Poder procesar la contabilidad mensual de 200-250 clientes sin dedicar 1,5 semanas a tareas manuales de organizacion y correccion
- Confiar en que las facturas escaneadas y contabilizadas estan bien sin tener que revisarlas una a una
- Tener tiempo libre para ofrecer servicios de mayor valor (investigacion de subvenciones, asesoramiento personalizado)
- No tener que sacrificar fines de semana para reorganizar carpetas y ponerse al dia
- Sentir que su negocio puede crecer sin que ella tenga que trabajar mas horas, sino mejores horas

---

👉 **Transformacion deseada**:

**De** asesora fiscal competente pero atrapada en trabajo manual repetitivo, compensando las deficiencias de su software con horas extra y revision constante **→ a** asesora estrategica con sistemas fiables que automatizan lo operativo, liberando tiempo para servicios de alto valor, formacion continua y calidad de vida.

---

## Sources digested
- IA 360 - Yanira Leyva _ Transcripcion cliente.md (discovery call transcript, ~41 minutes)

---

## Completion Checklist

Before marking this Context Document complete, verify:

- [x] Section 1 includes minimum 3 direct client quotes per subsection
- [x] Client voice is preserved (verbatim quotes in quotation marks)
- [x] Section 2 identifies minimum 3 distinct structural problems with root causes
- [x] Section 3 categorizes requirements into MUST/SHOULD/COULD
- [x] Section 4 captures both explicit and implicit beliefs
- [x] Section 5 articulates transformation (From → To)
- [x] All insights (👉) synthesize deeper meaning, not just restate
- [x] Sources are documented if multiple inputs used

<!-- FINAL VALIDATION: Context Document must be approved before proceeding to Offer Design -->
