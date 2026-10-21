"""Blueprints em corte dos 6 segmentos que faltavam (mesma linguagem do trator): caminhao, maquina industrial,
embarcacao, locomotiva, caminhao fora-de-estrada e grupo gerador. Cada um leva 3 filtros numa janela tracejada.
Injeta <symbol id="k-..."> no sprite (<!--veiculos-->) e grava os hotspots (% do viewBox 760x420) em tools/dados/seg-art.json.
Uso: python3 -I tools/gen_veiculos.py (apos gen_kit.py e gen_trator.py)"""
import importlib.util, json, math, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SPRITE = ROOT / "assets" / "svg" / "sprite.svg"
spec = importlib.util.spec_from_file_location("gen_trator", ROOT / "tools" / "gen_trator.py")
T = importlib.util.module_from_spec(spec)
spec.loader.exec_module(T)  # reaproveita roda(), st() e as cores; o bloco __main__ do trator nao roda
LINE, BODY, BODY2, ACC, st, roda, f = T.LINE, T.BODY, T.BODY2, T.ACC, T.st, T.roda, T.f

# o glifo de cada filtro e o MESMO da pagina de filtros e dos cards de segmento (consistencia entre ilustracao e card)
KIT = {"oleo": "spinon-a", "cabine": "painel", "combustivel": "spinon-b", "ar": "cartucho-a", "separadores": "linha",
       "arrefecimento": "spinon-a", "desumidificador": "linha", "hidraulico": "spinon-b"}
ROTULO = {"oleo": "Filtro de óleo", "cabine": "Filtro de cabine", "combustivel": "Filtro de combustível", "ar": "Filtro de ar",
          "separadores": "Filtros separadores", "arrefecimento": "Filtro de arrefecimento", "desumidificador": "Filtro desumidificador", "hidraulico": "Filtro hidráulico"}


def altura(kit, w):
    return w * (160 / 220 if kit == "painel" else 160 / 260 if kit == "linha" else 280 / 200)


def janela(x, y, w, h):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{BODY2}" stroke="{LINE}" stroke-width="1.6" stroke-dasharray="5 4"/>'


def montar(itens):
    """itens = [(ancora, x, y_centro, largura)] -> (svg dos filtros, hotspots em % do viewBox)"""
    svg, hs = [], []
    for anc, x, cy, w in itens:
        kit = KIT[anc]
        h = altura(kit, w)
        y = cy - h / 2
        svg.append(f'<use href="#k-{kit}" x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}"/>')
        hs.append({"x": round((x + w / 2) / 760 * 100, 1), "y": round(cy / 420 * 100, 1), "label": ROTULO[anc], "anchor": anc})
    return "".join(svg), hs


def roda_lisa(cx, cy, r, aro, cubo):
    """Pneu liso (sem garras): caminhao, locomotiva e fora-de-estrada nao usam o pneu agricola do trator."""
    raios = "".join(f'M{f(cx+cubo*math.cos(a))} {f(cy+cubo*math.sin(a))}L{f(cx+aro*math.cos(a))} {f(cy+aro*math.sin(a))}'
                    for a in (2*math.pi*i/8+0.2 for i in range(8)))
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{BODY}" {st()}/><circle cx="{cx}" cy="{cy}" r="{f(r*.78)}" fill="none" {st(1.6, op=.5)}/>'
            f'<circle cx="{cx}" cy="{cy}" r="{aro}" fill="{BODY2}" {st(2)}/><path d="{raios}" {st(1.6, op=.8)}/>'
            f'<circle cx="{cx}" cy="{cy}" r="{cubo}" fill="{ACC}" {st(2)}/>')


ARTS = {}


def caminhao():
    fil, hs = montar([("oleo", 236, 270, 52), ("ar", 292, 270, 52), ("cabine", 348, 270, 72)])
    return f'''<symbol id="k-caminhao" viewBox="0 0 760 420">
<path d="M10 396H750" {st(2, 'stroke-dasharray="2 8"')}/>
<rect x="56" y="314" width="646" height="12" rx="4" fill="{BODY2}" {st()}/>
{roda_lisa(118, 342, 54, 30, 9)}{roda_lisa(556, 342, 54, 30, 9)}{roda_lisa(664, 342, 54, 30, 9)}
<path d="M44 316V152Q44 120 76 120H150Q174 120 186 142L208 200V316Z" fill="{BODY}" {st()}/>
<path d="M68 142H148L172 194H68Z" fill="{BODY2}" {st(2)}/><path d="M86 160H126" {st(1.4, op=.45)}/>
<path d="M44 200H208" stroke="{ACC}" stroke-width="6" stroke-linecap="round"/>
<rect x="222" y="62" width="500" height="150" rx="6" fill="{BODY}" {st()}/>
<path d="M222 200H722" stroke="{ACC}" stroke-width="6" stroke-linecap="round"/><path d="M262 84V190M322 84V190M382 84V190M442 84V190M502 84V190M562 84V190M622 84V190M682 84V190" {st(1.4, op=.28)}/>
{janela(228, 224, 204, 92)}{fil}
<rect x="452" y="238" width="104" height="64" rx="22" fill="{BODY2}" {st(2)}/><path d="M480 238V302M508 238V302" {st(1.4, op=.5)}/>
<path d="M206 300H224" {st(2.5)}/><path d="M60 246H40M60 270H40" {st(2, op=.6)}/>
</symbol>''', hs


def industria():
    fil, hs = montar([("hidraulico", 322, 248, 52), ("separadores", 380, 248, 76), ("desumidificador", 464, 248, 76)])
    aletas = "".join(f'<path d="M{x} 218V318"/>' for x in range(598, 704, 9))
    return f'''<symbol id="k-industria" viewBox="0 0 760 420">
<path d="M10 396H750" {st(2, 'stroke-dasharray="2 8"')}/>
<rect x="30" y="366" width="700" height="18" rx="4" fill="{BODY2}" {st()}/>
<path d="M92 300V366M236 300V366" {st(8)}/><path d="M86 366H98M230 366H242" {st(5)}/>
<rect x="36" y="176" width="250" height="126" rx="60" fill="{BODY}" {st()}/>
<path d="M92 176V302M230 176V302" {st(1.6, op=.45)}/><path d="M36 239H52M270 239H286" {st(2, op=.6)}/>
<circle cx="160" cy="150" r="18" fill="{BODY2}" {st(2)}/><path d="M160 150L170 140" {st(2.5)}/><path d="M160 168V176" {st(4)}/>
<path d="M286 238H312M286 264H312" {st(5)}/>
<rect x="298" y="150" width="268" height="216" rx="6" fill="{BODY}" {st()}/>
<path d="M298 160H566" stroke="{ACC}" stroke-width="6" stroke-linecap="round"/>
{janela(312, 186, 242, 124)}{fil}
<path d="M312 322H554M312 336H554" {st(1.4, op=.35)}/>
<rect x="580" y="206" width="136" height="160" rx="8" fill="{BODY}" {st()}/><g {st(2, op=.55)}>{aletas}</g>
<rect x="716" y="256" width="16" height="40" rx="3" fill="{BODY2}" {st()}/>
<path d="M566 276H580" {st(5)}/><path d="M620 206V190H676V206" fill="none" {st(2.5)}/>
</symbol>''', hs


def barco():
    fil, hs = montar([("combustivel", 172, 316, 52), ("separadores", 236, 316, 76), ("arrefecimento", 326, 316, 52)])
    ondas = "M0 332Q22 322 44 332T88 332T132 332T176 332T220 332T264 332T308 332T352 332T396 332T440 332T484 332T528 332T572 332T616 332T660 332T704 332T748 332"
    return f'''<symbol id="k-barco" viewBox="0 0 760 420">
<path d="M30 252H722L672 360Q664 376 644 376H146Q126 376 116 360Z" fill="{BODY}" {st()}/>
<path d="M30 252H722" stroke="{ACC}" stroke-width="6" stroke-linecap="round"/>
{janela(160, 268, 228, 96)}{fil}
<path d="M426 268V364M470 268V364" {st(1.6, op=.4)}/><rect x="480" y="296" width="90" height="48" rx="8" fill="{BODY2}" {st(2)}/><path d="M580 320H650" {st(5)}/>
<path d="M452 252V176Q452 160 468 160H642Q658 160 662 176L676 252Z" fill="{BODY}" {st()}/>
<path d="M472 180H508V214H472ZM520 180H556V214H520ZM568 180H604V214H568Z" fill="{BODY2}" {st(1.8)}/>
<path d="M500 160V118Q500 104 514 104H600Q614 104 614 118V160Z" fill="{BODY}" {st()}/><path d="M514 120H600" {st(1.8, op=.5)}/>
<path d="M556 104V54M536 70H576M544 84H568" {st(2.5)}/><path d="M100 252V200H140V252M96 200H144" fill="none" {st(2.2)}/>
<path d="{ondas}" fill="none" stroke="{LINE}" stroke-width="2" stroke-opacity=".75" stroke-dasharray="14 8"/>
<path d="M10 396H750" {st(2, 'stroke-dasharray="2 8"')} stroke-opacity=".5"/>
</symbol>''', hs


def locomotiva():
    fil, hs = montar([("oleo", 124, 258, 52), ("combustivel", 196, 258, 52), ("ar", 268, 258, 52)])
    rodas = "".join(roda_lisa(x, 356, 29, 17, 6) for x in (108, 168, 228, 500, 560, 620))
    return f'''<symbol id="k-locomotiva" viewBox="0 0 760 420">
<path d="M10 386H750" {st(2.5)}/><path d="M10 392H750" {st(1.2, op=.5)}/><path d="M40 392V404M120 392V404M200 392V404M280 392V404M360 392V404M440 392V404M520 392V404M600 392V404M680 392V404" {st(2, op=.35)}/>
{rodas}
<rect x="88" y="326" width="164" height="12" rx="4" fill="{BODY2}" {st()}/><rect x="482" y="326" width="164" height="12" rx="4" fill="{BODY2}" {st()}/>
<rect x="290" y="338" width="170" height="30" rx="14" fill="{BODY2}" {st(2)}/>
<path d="M24 328V196Q24 176 44 176H470L498 148V108Q498 92 514 92H706Q726 92 726 112V328Z" fill="{BODY}" {st()}/>
<path d="M24 328H726" stroke="{ACC}" stroke-width="6" stroke-linecap="round"/><path d="M24 196H470" stroke="{ACC}" stroke-width="5" stroke-linecap="round"/>
{janela(100, 206, 248, 104)}{fil}
<path d="M372 206V310M396 206V310M420 206V310M444 206V310" {st(1.6, op=.4)}/>
<path d="M522 116H590V190H522ZM606 116H660V190H606Z" fill="{BODY2}" {st(2)}/><path d="M690 116V300" {st(1.6, op=.4)}/>
<rect x="388" y="150" width="46" height="26" rx="4" fill="{BODY2}" {st(2)}/><path d="M726 250H744M726 290H744" {st(3)}/>
</symbol>''', hs


def fora_de_estrada():
    fil, hs = montar([("hidraulico", 96, 257, 42), ("oleo", 160, 257, 42), ("ar", 224, 257, 42)])
    return f'''<symbol id="k-fora-de-estrada" viewBox="0 0 760 420">
<path d="M10 396H750" {st(2, 'stroke-dasharray="2 8"')}/>
{roda_lisa(192, 328, 68, 38, 12)}{roda_lisa(584, 328, 68, 38, 12)}
<path d="M300 262L346 96Q350 84 362 84H640Q652 84 660 94L732 176Q738 184 736 194L722 296H300Z" fill="{BODY}" {st()}/>
<path d="M340 262L378 112H640L706 190L696 262Z" fill="{BODY2}" {st(2)}/><path d="M400 130L372 244M470 118L444 250M540 118L520 250M610 120L596 252" {st(1.4, op=.3)}/>
<path d="M300 262H722" stroke="{ACC}" stroke-width="6" stroke-linecap="round"/>
<path d="M44 300V218Q44 202 60 202H300V300Z" fill="{BODY}" {st()}/>
<path d="M44 218H300" stroke="{ACC}" stroke-width="6" stroke-linecap="round"/>
{janela(74, 224, 214, 66)}{fil}
<path d="M54 202V150Q54 134 70 134H168Q184 134 190 148L204 202Z" fill="{BODY}" {st()}/><path d="M72 150H160L172 190H72Z" fill="{BODY2}" {st(2)}/>
<path d="M30 252H44M30 276H44" {st(3)}/><path d="M300 306H722" {st(2.5, op=.6)}/>
</symbol>''', hs


def gerador():
    fil, hs = montar([("oleo", 132, 232, 56), ("combustivel", 206, 232, 56), ("ar", 280, 232, 56)])
    louvers = "".join(f'<path d="M{x} 150V318"/>' for x in range(560, 676, 9))
    return f'''<symbol id="k-gerador" viewBox="0 0 760 420">
<path d="M10 396H750" {st(2, 'stroke-dasharray="2 8"')}/>
<rect x="64" y="350" width="632" height="18" rx="4" fill="{BODY2}" {st()}/><rect x="150" y="368" width="460" height="22" rx="10" fill="{BODY}" {st(2)}/>
<path d="M90 368V390M670 368V390" {st(6)}/>
<rect x="64" y="112" width="632" height="238" rx="10" fill="{BODY}" {st()}/>
<path d="M64 132H696" stroke="{ACC}" stroke-width="6" stroke-linecap="round"/>
<rect x="118" y="46" width="44" height="66" rx="10" fill="{BODY2}" {st()}/><path d="M140 46V26H182" fill="none" {st(4)}/><path d="M122 62H158M122 78H158" {st(1.4, op=.45)}/>
{janela(100, 156, 380, 168)}
<rect x="116" y="244" width="336" height="64" rx="6" fill="{BODY}" {st(2, op=.9)}/><path d="M136 244V308M160 244V308M440 244V308" {st(1.4, op=.35)}/>
{fil}
<rect x="540" y="136" width="136" height="188" rx="6" fill="{BODY2}" {st(2)}/><g {st(2, op=.55)}>{louvers}</g>
<rect x="494" y="172" width="32" height="88" rx="4" fill="{BODY2}" {st(2)}/><circle cx="510" cy="196" r="7" fill="{ACC}" {st(1.5)}/><path d="M500 224H520M500 238H520" {st(2, op=.6)}/>
<path d="M64 338H696" {st(1.4, op=.35)}/>
</symbol>''', hs


MAPA = {"transporte": caminhao, "industria": industria, "maritimo": barco, "ferrovia": locomotiva, "mineracao": fora_de_estrada, "geradores-de-energia": gerador}
ID = {"transporte": "caminhao", "industria": "industria", "maritimo": "barco", "ferrovia": "locomotiva", "mineracao": "fora-de-estrada", "geradores-de-energia": "gerador"}
ALT = {"transporte": "um caminhão em corte, com filtros no chassi", "industria": "uma máquina industrial em corte, com filtros no gabinete",
       "maritimo": "uma embarcação em corte, com filtros na casa de máquinas", "ferrovia": "uma locomotiva em corte, com filtros no capô",
       "mineracao": "um caminhão fora de estrada em corte, com filtros no cofre do motor", "geradores-de-energia": "um grupo gerador em corte, com filtros ao lado do motor"}

if __name__ == "__main__":
    syms, dados = [], {}
    for k, fn in MAPA.items():
        sym, hs = fn()
        syms.append(sym)
        dados[k] = {"id": ID[k], "alt": ALT[k], "hs": hs}
    s = SPRITE.read_text()
    s = re.sub(r"<!--veiculos-->.*?<!--/veiculos-->", "", s, flags=re.S)
    s = s.replace("</svg>", "<!--veiculos-->" + "".join(syms) + "<!--/veiculos--></svg>")
    SPRITE.write_text(s)
    (ROOT / "tools" / "dados" / "seg-art.json").write_text(json.dumps(dados, ensure_ascii=False, indent=1))
    print("sprite:", SPRITE.stat().st_size, "bytes;", len(syms), "ilustracoes")
