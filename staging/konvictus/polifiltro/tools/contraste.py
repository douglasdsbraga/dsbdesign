"""Verifica contraste WCAG dos pares de cor do prototipo (texto >= 4,5:1; texto grande/UI >= 3:1).
Uso: python3 -I tools/contraste.py"""
def lum(h):
    h = h.lstrip("#"); r, g, b = (int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
    return .2126 * f(r) + .7152 * f(g) + .0722 * f(b)
def cr(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + .05) / (lb + .05)
NAVY, ICE, ICE50, INK, GRAF, BLUE600, BLUE300, BLUE200 = "#0B1B3F", "#EBF3F2", "#F6FAF9", "#142033", "#5F6062", "#3157AE", "#8FB4E3", "#B9C6D8"
SEG = {"agricola": ("#8DB63C", "#436B12"), "transporte": ("#E3A623", "#7A5400"), "industria": ("#E0743A", "#9A3F0F"), "maritimo": ("#3FB0C4", "#0E6677"),
       "ferrovia": ("#B39A6E", "#6B5530"), "mineracao": ("#D9705A", "#9A2F1C"), "geradores-de-energia": ("#DDCB3A", "#6B6000")}
pares = [("texto ink / gelo", INK, ICE, 4.5), ("texto grafite / gelo", GRAF, ICE, 4.5), ("texto grafite / gelo-50", GRAF, ICE50, 4.5),
         ("botao: gelo-50 / azul UI", ICE50, BLUE600, 4.5), ("link azul UI / gelo", BLUE600, ICE, 4.5), ("link azul UI / gelo-50", BLUE600, ICE50, 4.5),
         ("texto gelo / navy", ICE, NAVY, 4.5), ("texto azul-200 / navy", BLUE200, NAVY, 4.5), ("botao: navy / azul-300", NAVY, BLUE300, 4.5),
         ("destaque azul-300 / navy (H1)", BLUE300, NAVY, 3.0), ("texto gelo-50 / azul UI (CTA final)", ICE50, BLUE600, 4.5)]
for k, (seg, deep) in SEG.items():
    pares += [(f"{k}: navy sobre --seg (faixa/CTA)", NAVY, seg, 4.5), (f"{k}: --seg-deep sobre gelo (texto)", deep, ICE, 4.5), (f"{k}: --seg sobre navy (acento/H1 grande)", seg, NAVY, 3.0)]
ruins = 0
for nome, fg, bg, minimo in pares:
    r = cr(fg, bg); ok = r >= minimo; ruins += not ok
    print(f"{'OK ' if ok else 'FALHA'} {r:5.2f} (min {minimo})  {nome}")
print("\nfalhas:", ruins)
