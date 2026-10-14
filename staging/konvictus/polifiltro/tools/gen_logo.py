"""Extrai o logo vetorial real (NAS) em variantes: cor, claro (p/ fundo navy), marca (cilindro) e 'desde 1989'.
Uso: python3 -I tools/gen_logo.py  (le o SVG do NAS, escreve em assets/svg/)"""
import re, pathlib
SRC = pathlib.Path("/Volumes/arquivos/clientes/konvictus/Projetos/Polifiltro/Contexto/Brutos/img/logo-vetor/logo-polifiltro-1989.svg")
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "svg"
s = SRC.read_text()
paths = re.findall(r'<path[^>]*d="([^"]+)"', s)
word, cyl, desde = paths[0:10], paths[10:15], paths[15:24]
rnd = lambda d: re.sub(r'(\d+\.\d{1})\d+', r'\1', d)   # 1 casa decimal basta no logo (<=40px de altura)
def svg(vb, groups):
    body = "".join(f'<path fill="{c}" d="{rnd(d)}"/>' for c, ds in groups for d in ds)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{body}</svg>'
BLUE, GREY = "#3B73B9", "#5F6062"
ICE, ICEGREY = "#EBF3F2", "#B9C6D8"
(OUT/"logo.svg").write_text(svg("54 200 735 192", [(BLUE, word), (GREY, cyl)]))
(OUT/"logo-claro.svg").write_text(svg("54 200 735 192", [(ICE, word), (ICEGREY, cyl)]))
(OUT/"logo-completo.svg").write_text(svg("54 200 735 192", [(BLUE, word), (GREY, cyl), (GREY, desde)]))
(OUT/"logo-completo-claro.svg").write_text(svg("54 200 735 192", [(ICE, word), (ICEGREY, cyl), (ICEGREY, desde)]))
(OUT/"marca.svg").write_text(svg("271 201 185 192", [(GREY, cyl)]))
for f in ("logo", "logo-claro", "logo-completo", "logo-completo-claro", "marca"):
    print(f, (OUT/f"{f}.svg").stat().st_size, "bytes")
