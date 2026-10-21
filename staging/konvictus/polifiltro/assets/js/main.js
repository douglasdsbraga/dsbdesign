/* Polifiltro v1: shell (super menu, sheets) e pausa do hero. Sem dependencias. Todo o conteudo funciona sem JS. */
(function () {
  'use strict';
  // super menu: reforca aria-expanded + Esc (a abertura em si e CSS puro)
  document.querySelectorAll('li.has-super').forEach(function (li) {
    var a = li.querySelector(':scope > a');
    function set(v) { a.setAttribute('aria-expanded', v); }
    li.addEventListener('mouseenter', function () { set('true'); });
    li.addEventListener('mouseleave', function () { set('false'); });
    li.addEventListener('focusin', function () { set('true'); });
    li.addEventListener('focusout', function (e) { if (!li.contains(e.relatedTarget)) set('false'); });
    // Esc fecha e devolve o foco ao gatilho; so reabre quando o foco sai e volta, ou o mouse sai e volta
    li.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { set('false'); li.classList.add('closed'); a.focus(); }
    });
    function reabrivel() { li.classList.remove('closed'); }
    li.addEventListener('mouseleave', reabrivel);
    li.addEventListener('focusout', function (e) { if (!li.contains(e.relatedTarget)) reabrivel(); });
  });
  // app shell: abas abrem bottom sheets so no mobile; sem JS cada aba e um link normal
  var mq = matchMedia('(max-width:980px)');
  document.querySelectorAll('[data-sheet]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      if (!mq.matches) return;
      var d = document.getElementById(a.getAttribute('data-sheet'));
      if (!d || !d.showModal) return;
      e.preventDefault();
      document.querySelectorAll('dialog[open]').forEach(function (o) { o.close(); });
      d.showModal();
    });
  });
  document.querySelectorAll('dialog.sheet').forEach(function (d) {
    d.addEventListener('click', function (e) { if (e.target === d) d.close(); });
    d.querySelectorAll('[data-close]').forEach(function (b) { b.addEventListener('click', function () { d.close(); }); });
  });
  // pausa as animacoes de quem sai da viewport (economia de CPU/bateria)
  if ('IntersectionObserver' in window) {
    var po = new IntersectionObserver(function (es) {
      es.forEach(function (e) { e.target.classList.toggle('is-off', !e.isIntersecting); });
    }, { threshold: 0.02 });
    document.querySelectorAll('.hero, .rx, .mapa').forEach(function (el) { po.observe(el); });
  }
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  // contadores: o valor final ja esta no HTML; a contagem so embeleza
  var cs = document.querySelectorAll('[data-count]');
  if (cs.length && 'IntersectionObserver' in window && !reduce) {
    var co = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        co.unobserve(e.target);
        var el = e.target, to = parseFloat(el.dataset.count), pre = el.dataset.prefix || '', suf = el.dataset.suffix || '', t0 = null, dur = 1400;
        (function tick(t) {
          if (t0 === null) t0 = t;
          var p = Math.min((t - t0) / dur, 1), v = 1 - Math.pow(2, -10 * p);
          el.textContent = pre + Math.round(to * (p === 1 ? 1 : v)) + suf;
          if (p < 1) requestAnimationFrame(tick);
        })(performance.now());
      });
    }, { rootMargin: '0px 0px -15% 0px' });
    cs.forEach(function (el) { co.observe(el); });
  }
  // mapa: lista de unidades acende o pin correspondente
  var pins = document.querySelectorAll('.pin');
  document.querySelectorAll('#uni-list a').forEach(function (a) {
    var i = +a.dataset.i;
    function on(v) { if (pins[i]) pins[i].classList.toggle('on', v); }
    a.addEventListener('mouseenter', function () { on(true); }); a.addEventListener('mouseleave', function () { on(false); });
    a.addEventListener('focus', function () { on(true); }); a.addEventListener('blur', function () { on(false); });
  });
  var sel = document.getElementById('uni-sel');
  var cards = document.querySelectorAll('.un-card');
  function destacar(i) {  // acende o pin e, na pagina de Unidades, o card correspondente
    pins.forEach(function (p) { p.classList.remove('on'); });
    cards.forEach(function (c) { c.classList.remove('on'); });
    if (pins[i]) pins[i].classList.add('on');
    if (cards[i]) cards[i].classList.add('on');
  }
  cards.forEach(function (c) {
    var i = +c.dataset.i;
    c.addEventListener('mouseenter', function () { if (pins[i]) pins[i].classList.add('on'); });
    c.addEventListener('mouseleave', function () { if (pins[i]) pins[i].classList.remove('on'); });
  });
  if (sel) sel.addEventListener('change', function () {
    var i = sel.selectedIndex - 1;
    destacar(i);
    if (i >= 0 && cards[i]) cards[i].scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' });
  });
  // "usar minha localizacao": unidade mais proxima em linha reta (centro aproximado de cada municipio, na ordem do select)
  var PTS = [[-3.119, -60.022], [-1.366, -48.372], [-11.864, -55.502], [-15.601, -56.097], [-16.686, -49.264], [-18.918, -48.277],
             [-19.932, -44.054], [-23.55, -46.633], [-21.208, -50.433], [-25.43, -49.27], [-26.908, -48.662], [-30.03, -51.23]];
  document.querySelectorAll('[data-geo]').forEach(function (b) {
    var msg = document.getElementById('geo-msg');
    function say(t) { if (msg) msg.textContent = t; }
    if (!navigator.geolocation) { b.hidden = true; return; }
    b.addEventListener('click', function () {
      say('Buscando sua localização…');
      navigator.geolocation.getCurrentPosition(function (pos) {
        var la = pos.coords.latitude * Math.PI / 180, lo = pos.coords.longitude * Math.PI / 180, best = 0, bd = 1e9;
        PTS.forEach(function (p, i) {
          var a = p[0] * Math.PI / 180, o = p[1] * Math.PI / 180;
          var d = 6371 * 2 * Math.asin(Math.sqrt(Math.pow(Math.sin((a - la) / 2), 2) + Math.cos(la) * Math.cos(a) * Math.pow(Math.sin((o - lo) / 2), 2)));
          if (d < bd) { bd = d; best = i; }
        });
        if (sel) { sel.selectedIndex = best + 1; sel.dispatchEvent(new Event('change')); }
        say('Unidade mais próxima: ' + (sel ? sel.options[best + 1].text : '') + ', a cerca de ' + Math.round(bd) + ' km em linha reta.');
      }, function () { say('Não foi possível ler sua localização. Escolha a cidade na lista.'); }, { timeout: 8000, maximumAge: 600000 });
    });
  });
  // formularios de cotacao: PROTOTIPO, sem validacao e sem envio. O submit so segue para /obrigado/ levando as escolhas de segmento/solucao/filtro/unidade
  // (nunca nome, telefone, e-mail ou mensagem: nada pessoal vai para a URL)
  document.querySelectorAll('#cotacao, form.cot').forEach(function (f) {
    f.setAttribute('novalidate', '');
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var q = new URLSearchParams();
      ['segmento', 'solucao', 'filtro', 'unidade'].forEach(function (k) { if (f.elements[k] && f.elements[k].value) q.set(k, f.elements[k].value); });
      location.href = f.getAttribute('action') + (q.toString() ? '?' + q.toString() : '');
    });
  });
  // cotacao: os links "Cotacao para ..." mandam ?segmento= ?solucao= ?filtro= ?unidade=; aqui viram campo ja preenchido
  var cot = document.getElementById('cotacao');
  if (cot) {
    var q = new URLSearchParams(location.search);
    ['segmento', 'solucao', 'filtro', 'unidade'].forEach(function (k) {
      var v = q.get(k), s = cot.elements[k];
      if (!v || !s) return;
      for (var i = 0; i < s.options.length; i++) if (s.options[i].value === v) { s.selectedIndex = i; break; }
    });
    if (q.get('filtro') && !q.get('solucao') && cot.elements.solucao) cot.elements.solucao.value = 'filtros';
  }
  // obrigado: resumo do que foi preenchido (so no navegador; nada e enviado)
  var recap = document.getElementById('recap'), rot = document.getElementById('rotulos');
  if (recap && rot) {
    var L = JSON.parse(rot.textContent), p = new URLSearchParams(location.search), linhas = [['segmento', 'Segmento'], ['solucao', 'Solução'], ['filtro', 'Filtro'], ['unidade', 'Unidade']];
    linhas.forEach(function (l) {
      var v = p.get(l[0]); if (!v) return;
      var dt = document.createElement('dt'), dd = document.createElement('dd');
      dt.textContent = l[1]; dd.textContent = (L[l[0]] && L[l[0]][v]) || v;
      recap.appendChild(dt); recap.appendChild(dd);
    });
    if (recap.children.length) recap.hidden = false;
  }
})();
