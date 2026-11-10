---
tipo: readme-prototipo
projeto: "[[@Polifiltro]]"
versao: v1
status: 🟡 PROPOSTA — protótipo hi-fi para a reunião de layout (até 23/10/2026); nada decidido pela agência
created: 2026-10-10
---

# Protótipo hi-fi v1 — Polifiltro (Home + 7 segmentos + Filtros + Unidades + institucionais)

> **Projeto Konvictus, não Incuca:** sem `report/`, sem modo espelho, sem `incuca-ai`. Nada vai ao grupo do cliente antes de Ismael/Vitória verem.
> **Copy do cliente não foi editada.** Onde o cliente não tem texto, o texto é **proposta nossa** (marcado `data-copy="proposta"` no HTML).

## Como abrir
```bash
cd Design-projects/Site/v1
python3 tools/serve.py 8742        # servidor local com gzip (sem cache)
open http://127.0.0.1:8742/        # View Transitions só funcionam em http, não em file://
```
Parar o servidor: `pkill -f "serve.py 8742"`. Reconstruir páginas após editar `src/` ou os CSS parciais: `python3 -I tools/build.py`.

## Atualização 10/11/2026 — conteúdo de exemplo (lorem + fotos Unsplash) e páginas que faltavam
> Pedido do Douglas: onde não há texto do cliente, montar com **lorem ipsum** e **fotos do Unsplash**, para já termos protótipo de tudo. Tudo marcado "exemplo" / "a receber do cliente" (chip tracejado).
- **Fotos:** 21 imagens do Unsplash em `assets/img/stock/` (1200x800, ~4 MB no total; ids em `CREDITOS.md`). **Provisórias: trocar por fotos do cliente.** Pesam; otimizar (WebP, menor) antes de ir ao ar.
- **Notícias, com listagem e view:** `noticias/` (destaque + lista, chips de categoria que filtram) e 6 artigos de exemplo (`noticias/noticia-exemplo-NN/`: capa, texto, citação, lista, "Leia também").
- **Lançamentos, com listagem e view:** mesmo gabarito (`lancamentos/` + 3 itens de exemplo).
- **Unidades, com listagem e view:** a view (`unidades/<cidade-uf>/`) agora tem texto de exemplo, foto, galeria, "Quem atendemos" e a cor oficial da unidade.
- **Copa Truck** (`copa-truck/`, nova): como participar (3 passos), cadastro da nota fiscal, **etapas com estados de exemplo** (encerrada, esgotado, inscrições abertas, em breve) e regulamento. **A regra do ingresso segue em aberto**; datas e estados são exemplo. Linkada no rodapé e no menu do celular.
- **Construção** (segmento novo, linha amarela): herói com **foto** (não há ilustração em corte), mesma estrutura dos outros, faixa na Home e item nos menus. **Ainda é pergunta aberta ao Ismael se é segmento ou subitem.** Cor `--seg-construcao` provisória (perto de Transporte e Geradores).
- **Soluções (Aditivos, Ultrafiltração, Equipamentos) e páginas legais** agora com lorem e fotos, no lugar do espaço reservado. **"Sobre o segmento"** dos segmentos também.
- **Verificado:** 50 páginas, 0 links locais quebrados (só o botão do WhatsApp cai no stub, número a coletar); nenhuma imagem quebrada; sem rolagem horizontal em 360 e 1440 px nas páginas novas; contraste 0 falhas. **Não verificado:** Lighthouse, iOS Safari real, 768 e 1920 px, leitor de tela.

## Atualização 09/11/2026 — páginas restantes da IA v1 + ajustes da call de 07/11
> Origem dos pedidos: [[../../../Estratégia/Analises/ata-call-ismael-2026-11-07|ata da call de 07/11]]. Prazo: site no ar ainda em novembro.
- **12 páginas institucionais/soluções novas** (as 25 da IA v1, exceto Notícias): `segmentos/` (hub), `empresa/`, `qualidade-e-certificados/`, `lubrificantes/`, `aditivos/`, `ultrafiltracao-de-diesel/`, `equipamentos-e-armazenamento/`, `marcas/`, `lancamentos/`, `trabalhe-conosco/`, `politica-de-privacidade/`, `politica-de-cookies/`. Código em `tools/build.py` (bloco "PAGINAS RESTANTES") e `assets/css/inst.css`.
- **Copy do cliente, sem edição** (do site atual, copiado em 09/11, marcada `data-copy="cliente"`): História, Política da Qualidade, ISO 9001, números (20.000 / 30.000 / 200), Lubrificantes (Petrol, Repsol, Valvoline, YPF, Idemitsu) e Trabalhe conosco (com `rh@polifiltro.com.br`). O texto de História lista Belo Horizonte e Araçatuba como matriz; o de Unidades, Contagem e São Paulo. Fica para confirmar.
- **Sem texto do cliente ainda** (espaço reservado `.txt-vazio`, "a receber"): Aditivos, Ultrafiltração, Equipamentos, os textos de cada unidade e as **páginas legais** (o texto jurídico não foi enviado; só a estrutura de seções). **Lançamentos** tem estado vazio porque a página do site atual também está vazia.
- **Notícias (P20) não foi desenhada**, de propósito: blog fica fora por decisão de 07/11 ([[../../../Estratégia/global-Docs/Tradeoff/tradeoffs-call-2026-11-07|T-04]]). Links para `/noticias/` ainda caem no `stub.html`.
- **Página por unidade** (N-02): `unidades/<cidade-uf>/` ×12, gerada de `UNIDADES`, com fachada, endereço, telefone, "Como chegar", cotação já direcionada, bloco "Sobre a unidade" reservado e lista das outras unidades. Os cards de Unidades ganharam o link "Página da unidade".
- **Mapa por estado** (N-01): `assets/svg/brasil-estados.svg` pinta AM, PA, MT, GO, MG, SP, PR, SC e RS com a **paleta oficial da Política de Identidade Visual** (Marketing Polifiltro v1.0, set/2026; PDF reenviado pelo Ismael em 14/10), hex exato, sem clarear (`tools/gen_brasil.py`, tabela `COR_UF`). Estado com mais de uma unidade usa a da matriz/capital (SP = matriz `#066FBA`, MT = Cuiabá, MG = Belo Horizonte; **Contagem ainda sem cor própria**). Como SP usa o mesmo azul do fundo do herói, o mapa do herói de Unidades ganhou uma placa marinho atrás. Estado novo = uma linha em `COR_UF`. (Na primeira rodada de 09/11 eu tinha amostrado as cores do vídeo do Instagram; foi substituído pela paleta oficial.)
- **Cor de cada unidade** (hex oficial) aparece na faixa do herói de cada página de unidade (`UNIT_COR` em `tools/build.py`).
- **Cotação com região obrigatória** (N-04): campo **Estado** (obrigatório, com erro inline e foco) e **Cidade** (opcional) no `contato/` e no formulário rápido da aba Cotar. Mostra "Seu atendimento será feito pela Polifiltro <cidade>"; em **SP, MG e MT** (duas unidades) pede para escolher a unidade. Vindo da página de uma unidade, já abre com estado e unidade. **Regra de UF → unidade: WhatsApp do Ismael, 07/11 12:48.** Estados sem unidade: texto de fallback é **proposta nossa**. **Só o estado é validado; nada é enviado** (decisão de 21/10 mantida para o resto). WhatsApp das unidades: **a coletar**.
- **Pequenos ajustes:** faixa verde do Agrícola deixou de vazar no herói das páginas neutras; "Canal Voz Segura" aponta para o link externo da IA v1 (`aloetica.com.br/polifiltro`).
- **Fora desta rodada (depende de gente):** regra real do ingresso da Copa Truck (P-03), confirmação de que Construção é segmento, **logos de marcas** (autorização), texto real das unidades e das páginas legais, WhatsApp das unidades.
- **Verificado:** 38 páginas, 0 links locais quebrados; sem rolagem horizontal em 360 e 1440 px nas páginas novas; contraste dos segmentos 0 falhas; validação do estado (bloqueia envio, foca o campo); fluxo unidade → cotação. **Não verificado:** Lighthouse das páginas novas, iOS Safari real, 768 e 1920 px, leitor de tela.

## Atualização 21/10/2026 — segmentos restantes + página Unidades (pedido do Ismael, 16/10)
- **6 segmentos novos** (Transporte, Indústria, Marítimo, Ferrovia, Mineração, Geradores de energia), mesmo gabarito do Agrícola: herói com **ilustração em corte e 3 hotspots de filtro**, soluções, onde atendemos, parceiros, CTA. Arte: `tools/gen_veiculos.py` (escreve no sprite e em `tools/dados/seg-art.json`); páginas: `segmento_body()` em `tools/build.py`. O glifo de cada filtro é o mesmo da página de Filtros.
- **Página Unidades** (`unidades/`): cards por região (Norte, Centro-Oeste, Sudeste, Sul), mapa no herói, "usar minha localização" (unidade mais próxima em linha reta), `tel:` e "Como chegar". **Dados de endereço/telefone vêm do site atual** (polifiltro.com.br/unidades, 21/10/2026), copiados como estão. **Contagem e Uberlândia sem dado** (BH virou Contagem; Uberlândia é nova) → "a confirmar".
- **Fotos de fachada: espaço reservado.** Soltar `assets/img/fachadas/<cidade-uf>.webp|jpg` (ver `LEIA-ME.md` da pasta) e rodar `python3 -I tools/build.py`. As fotos de cidade em `assets/img/unidades/` seguem só no hover do mapa (desktop).
- **Bloco de texto livre em cada segmento** ("Sobre o segmento"): espaço para o cliente escrever depois, com título, parágrafos, listas, links, citação e imagem (a tipografia cobre tudo isso). Hoje mostra um espaço reservado. Quando o texto chegar, salvar o HTML em `src/segmentos-texto/<segmento>.html` (ex.: `agricola.html`) e rodar `python3 -I tools/build.py`. No WordPress vira um bloco com `InnerBlocks`, sem HTML fixo. **Esse texto é copy do cliente: não escrevemos nem editamos.**
- **Contato e cotação** (`contato/`) + **Obrigado** (`obrigado/`): formulário com os campos da IA v1 (nome, WhatsApp/telefone, e-mail, segmento, solução, tipo de filtro, unidade, mensagem, aceite LGPD). Todo botão "Cotação para…" do site já abre o formulário preenchido (`?segmento=` `?solucao=` `?filtro=` `?unidade=`), e o formulário do celular (aba Cotar) também envia para `obrigado/`. **Por decisão do Douglas (21/10/2026) é só validação de página: sem validação de campo e sem envio.** O botão só leva a `obrigado/`, com apenas segmento/solução/filtro/unidade na URL (nada pessoal). Destino do lead (R&D Station) a definir. Textos de apoio e do aceite LGPD são proposta nossa. Número de WhatsApp: a coletar.
- **Hub Soluções** (`solucoes/`): entrada por solução (Filtros com os 10 tipos, Lubrificantes, Aditivos, Ultrafiltração de diesel, Equipamentos e armazenamento) e por segmento (7 tiles). É o destino do "Soluções" do menu e da tab bar. As 4 linhas além de Filtros ainda não têm página (vão ao `stub.html`); os textos delas são proposta nossa.
- **Correção:** hotspots do trator (Home e Agrícola) eram calibrados à mão contra o padding da figura e desalinhavam fora de 1440 px; agora ficam presos ao SVG (`.rx-in`, y exato 59,3%).
- **Proposta nossa, a validar:** seleção de unidades por segmento ("onde atendemos"); textos de apoio dos segmentos; os 8 parceiros repetem os da Home.
- **Copy do cliente mantida como veio:** "Águas Linda" (Ananindeua) e "n1364 qd40" (Goiânia) parecem erro de digitação no site atual; não corrigi (copy do cliente é imutável), fica para confirmar.
- **Não medido:** Lighthouse das páginas novas, iOS Safari real, botão de localização (precisa da permissão do navegador).

## Design Read e dials
*Distribuidor industrial B2B (operadores de frota, agro, mineração, compradores). Linguagem de engenharia de precisão / blueprint técnico, com tipografia bold e corte em raio-X.*
`DESIGN_VARIANCE 8 · MOTION_INTENSITY 6 · VISUAL_DENSITY 4`.

## A assinatura: "A passagem pelo filtro"
O hero **é** o negócio: partículas escuras (sujeira) entram pela esquerda, atravessam o **cilindro inclinado do logo** em corte (pregas de mídia filtrante) e saem como **linhas azuis limpas**. Geometria rígida, uma cor de acento.
- **2 animações compostas** (`translateX` das duas tiras), mais a entrada única do H1 (peso 300→900 e largura 62→78%, sem mover layout). Pausam fora da viewport.
- O H1 já está visível no primeiro frame; `prefers-reduced-motion` mostra o quadro limpo e **zero** animações (medido).
- Ocupa o lugar do vídeo (M1 da spec): se houver vídeo real, o slot é o mesmo.

Secundárias: faixas por segmento (`flex-grow` + `font-stretch` crescendo junto), respiro com filtros e palavras-fantasma (CSS scroll-driven), trator em corte com hotspots, mapa em matriz de pontos (IBGE), super menu com prévia por segmento (`:has()`), app shell no mobile (tab bar + bottom sheets + menu tipográfico), View Transitions entre páginas.

## Decisões propostas (ADR leves; ainda não aprovadas)
| ID | Decisão | Por quê |
|---|---|---|
| ADR-D15 | **Hero em SVG/CSS no lugar do vídeo (M1)** | LCP 2,0 s e 151 KiB; HIFI (WebGL+Vimeo) tem Performance 27 / LCP 7,9 s |
| ADR-D16 | **GSAP fora do protótipo** | tudo coube em CSS; GSAP+ScrollTrigger (~45 KB gz) estouraria o teto de 30 KB da spec |
| ADR-D17 | **Display = Archivo variável (wdth+wght), texto = Poppins** | Sharp Sans Display é TRIAL e não tem acentos PT-BR (proibida na web). **Depende de ADR-D03** |
| ADR-D18 | **Botão em paralelogramo** | repete a inclinação do cilindro do logo (forma de marca) |
| ADR-D19 | **Bookends navy (hero, números, rodapé)** | exceção consciente à regra "tema único" do taste: B2B + folder; um só acento |
| ADR-D20 | **Arte própria em SVG (kit de 4 formas + trator)** | sem direito de imagem confirmado; sem foto de banco/IA |

## Medições (Lighthouse mobile simulado, servidor com gzip)
| Página | Perf | A11y | Boas práticas | LCP | FCP | TBT | CLS | Peso |
|---|---|---|---|---|---|---|---|---|
| Home (mediana de 3) | **99** | **100** | 100 | **2,0 s** | 1,4 s | 0 ms | 0–0,017 | 151 KiB |
| Filtros | 97 | 100 | 100 | 2,4 s* | 1,5 s | 0 ms | 0,001 | 233 KiB* |
| Agrícola | 97 | 100 | 100 | 2,4 s* | 1,7 s | 0 ms | 0,025 | 267 KiB* |
\* medidos **antes** de ligar o gzip no servidor de teste (1 rodada); a Home, depois, caiu de 2,7 s para 2,0 s. **Não remedi** Filtros e Agrícola com gzip.
Referências medidas antes: HIFI 27 (LCP 7,9 s), UFI 38 (LCP 30 s), site atual 54 (LCP 15 s). *Lab, não campo.*

## Verificado (com evidência)
- **Movimento:** `getAnimations()` na Home = exatamente `flow`×2 (rodando), `h1-fill`×2 e `rise`×2 (terminadas), 5 scroll-driven; pulsos pausados fora da viewport. 4 frames do hero por seek diferem ~1,8% dos pixels (a faixa se move). `reduced-motion`: 0 animações, H1 em peso 900.
- **Transições:** `pagereveal.viewTransition` presente Home→Agrícola→Filtros; sem nomes duplicados; com `reduced-motion` não há transição.
- **Teclado:** foco abre o super menu; `Esc` fecha e devolve o foco; âncora `/filtros/#ureia` para abaixo do índice pegajoso.
- **Sem JS (main.js bloqueado):** números finais no HTML, H1 e links intactos, 1ª faixa aberta.
- **Links:** 182 links locais nas 4 páginas, todos 200. **Overflow horizontal:** 0 em 360, 390, 1440 e 1920.
- **Contraste (`tools/contraste.py`):** 0 falhas (a Mineração foi clareada de `#CC5B45` para `#D9705A`).

## NÃO verificado
- **iOS Safari real** (safe-area, `<dialog>`, `:has()`, scroll-driven); só Chromium. Firefox ignora View Transitions e scroll-driven (cai no estático).
- Lighthouse de Filtros/Agrícola **com gzip**; Lighthouse em dispositivo real; leitor de tela real.
- 320 e 768 px (medi 360, 390, 1440, 1920).

## Pendências que dependem de gente
ADR-D02 (azul oficial) · ADR-D03 (fonte) · **cor por segmento** (provisória) · números oficiais (12 unidades, "+250" vs "200", "+30 mil", clientes ativos) · telefones/WhatsApp das unidades · vídeo do hero · autorização de logos de marcas · **copy**: o sub do hero é o texto do site atual **com erro de concordância ("Distribuidora autorizado")**, mantido porque copy do cliente é imutável (confirmar com o cliente) · textos de apoio de segmento/filtro são **proposta nossa**.

## Estrutura
`src/pages/*.html` (corpo) + `tools/build.py` (header, super menu, rodapé, sheets, tab bar) → `index.html`, `segmentos/agricola/`, `filtros/`, `stub.html`. CSS parciais em `assets/css/` (`app.css` e `page-*.css` são **gerados**). Arte gerada por scripts reprodutíveis em `tools/` (`gen_hero`, `gen_kit`, `gen_trator`, `gen_brasil`, `gen_logo`, `gen_sprite`). Dado externo (GeoJSON IBGE) em `tools/dados/`, lido só com `python3 -I`. Fontes e ícones: Archivo/Poppins (OFL, Google Fonts) e Phosphor (MIT), self-hosted.
Ordem para regenerar a arte: `gen_logo` → `gen_sprite <pasta phosphor/assets/regular>` → `gen_kit` → `gen_trator` → `gen_hero` → `gen_brasil` → `build`.

↩︎ [[@Polifiltro]] · [[Estratégia/Wireframes/wireframe-v2|wireframe-v2]] · [[Estratégia/Analises/motion-e-momentos-polifiltro-v1|motion-e-momentos]]
