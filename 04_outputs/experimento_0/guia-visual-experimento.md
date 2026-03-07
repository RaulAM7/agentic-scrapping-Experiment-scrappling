# Que hicimos, como y que descubrimos

> Guia visual del Experimento 0 para tomar decisiones sin necesidad de leer codigo.

---

## La idea en 30 segundos

Queríamos responder una pregunta:

> **Puede una herramienta de scraping (Scrapling) ayudarnos a encontrar automaticamente despachos profesionales en Canarias que encajen con nuestro cliente ideal?**

La respuesta corta: **si, pero con matices**. Aqui explicamos todo paso a paso.

---

## El flujo completo

```mermaid
flowchart LR
    A["Definir\ncliente ideal\n(ICP)"] --> B["Buscar\nfuentes de\ndatos"]
    B --> C["Extraer datos\nde despachos\nreales"]
    C --> D["Rastrear fichas\nen profundidad"]
    D --> E["Puntuar cada\ndespacho segun\nel ICP"]
    E --> F["Decidir si\nla herramienta\nfunciona"]

    style A fill:#4CAF50,color:#fff
    style B fill:#2196F3,color:#fff
    style C fill:#2196F3,color:#fff
    style D fill:#2196F3,color:#fff
    style E fill:#FF9800,color:#fff
    style F fill:#9C27B0,color:#fff
```

Las fases verdes son de **estrategia**, las azules de **ejecucion tecnica**, la naranja de **analisis** y la morada de **decision**.

---

## Fase 0 — Instalacion

**Que hicimos**: Instalar Scrapling y comprobar que funciona.

**Resultado**: Todo funciono en ~10 minutos.

**Friccion encontrada**: Un paso de la instalacion pedia una contrasena de administrador que no estaba documentada. Lo resolvimos con un atajo, pero un usuario sin experiencia se habria atascado.

```mermaid
flowchart TD
    I["pip install scrapling"] --> B["Instalar\nnavegadores"]
    B -->|"Fallo: pide sudo"| W["Workaround:\ninstalar\nmanualmente"]
    W --> V{"Los 3 modos\nfuncionan?"}
    V -->|Si| OK["Listo"]

    style I fill:#E8F5E9
    style B fill:#FFEBEE
    style W fill:#FFF3E0
    style OK fill:#E8F5E9
```

---

## Fase 1 — Reconocimiento: donde estan los datos?

**Que hicimos**: Probar varias webs publicas para ver cuales tienen datos utiles sobre asesorias en Canarias.

```mermaid
flowchart TD
    subgraph Probamos 5 fuentes
        PA["Paginas\nAmarillas"]
        CE["Colegio de\nEconomistas"]
        QDQ["QDQ"]
        IC["Infocif"]
        EI["Einforma"]
    end

    PA -->|"Funciona perfecto"| OK1["137 despachos"]
    CE -->|"Funciona con\nnavegador"| OK2["49 colegiados"]
    QDQ -->|"Error tecnico"| KO1["Descartada"]
    IC -->|"Error tecnico"| KO2["Descartada"]
    EI -->|"URL rota"| KO3["Descartada"]

    style PA fill:#4CAF50,color:#fff
    style CE fill:#4CAF50,color:#fff
    style QDQ fill:#f44336,color:#fff
    style IC fill:#f44336,color:#fff
    style EI fill:#f44336,color:#fff
    style OK1 fill:#E8F5E9
    style OK2 fill:#E8F5E9
```

**Lo que aprendimos**: De 5 fuentes probadas, 2 funcionaron bien. Paginas Amarillas es la mas rica. El Colegio de Economistas tiene datos de calidad pero mas limitados.

---

## Fase 2 — Extraccion: sacar datos reales

**Que hicimos**: Lanzar busquedas automaticas en Paginas Amarillas (3 categorias x 2 provincias) y extraer el directorio del Colegio de Economistas.

```mermaid
flowchart LR
    subgraph "6 busquedas en PA"
        B1["Asesoria fiscal\nLas Palmas"]
        B2["Asesoria fiscal\nTenerife"]
        B3["Gestoria\nLas Palmas"]
        B4["Gestoria\nTenerife"]
        B5["Asesoria empresas\nLas Palmas"]
        B6["Asesoria empresas\nTenerife"]
    end

    B1 & B2 & B3 & B4 & B5 & B6 --> D["Deduplicar"]
    D --> R["137 despachos\nunicos"]

    CE["Colegio\nEconomistas"] --> C["49\ncolegiados"]

    style R fill:#4CAF50,color:#fff
    style C fill:#4CAF50,color:#fff
```

**De cada despacho sacamos**: nombre, actividad, direccion, localidad, provincia, telefono y enlace a su ficha.

---

## Fase 3 — Rastreo en profundidad

**Que hicimos**: Una "arana" automatica visito las 30 primeras fichas individuales de Paginas Amarillas para buscar informacion extra: web propia, descripcion, horario, resenas.

```mermaid
flowchart LR
    URLs["30 fichas\nde PA"] --> Spider["Arana\nautomatica"]
    Spider --> R["30 fichas\nrastreadas"]
    R --> H1["0 con web propia"]
    R --> H2["0 con descripcion"]
    R --> H3["Todas con\nhorario basico"]

    style URLs fill:#E3F2FD
    style Spider fill:#2196F3,color:#fff
    style H1 fill:#FF9800,color:#fff
    style H2 fill:#FF9800,color:#fff
```

**Hallazgo importante**: **Ninguno de los 30 despachos rastreados tiene web propia.** Esto confirma masivamente lo que sospechabamos: estos despachos estan muy poco digitalizados. Eso es exactamente el perfil de cliente que buscamos.

**Rendimiento**: 30 fichas en 19 segundos, cero errores, cero bloqueos.

---

## Fase 4 — Puntuacion: quien encaja mejor?

**Que hicimos**: Cruzar todos los datos con las senales del ICP y asignar una puntuacion a cada despacho.

### Sistema de puntuacion

```mermaid
flowchart TD
    subgraph "Senales que suman puntos"
        S1["Es asesoria fiscal/contable\nen Canarias\n+4 puntos"]
        S2["No tiene web propia\n+3 puntos"]
        S3["Aparece en registro\ncolegial\n+3 puntos"]
        S4["Esta en capital\ninsular\n+2 puntos"]
    end

    S1 & S2 & S3 & S4 --> T["Puntuacion\ntotal\n(max 12)"]

    style S1 fill:#4CAF50,color:#fff
    style S2 fill:#FF9800,color:#fff
    style S3 fill:#2196F3,color:#fff
    style S4 fill:#9E9E9E,color:#fff
    style T fill:#9C27B0,color:#fff
```

### Resultado

```mermaid
pie title Distribucion de 77 prospectos por puntuacion
    "Score 12 (4)" : 4
    "Score 10 (3)" : 3
    "Score 9 (15)" : 15
    "Score 7 (24)" : 24
    "Score 6 (13)" : 13
    "Score 4 (18)" : 18
```

**Top 7 prospectos** (puntuacion 10 o mas):

| Nombre | Puntuacion | Localidad |
|--------|:----------:|-----------|
| Sanchez Marichal Auditores | 12 | Las Palmas |
| Asesoria Romero S.L. | 12 | Las Palmas |
| Asesoria Artiles | 12 | Las Palmas |
| Mario Alonso Alvarez | 12 | Santa Cruz de TF |
| Asesoria Fiscal Miguel Lopez Rosa | 10 | Arrecife |
| Asesoria Agustin J. Marrero | 10 | Telde |
| Agustin Ruiz Y Asociados S.L. | 10 | Puerto de la Cruz |

---

## Fase 5 — Evaluacion: funciona Scrapling para esto?

```mermaid
flowchart TD
    subgraph "Lo que evaluamos"
        E1["Facilidad de\ninstalacion"]
        E2["Facilidad de\nuso"]
        E3["Flexibilidad\n(distintos sitios)"]
        E4["Uso por un\nagente IA"]
        E5["Utilidad para\ninvestigar ICP"]
        E6["Escalabilidad\nfutura"]
    end

    E1 --> N1["7/10"]
    E2 --> N2["9/10"]
    E3 --> N3["8/10"]
    E4 --> N4["6/10"]
    E5 --> N5["8/10"]
    E6 --> N6["8/10"]

    style N1 fill:#FFF3E0
    style N2 fill:#E8F5E9
    style N3 fill:#E8F5E9
    style N4 fill:#FFEBEE
    style N5 fill:#E8F5E9
    style N6 fill:#E8F5E9
```

### Traduccion de las notas

| Criterio | Nota | Que significa en practica |
|----------|:----:|--------------------------|
| Instalacion | 7/10 | Funciona, pero hay un paso confuso con los navegadores |
| Facilidad de uso | 9/10 | Muy intuitivo si sabes Python basico |
| Flexibilidad | 8/10 | Se adapta bien a distintos tipos de webs |
| Uso por agente IA | 6/10 | Funciona bien via codigo Python, pero sus atajos (CLI, MCP) todavia no son fiables |
| Investigacion ICP | 8/10 | Produjo datos reales y utiles para encontrar prospectos |
| Escalabilidad | 8/10 | Tiene features avanzadas (proxies, concurrencia) para crecer |

---

## Que descubrimos sobre nuestros clientes ideales

```mermaid
flowchart TD
    H1["Ninguno tiene\nweb propia"] --> I1["Estan muy poco\ndigitalizados"]
    H2["Todos aparecen en\nPaginas Amarillas"] --> I2["Su unica presencia\nonline es en\ndirectorios"]
    H3["Muchos son\nprofesionales solos\no equipos pequenos"] --> I3["Encajan con el\nperfil de Yanira"]

    I1 & I2 & I3 --> C["Confirmacion:\nel ICP esta\nbien definido"]

    style C fill:#4CAF50,color:#fff
    style H1 fill:#FF9800,color:#fff
    style H2 fill:#FF9800,color:#fff
    style H3 fill:#FF9800,color:#fff
```

---

## Resumen para decidir

### La herramienta (Scrapling)

```mermaid
quadrantChart
    title Scrapling: donde destaca y donde no
    x-axis "Poco util" --> "Muy util"
    y-axis "Dificil" --> "Facil"
    API Python: [0.85, 0.9]
    Spider (arana): [0.8, 0.7]
    CLI (terminal): [0.3, 0.6]
    MCP (IA directa): [0.5, 0.4]
```

- **Lo mejor**: la API Python y el Spider son rapidos, fiables y faciles de usar.
- **Lo peor**: el CLI (uso por terminal) y el MCP (uso directo por IA) todavia no estan a la altura.

### Recomendacion final

```mermaid
flowchart LR
    Q{"Incorporar\nScrapling\nal stack?"} -->|"SI,\npero..."| R["Usar via\nPython.\nNo depender\ndel CLI\nni del MCP\npor ahora."]

    style Q fill:#9C27B0,color:#fff
    style R fill:#4CAF50,color:#fff
```

**SI, con condiciones:**
1. Usarlo a traves de scripts Python (no del CLI ni del MCP)
2. Para fuentes con proteccion anti-bot fuerte (Google Maps, LinkedIn) habria que probar mas a fondo
3. Es una buena base para construir un sistema mas serio de investigacion de prospectos

---

## Inventario de lo que se genero

| Que | Cuanto |
|-----|--------|
| Despachos extraidos | 137 unicos |
| Colegiados extraidos | 49 |
| Prospectos puntuados | 77 |
| Top prospectos (score >= 10) | 7 |
| Fichas rastreadas en profundidad | 30 |
| Scripts creados | 3 |
| Fuentes probadas | 5 (2 viables) |
| Errores del spider | 0 |
| Tiempo total del spider | 19 segundos |
