"""Mapa do Brasil em matriz de pontos (um unico <path>) + posicoes dos 12 pins.
Fonte: IBGE, malha do pais (qualidade minima), em tools/dados/ (dado externo, lido so com json). Uso: python3 -I tools/gen_brasil.py"""
import json, math, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
d = json.loads((ROOT / "tools" / "dados" / "brasil-ibge-minima.geojson").read_text())
geoms = [f["geometry"] for f in d["features"]]
polys = []
for g in geoms:
    polys += g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
rings = [p[0] for p in polys]
LAT0, K = -15.0, math.cos(math.radians(15))
lon_min, lon_max, lat_min, lat_max = -74.2, -34.4, -34.2, 5.6
S = 16.0                                  # px por grau de latitude
W, H = round((lon_max - lon_min) * K * S), round((lat_max - lat_min) * S)
proj = lambda lon, lat: ((lon - lon_min) * K * S, (lat_max - lat) * S)

def dentro(x, y, ring):
    c = False
    j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i]; xj, yj = ring[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            c = not c
        j = i
    return c

STEP = 10.5
pts = []
y = STEP / 2
while y < H:
    x = STEP / 2 + (STEP / 2 if int(y // STEP) % 2 else 0)
    while x < W:
        lon, lat = x / (K * S) + lon_min, lat_max - y / S
        if any(dentro(lon, lat, r) for r in rings):
            pts.append((x, y))
        x += STEP
    y += STEP
path = "".join(f"M{x:.0f} {y:.0f}h0" for x, y in pts)
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" fill="none" stroke="#0B1B3F" stroke-opacity=".34" stroke-width="5.2" stroke-linecap="round">'
       f'<path d="{path}"/></svg>')
(ROOT / "assets" / "svg" / "brasil-pontos.svg").write_text(svg)

# Mapa com divisas dos estados (IBGE, malha por UF, qualidade minima): mesma projecao e viewBox da matriz de pontos, entao os pins servem nos dois.
uf = json.loads((ROOT / "tools" / "dados" / "brasil-ibge-uf-minima.geojson").read_text())
def anel(r):
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in (proj(lon, lat) for lon, lat in r)) + "Z"
estados = []
for f in uf["features"]:
    g = f["geometry"]
    for poly in (g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]):
        estados.append("".join(anel(r) for r in poly))
svg_uf = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" fill="#0B1B3F" stroke="#9CC3F0" stroke-opacity=".75" stroke-width="2" stroke-linejoin="round">'
          f'<path d="{"".join(estados)}"/></svg>')
(ROOT / "assets" / "svg" / "brasil-estados.svg").write_text(svg_uf)

CIDADES = [("Manaus/AM", -3.12, -60.02), ("Ananindeua/PA", -1.37, -48.38), ("Sinop/MT", -11.86, -55.50), ("Cuiabá/MT", -15.60, -56.10),
           ("Goiânia/GO", -16.68, -49.25), ("Uberlândia/MG", -18.92, -48.28), ("Contagem/MG", -19.92, -43.94), ("São Paulo/SP", -23.55, -46.63),
           ("Araçatuba/SP", -21.21, -50.43), ("Curitiba/PR", -25.43, -49.27), ("Itajaí/SC", -26.91, -48.66), ("Porto Alegre/RS", -30.03, -51.23)]
pins = []
for i, (n, lat, lon) in enumerate(CIDADES):
    px, py = proj(lon, lat)
    pins.append(f'<a class="pin" href="{{{{R}}}}stub.html?u=/unidades/" style="left:{px/W*100:.2f}%;top:{py/H*100:.2f}%;--i:{i}"><span class="l">{n}</span></a>')
(ROOT / "src" / "parts").mkdir(exist_ok=True)
# pins.html agora tem foto no hover e link por unidade (feito a mao em build/parts): este script NAO sobrescreve mais
if not (ROOT / "src" / "parts" / "pins.html").exists():
    (ROOT / "src" / "parts" / "pins.html").write_text("".join(pins))
print(f"{len(pts)} pontos, {len(svg)/1024:.1f} KB, viewBox {W}x{H}, razao {W/H:.3f}")
