// Başka bir sitenin içine (iframe) gömülmeyi engelle
if (window.top !== window.self) { try { window.top.location = window.self.location.href; } catch (e) { document.documentElement.style.display = "none"; } }

// "Bir gün": kaydırdıkça üstteki saat, günlük kalori ve gün çizgisi ilerler
(function () {
  if (!('IntersectionObserver' in window)) return;
  var root = document.documentElement;
  root.classList.add('js');
  var top = document.getElementById('top');
  var chip = document.getElementById('saat-chip');
  var kcalEl = document.getElementById('kcal');
  var bar = document.getElementById('gunbar');
  var altbar = document.getElementById('altbar');
  var hero = document.getElementById('ust');
  var meta = document.querySelector('meta[name="theme-color"]');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var shownKcal = 432, raf = 0;

  function countTo(target) {
    cancelAnimationFrame(raf);
    if (reduce) { shownKcal = target; kcalEl.textContent = target; return; }
    var from = shownKcal, t0 = performance.now(), dur = 700;
    (function step(now) {
      var p = Math.min(1, (now - t0) / dur);
      var e = 1 - Math.pow(1 - p, 4);
      shownKcal = Math.round(from + (target - from) * e);
      kcalEl.textContent = shownKcal;
      if (p < 1) raf = requestAnimationFrame(step);
    })(t0);
  }

  function apply(sec) {
    var s = sec.getAttribute('data-saat');
    if (s) chip.textContent = s;
    var k = sec.getAttribute('data-kcal');
    if (k) countTo(parseInt(k, 10));
    var p = sec.getAttribute('data-pct');
    if (p) bar.style.width = p + '%';
    var dark = sec.hasAttribute('data-koyu');
    top.classList.toggle('koyu', dark);
    if (meta) meta.setAttribute('content', dark ? '#14213D' : '#CFE4F4');
  }

  var moments = document.querySelectorAll('.m, .blok[data-koyu]');
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) {
        en.target.classList.add('gorundu');
        apply(en.target);
      }
    });
  }, { rootMargin: '-45% 0px -45% 0px' });
  moments.forEach(function (m) { io.observe(m); });

  // Balonlar: bölüm ekrana girer girmez görünür olsun (orta çizgiyi beklemeden)
  var reveal = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) { if (en.isIntersecting) en.target.classList.add('gorundu'); });
  }, { threshold: 0.15 });
  document.querySelectorAll('.m').forEach(function (m) { reveal.observe(m); });

  // Telefonda: ilk ekran geçince alttaki sabit buton belirir
  var son = document.getElementById('son');
  if (altbar && hero) {
    var heroVar = true, sonVar = false;
    var guncelle = function () { altbar.classList.toggle('acik', !heroVar && !sonVar); };
    new IntersectionObserver(function (e) { heroVar = e[0].isIntersecting; guncelle(); }).observe(hero);
    if (son) new IntersectionObserver(function (e) { sonVar = e[0].isIntersecting; guncelle(); }).observe(son);
  }
})();
