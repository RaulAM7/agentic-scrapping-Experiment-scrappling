# Source Map - Experimento 1 Scrapling (Fase 2)

> Fecha: 2026-03-07
> Version: v1
> Estado: listo para Checkpoint 2
> Base de consulta: evidencia web actual + aprendizajes del Experimento 0 + microvalidacion Scrapling en `05_scratch/experimento_1/2026-03-07_scrapling-source-validation.md`

## 1. Decision ejecutiva

### PASS

- `google_basic` -> webs propias con email visible en `contacto`, `team/about` o `home/servicios`
- `specialized_directory` -> `AAFC / Despachos Profesionales`

### WATCH

- `google_maps` -> ficha first-party de Google Business / Google Maps
- `google_maps` -> handoff desde ficha de Maps hacia web propia enlazada
- `specialized_directory` -> `Colegio de Gestores Administrativos de Santa Cruz de Tenerife / Localiza tu GA + PDF de colegiados`
- `specialized_directory` -> `Colegio de Gestores Administrativos de Las Palmas / Localiza tu GA`
- `specialized_directory` -> `Colegio Oficial de Economistas de Las Palmas / Directorio de colegiados`

### DROP

- Republishers de datos de Maps tipo `ccasesoria.com`
- `COETE` y `COTIME` como fuentes primarias de leads contactables
- `Paginas Amarillas` como fuente principal del diseno; se mantiene solo como benchmark/control

## 2. Criterio de lectura

En Fase 2 no se puntua todavia `source_quality_score` final. Aqui solo se decide si una fuente merece piloto con esta lectura:

- `Email probability`: alta / media / baja
- `Authority`: alta / media / baja
- `ICP density`: alta / media / baja
- `Technical cost`: bajo / medio / alto
- `Blocking risk`: bajo / medio / alto
- `Expected noise`: bajo / medio / alto

## 2.1 Microvalidacion tecnica con Scrapling

Resultado de la validacion real via API Python de Scrapling sobre las tres fuentes candidatas:

- `google_basic / webs propias con email visible` -> `PASS_TECH`
- `AAFC / Despachos Profesionales` -> `PASS_TECH`
- `Gestores Tenerife / Localiza tu GA + PDF` -> `WATCH`

Lectura:

- En `google_basic`, `Fetcher` cargo y extrajo emails visibles de `jmsconsulting.es`, `unificont.es` y `asesoriafiscaltenerife.es`
- En `AAFC`, `Fetcher` cargo `https://asesoresfiscalesdecanarias.org/servicios/despachos-profesionales/` y detecto emails reales en la pagina del directorio
- En `Gestores Tenerife`, `Fetcher` carga el entrypoint, pero el PDF no queda demostrado como fuente reutilizable de contactos con Scrapling; el flujo cae en `docs.google.com/gview` y no devuelve emails extraibles en esta microprueba

## 3. Source-map por carril

### 3.1 `google_basic`

| Fuente/patron | Evidencia actual | Email probability | Authority | ICP density | Technical cost | Blocking risk | Expected noise | Status | Lectura operativa |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| SERP -> pagina de contacto propia con email visible | `jmsconsulting.es/contacto/` publica `asesoria@jmsconsulting.es`; `gestoriavegalujan.es/contacto/` publica `mvegalujan@gestores.net` | Alta | Alta | Media-alta | Bajo | Bajo | Medio | `PASS` | Mejor opcion email-first. El contacto ya esta visible y la trazabilidad al negocio es clara. |
| SERP -> pagina `team/about` con emails nominales | `asesoriafiscaltenerife.es` publica `javier@...`, `sandra@...`, `sonsoles@...`, `veronica@...` | Muy alta | Alta | Media | Bajo | Bajo | Medio | `PASS` | Fuente especialmente buena para outreach porque convierte email generico en email nominal o funcional por rol. |
| SERP -> `home/servicios` con email en cabecera o pie | `unificont.es` muestra `direccion@unificont.es`; `asesoramientostenerife.com` muestra `administracion@asesoramientostenerife.com`; `fiscaltaxcanarias.com/servicios/` muestra `info@fiscaltaxcanarie.com`; `openplusasesores.es` muestra `info@openplusasesores.es` | Alta | Alta | Alta | Bajo | Bajo | Medio | `PASS` | Sube el yield sin depender de pagina de contacto exacta. Muy util para extraer primero contacto y despues servicios/ICP. |
| SERP -> sitios con formulario o telefono pero sin email visible | `asesoriaentenerife.es` expone telefono y formulario, pero no email visible en la pagina principal | Baja | Media | Media | Bajo | Bajo | Medio | `WATCH` | Puede servir para `form` u `other_direct`, pero no es un buen carril email-first salvo que el email aparezca en una subpagina. |

### 3.2 `google_maps`

| Fuente/patron | Evidencia actual | Email probability | Authority | ICP density | Technical cost | Blocking risk | Expected noise | Status | Lectura operativa |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| Ficha first-party de Google Business / Google Maps | `openplusasesores.es` enlaza a su ficha de Maps y a sus Google Reviews; en organic aparece la referencia explicita a su `Google Business` | Media | Muy alta | Alta | Alto | Alto | Medio | `WATCH` | Sigue siendo un carril de alto valor, pero la viabilidad tecnica con Scrapling sigue abierta. No lo meto en piloto principal sin microprueba previa. |
| Handoff `Google Maps -> web propia enlazada` | Casos como OpenPlus conectan bien ficha local + web propia; en directorios que republican Maps se ve a veces `sitio web` disponible y a veces `No disponible` | Media-alta | Alta | Alta | Medio-alto | Alto | Medio | `WATCH` | Puede ser rentable si Maps deja llegar a la web. El problema no es el website final, sino el acceso estable a la ficha. |
| Republishers de Maps tipo `ccasesoria.com` | Republican direccion, actividad, reseñas y `Ver en Google Maps`; en algunos negocios el `sitio web` es `No disponible` y en otros si existe | Baja-media | Baja-media | Media | Bajo | Bajo | Alto | `DROP` | Introducen duplicados, pierden first-party context y degradan la trazabilidad. Sirven como control auxiliar, no como fuente del piloto. |

### 3.3 `specialized_directory`

| Fuente/patron | Evidencia actual | Email probability | Authority | ICP density | Technical cost | Blocking risk | Expected noise | Status | Lectura operativa |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| `AAFC - Despachos Profesionales` | La home publica `Buscador despachos profesionales`; la microvalidacion con Scrapling sobre `/servicios/despachos-profesionales/` detecta emails reales en el directorio | Alta | Alta | Muy alta | Medio | Bajo | Medio-bajo | `PASS` | Pasa discovery y pasa validacion tecnica con Scrapling. Es hoy la mejor fuente sectorial para piloto. |
| `Colegio de Gestores Administrativos de Santa Cruz de Tenerife - Localiza tu GA + PDF` | `Localiza tu GA` carga con Scrapling, pero la microvalidacion del PDF no devuelve emails extraibles; el flujo observado cae en `docs.google.com/gview` | Alta | Alta | Media-alta | Medio | Bajo | Medio | `WATCH` | Sigue siendo prometedora, pero no la meteria al piloto principal sin una prueba mas especifica del PDF o del buscador real. |
| `Colegio de Gestores Administrativos de Las Palmas - Localiza tu GA` | Existe localizador con especialidades y busqueda por direccion, pero en HTML estatico no aparece un listado publico equivalente al PDF de Tenerife | Media | Alta | Media-alta | Medio | Bajo | Medio | `WATCH` | Promete cobertura provincial util, pero antes del piloto conviene verificar si Scrapling puede materializar resultados sin depender de interaccion dificil. |
| `Colegio Oficial de Economistas de Las Palmas - Directorio de colegiados` | El directorio permite buscar por apellidos/localidad y solo expone `numero de colegiado`, `apellidos` y `nombre` en la vista publica observada | Baja | Alta | Media | Medio | Bajo | Medio-alto | `WATCH` | Buena fuente de precision profesional, pero floja para emailing. Podria servir mas para enrichment que para sourcing. |
| `COETE` / `COTIME` institucional | Los sitios muestran contacto institucional, formacion y transparencia, pero no un listado publico equivalente con email de despachos en la evidencia revisada | Baja | Alta | Media | Bajo | Bajo | Alto | `DROP` | Utiles como fuentes institucionales o de contexto, no como columna vertebral del piloto email-first. |

## 4. Control y baseline

| Fuente | Rol | Decision |
|---|---|---|
| `Paginas Amarillas` | Benchmark/control historico contra Experimento 0 | No entra en el diseno del piloto. Solo sirve para comparar yield, ruido y duplicados. |

## 5. Shortlist recomendada para piloto

Si apruebas el Checkpoint 2, mi recomendacion es pilotar solo estas 2 fuentes:

1. `google_basic / webs propias con email visible`
2. `specialized_directory / AAFC - Despachos Profesionales`

Y dejar fuera del piloto principal, por ahora:

- `Gestores Tenerife / Localiza tu GA + PDF` como `WATCH` tecnico
- `google_maps` como `WATCH` tecnico
- `Colegio de Gestores de Las Palmas` como `WATCH` por incertidumbre de extraccion
- `Economistas Las Palmas` como `WATCH` porque hoy parece mas enrichment que contacto

## 6. Recomendacion operativa de muestra

Si das luz verde al piloto:

- `google_basic`: 10-15 registros centrados en `contacto`, `team/about` y `home/servicios` con email visible
- `AAFC`: 10-15 registros distribuidos entre Gran Canaria y Tenerife si el buscador lo permite
- `Gestores Tenerife`: no entra en el piloto principal; si quieres rescatarla, haria antes una microprueba dedicada al PDF real o al buscador provincial

## 7. Unknown, riesgos y siguiente paso

### Unknown

- `Unknown`: viabilidad real de `google_maps` con Scrapling sin proxies complejos
- `Unknown`: cobertura real de email frente a formulario en `google_basic` cuando salgamos de ejemplos sueltos y entremos en muestra sistematica
- `Unknown`: si el directorio/PDF de Gestores Tenerife puede bypassear `gview` y entregar contactos reutilizables de forma estable

### Riesgos

- Duplicados altos entre `AAFC`, `google_basic` y colegios si el mismo despacho aparece en varias fuentes
- Sesgo comercial si tratamos igual emails nominales, emails genericos y formularios
- Coste oculto de limpieza si el directorio colegial devuelve personas y no empresas
- Falso positivo metodologico si tratamos `Gestores Tenerife` como validada cuando hoy solo pasa el entrypoint, no el contacto reusable

### Siguiente paso inmediato

Cerrar Checkpoint 2. Necesito aprobacion explicita sobre esta shortlist:

- `google_basic / webs propias con email visible`: `pass`
- `AAFC / Despachos Profesionales`: `pass`
- `Gestores Tenerife / Localiza tu GA + PDF`: `watch`
- `google_maps`: `watch`
- `Gestores Las Palmas`: `watch`
- `Economistas Las Palmas`: `watch`

Con esa aprobacion paso a Fase 3 y preparo el piloto acotado en `05_scratch/experimento_1/`.

## 8. Referencias consultadas

- `https://jmsconsulting.es/contacto/`
- `https://gestoriavegalujan.es/contacto/`
- `https://asesoriafiscaltenerife.es/`
- `https://unificont.es/`
- `https://www.asesoramientostenerife.com/`
- `https://fiscaltaxcanarias.com/servicios/`
- `https://openplusasesores.es/`
- `https://asesoresfiscalesdecanarias.org/`
- `https://gestorestenerife.org/localiza-ga/`
- `https://gestorestenerife.org/wp-content/uploads/2022/10/Listado_Colegiados_Web.pdf`
- `https://www.gestoreslaspalmas.org/localiza-ga/`
- `https://www.economistaslaspalmas.org/colegiados/`
- `https://ccasesoria.com/las-palmas/las-palmas-de-gran-canaria/asesoria-romero-s-l-113/`
- `https://ccasesoria.com/las-palmas/las-palmas-de-gran-canaria/asesoria-fiscal-y-contable-service-s-l-324/`
- `https://ccasesoria.com/las-palmas/las-palmas-de-gran-canaria/openplus-asesores-669/`
