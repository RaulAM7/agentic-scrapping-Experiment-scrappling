# STACK

- Runtime/framework: Python 3.12.3, Scrapling 0.4.1
- Project layout conventions: venv en `.venv/`, scripts en `05_scratch/scripts/`, datos en `05_scratch/data/`
- Build/test/dev commands:
  - Activar entorno: `source .venv/bin/activate`
  - Instalar deps: `pip install "scrapling[all]"` + `scrapling install`
  - Shell interactivo: `scrapling shell`
  - CLI extract: `scrapling extract get <url> <output>`
  - MCP server: configurado como `ScraplingServer` en Claude Code
