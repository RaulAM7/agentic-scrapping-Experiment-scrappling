# keep.eu source assessment

Fecha de assessment: 2026-05-31.

## 1. Source overview

keep.eu es una base de datos publica y consultable mantenida por Interact para agregar informacion de programas, proyectos, partners, partnerships y calls de cooperacion territorial europea. La propia plataforma indica que cubre los periodos 2000-2006, 2007-2013 y 2014-2020, y que esta incorporando 2021-2027.

Para este caladero, keep.eu es valiosa porque permite:

- localizar programas y proyectos Interreg;
- filtrar por periodo, geografia, tipologia de programa y temas;
- detectar entidades participantes y su rol;
- revisar objetivos, outputs, logros y documentos;
- identificar programas con calls en curso o futuras;
- reutilizar URLs estables de busqueda;
- exportar parte de la informacion a Excel;
- solicitar acceso a API open data.

## 2. Secciones relevantes a explorar

- `Projects and documents` — Confirmed.
- `Programmes` — Confirmed.
- `Partners` — Confirmed.
- `Partnerships` — Confirmed como capa de datos y metrica publica; `Unknown` como seccion de navegacion independiente.
- `Countries and regions` — Confirmed.
- `Calls for projects` — Confirmed.
- `Statistics` — Confirmed.
- `Search` — Confirmed.
- `Downloads / exports` — Confirmed.

## 3. Opciones de extraccion detectadas

| Opcion | Estado | Notas |
| --- | --- | --- |
| export GUI | Confirmed | Hay botones `Export to Excel` en paginas de programa y en otras areas. keep.eu ademas comunica que mejoro "all of keep.eu's Excel exports". |
| descarga XLSX/Excel | Confirmed | La plataforma habla explicitamente de `Export to Excel`. No se verifico la extension exacta del fichero en esta pasada. |
| descarga CSV | Not found | No encontre evidencia publica de export CSV en la GUI ni en la FAQ revisada. |
| filtros | Confirmed | Projects and documents permite keywords, campos, idiomas, geografia, periodo, tipo de programa, programa, temas, tiempo, presupuesto, public/private y tipo de organizacion. Programmes permite periodo, tipo, geografia, calls en curso y filtros tematicos. |
| API documentada | Confirmed | Existe `https://keep.eu/api/open-data` con FAQ publica y estructura documentada. |
| endpoints internos/publicos | Confirmed | Se observan endpoints publicos de export y adjuntos, por ejemplo `api/open-data` y `api/project-attachment/{id}/get_file/`. |
| paginas HTML scrapeables | Confirmed | Las paginas de programa, proyecto, FAQ y representatividad son scrapeables con HTML accesible. |
| documentos descargables | Confirmed | keep.eu almacena documentos de proyecto y enlaces directos de descarga. |

## 4. Interreg MAC dentro de keep.eu

Hallazgos confirmados:

- Existe el programa `2014 - 2020 INTERREG V-A Spain - Portugal (Madeira - Açores - Canarias (MAC))` en keep.eu.
- La pagina publica confirmada es: `https://keep.eu/programmes/83/2014-2020-Spain-Portugal-Madeira-Acores/`
- En esa pagina aparece geografia elegible para:
  - Espana / Canarias;
  - Portugal / Madeira y Azores;
  - Cabo Verde;
  - Mauritania;
  - Senegal.
- La pagina de programa confirma objetivos alineados con este caladero, por ejemplo:
  - competitividad de SMEs;
  - transferencia y difusion de tecnologia;
  - cooperacion entre empresas y universidades;
  - servicios de apoyo empresarial.

Puntos no cerrados:

- `Interreg MAC` exacto en 2021-2027 como pagina publica claramente localizable en keep.eu: `Unknown`.
- Variante exacta visible como `Interreg VI-D MAC`, `Interreg Madeira-Azores-Canarias` o similar: `Unknown`.

Inferencia util, no hecho duro:

- La pagina de representatividad de keep.eu muestra `Outermost regions` con `0` proyectos `2021-2027` en keep.eu sobre `65` del sector en el momento revisado. Esto sugiere que la cobertura publica actual de proyectos 2021-2027 para outermost regions, donde encajaria MAC, esta todavia incompleta o no publicada de forma util para este caladero.

## 5. Riesgos de extraccion

- paginacion: `Likely`; las listas y resultados pueden requerir navegacion por resultados.
- filtros dinamicos: `Confirmed`; buena parte del valor esta en combinaciones de filtros y vistas.
- posibles bloqueos: `Unknown`; no vi evidencia publica de rate limits web, pero conviene operar con prudencia.
- datos incompletos: `Confirmed`; keep.eu admite diferencias de cobertura y missing fields por programa.
- duplicados: `Confirmed`; keep.eu explica que una misma entidad puede aparecer con nombres distintos y que el concepto de partner no equivale a entidad unica limpia.
- cambios de estructura: `Likely`; la plataforma sigue incorporando 2021-2027 y ha lanzado API y mejoras recientes.
- limitaciones de export: `Confirmed`; no todo esta disponible como dataset simple y el acceso API requiere clave aprobada.
- terminos/robots: `Confirmed`; `robots.txt` solo bloquea `/wp-admin/`. Los terminos permiten copiar y redistribuir datos y archivos con atribucion a keep.eu y enlace a la fuente.
- geocodificacion imperfecta: `Confirmed`; keep.eu documenta errores posibles de region/ubicacion.
- lenguaje: `Confirmed`; keep.eu advierte que la deteccion de idioma falla mas en textos cortos.
- recencia documental: `Confirmed`; los documentos se recopilan tras el cierre de proyectos, asi que no son la mejor fuente para actividad reciente.

## 6. Recomendacion de extraccion

Metodo inicial recomendado:

1. `Export manual + URLs estables + enriquecimiento selectivo`.
2. `API` como siguiente mejor opcion, pero solo tras pedir clave.
3. `Scraping HTML` solo donde no exista export util ni respuesta API disponible.

Razon:

- La GUI ya ofrece filtros potentes y exportaciones Excel.
- Hay URLs estables para repetir consultas actualizadas sin reconstruir filtros cada vez.
- La API existe y es mas limpia para escalar, pero no es de acceso anonimo: requiere registro y aprobacion de clave.
- El HTML publico es util para complementar metadatos de programa/proyecto o comprobar gaps, pero no deberia ser la primera via si ya existe export.

Decision practica para este caladero:

- Para `Interreg MAC 2014-2020`, empezar por pagina de programa, projects/documents y representatividad/export.
- Para `2021-2027`, no asumir que MAC esta ya explotable dentro de keep.eu; validar primero si aparece como programa publico o si conviene trabajar temporalmente con filtros geograficos y calls/programmes de outermost regions o Atlantic Area.

## 7. Proximo paso recomendado

Recomendacion:

- `Wave 0` primero.

Acciones concretas de Wave 0:

- localizar manualmente en GUI el mejor filtro replicable para MAC;
- guardar URLs estables de 3 a 5 consultas base;
- descargar 1 a 3 exports pequenos de referencia;
- verificar si el programa MAC 2021-2027 existe publicamente o si hay que trabajar por proxy geografia + tipo de programa;
- solicitar API key a keep.eu si el canal va a escalar.

## Fuentes verificadas

- https://keep.eu/
- https://keep.eu/about-keep-eu/
- https://keep.eu/projects/
- https://keep.eu/programmes/
- https://keep.eu/programmes/83/2014-2020-Spain-Portugal-Madeira-Acores/
- https://keep.eu/representativeness/
- https://keep.eu/faq/api-how-to-access-keep_eu-data-in-open-data-format/
- https://keep.eu/faq/documents-what-is-a-document-for-keep-eu-how-can-an-exact-document-be-found-in-keep-eu/
- https://keep.eu/faq/calls-for-projects-in-keep-eu/
- https://keep.eu/faq/get-results-url-what-is-it/
- https://keep.eu/terms-of-use/
- https://keep.eu/robots.txt
