(function(){
  var nav=document.getElementById('nav');
  var onScroll=function(){nav.classList.toggle('scrolled',window.scrollY>40)};
  onScroll();window.addEventListener('scroll',onScroll,{passive:true});

  var burger=document.getElementById('burger'),sheet=document.getElementById('sheet'),close=document.getElementById('sheetClose');
  burger.addEventListener('click',function(){sheet.classList.add('open');burger.setAttribute('aria-expanded','true')});
  var shut=function(){sheet.classList.remove('open');burger.setAttribute('aria-expanded','false')};
  close.addEventListener('click',shut);
  sheet.querySelectorAll('a').forEach(function(a){a.addEventListener('click',shut)});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')shut()});

  document.getElementById('ano').textContent=new Date().getFullYear();

  var playBtn=document.getElementById('playBtn');
  if(playBtn){
    playBtn.addEventListener('click',function(){
      var player=document.getElementById('player'),vid=player.querySelector('.player__vid'),src=vid.querySelector('source');
      if(src&&!src.src&&src.dataset.src){src.src=src.dataset.src;vid.load();}
      vid.setAttribute('controls','');
      player.classList.add('is-playing');
      var p=vid.play();if(p&&p.catch){p.catch(function(){});}
    });
  }

  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var items=document.querySelectorAll('.reveal,.stagger');
  if(reduce||!('IntersectionObserver'in window)){items.forEach(function(el){el.classList.add('in')});return;}
  var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target)}})},{threshold:.16,rootMargin:'0px 0px -8% 0px'});
  items.forEach(function(el){io.observe(el)});
})();
