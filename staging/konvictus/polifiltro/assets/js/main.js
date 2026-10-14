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
  if (sel) sel.addEventListener('change', function () {
    pins.forEach(function (p) { p.classList.remove('on'); });
    if (sel.selectedIndex > 0 && pins[sel.selectedIndex - 1]) pins[sel.selectedIndex - 1].classList.add('on');
  });
})();
