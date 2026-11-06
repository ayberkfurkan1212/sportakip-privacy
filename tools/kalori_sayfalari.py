#!/usr/bin/env python3
"""/kalori/ rehber sayfalarını üretir. Değerler SporTakip besin veritabanından (foods + food_portions, doğrulanmış kayıtlar).
Çalıştırma: python3 tools/kalori_sayfalari.py  (depo kökünden)"""
import json, pathlib, html
ROOT = pathlib.Path(__file__).resolve().parent.parent
GUNCEL = "7 Kasım 2026"

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
 ("et-doner", "Et döner", (246.7, 21, 3.3, 16.7), [("1 porsiyon", 156.7)], 0,
  ["Bu değerler yalnızca döner etidir; pilav, ekmek ya da lavaş ayrıca hesaplanır.",
   "Et döner protein açısından zengindir ama yağ oranı tavuk dönerden yüksektir.",
   "Pilav üstü dönerde 1 porsiyon pirinç pilavı yaklaşık 275 kcal ekler."],
  "1 porsiyon et döner"),
 ("tavuk-doner", "Tavuk döner", (185, 20.3, 4.3, 9.7), [("1 porsiyon", 156.7)], 0,
  ["Tavuk döner aynı porsiyonda et dönerden yaklaşık 100 kcal daha hafiftir.",
   "Değerler yalnızca döner etidir; ekmek, lavaş, patates ve soslar ayrıca hesaplanır."],
  "1 porsiyon tavuk döner"),
 ("doner-durum", "Döner dürüm", (230, 14, 24, 9), [("1 adet", 250)], 0,
  ["Değer lavaş, döner ve içindeki sebzeyle birlikte ortalama bir dürüm içindir.",
   "Dürümün boyu ve içine konan patates ya da sos kaloriyi belirgin şekilde değiştirir.",
   "Yanında ayran içmek yaklaşık 75 kcal ekler."],
  "1 döner dürüm ve 1 ayran"),
 ("adana-durum", "Adana dürüm", (255, 18, 23, 11), [("1 adet", 250)], 0,
  ["Adana kebabın kıyması yağlı olduğu için dürümde yağ oranı yüksektir.",
   "Bir dürüm yaklaşık 45 g protein içerir."],
  "1 adana dürüm"),
 ("kiymali-pide", "Kıymalı pide", (240, 10.7, 30, 8.7), [("1 adet", 266.7), ("1 dilim", 44.5)], 0,
  ["Bir kıymalı pide genellikle 6 dilime kesilir; her dilim yaklaşık 107 kcal'dir.",
   "Üzerine yumurta ya da tereyağı eklemek kaloriyi artırır."],
  "1 kıymalı pide"),
 ("peynirli-pide", "Peynirli pide", (260, 11.7, 30, 10.7), [("1 adet", 266.7), ("1 dilim", 44.5)], 0,
  ["Kaşarlı ya da beyaz peynirli pidede kalori peynirin miktarına göre değişir.",
   "Sucuklu pide aynı boyda biraz daha kalorilidir."],
  "1 peynirli pide"),
 ("gozleme", "Peynirli gözleme", (251.7, 8.7, 30.3, 10.7), [("1 adet", 176.7), ("1 dilim", 44)], 0,
  ["Gözlemenin üzerine sürülen tereyağı her yemek kaşığında yaklaşık 100 kcal ekler.",
   "Ispanaklı gözleme peynirliden genellikle biraz daha hafiftir; sucuklu kaşarlı daha kalorilidir."],
  "1 peynirli gözleme ve 1 çay"),
 ("kuru-fasulye", "Etli kuru fasulye", (138.3, 9, 15, 5.3), [("1 kase", 220), ("1 porsiyon", 250), ("1 kepçe", 130)], 0,
  ["Kuru fasulye bitkisel protein ve lif kaynağıdır; et protein miktarını artırır.",
   "Klasik ikili pilavla yenir; 1 porsiyon pirinç pilavı yaklaşık 275 kcal ekler.",
   "Yanında turşu kaloriyi neredeyse hiç artırmaz."],
  "1 kase kuru fasulye ve 1 porsiyon pilav"),
 ("nohut-yemegi", "Nohut yemeği", (145, 7.5, 21, 4), [("1 kase", 220), ("1 porsiyon", 250)], 0,
  ["Nohut bitkisel protein ve lif açısından zengindir, uzun süre tok tutar.",
   "Etli ya da kavurmalı yapıldığında yağ ve kalori artar."],
  "1 kase nohut yemeği"),
 ("pirinc-pilavi", "Pirinç pilavı", (165, 3, 29.7, 4), [("1 porsiyon", 166.7), ("1 kase", 200), ("1 yemek kaşığı", 25)], 0,
  ["Değer tereyağlı klasik pirinç pilavı içindir; yağ miktarı kaloriyi değiştirir.",
   "Şehriyeli pilav benzer kalorilidir.",
   "Aynı miktar bulgur pilavı biraz daha az kalorili ve daha liflidir."],
  "1 porsiyon pirinç pilavı"),
 ("bulgur-pilavi", "Bulgur pilavı", (140, 3.8, 25, 3), [("1 porsiyon", 175), ("1 kase", 200), ("1 yemek kaşığı", 25)], 0,
  ["Bulgur, pirince göre daha fazla lif içerir.",
   "Domatesli ve biberli bulgur pilavında kalori farkı küçüktür; asıl farkı yağ yaratır."],
  "1 porsiyon bulgur pilavı"),
 ("izgara-kofte", "Izgara köfte", (225, 21, 4.3, 13.7), [("1 adet", 40), ("1 porsiyon", 110), ("4 adet", 160)], 1,
  ["Köftenin kalorisini en çok kıymanın yağ oranı belirler.",
   "Yanında piyaz, pilav ya da ekmek ayrıca hesaplanır.",
   "Tekirdağ ve İnegöl köftesi gibi yağlı türler daha kalorilidir."],
  "1 porsiyon ızgara köfte ve salata"),
 ("mercimek-koftesi", "Mercimek köftesi", (173.3, 5.7, 27.3, 4.5), [("1 adet", 35), ("1 porsiyon", 200), ("5 adet", 175)], 0,
  ["Etsiz olduğu için ızgara köfteye göre daha az protein ve yağ içerir.",
   "Marul ve limonla yemek kaloriyi neredeyse hiç artırmaz."],
  "5 adet mercimek köftesi"),
 ("cig-kofte", "Çiğ köfte", (165, 5, 26.3, 4.2), [("1 adet", 80), ("2 adet", 160)], 0,
  ["Değer bulgurla yapılan etsiz (vegan) çiğ köfte içindir.",
   "Dürüm olarak yenirse lavaş ve soslar ayrıca hesaplanır."],
  "2 adet çiğ köfte"),
 ("pogaca", "Peynirli poğaça", (326.7, 8, 35, 17.3), [("1 adet", 80), ("2 adet", 160)], 0,
  ["Poğaçanın yağ oranı yüksektir; boyuta göre 60–100 g arasında değişir.",
   "Açma benzer kalorilidir; simit daha az yağlıdır."],
  "1 peynirli poğaça ve 1 çay"),
 ("tavuk-gogsu", "Tavuk göğsü", (165, 31, 0, 3.6), [("1 porsiyon", 150), ("1 dilim", 30)], 0,
  ["Değer pişmiş (ızgara ya da haşlanmış) tavuk göğsü içindir.",
   "Yüksek proteinli ve düşük yağlı olduğu için sporcuların sık tercihidir.",
   "Çiğ tavuk göğsü pişince su kaybeder; aynı gram çiğ et daha az kalorilidir."],
  "150 gram ızgara tavuk göğsü"),
 ("patates-kizartmasi", "Patates kızartması", (312.3, 3.6, 40.7, 15), [("1 porsiyon", 150), ("Küçük porsiyon", 80)], 0,
  ["Kalorinin önemli kısmı kızartma yağından gelir.",
   "Fırında ya da air fryer'da yapılan patates daha az yağlıdır.",
   "Ketçap ve mayonez ayrıca kalori ekler."],
  "1 porsiyon patates kızartması"),
 ("beyaz-peynir", "Beyaz peynir", (250, 16, 2.5, 19), [("1 dilim", 30), ("1 küp", 15)], 0,
  ["Bir dilim beyaz peynir yaklaşık 5 g protein içerir.",
   "Tuz oranı yüksek olabilir; yarım yağlı türlerde kalori daha düşüktür."],
  "kahvaltıda 2 dilim beyaz peynir"),
 ("ekmek", "Ekmek", (265, 9, 49, 3.2), [("1 dilim", 30), ("1 kalın dilim", 50), ("Yarım ekmek", 125)], 0,
  ["Değer beyaz francala ekmek içindir; tam buğday ekmeğinde lif daha fazladır.",
   "Somun ekmeğin boyutu fırına göre değişir; yarım ekmek yaklaşık 125 g kabul edilir."],
  "2 dilim ekmek"),
 ("muz", "Muz", (89, 1.1, 22.8, 0.3), [("1 adet", 120), ("Yarım", 60)], 0,
  ["Muz antrenman öncesi hızlı enerji için sık tercih edilir.",
   "Olgunlaştıkça şekeri artar ama kalorisi neredeyse aynı kalır."],
  "1 muz"),
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
  kucuk = {"I": "ı", "İ": "i"}.get(ad[0], ad[0].lower()) + ad[1:]
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
<p>Simit, lahmacun, döner, pide, kuru fasulye, menemen, baklava… Sık yenen yiyeceklerin porsiyon başına kalori ve makro değerleri. Bir yiyeceğe dokun, ayrıntılı tabloyu gör.</p>
<div class="table-wrap"><table>
<thead><tr><th>Yiyecek</th><th>Porsiyon</th><th class="n">Kalori</th><th class="n">100 g'da</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<div class="wa">Listede olmayan bir şey mi yedin? SporTakip'te 2.800'den fazla besin ve paketli ürün var. WhatsApp'tan ne yediğini yaz ya da fotoğrafını at.<br>
<a href="{wa('merhaba')}">WhatsApp'ta başla</a></div>
"""
(out / "index.html").write_text(bas("Türk yemekleri kalori rehberi: simit, lahmacun, mercimek çorbası | SporTakip",
  "Simit, lahmacun, mercimek çorbası, menemen, iskender, baklava ve daha fazlası kaç kalori? Porsiyon başına kalori, protein, karbonhidrat ve yağ tablosu.", url, ld) + body + SON)
print(len(Y), "sayfa")
