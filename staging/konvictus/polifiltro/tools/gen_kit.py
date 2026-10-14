"""Kit de ilustracoes de filtro (elevacao tecnica com janela de corte em raio-X). 4 formas base x variantes de proporcao.
Cores via custom properties (herdam do <use>): --k-line, --k-body, --k-body2, --k-acc.
Gera os <symbol> e os injeta em assets/svg/sprite.svg (marcador <!--kit-->). Uso: python3 -I tools/gen_kit.py (rodar apos gen_sprite.py)."""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SPRITE = ROOT / "assets" / "svg" / "sprite.svg"
LINE, BODY, BODY2, ACC = "var(--k-line,#B9C6D8)", "var(--k-body,#10265A)", "var(--k-body2,#173474)", "var(--k-acc,#3B73B9)"
SW = 2.5
f = lambda v: f"{v:.1f}".rstrip("0").rstrip(".")


def st(w=SW, extra=""):
    return f'stroke="{LINE}" stroke-width="{w}" stroke-linejoin="round" {extra}'


def spinon(nome, h, vw=200, vh=280):
    yt = 240 - h
    pleats = "".join(f'<path d="M{x} {yt+46}V{225}"/>' for x in range(62, 140, 7))
    return f'''<symbol id="k-{nome}" viewBox="0 0 {vw} {vh}">
<defs><clipPath id="kc-{nome}"><rect x="58" y="{yt+40}" width="86" height="{h-52}" rx="4"/></clipPath></defs>
<path d="M32 240V{yt+36}Q32 {yt} 100 {yt}Q168 {yt} 168 {yt+36}V240Z" fill="{BODY}" {st()}/>
<path d="M32 {yt+36}Q32 {yt} 100 {yt}Q168 {yt} 168 {yt+36}" fill="none" stroke="{ACC}" stroke-width="5" stroke-linecap="round" opacity=".9" transform="translate(0 -1)"/>
<rect x="24" y="240" width="152" height="15" rx="5" fill="{BODY2}" {st()}/>
<rect x="46" y="255" width="108" height="8" rx="4" fill="{ACC}" {st(2)}/>
<g clip-path="url(#kc-{nome})"><rect x="58" y="{yt+40}" width="86" height="{h-52}" fill="{BODY2}"/><g stroke="{ACC}" stroke-width="2.2" opacity=".85">{pleats}</g><rect x="92" y="{yt+40}" width="18" height="{h-52}" fill="{BODY}" stroke="{LINE}" stroke-width="2"/></g>
<rect x="58" y="{yt+40}" width="86" height="{h-52}" rx="4" fill="none" stroke="{LINE}" stroke-width="1.6" stroke-dasharray="5 4"/>
<path d="M46 {yt+50}V228" stroke="#fff" stroke-opacity=".16" stroke-width="5" stroke-linecap="round"/>
</symbol>'''


def cartucho(nome, w, vw=200, vh=280):
    x0, x1 = 100 - w / 2, 100 + w / 2
    n = int(w // 6)
    pleats = "".join(f'<path d="M{f(x0+4+i*(w-8)/n)} 52V228"/>' for i in range(n + 1))
    return f'''<symbol id="k-{nome}" viewBox="0 0 {vw} {vh}">
<rect x="{f(x0)}" y="48" width="{f(w)}" height="184" fill="{BODY2}" {st()}/>
<g stroke="{ACC}" stroke-width="1.8" opacity=".7">{pleats}</g>
<rect x="{f(x0-8)}" y="30" width="{f(w+16)}" height="22" rx="7" fill="{BODY}" {st()}/>
<rect x="{f(x0-8)}" y="228" width="{f(w+16)}" height="22" rx="7" fill="{BODY}" {st()}/>
<rect x="{f(100-w*.18)}" y="30" width="{f(w*.36)}" height="22" rx="5" fill="{ACC}" {st(2)}/>
<path d="M{f(x0+6)} 60V220" stroke="#fff" stroke-opacity=".14" stroke-width="5" stroke-linecap="round"/>
</symbol>'''


def painel(nome, vw=220, vh=160):
    zig = "M30 40" + "".join(f"L{30+i*8} {(120 if i%2 else 40)}" for i in range(1, 21))
    return f'''<symbol id="k-{nome}" viewBox="0 0 {vw} {vh}">
<rect x="14" y="24" width="192" height="112" rx="6" fill="{BODY}" {st()}/>
<path d="{zig}" fill="none" stroke="{ACC}" stroke-width="2.2" stroke-linejoin="miter" opacity=".9"/>
<rect x="14" y="24" width="192" height="112" rx="6" fill="none" {st()}/>
<rect x="22" y="32" width="176" height="96" rx="2" fill="none" stroke="{LINE}" stroke-width="1.4" stroke-dasharray="5 4"/>
<path d="M14 24h192" stroke="{ACC}" stroke-width="5" stroke-linecap="round"/>
</symbol>'''


def linha(nome, vw=260, vh=160):
    pleats = "".join(f'<path d="M{x} 56V104"/>' for x in range(92, 190, 7))
    return f'''<symbol id="k-{nome}" viewBox="0 0 {vw} {vh}">
<rect x="44" y="38" width="172" height="84" rx="16" fill="{BODY}" {st()}/>
<rect x="30" y="52" width="16" height="56" rx="5" fill="{BODY2}" {st()}/><rect x="214" y="52" width="16" height="56" rx="5" fill="{BODY2}" {st()}/>
<path d="M84 38V22h22V38M154 38V22h22V38" fill="{BODY2}" {st()}/><rect x="80" y="14" width="30" height="10" rx="3" fill="{ACC}" {st(2)}/><rect x="150" y="14" width="30" height="10" rx="3" fill="{ACC}" {st(2)}/>
<path d="M118 122v14h24v-14" fill="{BODY2}" {st()}/>
<rect x="84" y="52" width="92" height="56" rx="4" fill="{BODY2}" stroke="{LINE}" stroke-width="1.6" stroke-dasharray="5 4"/>
<g stroke="{ACC}" stroke-width="2" opacity=".85">{pleats}</g>
<path d="M56 50V110" stroke="#fff" stroke-opacity=".16" stroke-width="5" stroke-linecap="round"/>
</symbol>'''


KIT = [spinon("spinon-a", 190), spinon("spinon-b", 130), cartucho("cartucho-a", 120), cartucho("cartucho-b", 76), painel("painel"), linha("linha")]

if __name__ == "__main__":
    s = SPRITE.read_text()
    s = re.sub(r"<!--kit-->.*?<!--/kit-->", "", s, flags=re.S)
    s = s.replace("</svg>", "<!--kit-->" + "".join(KIT) + "<!--/kit--></svg>")
    SPRITE.write_text(s)
    print(len(KIT), "formas; sprite:", SPRITE.stat().st_size, "bytes")
