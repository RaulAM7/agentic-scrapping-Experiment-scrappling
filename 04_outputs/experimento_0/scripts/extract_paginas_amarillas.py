"""
Fase 2 — Extraccion de asesorias desde Paginas Amarillas (Canarias)
Busca multiples categorias en Las Palmas y Tenerife, extrae datos estructurados.
"""
from scrapling.fetchers import Fetcher
import json
import time

SEARCHES = [
    ("asesoria-fiscal", "las-palmas"),
    ("asesoria-fiscal", "santa-cruz-de-tenerife"),
    ("gestoria-administrativa", "las-palmas"),
    ("gestoria-administrativa", "santa-cruz-de-tenerife"),
    ("asesoria-de-empresas", "las-palmas"),
    ("asesoria-de-empresas", "santa-cruz-de-tenerife"),
]

BASE_URL = "https://www.paginasamarillas.es/a/{category}/{province}/"


def extract_page(url: str) -> list[dict]:
    page = Fetcher.get(url)
    items = page.css('.listado-item')
    results = []
    for item in items:
        nombre = item.css('span[itemprop="name"]::text').get('').strip()
        if not nombre:
            continue
        direccion = item.css('span[itemprop="streetAddress"]::text').get('').strip()
        localidad = item.css('span[itemprop="addressLocality"]::text').get('').strip()
        telefono = (item.css('a[data-omniclick="phone"]::text').get('') or
                    item.css('[itemprop="telephone"]::text').get('') or '').strip()
        url_ficha = item.css('a[data-omniclick="name"]::attr(href)').get('')
        analytics_raw = item.attrib.get('data-analytics', '{}')
        try:
            analytics = json.loads(analytics_raw)
            actividad = analytics.get('activity', '')
            provincia = analytics.get('province', '')
        except (json.JSONDecodeError, TypeError):
            actividad, provincia = '', ''

        results.append({
            'nombre': nombre,
            'actividad': actividad,
            'direccion': direccion,
            'localidad': localidad,
            'provincia': provincia,
            'telefono': telefono,
            'url_ficha': url_ficha,
        })
    return results


def main():
    all_results = []
    seen_names = set()

    for category, province in SEARCHES:
        url = BASE_URL.format(category=category, province=province)
        print(f"\n--- Buscando: {category} en {province} ---")
        try:
            results = extract_page(url)
            new = 0
            for r in results:
                key = r['nombre'].lower()
                if key not in seen_names:
                    seen_names.add(key)
                    all_results.append(r)
                    new += 1
            print(f"  Encontrados: {len(results)}, nuevos: {new}")
        except Exception as e:
            print(f"  ERROR: {e}")
        time.sleep(1)  # rate limiting etico

    # Guardar resultados
    output_path = "05_scratch/data/paginas_amarillas_canarias.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print(f"\n=== TOTAL: {len(all_results)} despachos unicos guardados en {output_path} ===")


if __name__ == "__main__":
    main()
