# Scrapling Validation - Experimento 1

- Fecha: 2026-03-07
- Scope: microvalidacion tecnica con Scrapling API Python sobre las 3 fuentes `pass` de Fase 2

## Veredicto

### Google Basic -> webs propias con email visible

- Status tecnico: `PASS_TECH`
- Fetcher recomendado: `Fetcher`
- Veredicto: Fetcher carga varias webs propias y extrae emails visibles sin necesitar browser.

- `Fetcher` `https://jmsconsulting.es/contacto/` -> status `200`, emails `asesoria@jmsconsulting.es`, phones `1739797278, 1739969630, 1739969678`
- `Fetcher` `https://unificont.es/` -> status `200`, emails `direccion@unificont.es`, phones `1769356490, 1772177469, 1772177470`
- `Fetcher` `https://asesoriafiscaltenerife.es/` -> status `200`, emails `javier@asesoriafiscaltenerife.es, sandra@asesoriafiscaltenerife.es, sonsoles@asesoriafiscaltenerife.es, veronica@asesoriafiscaltenerife.es`, phones `1634734870, 670846472, 905943278`

### AAFC / Despachos Profesionales

- Status tecnico: `PASS_TECH`
- Fetcher recomendado: `Fetcher`
- Veredicto: Scrapling localiza el directorio o al menos un entrypoint usable del buscador/despachos.

- `Fetcher` `https://asesoresfiscalesdecanarias.org/` -> status `200`, emails `none`, phones `1395214731, 1772823856, 2147483647`
- `Fetcher` `https://asesoresfiscalesdecanarias.org/despachos-profesionales/` -> status `200`, emails `fiscal@asesoriahdez.com, asesoria@rygasesor.com, ramon@rcallero.es, galco2782@gmail.com`, phones `1772823890, 2147483647, 22533333333333`

### Gestores Tenerife / Localiza tu GA + PDF

- Status tecnico: `WATCH`
- Fetcher recomendado: `Fetcher`
- Veredicto: El entrypoint carga, pero el listado reusable no queda suficientemente demostrado.

- `Fetcher` `https://gestorestenerife.org/localiza-ga/` -> status `200`, emails `colgestfe@gestores.net`, phones `1744364139, 00106240502, 1475650289497`
- `Fetcher` `https://docs.google.com/gview?embedded=true&url=https://gestorestenerife.org/wp-content/uploads/2022/10/Listado_WEB.pdf` -> status `200`, emails `none`, phones `1772925975000`
