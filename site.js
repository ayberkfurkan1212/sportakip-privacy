// Başka bir sitenin içine (iframe) gömülmeyi engelle
if (window.top !== window.self) { try { window.top.location = window.self.location.href; } catch (e) { document.documentElement.style.display = "none"; } }
(function(){
  var plans={ay:['₺150','/ ay','3 aylık ve yıllık planda daha ucuz'],uc:['₺359','/ 3 ay','Ayda ₺120'],yil:['₺899','/ yıl','Ayda ₺75, en avantajlısı']};
  var btns=document.querySelectorAll('[data-period]');
  btns.forEach(function(b){b.addEventListener('click',function(){
    var p=plans[b.dataset.period];
    document.getElementById('fiyat-tutar').textContent=p[0];
    document.getElementById('fiyat-donem').textContent=p[1];
    document.getElementById('fiyat-not').textContent=p[2];
    btns.forEach(function(x){var on=x===b;x.setAttribute('aria-pressed',on);x.style.background=on?'#C8F04A':'transparent';x.style.color=on?'#0C0E0D':'#C9D0CB';});
  });});
})();
