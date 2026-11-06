#!/usr/bin/env python3
"""/kalori/ rehber sayfalarını üretir. Değerler SporTakip besin veritabanından (foods + food_portions, doğrulanmış kayıtlar).
Çalıştırma: python3 tools/kalori_sayfalari.py  (depo kökünden)"""
import json, pathlib, html
ROOT = pathlib.Path(__file__).resolve().parent.parent
GUNCEL = "6 Kasım 2026"

# slug, ad, 100 g değerleri (kcal, P, K, Y), porsiyonlar [(etiket, gram)], ana porsiyon indeksi, notlar, örnek mesaj
Y = [
 ("simit", "Simit", (275, 8.8, 53.3, 3.8), [("1 adet", 100), ("Yarım simit", 50)], 0,
  ["Simidin kalorisinin büyük kısmı karbonhidrattan gelir; susam az miktarda yağ ekler.",
   "Kahvaltıda peynir ya da yumurtayla yemek, öğüne protein ekler ve daha uzun tok tutar.",
   "Fırına ve boyuta göre simit 80–130 g arasında değişebilir; büyük simitte kalori de artar."],
  "kahvaltıda 1 simit ve 1 çay"),
 ("lahmacun", "Lahmacun", (218.3, 9.3, 28.7, 7.3), [("1 adet", 143.3), ("2 adet", 286.6)], 0,
  ["Bir lahmacunun yaklaşık 13 g'ı proteindir; kıymanın yağ oranı kaloriyi değiştirir.",
   "Maydanoz, soğan ve limonla yemek kaloriyi neredeyse hiç artırmaz.",
   "Yanında 1 bardak ayran yaklaşık 75 kcal ekler."],
  "öğlen 2 lahmacun ve 1 ayran"),
 ("mercimek-corbasi", "Mercimek çorbası", (65, 3.5, 10, 1.5), [("1 kase", 250), ("1 kepçe", 150), ("1 tabak", 300)], 0,
  ["Kırmızı mercimek bitkisel protein ve lif kaynağıdır.",
   "Üzerine dökülen tereyağlı sos her yemek kaşığında yaklaşık 100 kcal ekleyebilir.",
   "Yanında yarım ekmek (yaklaşık 50 g) yaklaşık 130 kcal getirir."],
  "bir kase mercimek çorbası ve yarım ekmek"),
 ("ezogelin-corbasi", "Ezogelin çorbası", (58.3, 2.5, 8.7, 1.5), [("1 kase", 250), ("1 kepçe", 150), ("1 tabak", 300)], 0,
  ["Mercimek, bulgur ve pirinçle yapıldığı için doyurucu ama hafif bir çorbadır.",
   "Kalorisi mercimek çorbasına yakındır; fark çoğunlukla kullanılan yağdan gelir."],
  "1 kase ezogelin çorbası"),
 ("menemen", "Menemen", (93.3, 4.8, 5, 6.3), [("1 porsiyon", 200), ("1 yumurtalı", 100)], 0,
  ["Menemenin kalorisini en çok tavaya konan yağ belirler.",
   "Peynirli ya da sucuklu menemende kalori ve yağ belirgin şekilde artar.",
   "Ekmekle yenirse her ince dilim (yaklaşık 25 g) yaklaşık 65 kcal ekler."],
  "kahvaltıda 1 porsiyon menemen"),
 ("haslanmis-yumurta", "Haşlanmış yumurta", (155, 13, 1.1, 11), [("1 adet", 50), ("2 adet", 100), ("3 adet", 150)], 0,
  ["Bir yumurta yaklaşık 6,5 g kaliteli protein içerir.",
   "Haşlama yağ eklemediği için yumurtanın en hafif pişirme şeklidir.",
   "Büyük boy yumurta 60 g civarındadır; kalorisi buna göre biraz artar."],
  "2 haşlanmış yumurta"),
 ("sucuklu-yumurta", "Sucuklu yumurta", (280, 15, 2, 22), [("1 porsiyon", 150)], 0,
  ["Kalorinin büyük kısmı sucuğun yağından gelir.",
   "Sucuğu yağsız tavada pişirmek eklenen yağı azaltır."],
  "sucuklu yumurta yedim"),
 ("iskender", "İskender", (231.7, 13.7, 13.7, 14), [("1 porsiyon", 333.3), ("Yarım porsiyon", 166.7)], 0,
  ["Bir porsiyon iskender günlük kalori ihtiyacının önemli bir kısmını karşılayabilir.",
   "Üzerine dökülen tereyağı ve pide kaloriyi en çok artıran kısımlardır.",
   "Yoğurt porsiyona protein ekler."],
  "1 porsiyon iskender"),
 ("manti", "Mantı", (226.7, 8.7, 30.3, 8.3), [("1 porsiyon", 250)], 0,
  ["Yoğurt ve tereyağlı sosla servis edildiği için porsiyon kalorisi yükselir.",
   "Sosu azaltmak kaloriyi düşürmenin en kolay yoludur."],
  "1 porsiyon mantı"),
 ("karniyarik", "Karnıyarık", (143.3, 6, 7.3, 10), [("1 adet", 220)], 0,
  ["Patlıcanı kızartmak yerine fırınlamak yağ miktarını azaltır.",
   "Yanında pilav yenirse 1 porsiyon pirinç pilavı yaklaşık 250–300 kcal ekler."],
  "1 karnıyarık"),
 ("tavuk-sis", "Tavuk şiş", (165, 23.7, 2, 6.7), [("1 şiş", 150)], 0,
  ["Yüksek proteinli ve görece düşük yağlı bir ana yemektir.",
   "Lavaş ya da pilavla yendiğinde öğünün toplam kalorisi belirgin artar."],
  "1 tavuk şiş ve salata"),
 ("su-boregi", "Su böreği", (260, 9.7, 25, 13.7), [("1 dilim", 130), ("1 porsiyon", 150)], 0,
  ["Peynirli su böreğinde kaloriyi tereyağı ve yufka belirler.",
   "Kıymalı su böreğinde protein ve yağ biraz daha yüksektir."],
  "1 dilim su böreği"),
 ("kasarli-tost", "Kaşarlı tost", (285, 13, 30, 11), [("1 adet", 180)], 0,
  ["Tost ekmeğine sürülen tereyağı her yemek kaşığında yaklaşık 100 kcal ekler.",
   "Karışık tostta sucuk eklendiği için kalori artar."],
  "1 kaşarlı tost ve 1 ayran"),
 ("baklava", "Baklava", (430, 5.7, 46.7, 25), [("1 dilim", 46.7), ("2 dilim", 93.4), ("4 dilim", 186.8)], 0,
  ["Baklavanın kalorisi şerbet, tereyağı ve fıstık ya da cevizden gelir.",
   "Kare dilimlerin boyutu dükkana göre değiştiği için kalori de değişir.",
   "Havuç dilimi baklava normal dilimden daha büyüktür."],
  "2 dilim baklava"),
 ("kunefe", "Künefe", (333.3, 6.7, 39.3, 16.7), [("1 porsiyon", 160)], 0,
  ["Peynir, tel kadayıf, tereyağı ve şerbetle yapılan yoğun bir tatlıdır.",
   "Paylaşarak yemek kaloriyi yarıya indirir."],
  "1 porsiyon künefe"),
 ("sutlac", "Sütlaç", (121.7, 3.2, 20.3, 3), [("1 kase", 183.3)], 0,
  ["Sütten gelen protein ve kalsiyum içerir.",
   "Üzerine tarçın eklemek kaloriyi değiştirmez; fındık ya da dondurma eklemek artırır."],
  "1 kase sütlaç"),
 ("ayran", "Ayran", (37, 1.8, 2.5, 2.1), [("1 bardak", 200), ("1 kutu", 200), ("1 şişe", 300)], 0,
  ["Yoğurt ve sudan yapıldığı için düşük kalorili bir içecektir.",
   "Tuz içerdiği için yemekle birlikte içilmesi yaygındır."],
  "1 bardak ayran"),
]

def sayi(x, d=1):
  s = f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
  return s[:-2] if d == 1 and s.endswith(",0") else s

def deger(m, g):
  return tuple(v * g / 100 for v in m)

STIL = """
  :root { --text:#1f2328; --muted:#59636e; --bg:#ffffff; --card:#f6f8fa; --line:#d1d9e0; --accent:#1a7f37; --lime:#C8F04A; }
  @media (prefers-color-scheme: dark) { :root { --text:#e6edf3; --muted:#9198a1; --bg:#0d1117; --card:#161b22; --line:#30363d; --accent:#3fb950; } }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--bg); color:var(--text); font:16px/1.65 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
  main { max-width:760px; margin:0 auto; padding:32px 16px 64px; }
  h1 { font-size:1.85rem; line-height:1.2; margin:0 0 4px; }
  h2 { font-size:1.2rem; margin:32px 0 8px; padding-top:8px; border-top:1px solid var(--line); }
  .meta { color:var(--muted); margin:0 0 20px; font-size:.95rem; }
  .cevap { font-size:1.15rem; background:var(--card); border:1px solid var(--line); border-left:6px solid var(--lime); border-radius:8px; padding:14px 16px; margin:16px 0; }
  .table-wrap { overflow-x:auto; }
  table { border-collapse:collapse; width:100%; font-size:.95rem; }
  th, td { border:1px solid var(--line); padding:8px 10px; text-align:left; }
  th { background:var(--card); }
  td.n, th.n { text-align:right; white-space:nowrap; }
  ul { padding-left:22px; } li { margin:4px 0; }
  a { color:var(--accent); }
  .wa { display:block; background:#14213D; color:#F3F6FB; border-radius:12px; padding:16px 18px; margin:24px 0; }
  .wa b { color:var(--lime); }
  .wa a { display:inline-block; margin-top:10px; background:var(--lime); color:#14210F; font-weight:700; text-decoration:none; border-radius:999px; padding:8px 18px; }
  .ilgili { display:flex; flex-wrap:wrap; gap:8px; padding:0; list-style:none; }
  .ilgili a { display:inline-block; border:1px solid var(--line); border-radius:999px; padding:4px 12px; text-decoration:none; }
  .kucuk { color:var(--muted); font-size:.9rem; }
  @media (max-width:480px) { th, td { padding:6px 5px; font-size:.82rem; } }
"""

def bas(title, desc, url, ld):
  e = html.escape
  return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; img-src 'self'; base-uri 'none'; form-action 'none'; upgrade-insecure-requests">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" href="/favicon.png">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="https://sportakip.tr/og.jpg">
<meta property="og:site_name" content="SporTakip">
<meta property="og:locale" content="tr_TR">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>{STIL}</style>
</head>
<body>
<main>
<p class="meta"><a href="/">SporTakip</a> · <a href="/kalori/">Kalori rehberi</a> · <a href="/komutlar/">Komutlar</a></p>
"""

SON = """<p class="kucuk">Değerler SporTakip besin veritabanındaki ortalama tarif değerleridir; tarife, malzemeye ve porsiyon boyutuna göre değişebilir. Tıbbi beslenme tavsiyesi değildir.</p>
</main>
</body>
</html>
"""

def wa(mesaj):
  from urllib.parse import quote
  return f"https://wa.me/905465537932?text={quote(mesaj)}"

out = ROOT / "kalori"; out.mkdir(exist_ok=True)
for slug, ad, m, pors, ana, notlar, ornek in Y:
  url = f"https://sportakip.tr/kalori/{slug}/"
  pl, pg = pors[ana]
  k, p, c, f = deger(m, pg)
  kucuk = ad[0].lower() + ad[1:]
  cevap = f"{pl} {kucuk} (yaklaşık {sayi(pg,0)} g) ortalama {sayi(k,0)} kcal'dir. {sayi(p)} g protein, {sayi(c)} g karbonhidrat ve {sayi(f)} g yağ içerir."
  title = f"{ad} kaç kalori? {pl} {kucuk} besin değerleri | SporTakip"
  desc = f"{pl} {kucuk} yaklaşık {sayi(k,0)} kcal. Porsiyona göre kalori, protein, karbonhidrat ve yağ tablosu; 100 gramında {sayi(m[0],0)} kcal."
  ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "FAQPage", "mainEntity": [
      {"@type": "Question", "name": f"{ad} kaç kalori?", "acceptedAnswer": {"@type": "Answer", "text": cevap}},
      {"@type": "Question", "name": f"100 gram {kucuk} kaç kalori?", "acceptedAnswer": {"@type": "Answer", "text": f"100 gram {kucuk} ortalama {sayi(m[0],0)} kcal; {sayi(m[1])} g protein, {sayi(m[2])} g karbonhidrat, {sayi(m[3])} g yağ."}}]},
    {"@type": "BreadcrumbList", "itemListElement": [
      {"@type": "ListItem", "position": 1, "name": "SporTakip", "item": "https://sportakip.tr/"},
      {"@type": "ListItem", "position": 2, "name": "Kalori rehberi", "item": "https://sportakip.tr/kalori/"},
      {"@type": "ListItem", "position": 3, "name": f"{ad} kaç kalori", "item": url}]}]}
  rows = "".join(
    f"<tr><td>{html.escape(l)}</td><td class='n'>{sayi(g,0)} g</td><td class='n'><b>{sayi(deger(m,g)[0],0)}</b></td><td class='n'>{sayi(deger(m,g)[1])} g</td><td class='n'>{sayi(deger(m,g)[2])} g</td><td class='n'>{sayi(deger(m,g)[3])} g</td></tr>"
    for l, g in pors + [("100 gram", 100)])
  ilgili = "".join(f'<li><a href="/kalori/{s}/">{a}</a></li>' for s, a, *_ in Y if s != slug)
  body = f"""<h1>{html.escape(ad)} kaç kalori?</h1>
<p class="meta">Son güncelleme: {GUNCEL}</p>
<p class="cevap">{html.escape(cevap)}</p>
<h2>Porsiyona göre besin değerleri</h2>
<div class="table-wrap"><table>
<thead><tr><th>Porsiyon</th><th class="n">Miktar</th><th class="n">Kalori</th><th class="n">Protein</th><th class="n">Karb.</th><th class="n">Yağ</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<h2>Bilmekte fayda var</h2>
<ul>{''.join(f'<li>{html.escape(n)}</li>' for n in notlar)}</ul>
<div class="wa">Kalori hesaplamakla uğraşma. SporTakip'e WhatsApp'tan <b>“{html.escape(ornek)}”</b> yaz; kalorisini, proteinini ve günlük hedefinden kalanı hemen söylesin.<br>
<a href="{wa(ornek)}">WhatsApp'ta dene</a></div>
<h2>Diğer yiyecekler</h2>
<ul class="ilgili">{ilgili}</ul>
"""
  d = out / slug; d.mkdir(exist_ok=True)
  (d / "index.html").write_text(bas(title, desc, url, ld) + body + SON)

# rehber ana sayfası
url = "https://sportakip.tr/kalori/"
ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Türk yemekleri kalori rehberi", "url": url, "inLanguage": "tr-TR",
      "hasPart": [{"@type": "WebPage", "name": f"{a} kaç kalori", "url": f"https://sportakip.tr/kalori/{s}/"} for s, a, *_ in Y]}
rows = "".join(f"<tr><td><a href='/kalori/{s}/'>{a}</a></td><td>{html.escape(pors[ana][0])} ({sayi(pors[ana][1],0)} g)</td><td class='n'><b>{sayi(deger(m,pors[ana][1])[0],0)}</b></td><td class='n'>{sayi(m[0],0)}</td></tr>"
               for s, a, m, pors, ana, *_ in Y)
body = f"""<h1>Türk yemekleri kalori rehberi</h1>
<p class="meta">Son güncelleme: {GUNCEL}</p>
<p>Simit, lahmacun, mercimek çorbası, menemen, baklava… Sık yenen yiyeceklerin porsiyon başına kalori ve makro değerleri. Bir yiyeceğe dokun, ayrıntılı tabloyu gör.</p>
<div class="table-wrap"><table>
<thead><tr><th>Yiyecek</th><th>Porsiyon</th><th class="n">Kalori</th><th class="n">100 g'da</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<div class="wa">Listede olmayan bir şey mi yedin? SporTakip'te 2.800'den fazla besin ve paketli ürün var. WhatsApp'tan ne yediğini yaz ya da fotoğrafını at.<br>
<a href="{wa('merhaba')}">WhatsApp'ta başla</a></div>
"""
(out / "index.html").write_text(bas("Türk yemekleri kalori rehberi: simit, lahmacun, mercimek çorbası | SporTakip",
  "Simit, lahmacun, mercimek çorbası, menemen, iskender, baklava ve daha fazlası kaç kalori? Porsiyon başına kalori, protein, karbonhidrat ve yağ tablosu.", url, ld) + body + SON)
print(len(Y), "sayfa")
