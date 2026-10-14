"""Monta assets/svg/sprite.svg com os icones Phosphor (regular, OFL) realmente usados.
Fonte: pacote npm @phosphor-icons/core (baixado fora do repo). Uso: python3 -I tools/gen_sprite.py <pasta assets/regular>"""
import re, sys, pathlib
SRC = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "svg" / "sprite.svg"
NOMES = ["house","squares-four","funnel","map-pin","pencil-simple-line","whatsapp-logo","list","x","arrow-right","arrow-up-right",
         "arrow-left","phone","magnifying-glass","caret-down","caret-right","plus","minus","instagram-logo","facebook-logo","linkedin-logo",
         "tractor","truck-trailer","factory","anchor","train","mountains","lightning","seal-check","crosshair","gear","drop","wind",
         "navigation-arrow","check","gas-pump","snowflake","cylinder","hard-hat","certificate","package","stack"]
sym = []
for n in NOMES:
    s = (SRC / f"{n}.svg").read_text()
    inner = re.search(r'<svg[^>]*>(.*)</svg>', s, re.S).group(1).strip()
    sym.append(f'<symbol id="i-{n}" viewBox="0 0 256 256">{inner}</symbol>')
OUT.write_text('<svg xmlns="http://www.w3.org/2000/svg" style="display:none">' + "".join(sym) + "</svg>")
print(len(NOMES), "icones,", OUT.stat().st_size, "bytes")
