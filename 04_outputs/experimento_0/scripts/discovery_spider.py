"""
Fase 3 — Spider de descubrimiento.
Parte de las URLs de fichas extraidas en Fase 2 y visita cada una
para extraer datos adicionales (descripcion, horario, resenas, web propia).
"""
from scrapling.spiders import Spider, Request, Response
import json


# Cargar URLs de fichas desde datos de Fase 2
def load_fichas(path="05_scratch/data/paginas_amarillas_canarias.json"):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [d for d in data if d.get('url_ficha')]


class DespachoSpider(Spider):
    name = "despachos_canarias"
    concurrent_requests = 3  # conservador para respetar rate limits
    download_delay = 1.5

    def __init__(self, **kwargs):
        fichas = load_fichas()
        self.start_urls = [f['url_ficha'] for f in fichas[:30]]  # limitar a 30 para el experimento
        self._fichas_lookup = {f['url_ficha']: f for f in fichas}
        super().__init__(**kwargs)

    async def parse(self, response: Response):
        url = str(response.url)
        base_data = self._fichas_lookup.get(url, {})

        # Extraer datos adicionales de la ficha
        descripcion = response.css('.descripcion-actividad::text').get('')
        horario = response.css('[class*="horario"]::text').getall()
        web_propia = ''
        for a in response.css('a[rel="nofollow noopener"]'):
            href = a.attrib.get('href', '')
            if href and 'paginasamarillas' not in href and 'beedigital' not in href and 'google' not in href:
                web_propia = href
                break

        # Resenas
        resenas_count = len(response.css('[class*="opinion"], [class*="review"], [class*="comentario"]'))

        # Actividades/servicios
        actividades = response.css('[class*="actividad"] a::text').getall()

        yield {
            **base_data,
            'descripcion': descripcion.strip(),
            'horario': ' | '.join(h.strip() for h in horario if h.strip()),
            'web_propia': web_propia,
            'tiene_web_propia': bool(web_propia),
            'resenas_count': resenas_count,
            'actividades_extra': [a.strip() for a in actividades if a.strip()],
        }


if __name__ == "__main__":
    spider = DespachoSpider(crawldir="05_scratch/data/crawl_despachos")
    result = spider.start()
    print(f"\nItems scraped: {len(result.items)}")

    # Guardar resultados
    output_path = "05_scratch/data/despachos_enriquecidos.json"
    result.items.to_json(output_path)
    print(f"Guardados en {output_path}")

    # Estadisticas rapidas
    con_web = sum(1 for i in result.items if i.get('tiene_web_propia'))
    con_desc = sum(1 for i in result.items if i.get('descripcion'))
    print(f"\nEstadisticas:")
    print(f"  Con web propia: {con_web}/{len(result.items)}")
    print(f"  Con descripcion: {con_desc}/{len(result.items)}")
