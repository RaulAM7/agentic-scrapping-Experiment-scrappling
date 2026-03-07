"""
Fase 2 — Extraccion del directorio de colegiados del Colegio de Economistas de Las Palmas.
Requiere DynamicFetcher (tabla carga via JS).
"""
from scrapling.fetchers import DynamicFetcher
import json


def main():
    print("Cargando directorio de colegiados...")
    page = DynamicFetcher.fetch(
        'https://www.economistaslaspalmas.org/colegiados/',
        headless=True,
        network_idle=True,
    )

    table = page.css('table')
    if not table:
        print("ERROR: No se encontro tabla")
        return

    rows = table[0].css('tr')
    colegiados = []
    for row in rows[1:]:  # skip header
        cells = row.css('td')
        if len(cells) >= 3:
            num = cells[0].css('::text').get('').strip()
            apellidos = cells[1].css('::text').get('').strip()
            nombre = cells[2].css('::text').get('').strip()
            if apellidos:
                colegiados.append({
                    'num_colegiado': num,
                    'apellidos': apellidos,
                    'nombre': nombre,
                    'nombre_completo': f"{nombre} {apellidos}".strip(),
                })

    output_path = "05_scratch/data/colegio_economistas_lp.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(colegiados, f, ensure_ascii=False, indent=2)

    print(f"Total colegiados extraidos: {len(colegiados)}")
    print(f"Guardados en {output_path}")
    for c in colegiados[:5]:
        print(f"  {c['num_colegiado']} - {c['nombre_completo']}")


if __name__ == "__main__":
    main()
