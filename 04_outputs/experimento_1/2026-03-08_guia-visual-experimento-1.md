# Que hicimos, como y que validamos

> Guia visual del Experimento 1 para entender la iteracion email-first sin leer scripts ni datasets.

---

## La idea en 30 segundos

Queríamos responder esta pregunta:

> **Puede Scrapling llevarnos desde research util hasta un dataset accionable para emailing sin ampliar el stack?**

La respuesta corta:
- **si** con `AAFC`
- **si** con `google_basic`, pero solo en modo curado
- **todavia no** con `google_maps`

---

## El cambio respecto al Experimento 0

```mermaid
flowchart LR
    E0["Experimento 0\nresearch ICP"] --> P["Pivot"]
    P --> E1["Experimento 1\nemail-first"]

    E0a["Descubrir fuentes"] --> E0b["Extraer fichas"] --> E0c["Scoring ICP"]
    E1a["Mapear queries"] --> E1b["Validar fuentes"] --> E1c["Extraer contacto"] --> E1d["Curar y consolidar"]

    style E0 fill:#9E9E9E,color:#fff
    style P fill:#FF9800,color:#fff
    style E1 fill:#4CAF50,color:#fff
    style E0a fill:#BDBDBD,color:#000
    style E0b fill:#BDBDBD,color:#000
    style E0c fill:#BDBDBD,color:#000
    style E1a fill:#2196F3,color:#fff
    style E1b fill:#2196F3,color:#fff
    style E1c fill:#2196F3,color:#fff
    style E1d fill:#9C27B0,color:#fff
```

Antes buscábamos entender el mercado.

Ahora buscamos una salida operativa:
- nombre
- fuente
- geografia
- email o canal
- trazabilidad
- score de contactabilidad

---

## El flujo completo del Experimento 1

```mermaid
flowchart LR
    A["Fase 0\ncongelar\ncontrato de datos"] --> B["Fase 1\nmapear queries\npor carril"]
    B --> C["Fase 2\ndescubrir y validar\nfuentes"]
    C --> D["Fase 3\npiloto acotado"]
    D --> E["Fase 4\nescalar y curar"]
    E --> F["Fase 5\nevaluar contra\nExperimento 0"]

    style A fill:#4CAF50,color:#fff
    style B fill:#2196F3,color:#fff
    style C fill:#2196F3,color:#fff
    style D fill:#FF9800,color:#fff
    style E fill:#9C27B0,color:#fff
    style F fill:#607D8B,color:#fff
```

---

## Los tres carriles que probamos

```mermaid
flowchart TD
    G1["google_basic\nSERP -> web propia -> contacto"]
    G2["google_maps\nficha -> web enlazada -> contacto"]
    G3["specialized_directory\ndirectorio sectorial -> email"]

    G1 --> R1["PASS\nsolo curado"]
    G2 --> R2["WATCH"]
    G3 --> R3["PASS"]

    style G1 fill:#2196F3,color:#fff
    style G2 fill:#2196F3,color:#fff
    style G3 fill:#2196F3,color:#fff
    style R1 fill:#4CAF50,color:#fff
    style R2 fill:#FFC107,color:#000
    style R3 fill:#4CAF50,color:#fff
```

---

## Fase 1 — Mapping ICP-driven

No empezamos scrapeando. Primero convertimos el ICP en packs de busqueda.

```mermaid
flowchart TD
    ICP["ICP\nasesorias fiscales/contables\nCanarias"] --> Q1["Servicio"]
    ICP --> Q2["Geografia"]
    ICP --> Q3["Pain / tipo de cliente"]
    ICP --> Q4["Rol / intencion"]
    ICP --> Q5["Variacion de busqueda"]

    Q1 & Q2 & Q3 & Q4 & Q5 --> OUT["16 queries\nagrupadas por carril"]

    style ICP fill:#4CAF50,color:#fff
    style OUT fill:#2196F3,color:#fff
```

La idea era simple:
- no depender de un solo directorio
- forzar webs propias cuando fuese posible
- separar discovery, validacion local y directorios sectoriales

---

## Fase 2 — Validacion de fuentes

```mermaid
flowchart LR
    A["google_basic"] --> A1["PASS_TECH"]
    B["AAFC"] --> B1["PASS_TECH"]
    C["Gestores Tenerife"] --> C1["WATCH"]
    D["google_maps"] --> D1["WATCH"]

    style A fill:#2196F3,color:#fff
    style B fill:#2196F3,color:#fff
    style C fill:#2196F3,color:#fff
    style D fill:#2196F3,color:#fff
    style A1 fill:#4CAF50,color:#fff
    style B1 fill:#4CAF50,color:#fff
    style C1 fill:#FFC107,color:#000
    style D1 fill:#FFC107,color:#000
```

Lo importante aqui no era solo "la fuente existe".

Lo importante era:
- Scrapling puede entrar
- Scrapling puede extraer contacto
- la fuente sirve para emailing

---

## Fase 3 — Piloto

```mermaid
flowchart LR
    GB["google_basic\nseeded websites"] --> GBR["12 registros\n100% email real\nWATCH"]
    AA["AAFC"] --> AAR["12 registros\n100% email real\nPASS"]

    style GB fill:#2196F3,color:#fff
    style AA fill:#2196F3,color:#fff
    style GBR fill:#FFC107,color:#000
    style AAR fill:#4CAF50,color:#fff
```

**Por que `google_basic` quedo en `WATCH` en el piloto?**

Porque en ese punto la extraccion de webs funcionaba, pero la discovery live en Google todavia devolvia `429 / sorry` con demasiada frecuencia.

---

## El rescate de `google_basic`

Esta fue la parte critica del experimento.

```mermaid
flowchart TD
    A["Google live con fetch simple"] --> A1["429 / sorry"]
    B["StealthySession\nhome -> search"] --> B1["SERP real"]
    B1 --> C["Extraer enlaces externos"]
    C --> D["Entrar en web propia"]
    D --> E["Sacar email / form / telefono"]
    E --> F["Curar ruido comercial"]

    style A fill:#f44336,color:#fff
    style A1 fill:#FFCDD2,color:#000
    style B fill:#4CAF50,color:#fff
    style B1 fill:#E8F5E9,color:#000
    style F fill:#9C27B0,color:#fff
```

Lo que demostramos:
- Scrapling **si** puede hacer discovery live en Google
- pero el raw live no es suficiente
- Google mezcla webs propias con agregadores, institucional y ruido SEO

Por eso el output valido es:
- `google_basic raw live` para evidencia tecnica
- `google_basic curated` para operacion comercial

---

## Fase 4 — Escalado

### `AAFC`

```mermaid
pie title AAFC escalado
    "Email real (70)" : 70
```

- `70` registros
- `100%` email real
- `0%` ruido
- `source_quality_score=95`

### `google_basic` curado

```mermaid
pie title google_basic curado
    "Email real (28)" : 28
    "Formulario (2)" : 2
    "Canal directo (1)" : 1
```

- `31` registros
- `90.3%` email real
- `0%` ruido
- `source_quality_score=95`

---

## El dataset final

```mermaid
flowchart LR
    A["AAFC\n70"] --> C["Consolidacion"]
    B["google_basic curated\n31"] --> C
    C --> D["Dataset final\n101 registros"]
    D --> E["98 emails reales"]
    D --> F["3 canales alternativos"]

    style A fill:#4CAF50,color:#fff
    style B fill:#4CAF50,color:#fff
    style C fill:#9C27B0,color:#fff
    style D fill:#2196F3,color:#fff
    style E fill:#4CAF50,color:#fff
    style F fill:#FFC107,color:#000
```

El dataset final ya permite:
- ordenar por `contactability_score`
- ordenar por `icp_score`
- saber de que fuente sale cada registro
- diferenciar email real de canal alternativo

---

## Comparacion con Experimento 0

```mermaid
flowchart TD
    E0["Experimento 0"] --> X1["137 registros de PA\n49 colegiados"]
    E0 --> X2["0/30 con web propia"]
    E0 --> X3["research y scoring"]

    E1["Experimento 1"] --> Y1["101 registros consolidados"]
    E1 --> Y2["98 emails reales"]
    E1 --> Y3["dataset listo para emailing"]

    style E0 fill:#9E9E9E,color:#fff
    style E1 fill:#4CAF50,color:#fff
    style Y3 fill:#9C27B0,color:#fff
```

El cambio clave no es de volumen bruto.

El cambio clave es de valor:
- menos dependencia del directorio generalista
- mucho mas contacto util
- mejor trazabilidad
- mas capacidad de activacion

---

## Lo que validamos

```mermaid
flowchart TD
    V1["AAFC escala bien"] --> OK["VALIDADO"]
    V2["google_basic funciona con Scrapling"] --> OK
    V3["google_basic raw necesita curacion"] --> OK
    V4["google_maps como carril"] --> W["PENDIENTE"]

    style V1 fill:#4CAF50,color:#fff
    style V2 fill:#4CAF50,color:#fff
    style V3 fill:#FF9800,color:#fff
    style V4 fill:#FFC107,color:#000
    style OK fill:#4CAF50,color:#fff
    style W fill:#FFC107,color:#000
```

---

## Resumen para decidir

### Lo que ya podemos hacer

- escalar `AAFC`
- escalar `google_basic` en modo curado
- trabajar el dataset consolidado como base de emailing

### Lo que todavia no debemos hacer

- escalar `google_basic` raw sin filtro
- meter `google_maps` en produccion sin validacion especifica

---

## Que proponemos para el siguiente experimento

```mermaid
flowchart LR
    A["Experimento 2A\nbulk AAFC + google_basic curated"] --> B["Volumen util\npara emailing"]
    C["Experimento 2B\nvalidacion google_maps"] --> D["Decidir si entra\ncomo tercer carril"]

    style A fill:#4CAF50,color:#fff
    style B fill:#2196F3,color:#fff
    style C fill:#FFC107,color:#000
    style D fill:#2196F3,color:#fff
```

La prioridad correcta es:
1. explotar lo que ya funciona
2. validar despues lo que sigue incierto

Eso significa:
- primero `AAFC + google_basic curated`
- despues `google_maps`
