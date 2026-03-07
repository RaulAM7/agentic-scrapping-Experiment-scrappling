# Fase 0 — Setup Log

Fecha: 2026-03-07

## Entorno

- OS: Linux 6.14.0-36-generic (Ubuntu)
- Python: 3.12.3
- Scrapling: 0.4.1
- Instalacion: `pip install "scrapling[all]"` (parser + fetchers + MCP + shell)

## Instalacion

1. `python3 -m venv .venv` — sin problemas
2. `pip install "scrapling[all]"` — instalacion limpia, sin conflictos de dependencias
3. `scrapling install` — **fallo**: requiere `sudo` para `playwright install-deps` (dependencias del sistema)
   - **Workaround**: instalar browsers directamente: `python -m playwright install chromium` + `python -m patchright install chromium`
   - Las dependencias del sistema ya estaban presentes en este equipo
   - **Friccion**: en un sistema limpio, el usuario necesitaria ejecutar `sudo playwright install-deps chromium` manualmente antes de `scrapling install`, o ejecutar `scrapling install` con sudo. Esto no esta bien documentado en el README.

## Verificacion de fetchers

| Fetcher | Resultado | Notas |
|---------|-----------|-------|
| `Fetcher.get()` | OK | HTTP puro, rapido, sin problemas |
| `StealthyFetcher.fetch()` | OK | Headless, bypass anti-bot |
| `DynamicFetcher.fetch()` | OK | Playwright Chromium headless |

Todos devolvieron 10 quotes de `quotes.toscrape.com` correctamente.

## MCP Server

- Configurado via `claude mcp add ScraplingServer`
- Path: `/home/reboot/Escritorio/agentic-scrapping-Experiment-scrappling/.venv/bin/scrapling mcp`
- Pendiente de verificacion funcional (requiere reinicio de sesion Claude Code)

## Fricciones encontradas

1. **`scrapling install` necesita sudo** — no queda claro en la documentacion. Hay que separar la instalacion de browsers (`playwright install`) de las dependencias del sistema (`playwright install-deps`).
2. **Patchright no se menciona explicitamente** — StealthyFetcher usa Patchright (fork de Playwright), no Playwright directamente. El usuario debe saber instalar ambos browsers.
3. **Por lo demas, setup limpio** — pip install funciono sin conflictos, los tres fetchers funcionan correctamente.

## Criterios de exito

- [x] `Fetcher.get()` devuelve pagina correcta
- [x] `StealthyFetcher.fetch()` funciona con headless
- [x] `DynamicFetcher.fetch()` funciona con headless
- [x] MCP server configurado (verificacion funcional pendiente reinicio)
- [x] Setup documentado con fricciones
