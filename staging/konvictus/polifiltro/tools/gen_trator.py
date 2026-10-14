"""Blueprint do trator em corte (elevacao lateral) com 3 filtros no capo. Injeta <symbol id="k-trator"> no sprite (<!--trator-->).
Hotspots (centro dos filtros em % do viewBox 760x420) saem no stdout. Uso: python3 -I tools/gen_trator.py (apos gen_kit.py)"""
import math, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent.parent
SPRITE = ROOT / "assets" / "svg" / "sprite.svg"
LINE, BODY, BODY2, ACC = "var(--k-line,#B9C6D8)", "var(--k-body,#10265A)", "var(--k-body2,#173474)", "var(--k-acc,#3B73B9)"
f = lambda v: f"{v:.1f}".rstrip("0").rstrip(".")
def st(w=2.5, extra="", op=None): return f'stroke="{LINE}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round" {extra}' + (f' stroke-opacity="{op}"' if op else "")

def roda(cx, cy, r, aro, cubo, lugs):
    ticks = "".join(f'M{f(cx+(r-9)*math.cos(a))} {f(cy+(r-9)*math.sin(a))}L{f(cx+(r+3)*math.cos(a))} {f(cy+(r+3)*math.sin(a))}'
                    for a in (2*math.pi*i/lugs for i in range(lugs)))
    raios = "".join(f'M{f(cx+cubo*math.cos(a))} {f(cy+cubo*math.sin(a))}L{f(cx+aro*math.cos(a))} {f(cy+aro*math.sin(a))}'
                    for a in (2*math.pi*i/6+0.3 for i in range(6)))
    return (f'<circle cx="{cx}" cy="{cy}" r="{r-9}" fill="{BODY}" {st()}/><path d="{ticks}" {st(3)}/>'
            f'<circle cx="{cx}" cy="{cy}" r="{aro}" fill="{BODY2}" {st(2)}/><path d="{raios}" {st(1.6, op=.8)}/>'
            f'<circle cx="{cx}" cy="{cy}" r="{cubo}" fill="{ACC}" {st(2)}/>')

FILTROS = [("spinon-b", 408, "oleo"), ("cartucho-a", 470, "ar"), ("spinon-a", 534, "combustivel")]
filtros = "".join(f'<use href="#k-{k}" x="{x}" y="210" width="56" height="78"/>' for k, x, _ in FILTROS)
sym = f'''<symbol id="k-trator" viewBox="0 0 760 420">
<path d="M10 396H750" {st(2, 'stroke-dasharray="2 8"')}/>
<rect x="228" y="296" width="386" height="14" rx="4" fill="{BODY2}" {st()}/>
{roda(232, 292, 112, 62, 18, 28)}
{roda(612, 336, 66, 36, 11, 20)}
<path d="M112 292A120 120 0 0 1 352 292" fill="none" {st(3)}/>
<path d="M116 200V64Q116 36 144 36H318Q340 36 344 56L360 200Z" fill="{BODY}" {st()}/>
<path d="M142 62H314L328 170H148Z" fill="{BODY2}" {st(2)}/><path d="M164 82L236 82M164 100L214 100" {st(1.4, op=.45)}/>
<path d="M120 52H340" {st(2, op=.5)}/>
<path d="M360 306V212Q360 190 384 190H618Q652 190 668 216L696 264V306Z" fill="{BODY}" {st()}/>
<path d="M360 200H668" stroke="{ACC}" stroke-width="6" stroke-linecap="round"/>
<rect x="392" y="206" width="196" height="84" rx="4" fill="{BODY2}" stroke="{LINE}" stroke-width="1.6" stroke-dasharray="5 4"/>
{filtros}
<path d="M668 232V288M676 232V288M684 238V288" {st(2, op=.7)}/>
<rect x="598" y="104" width="14" height="86" fill="{BODY2}" {st()}/><path d="M592 104H618L612 92H598Z" fill="{BODY2}" {st()}/>
<path d="M672 306H742M742 300V312M672 300V312" {st(1.4, op=.6)}/>
</symbol>'''

if __name__ == "__main__":
    s = SPRITE.read_text()
    s = re.sub(r"<!--trator-->.*?<!--/trator-->", "", s, flags=re.S)
    s = s.replace("</svg>", "<!--trator-->" + sym + "<!--/trator--></svg>")
    SPRITE.write_text(s)
    print("sprite:", SPRITE.stat().st_size, "bytes")
    for k, x, nome in FILTROS:
        print(nome, f"left:{(x+28)/760*100:.1f}% top:{(210+39)/420*100:.1f}%")
