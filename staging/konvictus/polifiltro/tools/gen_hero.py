"""Gera a arte do hero "A passagem pelo filtro" (SVG estatico, deterministico).

Saidas em assets/svg/:
  hero-cilindro.svg   o cilindro inclinado da marca, em corte, com pregas de midia filtrante
  hero-sujo.svg       tira de particulas escuras (periodo = largura do palco, 2 copias via <use>)
  hero-limpo.svg      tira de linhas azuis paralelas (idem)
E imprime os poligonos de recorte (em %) que o CSS usa para a tira "morrer" na parede do cilindro.

Sistema de coordenadas: palco 1600 x 900, igual para as tres camadas (alinham em qualquer tamanho).
Uso: python3 -I tools/gen_hero.py
"""
import math, random, pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "svg"
W, H = 1600, 900
TH = math.radians(54.6)                 # inclinacao do eixo (a do logo)
A = (math.cos(TH), -math.sin(TH))       # eixo: sobe para a direita
N = (math.sin(TH), math.cos(TH))        # perpendicular (aponta para a direita-baixo)
C = (1010, 430)                         # centro do cilindro
R, L, RATIO = 150, 700, 0.36            # raio, comprimento, achatamento das elipses
BAND = (150, 650)                       # faixa vertical onde corre o fluxo

NAVY, NAVY2, NAVY3 = "#0B1B3F", "#10265A", "#173474"
BLUE, BLUE_HI = "#3B73B9", "#8FB4E3"
ICE, ICEGREY = "#EBF3F2", "#B9C6D8"

f = lambda v: f"{v:.1f}".rstrip("0").rstrip(".")
add = lambda p, q, k=1: (p[0] + q[0] * k, p[1] + q[1] * k)
Ct, Cb = add(C, A, L / 2), add(C, A, -L / 2)
rot_n = math.degrees(math.atan2(N[1], N[0]))


def x_left(y):
    """x da parede esquerda do cilindro na altura y."""
    p0 = add(C, N, -R)
    return p0[0] + (y - p0[1]) * (A[0] / A[1])


CHORD = 2 * R / math.sin(TH)             # largura horizontal do cilindro
x_right = lambda y: x_left(y) + CHORD


def cilindro():
    pl_b, pr_b = add(Cb, N, -R), add(Cb, N, R)
    pl_t, pr_t = add(Ct, N, -R), add(Ct, N, R)
    body = " ".join(f"{f(p[0])},{f(p[1])}" for p in (pl_b, pr_b, pr_t, pl_t))
    folds = []
    n_folds = 15
    for k in range(1, n_folds):
        u = -R + 2 * R * k / n_folds
        a_, b_ = add(Cb, N, u), add(Ct, N, u)
        folds.append(f"M{f(a_[0])} {f(a_[1])}L{f(b_[0])} {f(b_[1])}")
    ell = lambda c, rx, ry, extra: (
        f'<ellipse cx="{f(c[0])}" cy="{f(c[1])}" rx="{f(rx)}" ry="{f(ry)}" '
        f'transform="rotate({f(rot_n)} {f(c[0])} {f(c[1])})" {extra}/>'
    )
    wall = lambda p, q: f'M{f(p[0])} {f(p[1])}L{f(q[0])} {f(q[1])}'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" fill="none">
<defs><linearGradient id="g" gradientUnits="userSpaceOnUse" x1="{f(add(C,N,-R)[0])}" y1="{f(add(C,N,-R)[1])}" x2="{f(add(C,N,R)[0])}" y2="{f(add(C,N,R)[1])}"><stop offset="0" stop-color="{NAVY3}"/><stop offset=".5" stop-color="{NAVY2}"/><stop offset="1" stop-color="{NAVY3}"/></linearGradient></defs>
<polygon points="{body}" fill="url(#g)" fill-opacity=".97"/>
<path d="{''.join(folds)}" stroke="{BLUE}" stroke-opacity=".28" stroke-width="1.6"/>
{ell(Ct, R, R*RATIO, f'fill="{NAVY}" stroke="{ICEGREY}" stroke-width="5"')}
{ell(Ct, R*.78, R*RATIO*.78, f'stroke="{BLUE}" stroke-opacity=".35" stroke-width="1.6"')}
<path d="{wall(add(Cb,N,-R), add(Ct,N,-R))}{wall(add(Cb,N,R), add(Ct,N,R))}" stroke="{ICEGREY}" stroke-width="5" stroke-linecap="round"/>
{ell(Cb, R, R*RATIO, f'fill="{NAVY3}" stroke="{ICEGREY}" stroke-width="5"')}
{ell(Cb, R*.62, R*RATIO*.62, f'stroke="{BLUE}" stroke-opacity=".45" stroke-width="1.6"')}
{ell(Cb, R*.3, R*RATIO*.3, f'fill="{NAVY}" stroke="{ICEGREY}" stroke-width="4"')}
</svg>'''


def poly(side, ov=26):
    """Poligono de recorte em % do palco; ov = quanto a tira entra embaixo do corpo do cilindro."""
    y1, y2 = BAND
    if side == "sujo":
        pts = [(0, y1), (x_left(y1) + ov, y1), (x_left(y2) + ov, y2), (0, y2)]
    else:
        pts = [(x_right(y1) - ov, y1), (W, y1), (W, y2), (x_right(y2) - ov, y2)]
    return "polygon(" + ",".join(f"{p[0]/W*100:.2f}% {p[1]/H*100:.2f}%" for p in pts) + ")"


def tira_suja(seed=7):
    rnd = random.Random(seed)
    y1, y2 = BAND
    cols = {"g": "#5F6062", "s": "#8A94A8", "i": "#B9C6D8"}
    buckets = {}                      # (cor, espessura) -> subpaths
    step_x, step_y = 44, 36
    for yi in range(int((y2 - y1) // step_y) + 1):
        for xi in range(W // step_x):
            if rnd.random() < 0.16:
                continue
            x = xi * step_x + rnd.uniform(-16, 16) + (step_x / 2 if yi % 2 else 0)
            y = y1 + yi * step_y + rnd.uniform(-12, 12)
            c = rnd.choices(["g", "s", "i"], weights=[5, 3, 2])[0]
            kind = rnd.choices(["dash", "dot"], weights=[6, 4])[0]
            if kind == "dash":
                ln, ang = rnd.uniform(10, 38), math.radians(rnd.uniform(-34, 34))
                w = rnd.choice([3, 4, 5])
                d = f"M{f(x)} {f(y)}l{f(ln*math.cos(ang))} {f(ln*math.sin(ang))}"
            else:
                w = rnd.choice([5, 7, 10])
                d = f"M{f(x)} {f(y)}h0"
            buckets.setdefault((c, w), []).append(d)
    paths = "".join(
        f'<path d="{"".join(v)}" stroke="{cols[c]}" stroke-width="{w}"/>' for (c, w), v in sorted(buckets.items())
    )
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W*2} {H}" fill="none" stroke-linecap="round">'
            f'<defs><g id="p">{paths}</g></defs><use href="#p"/><use href="#p" x="{W}"/></svg>')


def tira_limpa(seed=11):
    rnd = random.Random(seed)
    y1, y2 = BAND
    buckets = {}
    y, row = y1, 0
    while y <= y2 + 0.1:
        x = rnd.uniform(0, 180)
        while True:
            ln = rnd.uniform(110, 420)
            if x + ln > W - 10:
                break
            c, w = rnd.choices([(BLUE, 1.6), (BLUE_HI, 1.2), (BLUE, 2.6)], weights=[6, 2, 1])[0]
            buckets.setdefault((c, w), []).append(f"M{f(x)} {f(y)}h{f(ln)}")
            x += ln + rnd.uniform(60, 190)
        y += 25
        row += 1
    paths = "".join(f'<path d="{"".join(v)}" stroke="{c}" stroke-width="{w}"/>' for (c, w), v in sorted(buckets.items()))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W*2} {H}" fill="none" stroke-linecap="round">'
            f'<defs><g id="p">{paths}</g></defs><use href="#p"/><use href="#p" x="{W}"/></svg>')


if __name__ == "__main__":
    for nome, svg in (("hero-cilindro", cilindro()), ("hero-sujo", tira_suja()), ("hero-limpo", tira_limpa())):
        (OUT / f"{nome}.svg").write_text(svg)
        print(nome, (OUT / f"{nome}.svg").stat().st_size, "bytes")
    css = OUT.parent / "css" / "hero-clips.css"
    css.write_text(f"/* gerado por tools/gen_hero.py */\n.hero{{--clip-sujo:{poly('sujo')};--clip-limpo:{poly('limpo')}}}\n")
    print("clip sujo :", poly("sujo"))
    print("clip limpo:", poly("limpo"))
    print("x_left(150..650):", [round(x_left(y)) for y in (150, 400, 650)], "chord:", round(CHORD))
