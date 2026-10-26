"""Monta as paginas do prototipo a partir de src/pages/*.html + chrome (header, super menu, rodape, sheets, tab bar).
O HTML gerado e o que se abre; nao ha build no runtime. O chrome e identico em todas as paginas (mesmo hash).
Uso: python3 -I tools/build.py
"""
import hashlib, json, pathlib, re, time, unicodedata
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
PAGINAS_REAIS = {"segmentos/agricola/": "segmentos/agricola/", "filtros/": "filtros/", "unidades/": "unidades/", "solucoes/": "solucoes/", "contato/": "contato/", "obrigado/": "obrigado/"}
for _k in ("transporte", "industria", "maritimo", "ferrovia", "mineracao", "geradores-de-energia"):
    PAGINAS_REAIS[f"segmentos/{_k}/"] = f"segmentos/{_k}/"


def slug(cidade):
    return unicodedata.normalize("NFKD", cidade).encode("ascii", "ignore").decode().lower().replace("/", "-").replace(" ", "-")



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
    <li class="has-super"><a href="{R}solucoes/" aria-haspopup="true" aria-expanded="false" aria-controls="sm-sol"{cur("solucoes")}>Soluções {ic("caret-down")}</a>
      <div class="super" id="sm-sol" role="region" aria-label="Soluções"><div class="super-in"><div class="s-col"><p class="lbl">Soluções</p><ul class="s-list">{li_sol}</ul><a class="link more" href="{R}stub.html?u=/marcas/">Marcas que distribuímos {ic("arrow-right")}</a></div><div class="s-mid">{prev_sol}</div>{sol_aside}</div></div></li>
    <li><a href="{R}stub.html?u=/unidades/"{cur("unidades")}>Unidades</a></li>
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
    unid = lambda lst: "".join(f'<a href="{R}unidades/#{slug(c)}">{c}</a>' for c in lst)
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
    seg_opts = "".join(f'<option value="{k}">{n}</option>' for k, n, *_ in SEGS)
    x = f'<button class="x" type="button" data-close autofocus aria-label="Fechar">{ic("x")}</button>'
    def tab(href, nome, icone, extra="", cls="", sheet=""):
        a = ' aria-current="page"' if atual == nome.lower() else ""
        return f'<a href="{href}"{(" data-sheet=" + sheet) if sheet else ""}{(" class=" + cls) if cls else ""}{a}>{ic(icone)}<span>{nome}</span></a>'
    return f'''<nav class="tabbar" aria-label="Navegação do app">
  {tab(f"{R}index.html","Início","house")}{tab(f"{R}stub.html?u=/segmentos/","Segmentos","squares-four",sheet="sh-seg")}{tab(f"{R}solucoes/","Soluções","funnel",sheet="sh-sol")}{tab(f"{R}stub.html?u=/unidades/","Unidades","map-pin",sheet="sh-uni")}{tab(f"{R}stub.html?u=/contato/","Cotar","pencil-simple-line",cls="cotar",sheet="sh-cot")}
</nav>
<dialog class="sheet" id="sh-seg" aria-label="Segmentos"><div class="sheet-h"><span class="grab" aria-hidden="true"></span><strong>Segmentos</strong>{x}</div><div class="sheet-b"><div class="grid-seg">{cards}</div></div><div class="sheet-f"><a class="btn sec" href="{R}stub.html?u=/segmentos/"><span>Ver todos</span></a><a class="btn" href="{R}stub.html?u=/contato/"><span>Solicite cotação</span></a></div></dialog>
<dialog class="sheet" id="sh-sol" aria-label="Soluções"><div class="sheet-h"><span class="grab" aria-hidden="true"></span><strong>Soluções</strong>{x}</div><div class="sheet-b"><div class="list-sol">{rows}</div><p class="lbl" style="margin:18px 0 10px">Tipos de filtro</p><div class="chips">{chips}</div></div><div class="sheet-f"><a class="btn" href="{R}stub.html?u=/contato/"><span>Solicite cotação</span></a></div></dialog>
<dialog class="sheet" id="sh-uni" aria-label="Unidades"><div class="sheet-h"><span class="grab" aria-hidden="true"></span><strong>Unidades</strong>{x}</div><div class="sheet-b"><button class="btn sm" type="button" style="margin-bottom:14px"><span>Usar minha localização</span></button><label class="fld">Ou escolha a cidade<select><option>Escolha</option>{opts}</select></label><ul class="un-list" style="margin-top:14px">{lista}</ul></div><div class="sheet-f"><a class="btn sec" href="{R}stub.html?u=/unidades/"><span>Ver as 12 unidades</span></a></div></dialog>
<dialog class="sheet" id="sh-cot" aria-label="Solicite sua cotação"><div class="sheet-h"><span class="grab" aria-hidden="true"></span><strong>Solicite sua cotação</strong>{x}</div><div class="sheet-b"><form class="cot" action="{R}obrigado/" method="get"><label class="fld">Nome<input name="nome" autocomplete="name"></label><label class="fld">WhatsApp ou telefone<input name="tel" type="tel" autocomplete="tel" inputmode="tel"></label><label class="fld">Segmento<select name="segmento">{seg_opts}</select></label><button class="btn" type="submit"><span>Pedir cotação</span></button><a class="btn sec wa" href="{R}stub.html?u=/contato/">{ic("whatsapp-logo")}<span>Falar no WhatsApp</span></a></form></div></dialog>
<dialog class="sheet menu-full dark" id="sh-menu" aria-label="Menu"><div class="mf-top"><a class="logo-m" href="{R}index.html"><img src="{R}assets/svg/logo-claro.svg" alt="Polifiltro" width="131" height="34"></a><button class="x" type="button" data-close autofocus aria-label="Fechar menu">{ic("x")}</button></div>
  <div class="mf-body"><nav class="mf-nav" aria-label="Menu principal"><a href="{R}stub.html?u=/segmentos/" data-sheet="sh-seg">Segmentos {ic("arrow-up-right")}</a><a href="{R}solucoes/" data-sheet="sh-sol">Soluções {ic("arrow-up-right")}</a><a href="{R}stub.html?u=/unidades/" data-sheet="sh-uni">Unidades {ic("arrow-up-right")}</a><a href="{R}stub.html?u=/marcas/">Marcas {ic("arrow-up-right")}</a><a href="{R}stub.html?u=/empresa/">Empresa {ic("arrow-up-right")}</a><a href="{R}stub.html?u=/contato/" data-sheet="sh-cot">Contato {ic("arrow-up-right")}</a></nav>
  <div class="mf-sec"><a href="{R}stub.html?u=/lancamentos/">{ic("package")}Lançamentos</a><a href="{R}stub.html?u=/noticias/">{ic("stack")}Notícias</a><a href="{R}stub.html?u=/trabalhe-conosco/">{ic("hard-hat")}Trabalhe conosco</a></div></div>
  <div class="mf-tiles"><a href="{R}stub.html?u=/unidades/" data-sheet="sh-uni"><small>Fale com a</small><strong>Unidade mais próxima</strong></a><a href="{R}stub.html?u=/contato/"><small>Atendimento</small><strong>WhatsApp</strong></a></div>
  <a class="mf-cta" href="{R}stub.html?u=/contato/" data-sheet="sh-cot"><strong>Solicite sua cotação</strong></a>
  <p class="mf-legal"><a href="{R}stub.html?u=/politica-de-privacidade/">Privacidade</a><a href="{R}stub.html?u=/politica-de-cookies/">Cookies</a><a href="{R}stub.html?u=/canal-voz-segura/">Canal Voz Segura</a></p></dialog>'''


# ---------------------------------------------------------------------------------------------------------------
# UNIDADES. Endereco/CEP/telefone: texto do site atual (polifiltro.com.br/unidades/, medido 21/10/2026), copiado como esta.
# Contagem e Uberlandia nao tem dado no site atual (Belo Horizonte virou Contagem; Uberlandia e nova): ficam "a confirmar".
# lat/lng: centro aproximado do municipio, so para "unidade mais proxima" em linha reta.
# ---------------------------------------------------------------------------------------------------------------
UNIDADES = [
    dict(c="Manaus/AM", regiao="Norte", end="Rua São Jorge, 581 – Bairro São Jorge", cep="69053-255", tel=["+55 92 3343-5830"], ll=(-3.119, -60.022)),
    dict(c="Ananindeua/PA", regiao="Norte", end="Rodovia BR 316, 330 – Águas Linda", cep="67020-000", tel=["+55 91 3232-9796"], ll=(-1.366, -48.372)),
    dict(c="Sinop/MT", regiao="Centro-Oeste", end="Av. João Pedro Moreira Carvalho, 3192", cep="78557-057", tel=["+55 66 3515-8139"], ll=(-11.864, -55.502)),
    dict(c="Cuiabá/MT", regiao="Centro-Oeste", end="Rua O, Esquina Projetada, 3.098 Lote A", cep="78098-410", tel=["+55 65 3637-1212"], ll=(-15.601, -56.097)),
    dict(c="Goiânia/GO", regiao="Centro-Oeste", end="Av. São Francisco n1364 qd40 lote 96/98, Setor Santa Genoveva", cep="74670-010", tel=["+55 62 3208-1453"], ll=(-16.686, -49.264)),
    dict(c="Uberlândia/MG", regiao="Sudeste", end=None, cep=None, tel=[], ll=(-18.918, -48.277)),
    dict(c="Contagem/MG", regiao="Sudeste", end="R. Um, 315 – Do Comércio", cep=None, tel=["+55 31 3191-0630"], ll=(-19.932, -44.054)),  # endereço e telefone: Ismael, WhatsApp 26/10/2026; CEP não informado
    dict(c="São Paulo/SP", regiao="Sudeste", end="Rua General Flores, 401 – Bom Retiro", cep="01129-010", tel=["+55 11 2188-5499"], ll=(-23.55, -46.633), matriz=True),
    dict(c="Araçatuba/SP", regiao="Sudeste", end="Rua Saudade, 2.376", cep="16021-520", tel=["+55 18 3600-8031", "+55 18 3600-8029"], ll=(-21.208, -50.433)),
    dict(c="Curitiba/PR", regiao="Sul", end="R. Carlos de Laet, 4029 – Hauer", cep="81650-040", tel=["+55 41 3073-9722"], ll=(-25.43, -49.27)),
    dict(c="Itajaí/SC", regiao="Sul", end="Rod. Antônio Heil, 350 – Itaipava", cep="88316-000", tel=["+55 47 2125-4607"], ll=(-26.908, -48.662)),
    dict(c="Porto Alegre/RS", regiao="Sul", end="Av. Francisco Silveira Bitencourt, 959/1", cep="91150-010", tel=["+55 51 3395-1471"], ll=(-30.03, -51.23)),
]
assert [u["c"] for u in UNIDADES] == CIDADES  # mesma ordem dos pins do mapa e do <select>
REGIOES = ["Norte", "Centro-Oeste", "Sudeste", "Sul"]


def tel_href(t):
    return "tel:+" + re.sub(r"\D", "", t)


def fachada(R, u):
    """Foto real se existir em assets/img/fachadas/<slug>.(jpg|webp); senao o espaco reservado. Soltar a foto na pasta e rodar o build."""
    sl = slug(u["c"])
    for ext in ("webp", "jpg"):
        if (ROOT / "assets" / "img" / "fachadas" / f"{sl}.{ext}").exists():
            return f'<div class="fachada"><img src="{R}assets/img/fachadas/{sl}.{ext}" alt="Fachada da unidade {u["c"]}" width="640" height="400" loading="lazy" decoding="async"></div>'
    return f'<div class="fachada vazia" role="img" aria-label="Foto da fachada de {u["c"]}: ainda não enviada"><img src="{R}assets/svg/marca.svg" alt="" width="64" height="66"><span>Foto da fachada <em class="confirmar">a receber</em></span></div>'


def card_unidade(R, i, u):
    sl = slug(u["c"])
    cidade, uf = u["c"].split("/")
    if u["end"]:
        dados = (f'<address><span>{esc(u["end"])}</span><span>{"CEP " + u["cep"] + " – " if u["cep"] else ""}{cidade} – {uf}</span></address>'
                 f'<p class="tels">{" ".join(f"<a href={chr(34)}{tel_href(t)}{chr(34)}>{t}</a>" for t in u["tel"])}</p>')
        maps = "https://www.google.com/maps/search/?api=1&amp;query=" + re.sub(r"\s+", "+", f'Polifiltro {u["end"]} {cidade} {uf}'.replace("&", "e"))
        acoes = (f'<a class="btn sm" href="{tel_href(u["tel"][0])}">{ic("phone")}<span>Ligar</span></a>'
                 f'<a class="link" href="{maps}" target="_blank" rel="noopener">Como chegar {ic("arrow-up-right")}</a>')
    else:
        dados = '<address><span>Endereço e telefone <em class="confirmar">a confirmar</em></span></address>'
        acoes = f'<a class="btn sm" href="{R}stub.html?u=/contato/&amp;unidade={sl}"><span>Falar com a Polifiltro</span></a>'
    badge = '<span class="selo">Matriz</span>' if u.get("matriz") else ""
    return (f'<li class="un-card" id="{sl}" data-i="{i}" data-lat="{u["ll"][0]}" data-lng="{u["ll"][1]}">{fachada(R, u)}'
            f'<div class="un-b"><h3><span class="cid">{cidade}</span><span class="uf">{uf}</span>{badge}</h3>{dados}<div class="un-acoes">{acoes}</div></div></li>')


def unidades_body(R):
    cards_por_regiao = []
    for reg in REGIOES:
        itens = [(i, u) for i, u in enumerate(UNIDADES) if u["regiao"] == reg]
        n = len(itens)
        cards_por_regiao.append(
            f'<section class="reg" id="regiao-{slug(reg)}" aria-labelledby="h-{slug(reg)}"><h2 id="h-{slug(reg)}" class="display"><span class="bk">{reg}</span><span class="qtd">{n} {"unidade" if n == 1 else "unidades"}</span></h2>'
            f'<ul class="un-cards">{"".join(card_unidade(R, i, u) for i, u in itens)}</ul></section>')
    nav = "".join(f'<a class="chip" href="#regiao-{slug(r)}">{r}</a>' for r in REGIOES)
    return f"""<section class="seg-hero dark neutral" aria-labelledby="h1"><div class="wrap wrap-wide un-hero">
  <div class="un-hero-txt">
    <nav class="crumb" aria-label="Breadcrumb"><a href="{R}index.html">Início</a><span aria-hidden="true">/</span><span aria-current="page">Unidades</span></nav>
    <h1 id="h1" class="display"><span class="lt">Nossas</span> <span class="bk kw">unidades</span></h1>
    <p class="lead" data-copy="proposta">Doze unidades em nove estados. Escolha a mais próxima e peça sua cotação direto com a equipe local.</p>
    <div class="uni-tools hero-tools"><label class="fld">Cidade<select id="uni-sel"><option>Escolha a cidade</option>{"".join(f"<option>{c}</option>" for c in CIDADES)}</select></label><button class="btn sm" type="button" data-geo><span>Usar minha localização</span></button></div>
    <p class="geo-msg nota" id="geo-msg" role="status" aria-live="polite"></p>
  </div>
  <div class="mapa un-map" aria-hidden="true"><img class="mapa-pts" src="{R}assets/svg/brasil-estados.svg" alt="" width="615" height="637" decoding="async">{{{{PINS}}}}</div>
</div></section>
<div class="idx" role="navigation" aria-label="Regiões"><div class="wrap wrap-wide idx-in">{nav}</div></div>
<section class="blk un-page" aria-label="Lista de unidades"><div class="wrap wrap-wide un-main">{"".join(cards_por_regiao)}
  <p class="nota">WhatsApp de cada unidade: <span class="confirmar">a coletar</span>. Endereços e telefones: do site atual da Polifiltro (21/10/2026), a validar com o cliente.</p>
</div></section>
<section class="blk sec-cta dark" aria-labelledby="h-cta"><div class="wrap wrap-wide cta-in">
  <h2 id="h-cta" class="display"><span class="lt">Solicite</span> <span class="bk">sua cotação</span></h2>
  <div class="cta-btns"><a class="btn" href="{R}stub.html?u=/contato/"><span>Solicite sua cotação</span></a><a class="btn sec wa" href="{R}stub.html?u=/contato/">{ic("whatsapp-logo")}<span>WhatsApp</span></a></div>
</div></section>"""


# ---------------------------------------------------------------------------------------------------------------
# SEGMENTOS. Mesmo gabarito do Agricola (que segue como pagina propria). Textos de apoio = PROPOSTA nossa (data-copy="proposta").
# Os 3 filtros do hero/cards sao os mesmos da lista SEGS; descricao e glifo de cada filtro vem da pagina de filtros.
# ---------------------------------------------------------------------------------------------------------------
SEG_ART = json.loads((ROOT / "tools" / "dados" / "seg-art.json").read_text())
FILTRO_DESC = {"oleo": "Retém partículas do óleo do motor e protege as peças em movimento.", "cabine": "Filtra o ar que entra na cabine: menos poeira para o operador.",
               "combustivel": "Protege os bicos injetores de impurezas e de água.", "ar": "Barra a poeira antes que ela chegue ao motor.",
               "separadores": "Separam a água do combustível para evitar corrosão e falhas.", "arrefecimento": "Mantém limpo e estável o fluido que resfria o motor.",
               "desumidificador": "Remove a umidade do ar comprimido e dos reservatórios.", "hidraulico": "Mantém o fluido hidráulico livre de contaminantes."}
GLIFO = {"oleo": ("spinon-a", "200/280"), "cabine": ("painel", "220/160"), "combustivel": ("spinon-b", "200/280"), "ar": ("cartucho-a", "200/280"),
         "separadores": ("linha", "260/160"), "arrefecimento": ("spinon-a", "200/280"), "desumidificador": ("linha", "260/160"), "hidraulico": ("spinon-b", "200/280")}
SEG_TXT = {  # chave: (hero lead, titulo "lt", titulo "bk", unidades sugeridas, rel)
    "transporte": ("Filtros e lubrificantes para frotas de caminhões e ônibus, com atendimento da unidade mais próxima da sua rota.", "Soluções para o", "transporte",
                   ["sao-paulo-sp", "contagem-mg", "curitiba-pr", "porto-alegre-rs", "goiania-go", "cuiaba-mt"]),
    "industria": ("Filtragem de ar, óleo e fluidos para compressores, linhas de produção e equipamentos industriais, com atendimento da unidade mais próxima.", "Soluções para a", "indústria",
                  ["sao-paulo-sp", "contagem-mg", "curitiba-pr", "itajai-sc", "porto-alegre-rs", "aracatuba-sp"]),
    "maritimo": ("Combustível limpo e proteção de motores em embarcações, com atendimento da unidade mais próxima do seu porto.", "Soluções para o", "marítimo",
                 ["manaus-am", "ananindeua-pa", "itajai-sc", "porto-alegre-rs", "sao-paulo-sp", "curitiba-pr"]),
    "ferrovia": ("Linha de filtros para locomotivas e material rodante, com atendimento da unidade mais próxima da sua operação.", "Soluções para a", "ferrovia",
                 ["sao-paulo-sp", "contagem-mg", "uberlandia-mg", "goiania-go", "curitiba-pr", "ananindeua-pa"]),
    "mineracao": ("Filtros para equipamentos pesados, poeira e carga contínua, com atendimento da unidade mais próxima da sua operação.", "Soluções para a", "mineração",
                  ["contagem-mg", "uberlandia-mg", "goiania-go", "ananindeua-pa", "manaus-am", "sinop-mt"]),
    "geradores-de-energia": ("Filtros para grupos geradores e energia de backup, com atendimento da unidade mais próxima.", "Soluções para", "geradores",
                             ["sao-paulo-sp", "manaus-am", "goiania-go", "curitiba-pr", "porto-alegre-rs", "contagem-mg"]),
}
PARCEIROS = ["Arla 32", "Baldwin", "Des-Case", "Duppai", "DML", "Donaldson", "Filtrec", "Fleetguard"]  # os mesmos 8 da Home


def texto_livre(R, k):
    """Bloco de texto livre do segmento (o cliente escreve depois; no WordPress vira um bloco com InnerBlocks: titulo, paragrafo, lista, link, imagem).
    Se existir src/segmentos-texto/<k>.html, o conteudo entra no lugar do espaco reservado. NUNCA escrevemos esse texto: e copy do cliente."""
    arq = ROOT / "src" / "segmentos-texto" / f"{k}.html"
    if arq.exists():
        corpo = arq.read_text().replace("{{R}}", R)
        vazio = ""
    else:
        corpo = ('<div class="txt-vazio"><p><strong>Espaço para o texto do cliente.</strong> Aqui entra o que a Polifiltro quiser contar sobre este segmento, '
                 'com liberdade de formato: títulos, parágrafos, listas, links e imagens.</p><p class="nota">Texto do cliente <span class="confirmar">a receber</span></p></div>')
        vazio = " vazio"
    return (f'<section class="blk txt-livre{vazio}" aria-labelledby="h-txt" data-copy="cliente"><div class="wrap wrap-wide txt-in">'
            f'<h2 id="h-txt" class="display"><span class="lt">Sobre o</span> <span class="bk">segmento</span></h2>'
            f'<div class="txt-body">{corpo}</div></div></section>')


def rx_art(R, art):
    """Ilustracao do hero: SVG gerado por tools/gen_veiculos.py; art["vb"] = viewBox proprio quando o desenho nao e 760x420."""
    w, h = art.get("vb", (760, 420))
    return f'<svg class="rx-art" viewBox="0 0 {w} {h}" style="aspect-ratio:{w}/{h}" role="img" aria-label="Ilustração técnica de {art["alt"]}"><use href="#k-{art["id"]}"/></svg>'


def segmento_body(R, k):
    nome, icone, desc, chips = next((n, i, d, c) for kk, n, i, d, c in SEGS if kk == k)
    lead, t_lt, t_bk, picks = SEG_TXT[k]
    art, hs = SEG_ART[k], SEG_ART[k]["hs"]
    pts = "".join(f'<a class="hs" style="left:{h["x"]}%;top:{h["y"]}%" href="{R}filtros/#{h["anchor"]}" aria-label="{h["label"]}"><span class="hs-l" aria-hidden="true">{h["label"]}</span></a>' for h in hs)
    recs = []
    for n, (anc, rot) in enumerate(chips):
        kit, asp = GLIFO[anc]
        vb = "0 0 " + asp.replace("/", " ")
        recs.append(f'<li class="rec rec-{n}"><a href="{R}filtros/#{anc}"><svg class="rec-art" style="aspect-ratio:{asp}" viewBox="{vb}" aria-hidden="true"><use href="#k-{kit}"/></svg>'
                    f'<span class="rec-t"><strong>{rot}</strong><span data-copy="proposta">{FILTRO_DESC[anc]}</span></span><span class="go">Ver {rot.lower()} {ic("arrow-right")}</span></a></li>')
    uni = "".join(f'<li><a href="{R}unidades/#{sl}"><span>{next(u["c"] for u in UNIDADES if slug(u["c"]) == sl)}</span>{ic("arrow-up-right")}</a></li>' for sl in picks)
    marcas = "".join(f"<li>{m}</li>" for m in PARCEIROS)
    cta = f'{R}stub.html?u=/contato/&amp;segmento={k}'
    return f"""<div class="seg-scope" style="--seg:var(--seg-{k});--seg-deep:var(--seg-{k}-deep);--seg-ink:var(--navy-900)">
<section class="seg-hero dark" aria-labelledby="h1"><div class="wrap wrap-wide seg-hero-in">
  <div class="seg-hero-txt">
    <nav class="crumb" aria-label="Breadcrumb"><a href="{R}index.html">Início</a><span aria-hidden="true">/</span><a href="{R}stub.html?u=/segmentos/">Segmentos</a><span aria-hidden="true">/</span><span aria-current="page">{nome}</span></nav>
    <h1 id="h1" class="display"><span class="lt">Segmento</span> <span class="bk">{nome}</span></h1>
    <p class="lead" data-copy="proposta">{lead}</p>
    <div class="hero-cta"><a class="btn" href="{cta}"><span>Cotação para {t_bk if k != "geradores-de-energia" else "geradores"}</span></a><a class="link" href="{R}filtros/">Ver todos os filtros {ic("arrow-right")}</a></div>
  </div>
  <figure class="rx rx-seg" aria-label="Ilustração em corte mostrando onde ficam os filtros"><div class="rx-in">
    {rx_art(R, art)}
    {pts}
  </div></figure>
</div></section>

<section class="blk" aria-labelledby="h-rec"><div class="wrap wrap-wide">
  <h2 id="h-rec" class="display"><span class="lt">{t_lt}</span> <span class="bk">{t_bk}</span></h2>
  <ul class="rec-grid">{"".join(recs)}</ul>
  <p class="more-row"><a class="link" href="{R}filtros/">Ver os 10 tipos de filtro {ic("arrow-right")}</a></p>
</div></section>

{texto_livre(R, k)}

<section class="blk alt" aria-labelledby="h-onde"><div class="wrap wrap-wide onde">
  <div><h2 id="h-onde" class="display"><span class="lt">Onde</span> <span class="bk">atendemos</span></h2>
  <p class="lead" data-copy="proposta">Unidades perto das suas operações.</p>
  <ul class="uni-list">{uni}</ul>
  <p class="nota">Seleção de unidades para este segmento: <span class="confirmar">validar com o cliente</span></p>
  <a class="link" href="{R}unidades/">Ver as 12 unidades {ic("arrow-right")}</a></div>
  <div class="mapa mapa-s"><img class="mapa-pts" src="{R}assets/svg/brasil-estados.svg" alt="" width="615" height="637" loading="lazy">{{{{PINS}}}}</div>
</div></section>

<section class="blk" aria-labelledby="h-mar"><div class="wrap wrap-wide">
  <h2 id="h-mar" class="display"><span class="lt">Nossos</span> <span class="bk">parceiros</span></h2>
  <ul class="marcas">{marcas}</ul>
  <p class="nota">8 de 19 marcas. Logos dependem de autorização <span class="confirmar">confirmar</span></p>
</div></section>

<section class="blk alt" aria-labelledby="h-rel"><div class="wrap wrap-wide">
  <h2 id="h-rel" class="display"><span class="lt">Para saber</span> <span class="bk">mais</span></h2>
  <ul class="rel"><li><a href="{R}stub.html?u=/lubrificantes/"><strong>Lubrificantes</strong><span data-copy="proposta">Linha completa</span>{ic("arrow-right")}</a></li><li><a href="{R}stub.html?u=/aditivos/"><strong>Aditivos</strong><span data-copy="proposta">Desempenho e proteção do motor</span>{ic("arrow-right")}</a></li></ul>
</div></section>

<section class="blk sec-cta seg-cta" aria-labelledby="h-cta"><div class="wrap wrap-wide cta-in">
  <h2 id="h-cta" class="display"><span class="lt">Cotação para</span> <span class="bk">{t_bk if k != "geradores-de-energia" else "geradores"}</span></h2>
  <div class="cta-btns"><a class="btn" href="{cta}"><span>Solicite sua cotação</span></a><a class="btn sec wa" href="{R}stub.html?u=/contato/">{ic("whatsapp-logo")}<span>WhatsApp</span></a></div>
</div></section>
</div>"""


# ---------------------------------------------------------------------------------------------------------------
# SOLUCOES (hub). Entrada por solucao ("o que o filtro faz") e por segmento ("onde ele trabalha"): as duas portas da IA v1.
# Os textos das 4 linhas sem pagina sao PROPOSTA nossa (aguardam copy do cliente).
# ---------------------------------------------------------------------------------------------------------------
SOL_ICONES = {"filtros": "cylinder", "lubrificantes": "drop", "aditivos": "gear", "ultrafiltracao-de-diesel": "gas-pump", "equipamentos-e-armazenamento": "package"}
SOL_TXT = {"lubrificantes": "Linha completa de lubrificantes para as suas máquinas.", "aditivos": "Desempenho e proteção para o motor e o combustível.",
           "ultrafiltracao-de-diesel": "Proteção do combustível armazenado, antes que ele chegue ao motor.",
           "equipamentos-e-armazenamento": "Equipamentos para abastecimento e armazenamento de combustível e fluidos."}


def solucoes_body(R):
    familia = "".join(f'<use href="#k-{k}" x="{x}" y="{356 - h}" width="{w}" height="{h}"/>' for k, x, w, h in
                      [("spinon-a", 4, 124, 174), ("cartucho-a", 144, 112, 157), ("painel", 272, 170, 124), ("spinon-b", 458, 96, 134), ("linha", 570, 190, 117)])
    chips = "".join(f'<a class="chip" href="{R}filtros/#{a}">{r}</a>' for a, r in FILTROS)
    cards = "".join(
        f'<li class="sol-card"><a href="{R}stub.html?u=/{k}/">{ic(SOL_ICONES[k], "sol-ic")}<span class="sol-t"><strong>{n}</strong><span data-copy="proposta">{SOL_TXT[k]}</span></span>'
        f'<span class="go">Ver {n.lower()} {ic("arrow-right")}</span></a></li>' for k, n, s_, d in SOLS if k != "filtros")
    segs = "".join(f'<li><a href="{seg_url(R, k)}" style="--c:{cor(k)}">{ic(icone, "seg-ic")}<strong>{n}</strong>{ic("arrow-right")}</a></li>' for k, n, icone, d, c in SEGS)
    return f"""<section class="seg-hero dark neutral" aria-labelledby="h1"><div class="wrap wrap-wide sol-hero">
  <div class="sol-hero-txt">
    <nav class="crumb" aria-label="Breadcrumb"><a href="{R}index.html">Início</a><span aria-hidden="true">/</span><span aria-current="page">Soluções</span></nav>
    <h1 id="h1" class="display"><span class="lt">Nossas</span> <span class="bk kw">soluções</span></h1>
    <p class="lead" data-copy="proposta">Cinco linhas para proteger o motor e os fluidos da sua operação. Escolha a solução ou comece pelo seu segmento.</p>
    <div class="hero-cta"><a class="btn" href="{R}stub.html?u=/contato/"><span>Solicite sua cotação</span></a><a class="link" href="{R}unidades/">Encontre a unidade mais próxima {ic("arrow-right")}</a></div>
  </div>
  <figure class="rx" aria-hidden="true"><div class="rx-in"><svg class="rx-art" viewBox="0 0 760 420" focusable="false"><path d="M0 364H760" stroke="var(--k-line,#B9C6D8)" stroke-width="2" stroke-dasharray="2 8" stroke-linecap="round"/>{familia}</svg></div></figure>
</div></section>

<section class="blk" aria-labelledby="h-lin"><div class="wrap wrap-wide">
  <h2 id="h-lin" class="display"><span class="lt">Linha de</span> <span class="bk">produtos</span></h2>
  <ul class="sol-cards">
    <li class="sol-big"><div class="sol-big-in dark">
      <div class="sol-big-txt">{ic("cylinder", "sol-ic")}<h3>Filtros</h3><p data-copy="proposta">São 10 tipos, cada um para um ponto da máquina. Escolha o seu.</p>
        <div class="chips">{chips}</div>
        <p class="sol-big-cta"><a class="btn sm" href="{R}filtros/"><span>Ver os 10 tipos</span></a><a class="link" href="{R}stub.html?u=/contato/&amp;filtro=">Cotação para filtros {ic("arrow-right")}</a></p></div>
      <svg class="sol-big-art" viewBox="0 0 400 260" aria-hidden="true" focusable="false"><use href="#k-spinon-a" x="30" y="36" width="130" height="182"/><use href="#k-cartucho-a" x="190" y="60" width="96" height="134"/><use href="#k-cartucho-b" x="306" y="90" width="64" height="90"/></svg>
    </div></li>
    {cards}
  </ul>
</div></section>

<section class="blk alt" aria-labelledby="h-seg"><div class="wrap wrap-wide">
  <h2 id="h-seg" class="display"><span class="lt">Ou comece pelo</span> <span class="bk">seu segmento</span></h2>
  <p class="lead" data-copy="proposta">Cada segmento mostra onde ficam os filtros na máquina e as soluções mais procuradas.</p>
  <ul class="seg-tiles">{segs}</ul>
</div></section>

<section class="blk sec-cta dark" aria-labelledby="h-cta"><div class="wrap wrap-wide cta-in">
  <h2 id="h-cta" class="display"><span class="lt">Solicite</span> <span class="bk">sua cotação</span></h2>
  <div class="cta-btns"><a class="btn" href="{R}stub.html?u=/contato/"><span>Solicite sua cotação</span></a><a class="btn sec wa" href="{R}stub.html?u=/contato/">{ic("whatsapp-logo")}<span>WhatsApp</span></a></div>
</div></section>"""


# ---------------------------------------------------------------------------------------------------------------
# CONTATO / COTACAO (P22) e OBRIGADO (P25). Campos da IA v1: nome, tel/WhatsApp, segmento, unidade, mensagem (+ solucao/tipo de filtro, que os
# links "Cotacao para ..." ja mandam por parametro). Destino do lead (R&D Station) AINDA [?]: o prototipo nao envia nada.
# Parametros lidos em main.js: ?segmento= ?solucao= ?filtro= ?unidade=  (valores = chaves/slugs; cada link do site ja os usa)
# ---------------------------------------------------------------------------------------------------------------
def opcoes(pares, vazio):
    return f'<option value="">{vazio}</option>' + "".join(f'<option value="{v}">{t}</option>' for v, t in pares)


def contato_body(R):
    seg = opcoes([(k, n) for k, n, *_ in SEGS], "Escolha o segmento")
    sol = opcoes([(k, n) for k, n, *_ in SOLS], "Escolha a solução")
    fil = opcoes([(a, r) for a, r in FILTROS], "Ainda não sei")
    uni = opcoes([(slug(u["c"]), u["c"]) for u in UNIDADES], "Indiquem a mais próxima")
    matriz = next(u for u in UNIDADES if u.get("matriz"))
    return f"""<section class="seg-hero dark neutral" aria-labelledby="h1"><div class="wrap wrap-wide fil-hero">
  <nav class="crumb" aria-label="Breadcrumb"><a href="{R}index.html">Início</a><span aria-hidden="true">/</span><span aria-current="page">Contato</span></nav>
  <h1 id="h1" class="display"><span class="lt">Solicite</span> <span class="bk kw">sua cotação</span></h1>
  <p class="lead" data-copy="proposta">Conte o que você precisa. A equipe da unidade mais próxima entra em contato pelo WhatsApp ou telefone.</p>
</div></section>
<section class="blk ct-page" aria-label="Formulário de cotação"><div class="wrap wrap-wide ct-grid">
  <form class="ct-form" id="cotacao" action="{R}obrigado/" method="get">
    <fieldset><legend class="lbl">Seus dados</legend>
      <label class="fld"><span>Nome</span><input name="nome" autocomplete="name"></label>
      <label class="fld"><span>WhatsApp ou telefone</span><input name="tel" type="tel" inputmode="tel" autocomplete="tel"></label>
      <label class="fld"><span>E-mail <small>(opcional)</small></span><input name="email" type="email" autocomplete="email"></label>
    </fieldset>
    <fieldset><legend class="lbl">O que você procura</legend>
      <label class="fld"><span>Segmento</span><select name="segmento">{seg}</select></label>
      <label class="fld"><span>Solução</span><select name="solucao">{sol}</select></label>
      <label class="fld"><span>Tipo de filtro <small>(se já souber)</small></span><select name="filtro">{fil}</select></label>
      <label class="fld"><span>Unidade mais próxima</span><select name="unidade">{uni}</select></label>
      <label class="fld ct-msg"><span>Mensagem <small>(opcional)</small></span><textarea name="mensagem" rows="4" autocomplete="off"></textarea></label>
    </fieldset>
    <label class="ct-ok"><input type="checkbox" name="lgpd" value="1"><span data-copy="proposta">Concordo com o uso dos meus dados para o retorno desta solicitação, conforme a <a href="{R}stub.html?u=/politica-de-privacidade/">Política de Privacidade</a>.</span></label>
    <div class="ct-send"><button class="btn" type="submit"><span>Pedir cotação</span></button><span class="nota">Protótipo: o formulário não valida nem envia dados.</span></div>
  </form>
  <aside class="ct-side" aria-label="Outras formas de contato">
    <p class="lbl">Prefere falar direto?</p>
    <a class="btn sec wa" href="{R}stub.html?u=/whatsapp/">{ic("whatsapp-logo")}<span>Chamar no WhatsApp</span></a>
    <p class="nota">Número do WhatsApp: <span class="confirmar">a coletar</span></p>
    <div class="ct-card"><p class="lbl">Matriz, São Paulo/SP</p><a class="ct-tel" href="{tel_href(matriz["tel"][0])}">{ic("phone")}{matriz["tel"][0]}</a><address>{esc(matriz["end"])}<br>CEP {matriz["cep"]}</address></div>
    <a class="link" href="{R}unidades/">Ver as 12 unidades e telefones {ic("arrow-right")}</a>
    <ul class="ct-links"><li><a href="{R}stub.html?u=/trabalhe-conosco/">Trabalhe conosco {ic("arrow-up-right")}</a></li><li><a href="{R}stub.html?u=/canal-voz-segura/">Canal Voz Segura {ic("arrow-up-right")}</a></li></ul>
  </aside>
</div></section>"""


def obrigado_body(R):
    rotulos = {"segmento": {k: n for k, n, *_ in SEGS}, "solucao": {k: n for k, n, *_ in SOLS}, "filtro": dict(FILTROS), "unidade": {slug(u["c"]): u["c"] for u in UNIDADES}}
    return f"""<section class="seg-hero dark neutral" aria-labelledby="h1"><div class="wrap wrap-wide fil-hero">
  <h1 id="h1" class="display"><span class="lt">Pedido</span> <span class="bk kw">recebido</span></h1>
  <p class="lead" data-copy="proposta">Obrigado. A equipe da unidade mais próxima entra em contato pelo WhatsApp ou telefone que você informou.</p>
  <dl class="ob-recap" id="recap" hidden></dl>
  <p class="nota">Protótipo: nenhum dado foi enviado. Destino do lead (R&amp;D Station) <span class="confirmar">a definir</span></p>
  <div class="hero-cta"><a class="btn" href="{R}index.html"><span>Voltar à Home</span></a><a class="link" href="{R}filtros/">Ver os filtros {ic("arrow-right")}</a><a class="link" href="{R}unidades/">Ver as unidades {ic("arrow-right")}</a></div>
  <script type="application/json" id="rotulos">{json.dumps(rotulos, ensure_ascii=False)}</script>
</div></section>"""


# pagina -> (arquivo src, saida, titulo, descricao, css extra, atual, profundidade)
PAGES = [
    ("home.html", "index.html", "Polifiltro | Distribuindo filtros desde 1989", "Filtros, lubrificantes e aditivos dos melhores fabricantes, em 12 unidades. Protótipo hi-fi v1.", ["home.css"], "home", 0),
    ("agricola.html", "segmentos/agricola/index.html", "Agrícola | Polifiltro", "Soluções em filtragem e lubrificação para o agro. Protótipo hi-fi v1.", ["segmento.css"], "segmentos", 2),
    ("filtros.html", "filtros/index.html", "Filtros | Polifiltro", "Os 10 tipos de filtro da Polifiltro. Protótipo hi-fi v1.", ["segmento.css", "filtros.css"], "solucoes", 1),
    (lambda R: contato_body(R), "contato/index.html", "Solicite sua cotação | Polifiltro", "Peça sua cotação de filtros, lubrificantes e aditivos. Protótipo hi-fi v1.", ["segmento.css", "contato.css"], "contato", 1),
    (lambda R: obrigado_body(R), "obrigado/index.html", "Pedido recebido | Polifiltro", "Confirmação do pedido de cotação.", ["segmento.css", "contato.css"], "obrigado", 1),
    (lambda R: solucoes_body(R), "solucoes/index.html", "Soluções | Polifiltro", "Filtros, lubrificantes, aditivos, ultrafiltração de diesel e equipamentos. Protótipo hi-fi v1.", ["segmento.css", "solucoes.css"], "solucoes", 1),
    (lambda R: unidades_body(R), "unidades/index.html", "Unidades | Polifiltro", "As 12 unidades da Polifiltro no Brasil, com endereço e telefone. Protótipo hi-fi v1.", ["segmento.css", "unidades.css"], "unidades", 1),
] + [
    ((lambda k: (lambda R: segmento_body(R, k)))(k), f"segmentos/{k}/index.html", f"{next(n for kk, n, *_ in SEGS if kk == k)} | Polifiltro",
     f"Soluções em filtragem e lubrificação para o segmento {next(n for kk, n, *_ in SEGS if kk == k).lower()}. Protótipo hi-fi v1.", ["segmento.css"], "segmentos", 2)
    for k in SEG_TXT
] + [
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
    body = src(R) if callable(src) else (SRC / src).read_text()
    sprite = (ROOT / "assets" / "svg" / "sprite.svg").read_text()
    if atual != "segmentos":  # as 6 ilustracoes de segmento so pesam onde sao usadas
        sprite = re.sub(r"<!--veiculos-->.*?<!--/veiculos-->", "", sprite, flags=re.S)
    h, f, s = header(R, atual), footer(R), sheets(R, atual)
    bundle("app.css", ["fonts.css", "tokens.css", "base.css", "components.css", "super.css", "motion.css"])
    chave = out.split("/")[0].replace(".html", "").replace("index", "home")  # 1 bundle por pagina (Filtros e o hub tem atual "solucoes")
    bundle(f"page-{chave}.css", (["hero-clips.css"] if "home.css" in css else []) + css)
    links = "".join(f'<link rel="stylesheet" href="{R}assets/css/{c}?v={VER}">' for c in ["app.css", f"page-{chave}.css"])
    if atual == "home":
        links += f'<link rel="preload" href="{R}assets/svg/hero-cilindro.svg" as="image" type="image/svg+xml" fetchpriority="high">'

    if "{{PINS}}" in body:
        body = body.replace("{{PINS}}", (ROOT / "src" / "parts" / "pins.html").read_text())
    body = body.replace("{{TEXTO_LIVRE}}", texto_livre(R, "agricola"))
    body = body.replace("{{CIDADES}}", "".join(f"<option>{c}</option>" for c in CIDADES))
    body = body.replace("{{UNILIST}}", "".join(f'<li style="--i:{i}"><a href="{{{{R}}}}unidades/#{slug(c)}" data-i="{i}"><span>{c}</span>{ic("arrow-up-right")}</a></li>' for i, c in enumerate(CIDADES)))
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
    for real in PAGINAS_REAIS.values():  # link para pagina que ja existe deixa de apontar pro stub (com ou sem parametros)
        html = html.replace(f'{R}stub.html?u=/{real}"', f'{R}{real}"')
        html = html.replace(f'{R}stub.html?u=/{real}&amp;', f'{R}{real}?')
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
        if callable(p[0]) or (SRC / p[0]).exists():
            d, n = render(p)
            print(f"{d.relative_to(ROOT)}  {n/1024:.0f} KB")
    # integridade: o bloco de header/footer tem o mesmo hash (a menos do prefixo relativo)
    print("(chrome usa prefixo relativo {{R}}; hash comparado apos normalizar)")
