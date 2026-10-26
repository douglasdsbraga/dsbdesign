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


def arco(cx, cy, r, extra=0):
    """Para-lama: arco sobre a roda (corpo desenhado antes, roda depois, arco por cima)."""
    R = r + extra
    return f'<path d="M{cx-R} {cy}A{R} {R} 0 0 1 {cx+R} {cy}" fill="none" {st(2.2)}/>'


def montanhas():
    """Contexto da mineracao: morros de minerio ao fundo, so contorno e baixa opacidade."""
    return (f'<path d="M20 396L130 286L176 322L262 238L352 330L420 292L470 330" fill="none" {st(1.8, op=.28)}/>'
            f'<path d="M520 396L600 318L650 350L712 270L750 310" fill="none" {st(1.8, op=.28)}/>')


def fabrica():
    """Contexto da industria: telhado em shed + chamines ao fundo, so contorno e baixa opacidade."""
    return (f'<path d="M20 150V108L70 136V108L120 136V108L170 136V150" fill="none" {st(1.8, op=.28)}/>'
            f'<path d="M540 150V64H566V150M600 150V92H622V150" fill="none" {st(1.8, op=.28)}/>'
            f'<path d="M530 64H576M594 92H628" {st(1.8, op=.28)}/>')


def torre():
    """Contexto do gerador: torre de transmissao ao fundo, so contorno e baixa opacidade."""
    return (f'<path d="M700 396L716 150L732 396M706 330H726M709 270H723M712 210H720M690 150H742M698 128H734M716 150V106" '
            f'fill="none" {st(1.8, op=.28)}/>'
            f'<path d="M690 150Q716 160 742 150M698 128Q716 136 734 128" fill="none" {st(1.4, op=.28)}/>')


def caminhao():
    # cavalo + bau, visto de lado (frente a esquerda); 3 filtros no vao do chassi, atras do tanque
    fil, hs = montar([("oleo", 336, 282, 44), ("ar", 386, 282, 44), ("cabine", 436, 282, 60)])
    rodas = roda_lisa(138, 346, 50, 29, 9) + roda_lisa(566, 346, 50, 29, 9) + roda_lisa(664, 346, 50, 29, 9)
    arcos = arco(138, 346, 50, 9) + arco(566, 346, 50, 9) + arco(664, 346, 50, 9)
    return f'''<symbol id="k-caminhao" viewBox="0 0 760 420">
<path d="M10 396H750" {st(2, 'stroke-dasharray="2 8"')}/>
<rect x="66" y="322" width="650" height="12" rx="4" fill="{BODY2}" {st()}/>
<rect x="316" y="58" width="394" height="170" rx="8" fill="{BODY}" {st()}/>
<path d="M316 214H710" stroke="{ACC}" stroke-width="6" stroke-linecap="round"/>
<path d="M365 74V204M414 74V204M463 74V204M512 74V204M561 74V204M610 74V204M659 74V204" {st(1.4, op=.28)}/>
<path d="M316 70H710" {st(1.4, op=.4)}/><rect x="696" y="226" width="8" height="14" rx="2" fill="{ACC}" {st(1.4)}/>
<rect x="252" y="240" width="56" height="76" rx="22" fill="{BODY2}" {st(2)}/><path d="M252 266H308M252 290H308" {st(1.4, op=.45)}/>
<path d="M100 144Q122 86 178 78L316 66V136Z" fill="{BODY2}" {st()}/><path d="M170 98H300" {st(1.4, op=.4)}/>
<path d="M58 322V228Q58 210 68 198L104 142Q114 124 134 124H236Q250 124 254 138V322Z" fill="{BODY}" {st()}/>
<path d="M82 198L110 148Q116 138 130 138H224Q232 138 232 148V198Z" fill="{BODY2}" {st(2)}/><path d="M104 188L136 152M126 190L150 158" {st(1.4, op=.4)}/>
<path d="M232 138V300" {st(1.6, op=.45)}/><rect x="212" y="206" width="14" height="5" rx="2.5" fill="{BODY2}" {st(1.4)}/>
<path d="M58 266H254" stroke="{ACC}" stroke-width="5" stroke-linecap="round"/>
<rect x="58" y="232" width="14" height="22" rx="4" fill="{ACC}" {st(1.6)}/><path d="M60 274H100M60 286H100M60 298H100" {st(1.4, op=.5)}/>
<rect x="48" y="304" width="70" height="18" rx="5" fill="{BODY2}" {st(2)}/><rect x="40" y="152" width="20" height="30" rx="4" fill="{BODY2}" {st(2)}/>
<path d="M254 306H276" {st(2.5)}/>
{janela(326, 240, 178, 84)}{fil}
<path d="M512 322V300H520" {st(1.6, op=.5)}/><rect x="506" y="300" width="9" height="14" rx="2" fill="{BODY2}" {st(1.4)}/>
{rodas}{arcos}
<path d="M722 312V352" {st(2.5)}/><rect x="716" y="340" width="12" height="22" rx="2" fill="{BODY2}" {st(1.6)}/>
</symbol>''', hs


def industria():
    # pacote compressor/filtragem: reservatorio, gabinete com filtros, motor; fabrica ao fundo
    fil, hs = montar([("hidraulico", 322, 250, 46), ("separadores", 376, 250, 78), ("desumidificador", 462, 250, 78)])
    aletas = "".join(f'<path d="M{x} 226V326"/>' for x in range(604, 704, 9))
    return f'''<symbol id="k-industria" viewBox="0 0 760 420">
{fabrica()}
<path d="M10 396H750" {st(2, 'stroke-dasharray="2 8"')}/>
<rect x="24" y="364" width="712" height="20" rx="4" fill="{BODY2}" {st()}/><path d="M56 384V396M150 384V396M300 384V396M470 384V396M610 384V396M700 384V396" {st(5)}/>
<path d="M88 306V364M232 306V364" {st(8)}/><path d="M78 364H98M222 364H242" {st(5)}/>
<path d="M36 196Q36 178 56 178H266Q286 178 286 196V288Q286 306 266 306H56Q36 306 36 288Z" fill="{BODY}" {st()}/>
<path d="M92 178V306M230 178V306" {st(1.6, op=.45)}/>
<circle cx="160" cy="146" r="22" fill="{BODY2}" {st(2)}/><path d="M160 146L173 133" {st(2.5)}/><path d="M142 146H146M174 146H178M160 128V132" {st(1.6, op=.6)}/><path d="M160 168V178" {st(5)}/>
<rect x="100" y="206" width="120" height="14" rx="3" fill="{BODY2}" {st(1.6)}/><path d="M112 213H208" {st(1.4, op=.5)}/>
<path d="M286 242H306M286 270H306" {st(6)}/><circle cx="296" cy="256" r="5" fill="{ACC}" {st(1.4)}/>
<rect x="300" y="154" width="276" height="212" rx="6" fill="{BODY}" {st()}/>
<path d="M300 166H576" stroke="{ACC}" stroke-width="6" stroke-linecap="round"/>
<rect x="318" y="176" width="64" height="22" rx="3" fill="{BODY2}" {st(1.6)}/><path d="M326 187H374" {st(1.4, op=.5)}/><circle cx="552" cy="188" r="6" fill="{ACC}" {st(1.4)}/><circle cx="532" cy="188" r="6" fill="{BODY2}" {st(1.4)}/>
{janela(312, 206, 252, 118)}{fil}
<path d="M312 336H564M312 348H564" {st(1.4, op=.35)}/>
<path d="M576 276H592" {st(6)}/><rect x="590" y="208" width="132" height="158" rx="8" fill="{BODY}" {st()}/><g {st(2, op=.55)}>{aletas}</g>
<rect x="598" y="190" width="30" height="18" rx="3" fill="{BODY2}" {st(1.8)}/><rect x="722" y="262" width="14" height="44" rx="3" fill="{BODY2}" {st()}/>
<path d="M618 190V170H676V190" fill="none" {st(2.5)}/>
</symbol>''', hs


def locomotiva():
    # diesel-eletrica de lado (frente a direita): capo longo, cabine, truques de 3 eixos, tanque, trilho com dormentes
    fil, hs = montar([("oleo", 124, 268, 48), ("combustivel", 196, 268, 48), ("ar", 268, 268, 48)])
    rodas = "".join(roda_lisa(x, 358, 29, 17, 6) for x in (108, 168, 228, 500, 560, 620))
    postes = "".join(f'<path d="M{x} 212V192"/>' for x in range(52, 470, 62))
    return f'''<symbol id="k-locomotiva" viewBox="0 0 760 420">
<path d="M10 388H750" {st(2.5)}/><path d="M10 394H750" {st(1.2, op=.5)}/><path d="M30 394V408M110 394V408M190 394V408M270 394V408M350 394V408M430 394V408M510 394V408M590 394V408M670 394V408" {st(2, op=.35)}/>
<rect x="84" y="316" width="174" height="14" rx="5" fill="{BODY2}" {st()}/><rect x="478" y="316" width="174" height="14" rx="5" fill="{BODY2}" {st()}/>
<path d="M92 316V330M250 316V330M486 316V330M644 316V330" {st(2, op=.5)}/><path d="M96 340H240M490 340H634" {st(1.4, op=.4)}/>
<rect x="288" y="340" width="176" height="32" rx="15" fill="{BODY2}" {st(2)}/><path d="M318 340V372M432 340V372" {st(1.4, op=.4)}/>
{rodas}
<path d="M24 316V212Q24 196 44 196H470L498 164V128Q498 112 514 112H690L726 148V316Z" fill="{BODY}" {st()}/>
<path d="M24 316H726" stroke="{ACC}" stroke-width="6" stroke-linecap="round"/><path d="M24 212H470" stroke="{ACC}" stroke-width="5" stroke-linecap="round"/>
<g {st(2.5)} stroke="{ACC}">{postes}</g><path d="M24 192H470" stroke="{ACC}" stroke-width="3" stroke-linecap="round"/>
<rect x="76" y="176" width="68" height="20" rx="5" fill="{BODY2}" {st(1.8)}/><rect x="226" y="176" width="68" height="20" rx="5" fill="{BODY2}" {st(1.8)}/><rect x="376" y="178" width="62" height="18" rx="5" fill="{BODY2}" {st(1.8)}/>
{janela(100, 222, 248, 90)}{fil}
<path d="M366 224V310M390 224V310M414 224V310M438 224V310" {st(1.6, op=.4)}/>
<rect x="38" y="226" width="44" height="72" rx="4" fill="{BODY2}" {st(1.8)}/><path d="M38 242H82M38 258H82M38 274H82M38 288H82" {st(1.4, op=.45)}/>
<path d="M516 134H592V198H516ZM608 134H662V198H608Z" fill="{BODY2}" {st(2)}/><path d="M512 124H668" {st(3.5)}/><path d="M690 118V300" {st(1.6, op=.4)}/>
<rect x="676" y="224" width="34" height="22" rx="3" fill="{BODY2}" {st(1.8)}/><circle cx="716" cy="156" r="6" fill="{ACC}" {st(1.6)}/>
<path d="M726 262H746M726 294H746" {st(3)}/><path d="M726 262V316M740 262V316" {st(2, op=.55)}/>
<path d="M24 300H4M24 270H4M4 270V316H20" fill="none" {st(2.2, op=.6)}/>
</symbol>''', hs


def fora_de_estrada():
    # caminhao fora-de-estrada rigido: cabine pequena sob a viseira, cacamba basculante, pneus enormes; filtros no cofre
    fil, hs = montar([("hidraulico", 326, 270, 42), ("oleo", 380, 270, 42), ("ar", 434, 270, 42)])
    rodas = roda_lisa(204, 312, 84, 46, 14) + roda_lisa(590, 312, 84, 46, 14)
    return f'''<symbol id="k-fora-de-estrada" viewBox="0 0 760 420">
{montanhas()}
<path d="M10 396H750" {st(2, 'stroke-dasharray="2 8"')}/>
<path d="M330 90H640L722 168Q730 178 728 190L716 226H330Z" fill="{BODY}" {st()}/>
<path d="M356 112H632L700 178L694 208H356Z" fill="{BODY2}" {st(2)}/><path d="M410 114L388 206M476 114L458 206M542 114L530 206M608 118L598 206" {st(1.4, op=.3)}/>
<path d="M342 100H640" stroke="{ACC}" stroke-width="6" stroke-linecap="round"/><path d="M330 226H716" {st(3)}/>
<path d="M728 190L744 192M722 204L738 208" {st(2.2, op=.6)}/><path d="M372 230L396 212" {st(5)}/><circle cx="372" cy="230" r="5" fill="{ACC}" {st(1.4)}/>
<rect x="296" y="228" width="226" height="92" rx="6" fill="{BODY}" {st()}/>
<path d="M62 322V214Q62 200 76 200H300V322Z" fill="{BODY}" {st()}/><path d="M62 214H300" stroke="{ACC}" stroke-width="6" stroke-linecap="round"/>
<path d="M92 200V148Q92 132 108 132H248Q260 132 266 144L282 200Z" fill="{BODY}" {st()}/>
<path d="M114 150H236L248 190H114Z" fill="{BODY2}" {st(2)}/><path d="M130 160L152 182M154 160L176 182" {st(1.4, op=.4)}/>
<rect x="80" y="108" width="256" height="16" rx="5" fill="{BODY2}" {st(2)}/><path d="M104 124V132M312 124V228" {st(2.5, op=.7)}/>
<path d="M74 200V318M62 232H92M62 258H92M62 284H92" {st(2.2, op=.7)}/><path d="M44 262H62M44 290H62" {st(3)}/>
{janela(308, 238, 182, 76)}{fil}
{rodas}{arco(204, 312, 84, 10)}{arco(590, 312, 84, 10)}
</symbol>''', hs


def gerador():
    # grupo gerador em carenagem: motor (filtros), alternador, radiador, escapamento, tanque-base, painel; torre de transmissao ao fundo
    fil, hs = montar([("oleo", 132, 232, 56), ("combustivel", 206, 232, 56), ("ar", 280, 232, 56)])
    louvers = "".join(f'<path d="M{x} 150V318"/>' for x in range(556, 672, 9))
    return f'''<symbol id="k-gerador" viewBox="0 0 760 420">
{torre()}
<path d="M10 396H750" {st(2, 'stroke-dasharray="2 8"')}/>
<rect x="56" y="352" width="648" height="18" rx="4" fill="{BODY2}" {st()}/><rect x="140" y="370" width="480" height="22" rx="10" fill="{BODY}" {st(2)}/><path d="M164 380H596" {st(1.4, op=.4)}/>
<path d="M88 370V392M672 370V392" {st(6)}/>
<rect x="56" y="112" width="648" height="240" rx="10" fill="{BODY}" {st()}/>
<path d="M56 132H704" stroke="{ACC}" stroke-width="6" stroke-linecap="round"/>
<rect x="112" y="40" width="46" height="72" rx="10" fill="{BODY2}" {st()}/><path d="M135 40V20H184" fill="none" {st(4)}/><path d="M116 58H154M116 76H154M116 94H154" {st(1.4, op=.45)}/>
<path d="M190 112V98H214V112M520 112V98H544V112" fill="none" {st(2.5)}/>
{janela(92, 156, 380, 170)}
<rect x="108" y="248" width="344" height="64" rx="6" fill="{BODY}" {st(2, op=.9)}/><path d="M130 248V312M154 248V312M430 248V312" {st(1.4, op=.35)}/>
{fil}
<rect x="486" y="164" width="52" height="108" rx="5" fill="{BODY2}" {st(2)}/><rect x="494" y="174" width="36" height="24" rx="3" fill="{BODY}" {st(1.6)}/><path d="M506 190L514 180L514 188L522 186" fill="none" stroke="{ACC}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/><circle cx="504" cy="220" r="6" fill="{ACC}" {st(1.4)}/><circle cx="522" cy="220" r="6" fill="{BODY}" {st(1.4)}/><path d="M494 246H530M494 258H530" {st(2, op=.6)}/>
<rect x="548" y="136" width="136" height="188" rx="6" fill="{BODY2}" {st(2)}/><g {st(2, op=.55)}>{louvers}</g>
<path d="M56 338H704" {st(1.4, op=.35)}/>
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
