# Fase 1 — Reconocimiento de fuentes

Fecha: 2026-03-07

## Fuentes probadas

### 1. Paginas Amarillas (paginasamarillas.es)
- **Status**: VIABLE — fuente principal
- **Fetcher necesario**: `Fetcher` (HTTP puro) — sin proteccion anti-bot
- **Datos disponibles**: nombre, actividad, direccion completa, telefono, URL ficha, localizacion
- **Paginacion**: Si (multiples paginas por busqueda)
- **Cobertura**: ~29 asesorias fiscales en Las Palmas, ~28 en Tenerife por pagina
- **Busquedas utiles**: "asesoria fiscal", "gestoria contable", "asesoria contable", "asesoria de empresas"
- **Notas**:
  - Estructura HTML limpia con schema.org (itemprop) y data-analytics JSON
  - Las fichas individuales NO contienen web propia del despacho (solo links a beedigital/PA)
  - Esto confirma senal ICP: la mayoria de despachos pequenos no tienen web propia
  - Selectores clave: `.listado-item`, `span[itemprop="name"]`, `span[itemprop="streetAddress"]`

### 2. Colegio de Economistas de Las Palmas (economistaslaspalmas.org)
- **Status**: VIABLE — fuente complementaria de alta calidad
- **Fetcher necesario**: `DynamicFetcher` — directorio carga via JS dinamico
- **Datos disponibles**: numero de colegiado, apellidos, nombre
- **Paginacion**: Si (tabla con 50 registros visibles, probablemente paginada)
- **Cobertura**: Todos los economistas colegiados en Las Palmas
- **Notas**:
  - Requiere browser real (Playwright) para cargar tabla
  - Datos limpios pero limitados (solo nombre + num colegiado, sin direccion/telefono)
  - Util para cruzar con datos de PA y confirmar profesionalidad

### 3. QDQ (qdq.com)
- **Status**: NO VIABLE — error TLS con Fetcher
- **Error**: `WRONG_VERSION_NUMBER` en handshake TLS
- **No probado con StealthyFetcher** (podria funcionar pero la fuente es secundaria)

### 4. Infocif (infocif.es)
- **Status**: NO VIABLE — error certificado SSL
- **Error**: `no alternative certificate subject name matches target hostname`

### 5. Einforma (einforma.com)
- **Status**: NO VIABLE — 404 en busqueda
- **La URL de busqueda ha cambiado o requiere formato diferente**

### 6. CGCAFE (cgcafe.org — Colegio General de Gestores Administrativos)
- **Status**: ACCESIBLE — pendiente explorar directorio
- **Fetcher**: `Fetcher` (HTTP puro)
- **Potencial**: medio — si tiene directorio de gestores administrativos en Canarias

## Mapa fuente → senales ICP

| Senal ICP | Paginas Amarillas | Colegio Economistas |
|-----------|:-:|:-:|
| Nombre del despacho | x | x |
| Direccion/localidad | x | |
| Telefono | x | |
| Actividad/sector | x | |
| Sin web propia | x (confirmado via fichas) | |
| Registro colegial | | x |
| Num colegiado | | x |

## Hallazgos clave

1. **Paginas Amarillas es la fuente mas rica** — datos estructurados, sin proteccion anti-bot, schema.org
2. **El Colegio de Economistas requiere DynamicFetcher** — primer caso real de necesidad de browser
3. **La mayoria de despachos no tienen web propia** — confirmado via fichas PA. Esto valida la senal ICP "sin web propia o web basica"
4. **Las fuentes de registro mercantil (Infocif, Einforma) no funcionaron** — problemas SSL o URLs rotas
5. **Scrapling manejo bien los errores** — reintentos automaticos con logging claro, mensajes de error utiles

## Clasificacion de fetchers por fuente

| Fuente | Fetcher | DynamicFetcher | StealthyFetcher |
|--------|:-------:|:--------------:|:---------------:|
| Paginas Amarillas | OK | innecesario | innecesario |
| Colegio Economistas | no carga datos | OK | no probado |
| QDQ | error TLS | pendiente | pendiente |
| Infocif | error SSL | pendiente | pendiente |

## Siguiente paso

Pasar a Fase 2: extraccion masiva de PA (Las Palmas + Tenerife, multiples categorias) y extraccion del directorio completo del Colegio de Economistas.
