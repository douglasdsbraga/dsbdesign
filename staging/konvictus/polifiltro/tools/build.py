"""Monta as paginas do prototipo a partir de src/pages/*.html + chrome (header, super menu, rodape, sheets, tab bar).
O HTML gerado e o que se abre; nao ha build no runtime. O chrome e identico em todas as paginas (mesmo hash).
Uso: python3 -I tools/build.py
"""
import hashlib, pathlib, re, time
VER = str(int(time.time()))

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "pages"

SEGS = [  # chave, nome, icone, 1 linha de apoio (PROPOSTA, aguarda copy do cliente), chips (ancora, rotulo)
    ("agricola", "Agrícola", "tractor", "Filtros e lubrificantes para tratores, colheitadeiras e pulverizadores.", [("oleo", "Filtro de óleo"), ("combustivel", "Filtro de combustível"), ("ar", "Filtro de ar")]),
    ("transporte", "Transporte", "truck-trailer", "Para frotas de caminhões e ônibus que não podem parar.", [("oleo", "Filtro de óleo"), ("ar", "Filtro de ar"), ("cabine", "Filtro de cabine")]),
    ("industria", "Indústria", "factory", "Filtragem de ar, óleo e fluidos para linhas de produção.", [("hidraulico", "Filtro hidráulico"), ("separadores", "Filtros separadores"), ("desumidificador", "Filtro desumidificador")]),
    ("maritimo", "Marítimo", "anchor", "Combustível limpo e proteção de motores em embarcações.", [("combustivel", "Filtro de combustível"), ("separadores", "Filtros separadores"), ("arrefecimento", "Filtro de arrefecimento")]),
    ("ferrovia", "Ferrovia", "train", "Linha de filtros para locomotivas e material rodante.", [("oleo", "Filtro de óleo"), ("combustivel", "Filtro de combustível"), ("ar", "Filtro de ar")]),
    ("mineracao", "Mineração", "mountains", "Equipamentos pesados, poeira e carga contínua.", [("hidraulico", "Filtro hidráulico"), ("oleo", "Filtro de óleo"), ("ar", "Filtro de ar")]),
    ("geradores-de-energia", "Geradores de energia", "lightning", "Filtros para grupos geradores e energia de backup.", [("oleo", "Filtro de óleo"), ("combustivel", "Filtro de combustível"), ("ar", "Filtro de ar")]),
]
SOLS = [  # chave, nome, 1 linha, destino
    ("filtros", "Filtros", "10 tipos", "filtros/"),
    ("lubrificantes", "Lubrificantes", "linha completa", None),
    ("aditivos", "Aditivos", "desempenho", None),
    ("ultrafiltracao-de-diesel", "Ultrafiltração de diesel", "proteção do combustível", None),
    ("equipamentos-e-armazenamento", "Equipamentos e armazenamento", "abastecimento", None),
]
FILTROS = [("oleo", "Óleo"), ("cabine", "Cabine"), ("combustivel", "Combustível"), ("ar", "Ar"), ("separadores", "Separadores"), ("ecologicos", "Ecológicos"),
           ("arrefecimento", "Arrefecimento"), ("desumidificador", "Desumidificador"), ("ureia", "Ureia"), ("hidraulico", "Hidráulico")]
CIDADES = ["Manaus/AM", "Ananindeua/PA", "Sinop/MT", "Cuiabá/MT", "Goiânia/GO", "Uberlândia/MG", "Contagem/MG", "São Paulo/SP", "Araçatuba/SP", "Curitiba/PR", "Itajaí/SC", "Porto Alegre/RS"]
PAGINAS_REAIS = {"segmentos/agricola/": "segmentos/agricola/", "filtros/": "filtros/"}


def ic(nome, cls=""):
    return f'<svg class="ic {cls}" aria-hidden="true" focusable="false"><use href="#i-{nome}"/></svg>'


def esc(s):
    return s.replace("&", "&amp;")


def url(R, caminho):
    """Pagina real se existir; senao stub com a URL prevista."""
    if caminho in PAGINAS_REAIS:
        return f"{R}{PAGINAS_REAIS[caminho]}"
    return f"{R}stub.html?u=/{caminho}"


def seg_url(R, k):
    return url(R, f"segmentos/{k}/")


def cor(k):
    return f"var(--seg-{k})"


def header(R, atual):
    def li_seg(k, nome, icone, d, chips):
        return (f'<li><a href="{seg_url(R,k)}" data-k="{k}" style="--c:{cor(k)}"><span class="dot"></span><span><strong>{nome}</strong></span></a></li>')
    prev_seg = "".join(
        f'<div class="s-prev" data-k="{k}" style="--c:{cor(k)}"><div class="s-art">{ic(icone,"ic-big")}<b>{nome}</b></div>'
        f'<div class="s-info"><h3>{nome}</h3><p class="d" data-copy="proposta">{esc(d)}</p><p class="lbl">Mais procurados</p>'
        f'<div class="chips">{"".join(f"<a class=chip href={R}filtros/#{a}>{r}</a>" for a, r in chips)}</div>'
        f'<p class="s-cta"><a class="btn sm" href="{seg_url(R,k)}"><span>Ver segmento</span></a>'
        f'<a class="link" href="{R}stub.html?u=/contato/&amp;segmento={k}">Cotação para {nome.lower()} {ic("arrow-right")}</a></p></div></div>'
        for k, nome, icone, d, chips in SEGS)
    opts = "".join(f"<option>{c}</option>" for c in CIDADES)
    seg_aside = (f'<div class="s-aside"><p class="lbl">Fale com a gente</p>'
                 f'<a class="btn" href="{R}stub.html?u=/contato/"><span>Solicite sua cotação</span></a>'
                 f'<a class="btn sec wa" href="{R}stub.html?u=/contato/">{ic("whatsapp-logo")}<span>WhatsApp</span></a>'
                 f'<label class="lbl" for="sm-cidade">Unidade mais próxima</label><select id="sm-cidade"><option>Escolha a cidade</option>{opts}</select>'
                 f'<a class="link" href="{R}stub.html?u=/unidades/">Ver as 12 unidades {ic("arrow-right")}</a></div>')
    li_sol = "".join(
        f'<li><a href="{R + d if d else R + "stub.html?u=/" + k + "/"}" data-k="{k}" style="--c:var(--blue-500)"><span class="dot"></span><span><strong>{n}</strong><small>{s}</small></span></a></li>'
        for k, n, s, d in SOLS)
    prev_sol = "".join(
        f'<div class="s-prev" data-k="{k}" style="--c:var(--blue-300)"><div class="s-art">{ic("cylinder" if k=="filtros" else "drop","ic-big")}<b>{n}</b></div>'
        f'<div class="s-info"><h3>{n}</h3>'
        + (f'<p class="lbl">Escolha o tipo</p><div class="chips">{"".join(f"<a class=chip href={R}filtros/#{a}>{r}</a>" for a, r in FILTROS)}</div>' if k == "filtros" else f'<p class="d" data-copy="proposta">{s}</p>')
        + f'<p class="s-cta"><a class="btn sm" href="{R + d if d else R + "stub.html?u=/" + k + "/"}"><span>Ver {n.lower()}</span></a></p></div></div>'
        for k, n, s, d in SOLS)
    sol_aside = (f'<div class="s-aside"><p class="lbl">Por segmento</p><div class="chips">'
                 + "".join(f'<a class="chip" href="{seg_url(R,k)}">{n}</a>' for k, n, *_ in SEGS)
                 + f'</div><a class="btn" href="{R}stub.html?u=/contato/"><span>Solicite sua cotação</span></a></div>')

    def cur(nome):
        return ' aria-current="page"' if atual == nome else ""
    return f'''<header class="site dark"><div class="bar">
  <a class="appbar-menu" href="{R}stub.html?u=/empresa/" data-sheet="sh-menu" aria-label="Abrir menu">{ic("list")}<span>Menu</span></a>
  <a class="logo" href="{R}index.html" aria-label="Polifiltro, página inicial"><img src="{R}assets/svg/logo-claro.svg" alt="Polifiltro" width="131" height="34"></a>
  <nav class="nav" aria-label="Principal"><ul>
    <li class="has-super"><a href="{R}stub.html?u=/segmentos/" aria-haspopup="true" aria-expanded="false" aria-controls="sm-seg"{cur("segmentos")}>Segmentos {ic("caret-down")}</a>
      <div class="super" id="sm-seg" role="region" aria-label="Segmentos"><div class="super-in"><div class="s-col"><p class="lbl">Segmentos</p><ul class="s-list">{"".join(li_seg(*s) for s in SEGS)}</ul><a class="link more" href="{R}stub.html?u=/segmentos/">Ver todos os segmentos {ic("arrow-right")}</a></div><div class="s-mid">{prev_seg}</div>{seg_aside}</div></div></li>
    <li class="has-super"><a href="{R}filtros/" aria-haspopup="true" aria-expanded="false" aria-controls="sm-sol"{cur("solucoes")}>Soluções {ic("caret-down")}</a>
      <div class="super" id="sm-sol" role="region" aria-label="Soluções"><div class="super-in"><div class="s-col"><p class="lbl">Soluções</p><ul class="s-list">{li_sol}</ul><a class="link more" href="{R}stub.html?u=/marcas/">Marcas que distribuímos {ic("arrow-right")}</a></div><div class="s-mid">{prev_sol}</div>{sol_aside}</div></div></li>
    <li><a href="{R}stub.html?u=/unidades/">Unidades</a></li>
    <li><a href="{R}stub.html?u=/marcas/">Marcas</a></li>
    <li><a href="{R}stub.html?u=/empresa/">Empresa</a></li>
  </ul></nav>
  <span class="spacer"></span>
  <a class="appbar-wa" href="{R}stub.html?u=/contato/" aria-label="WhatsApp">{ic("whatsapp-logo")}</a>
  <div class="actions"><a class="btn sec sm wa" href="{R}stub.html?u=/contato/">{ic("whatsapp-logo")}<span>WhatsApp</span></a><a class="btn sm" href="{R}stub.html?u=/contato/"><span>Solicite sua cotação</span></a></div>
</div></header>'''


def footer(R):
    cols_seg = "".join(f'<a href="{seg_url(R,k)}">{n}</a>' for k, n, *_ in SEGS)
    cols_sol = "".join(f'<a href="{R + d if d else R + "stub.html?u=/" + k + "/"}">{n}</a>' for k, n, s, d in SOLS) + f'<a href="{R}stub.html?u=/marcas/">Marcas</a>'
    unid = lambda lst: "".join(f'<a href="{R}stub.html?u=/unidades/">{c}</a>' for c in lst)
    empresa = "".join(f'<a href="{R}stub.html?u=/{p}/">{n}</a>' for p, n in [("empresa", "História"), ("qualidade-e-certificados", "Qualidade e certificados"), ("lancamentos", "Lançamentos"), ("noticias", "Notícias"), ("trabalhe-conosco", "Trabalhe conosco"), ("canal-voz-segura", "Canal Voz Segura")])
    return f'''<footer class="site dark">
  <div class="foot"><div class="foot-brand"><a class="logo-f" href="{R}index.html"><img src="{R}assets/svg/logo-completo-claro.svg" alt="Polifiltro, desde 1989" width="240" height="63" loading="lazy"></a><p>ISO 9001. Distribuindo filtros desde 1989. <span class="confirmar">confirmar</span></p></div>
  <div class="foot-cols"><div><strong>Segmentos</strong>{cols_seg}</div><div><strong>Soluções</strong>{cols_sol}</div><div><strong>Unidades</strong>{unid(CIDADES[:6])}</div><div><strong>&nbsp;</strong>{unid(CIDADES[6:])}</div><div><strong>Empresa</strong>{empresa}</div></div></div>
  <div class="foot-line"><div class="foot-bar"><a class="foot-cta" href="{R}stub.html?u=/unidades/">Fale com a unidade mais próxima {ic("arrow-up-right")}</a>
    <div class="redes"><a href="{R}stub.html?u=/contato/" aria-label="Instagram">{ic("instagram-logo")}</a><a href="{R}stub.html?u=/contato/" aria-label="Facebook">{ic("facebook-logo")}</a><a href="{R}stub.html?u=/contato/" aria-label="LinkedIn">{ic("linkedin-logo")}</a></div>
    <div class="legal"><a href="{R}stub.html?u=/politica-de-privacidade/">Privacidade</a><a href="{R}stub.html?u=/politica-de-cookies/">Cookies</a></div></div></div>
</footer>'''


def sheets(R, atual):
    cards = "".join(f'<a class="card-seg" href="{seg_url(R,k)}" style="--c:{cor(k)}"><strong>{n}</strong></a>' for k, n, i, d, c in SEGS)
    rows = "".join(f'<a class="row-sol" href="{R + d if d else R + "stub.html?u=/" + k + "/"}"><span>{n}</span>{ic("arrow-right")}</a>' for k, n, s, d in SOLS)
    chips = "".join(f'<a class="chip" href="{R}filtros/#{a}">{r}</a>' for a, r in FILTROS)
    opts = "".join(f"<option>{c}</option>" for c in CIDADES)
    lista = "".join(f'<li class="un"><strong>{c}</strong><span class="acoes"><a class="chip" href="{R}stub.html?u=/unidades/">tel</a><a class="chip" href="{R}stub.html?u=/unidades/">WhatsApp</a><a class="chip" href="{R}stub.html?u=/unidades/">Rotas</a></span></li>' for c in CIDADES[:4])
    seg_opts = "".join(f"<option>{n}</option>" for k, n, *_ in SEGS)
    x = f'<button class="x" type="button" data-close autofocus aria-label="Fechar">{ic("x")}</button>'
    def tab(href, nome, icone, extra="", cls="", sheet=""):
        a = ' aria-current="page"' if atual == nome.lower() else ""
        return f'<a href="{href}"{(" data-sheet=" + sheet) if sheet else ""}{(" class=" + cls) if cls else ""}{a}>{ic(icone)}<span>{nome}</span></a>'
    return f'''<nav class="tabbar" aria-label="Navegação do app">
  {tab(f"{R}index.html","Início","house")}{tab(f"{R}stub.html?u=/segmentos/","Segmentos","squares-four",sheet="sh-seg")}{tab(f"{R}filtros/","Soluções","funnel",sheet="sh-sol")}{tab(f"{R}stub.html?u=/unidades/","Unidades","map-pin",sheet="sh-uni")}{tab(f"{R}stub.html?u=/contato/","Cotar","pencil-simple-line",cls="cotar",sheet="sh-cot")}
</nav>
<dialog class="sheet" id="sh-seg" aria-label="Segmentos"><div class="sheet-h"><span class="grab" aria-hidden="true"></span><strong>Segmentos</strong>{x}</div><div class="sheet-b"><div class="grid-seg">{cards}</div></div><div class="sheet-f"><a class="btn sec" href="{R}stub.html?u=/segmentos/"><span>Ver todos</span></a><a class="btn" href="{R}stub.html?u=/contato/"><span>Solicite cotação</span></a></div></dialog>
<dialog class="sheet" id="sh-sol" aria-label="Soluções"><div class="sheet-h"><span class="grab" aria-hidden="true"></span><strong>Soluções</strong>{x}</div><div class="sheet-b"><div class="list-sol">{rows}</div><p class="lbl" style="margin:18px 0 10px">Tipos de filtro</p><div class="chips">{chips}</div></div><div class="sheet-f"><a class="btn" href="{R}stub.html?u=/contato/"><span>Solicite cotação</span></a></div></dialog>
<dialog class="sheet" id="sh-uni" aria-label="Unidades"><div class="sheet-h"><span class="grab" aria-hidden="true"></span><strong>Unidades</strong>{x}</div><div class="sheet-b"><button class="btn sm" type="button" style="margin-bottom:14px"><span>Usar minha localização</span></button><label class="fld">Ou escolha a cidade<select><option>Escolha</option>{opts}</select></label><ul class="un-list" style="margin-top:14px">{lista}</ul></div><div class="sheet-f"><a class="btn sec" href="{R}stub.html?u=/unidades/"><span>Ver as 12 unidades</span></a></div></dialog>
<dialog class="sheet" id="sh-cot" aria-label="Solicite sua cotação"><div class="sheet-h"><span class="grab" aria-hidden="true"></span><strong>Solicite sua cotação</strong>{x}</div><div class="sheet-b"><form class="cot" action="{R}stub.html" method="get"><input type="hidden" name="u" value="/obrigado/"><label class="fld">Nome<input name="nome" autocomplete="name" required></label><label class="fld">WhatsApp ou telefone<input name="tel" type="tel" autocomplete="tel" required></label><label class="fld">Segmento<select name="seg">{seg_opts}</select></label><button class="btn" type="submit"><span>Pedir cotação</span></button><a class="btn sec wa" href="{R}stub.html?u=/contato/">{ic("whatsapp-logo")}<span>Falar no WhatsApp</span></a></form></div></dialog>
<dialog class="sheet menu-full dark" id="sh-menu" aria-label="Menu"><div class="mf-top"><a class="logo-m" href="{R}index.html"><img src="{R}assets/svg/logo-claro.svg" alt="Polifiltro" width="131" height="34"></a><button class="x" type="button" data-close autofocus aria-label="Fechar menu">{ic("x")}</button></div>
  <div class="mf-body"><nav class="mf-nav" aria-label="Menu principal"><a href="{R}stub.html?u=/segmentos/" data-sheet="sh-seg">Segmentos {ic("arrow-up-right")}</a><a href="{R}filtros/" data-sheet="sh-sol">Soluções {ic("arrow-up-right")}</a><a href="{R}stub.html?u=/unidades/" data-sheet="sh-uni">Unidades {ic("arrow-up-right")}</a><a href="{R}stub.html?u=/marcas/">Marcas {ic("arrow-up-right")}</a><a href="{R}stub.html?u=/empresa/">Empresa {ic("arrow-up-right")}</a><a href="{R}stub.html?u=/contato/" data-sheet="sh-cot">Contato {ic("arrow-up-right")}</a></nav>
  <div class="mf-sec"><a href="{R}stub.html?u=/lancamentos/">{ic("package")}Lançamentos</a><a href="{R}stub.html?u=/noticias/">{ic("stack")}Notícias</a><a href="{R}stub.html?u=/trabalhe-conosco/">{ic("hard-hat")}Trabalhe conosco</a></div></div>
  <div class="mf-tiles"><a href="{R}stub.html?u=/unidades/" data-sheet="sh-uni"><small>Fale com a</small><strong>Unidade mais próxima</strong></a><a href="{R}stub.html?u=/contato/"><small>Atendimento</small><strong>WhatsApp</strong></a></div>
  <a class="mf-cta" href="{R}stub.html?u=/contato/" data-sheet="sh-cot"><strong>Solicite sua cotação</strong></a>
  <p class="mf-legal"><a href="{R}stub.html?u=/politica-de-privacidade/">Privacidade</a><a href="{R}stub.html?u=/politica-de-cookies/">Cookies</a><a href="{R}stub.html?u=/canal-voz-segura/">Canal Voz Segura</a></p></dialog>'''


# pagina -> (arquivo src, saida, titulo, descricao, css extra, atual, profundidade)
PAGES = [
    ("home.html", "index.html", "Polifiltro | Distribuindo filtros desde 1989", "Filtros, lubrificantes e aditivos dos melhores fabricantes, em 12 unidades. Protótipo hi-fi v1.", ["home.css"], "home", 0),
    ("agricola.html", "segmentos/agricola/index.html", "Agrícola | Polifiltro", "Soluções em filtragem e lubrificação para o agro. Protótipo hi-fi v1.", ["segmento.css"], "segmentos", 2),
    ("filtros.html", "filtros/index.html", "Filtros | Polifiltro", "Os 10 tipos de filtro da Polifiltro. Protótipo hi-fi v1.", ["segmento.css", "filtros.css"], "solucoes", 1),
    ("stub.html", "stub.html", "Página ainda sem protótipo | Polifiltro", "Página prevista, ainda não desenhada.", ["segmento.css"], "stub", 0),
]


def bundle(nome, arquivos):
    """Concatena CSS (sem comentarios) em assets/css/<nome>: menos requisicoes bloqueando o render. Fontes ficam editaveis nos parciais."""
    partes = []
    for a in arquivos:
        txt = (ROOT / "assets" / "css" / a).read_text()
        txt = re.sub(r"/\*.*?\*/", "", txt, flags=re.S)
        partes.append(re.sub(r"\n\s*\n+", "\n", txt).strip())
    (ROOT / "assets" / "css" / nome).write_text("/* gerado por tools/build.py: edite os parciais */\n" + "\n".join(partes) + "\n")


def write_super_css():
    """Regras :has() do super menu (previa por item). Geradas dos mesmos dados do menu."""
    out = ["/* gerado por tools/build.py */",
           ".super-in:has(.s-list a:is(:hover,:focus-visible)) .s-prev:first-child{opacity:0;visibility:hidden}"]
    for k in [s[0] for s in SEGS] + [s[0] for s in SOLS]:
        out.append(f'.super-in:has(.s-list a[data-k="{k}"]:is(:hover,:focus-visible)) .s-prev[data-k="{k}"]{{opacity:1;visibility:visible}}')
    (ROOT / "assets" / "css" / "super.css").write_text("\n".join(out) + "\n")


def render(p):
    src, out, titulo, desc, css, atual, depth = p
    R = "./" if depth == 0 else "../" * depth
    body = (SRC / src).read_text()
    sprite = (ROOT / "assets" / "svg" / "sprite.svg").read_text()
    h, f, s = header(R, atual), footer(R), sheets(R, atual)
    bundle("app.css", ["fonts.css", "tokens.css", "base.css", "components.css", "super.css", "motion.css"])
    bundle(f"page-{atual}.css", (["hero-clips.css"] if "home.css" in css else []) + css)
    links = "".join(f'<link rel="stylesheet" href="{R}assets/css/{c}?v={VER}">' for c in ["app.css", f"page-{atual}.css"])
    if atual == "home":
        links += f'<link rel="preload" href="{R}assets/svg/hero-cilindro.svg" as="image" type="image/svg+xml" fetchpriority="high">'

    if "{{PINS}}" in body:
        body = body.replace("{{PINS}}", (ROOT / "src" / "parts" / "pins.html").read_text())
    body = body.replace("{{CIDADES}}", "".join(f"<option>{c}</option>" for c in CIDADES))
    body = body.replace("{{UNILIST}}", "".join(f'<li style="--i:{i}"><a href="{{{{R}}}}stub.html?u=/unidades/" data-i="{i}"><span>{c}</span>{ic("arrow-up-right")}</a></li>' for i, c in enumerate(CIDADES)))
    body = body.replace("{{R}}", R)
    html = f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,interactive-widget=resizes-content">
<title>{titulo}</title><meta name="description" content="{desc}"><meta name="robots" content="noindex"><meta name="theme-color" content="#066FBA"><link rel="icon" href="{R}assets/svg/marca.svg" type="image/svg+xml">
<link rel="preload" href="{R}assets/fonts/archivo-var-latin.woff2" as="font" type="font/woff2" crossorigin>
{links}
</head><body class="p-{atual}">{sprite}<a class="skip" href="#conteudo">Ir para o conteúdo</a>
<!--chrome:header-->{h}<!--/chrome:header-->
<main id="conteudo">{body}</main>
<!--chrome:footer-->{f}<!--/chrome:footer-->
<!--chrome:sheets-->{s}<!--/chrome:sheets-->
<script src="{R}assets/js/main.js?v={VER}" defer></script></body></html>'''
    dest = ROOT / out
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html)
    return dest, len(html)


def hash_chrome(txt, nome):
    return hashlib.sha1(re.search(rf"<!--chrome:{nome}-->(.*?)<!--/chrome:{nome}-->", txt, re.S).group(1).encode()).hexdigest()[:8]


if __name__ == "__main__":
    # logos derivados que dependem do build
    write_super_css()
    for p in PAGES:
        if (SRC / p[0]).exists():
            d, n = render(p)
            print(f"{d.relative_to(ROOT)}  {n/1024:.0f} KB")
    # integridade: o bloco de header/footer tem o mesmo hash (a menos do prefixo relativo)
    print("(chrome usa prefixo relativo {{R}}; hash comparado apos normalizar)")
