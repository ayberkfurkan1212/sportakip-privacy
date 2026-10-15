// SporTakip web paneli: WhatsApp'tan gelen tek kullanımlık bağlantıyla (24 saat) son 30 günü gösterir.
(function () {
  "use strict";
  var API = "https://dlipccqhuypwybembzxv.supabase.co/functions/v1/public-api";
  var app = document.getElementById("app");
  var LABELS = { breakfast: "Kahvaltı", lunch: "Öğle", dinner: "Akşam", snack: "Ara öğün" };

  function token() {
    var m = location.hash.match(/t=([A-Za-z0-9_-]{16,80})/);
    var t = m ? m[1] : null;
    try {
      if (t) sessionStorage.setItem("st_panel", t); else t = sessionStorage.getItem("st_panel");
    } catch (e) { /* gizli sekme */ }
    if (m) history.replaceState(null, "", location.pathname); // anahtarı adres çubuğundan kaldır
    return t;
  }

  function el(tag, attrs, kids) {
    var e = document.createElement(tag);
    for (var k in attrs || {}) { if (k === "text") e.textContent = attrs[k]; else e.setAttribute(k, attrs[k]); }
    (kids || []).forEach(function (c) { if (c) e.appendChild(c); });
    return e;
  }
  function fmt(n) { return Math.round(n).toLocaleString("tr-TR"); }
  function dShort(s) { var p = s.split("-"); return p[2] + "." + p[1]; }

  function message(title, body) {
    app.innerHTML = "";
    var box = el("div", { "class": "msg" }, [el("h1", { "class": "disp", text: title })]);
    var p = el("p", { "class": "sub" }); p.innerHTML = body; box.appendChild(p);
    app.appendChild(box);
  }

  var NS = "http://www.w3.org/2000/svg";
  function s(tag, attrs) { var e = document.createElementNS(NS, tag); for (var k in attrs) e.setAttribute(k, attrs[k]); return e; }

  // Basit SVG grafikleri (dış kütüphane yok)
  function barChart(points, goal, color) {
    var W = 640, H = 200, P = 26, n = points.length || 1;
    var max = Math.max(goal || 0, Math.max.apply(null, points.map(function (p) { return p.v; }).concat([1]))) * 1.1;
    var svg = s("svg", { viewBox: "0 0 " + W + " " + H, role: "img" });
    var bw = (W - P * 2) / n;
    points.forEach(function (p, i) {
      var h = (p.v / max) * (H - P * 2);
      var r = s("rect", { x: P + i * bw + bw * 0.15, y: H - P - h, width: bw * 0.7, height: Math.max(h, 0), rx: 3, fill: p.v > (goal || Infinity) * 1.1 ? "#F2A65E" : color });
      var t = s("title", {}); t.textContent = dShort(p.d) + ": " + fmt(p.v); r.appendChild(t); svg.appendChild(r);
      if (n <= 31 && (i % Math.ceil(n / 8) === 0 || i === n - 1)) {
        var lab = s("text", { x: P + i * bw + bw / 2, y: H - 8, "text-anchor": "middle", fill: "#9AA39E", "font-size": 11 });
        lab.textContent = dShort(p.d); svg.appendChild(lab);
      }
    });
    if (goal) {
      var y = H - P - (goal / max) * (H - P * 2);
      svg.appendChild(s("line", { x1: P, x2: W - P, y1: y, y2: y, stroke: "#F2F5F3", "stroke-dasharray": "4 5", "stroke-opacity": 0.5 }));
      var gl = s("text", { x: W - P, y: y - 6, "text-anchor": "end", fill: "#9AA39E", "font-size": 11 }); gl.textContent = "hedef " + fmt(goal); svg.appendChild(gl);
    }
    return svg;
  }

  function lineChart(points, color, unit) {
    var W = 640, H = 200, P = 30;
    var svg = s("svg", { viewBox: "0 0 " + W + " " + H, role: "img" });
    if (points.length < 2) return null;
    var vs = points.map(function (p) { return p.v; });
    var min = Math.min.apply(null, vs), max = Math.max.apply(null, vs);
    var pad = Math.max((max - min) * 0.2, 0.5); min -= pad; max += pad;
    var t0 = Date.parse(points[0].d), t1 = Date.parse(points[points.length - 1].d) || t0 + 1;
    var xy = points.map(function (p) {
      return [P + (Date.parse(p.d) - t0) / Math.max(t1 - t0, 1) * (W - P * 2), H - P - (p.v - min) / (max - min) * (H - P * 2)];
    });
    svg.appendChild(s("polyline", { points: xy.map(function (a) { return a.join(","); }).join(" "), fill: "none", stroke: color, "stroke-width": 3, "stroke-linejoin": "round", "stroke-linecap": "round" }));
    xy.forEach(function (a, i) {
      var c = s("circle", { cx: a[0], cy: a[1], r: 4, fill: color });
      var t = s("title", {}); t.textContent = dShort(points[i].d) + ": " + points[i].v + " " + unit; c.appendChild(t); svg.appendChild(c);
    });
    [0, points.length - 1].forEach(function (i) {
      var lab = s("text", { x: xy[i][0], y: H - 8, "text-anchor": i ? "end" : "start", fill: "#9AA39E", "font-size": 11 });
      lab.textContent = dShort(points[i].d) + " · " + points[i].v + " " + unit; svg.appendChild(lab);
    });
    return svg;
  }

  function stat(label, value, unit, goal) {
    var c = el("div", { "class": "card c3" }, [el("p", { "class": "k", text: label })]);
    var v = el("p", { "class": "v disp" }); v.textContent = fmt(value);
    if (unit) v.appendChild(el("small", { text: unit + (goal ? " / " + fmt(goal) : "") }));
    c.appendChild(v);
    if (goal) { var b = el("div", { "class": "bar" }, [el("i", { style: "width:" + Math.min(100, value / goal * 100) + "%" })]); c.appendChild(b); }
    return c;
  }

  function render(d) {
    app.innerHTML = "";
    document.getElementById("date").textContent = d.today.split("-").reverse().join(".");
    app.appendChild(el("h1", { "class": "disp", text: "Merhaba" + (d.name ? " " + d.name : "") + " 👋" }));
    app.appendChild(el("p", { "class": "sub", text: "Son 30 günün özeti. Veriler WhatsApp'ta yazdıklarından geliyor." }));

    var today = d.days.filter(function (x) { return x.date === d.today; })[0] || { kcal: 0, protein: 0 };
    var logged = d.days.filter(function (x) { return x.kcal > 0; });
    var avg = logged.length ? logged.reduce(function (a, x) { return a + x.kcal; }, 0) / logged.length : 0;
    var water = (d.water.filter(function (x) { return x.date === d.today; })[0] || { ml: 0 }).ml;
    var steps = (d.steps.filter(function (x) { return x.date === d.today; })[0] || { steps: 0 }).steps;

    var g = el("div", { "class": "grid" });
    g.appendChild(stat("Bugün kalori", today.kcal, "kcal", d.goals.kcal));
    g.appendChild(stat("Bugün protein", today.protein, "g", d.goals.protein));
    g.appendChild(stat("Bugün su", water, "ml", d.goals.water));
    g.appendChild(stat(d.goals.steps ? "Bugün adım" : "30 günde antrenman", d.goals.steps ? steps : d.workouts, d.goals.steps ? "adım" : "gün", d.goals.steps || 0));

    // Kalori grafiği (30 gün, boş günler 0)
    var series = [];
    for (var i = 29; i >= 0; i--) {
      var dt = new Date(Date.parse(d.today + "T12:00:00Z") - i * 86400000).toISOString().slice(0, 10);
      var row = d.days.filter(function (x) { return x.date === dt; })[0];
      series.push({ d: dt, v: row ? row.kcal : 0 });
    }
    var kc = el("div", { "class": "card c8" }, [el("h2", { text: "Kalori · son 30 gün" }), barChart(series, d.goals.kcal, "#C8F04A")]);
    kc.appendChild(el("p", { "class": "legend", text: logged.length + " gün kayıt · ortalama " + fmt(avg) + " kcal/gün" }));
    g.appendChild(kc);

    // Makro dağılımı (kayıtlı günlerin ortalaması)
    var mac = el("div", { "class": "card c4" }, [el("h2", { text: "Ortalama makrolar" })]);
    if (logged.length) {
      var P = logged.reduce(function (a, x) { return a + x.protein; }, 0) / logged.length;
      var C = logged.reduce(function (a, x) { return a + x.carbs; }, 0) / logged.length;
      var F = logged.reduce(function (a, x) { return a + x.fat; }, 0) / logged.length;
      var tot = P * 4 + C * 4 + F * 9 || 1;
      var parts = [["Protein", P, P * 4 / tot, "#C8F04A"], ["Karbonhidrat", C, C * 4 / tot, "#5EC8F2"], ["Yağ", F, F * 9 / tot, "#F2A65E"]];
      var svg = s("svg", { viewBox: "0 0 200 200" }), a0 = -Math.PI / 2;
      parts.forEach(function (p) {
        var a1 = a0 + p[2] * Math.PI * 2, large = p[2] > 0.5 ? 1 : 0;
        var path = "M100 100 L" + (100 + 80 * Math.cos(a0)) + " " + (100 + 80 * Math.sin(a0)) + " A80 80 0 " + large + " 1 " + (100 + 80 * Math.cos(a1)) + " " + (100 + 80 * Math.sin(a1)) + " Z";
        svg.appendChild(s("path", { d: path, fill: p[3] })); a0 = a1;
      });
      svg.appendChild(s("circle", { cx: 100, cy: 100, r: 48, fill: "#141816" }));
      svg.style.maxWidth = "200px"; svg.style.margin = "0 auto";
      mac.appendChild(svg);
      var lg = el("div", { "class": "legend" });
      parts.forEach(function (p) { var sp = el("span"); sp.appendChild(el("b", { style: "background:" + p[3] })); sp.appendChild(document.createTextNode(p[0] + " " + fmt(p[1]) + " g (%" + Math.round(p[2] * 100) + ")")); lg.appendChild(sp); });
      mac.appendChild(lg);
    } else mac.appendChild(el("p", { "class": "empty", text: "Henüz kayıt yok." }));
    g.appendChild(mac);

    // Kilo
    var wc = el("div", { "class": "card c6" }, [el("h2", { text: "Kilo" })]);
    var wl = lineChart(d.weights.map(function (x) { return { d: x.date, v: x.kg }; }), "#5EC8F2", "kg");
    if (wl) {
      wc.appendChild(wl);
      var f = d.weights[0].kg, l = d.weights[d.weights.length - 1].kg, df = Math.round((l - f) * 10) / 10;
      wc.appendChild(el("p", { "class": "legend", text: f + " → " + l + " kg (" + (df > 0 ? "+" : "") + df + ")" }));
    } else wc.appendChild(el("p", { "class": "empty", text: "Grafik için en az 2 kilo kaydı gerekiyor. WhatsApp'ta: \"kilom 78.4\"" }));
    g.appendChild(wc);

    // Adım
    var sc = el("div", { "class": "card c6" }, [el("h2", { text: "Adım" })]);
    if (d.steps.length) sc.appendChild(barChart(d.steps.map(function (x) { return { d: x.date, v: x.steps }; }), d.goals.steps, "#5EC8F2"));
    else sc.appendChild(el("p", { "class": "empty", text: "Adım kaydı yok. WhatsApp'ta \"8500 adım\" yaz ya da iPhone için \"apple sağlık bağla\"." }));
    g.appendChild(sc);

    // Bugünün öğünleri
    var mc = el("div", { "class": "card c12" }, [el("h2", { text: "Bugün ne yedim" })]);
    if (d.todayMeals.length) {
      d.todayMeals.forEach(function (m) {
        var box = el("div", { "class": "meal" });
        var h = el("h3"); h.appendChild(el("span", { text: LABELS[m.type] || m.type })); h.appendChild(el("span", { text: fmt(m.kcal) + " kcal" }));
        box.appendChild(h);
        box.appendChild(el("p", { text: m.items.map(function (i) { return i.qty + " " + (i.unit || "") + " " + i.name; }).join(" · ") }));
        mc.appendChild(box);
      });
    } else mc.appendChild(el("p", { "class": "empty", text: "Bugün henüz öğün kaydı yok." }));
    g.appendChild(mc);
    app.appendChild(g);
  }

  var t = token();
  if (!t) { message("Bağlantı gerekli", "Paneli açmak için WhatsApp'ta SporTakip'e <code>panelim</code> yaz; sana özel bir bağlantı göndereyim."); return; }
  fetch(API, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ action: "panel", token: t }) })
    .then(function (r) { return r.json().then(function (j) { return { s: r.status, j: j }; }); })
    .then(function (x) {
      if (x.s === 401) { try { sessionStorage.removeItem("st_panel"); } catch (e) {} message("Bağlantının süresi doldu", "Yeni bağlantı için WhatsApp'ta <code>panelim</code> yaz."); return; }
      if (!x.j.ok) { message("Bir sorun oldu", "Biraz sonra tekrar dener misin?"); return; }
      render(x.j);
    })
    .catch(function () { message("Bağlanamadım", "İnternet bağlantını kontrol edip sayfayı yenile."); });
})();
