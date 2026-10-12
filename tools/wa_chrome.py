"""Telefon maketlerini iPhone'daki güncel WhatsApp görünümüne çevirir (Gürkan'ın 12 Ekim ekran görüntüsü referans)."""
import re, sys, urllib.parse
p = sys.argv[1]; logo = sys.argv[2] if len(sys.argv) > 2 else '/logo.png'
s = open(p, encoding='utf8').read()
assert '.wa-status' not in s, 'zaten uygulanmış'

# WhatsApp duvar kâğıdı benzeri silik çizim deseni
doodle = ('<svg xmlns="http://www.w3.org/2000/svg" width="132" height="132" viewBox="0 0 132 132" fill="none" stroke="#DED6C8" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">'
  '<circle cx="18" cy="20" r="8"/><path d="M14 19h8M18 15v8"/>'
  '<path d="M52 10l3 6 6 1-4.5 4 1 6-5.5-3-5.5 3 1-6L43 17l6-1z"/>'
  '<path d="M96 14c-4-5-11-1-8 5l8 8 8-8c3-6-4-10-8-5z"/>'
  '<rect x="10" y="52" width="18" height="13" rx="3"/><circle cx="19" cy="58.5" r="3.5"/>'
  '<path d="M50 50h14l-2 16h-10z"/><path d="M64 54h3a3 3 0 0 1 0 6h-3"/>'
  '<path d="M92 50c6 0 10 4 10 9s-4 9-10 9-10-4-10-9"/><path d="M86 46l3 4M98 46l-3 4"/>'
  '<path d="M14 96c0-6 4-10 9-10M23 86c5 0 9 4 9 10"/><path d="M12 100h22"/>'
  '<circle cx="58" cy="96" r="9"/><path d="M54 94h.01M62 94h.01M54 99c2 2 6 2 8 0"/>'
  '<path d="M90 88l12 12M102 88l-12 12"/><circle cx="96" cy="94" r="10"/>'
  '<path d="M40 122h10M45 117v10"/><path d="M114 118c3 0 5 2 5 5s-2 5-5 5"/><path d="M118 70l6-6M120 64h4v4"/>'
  '</svg>')
bg = "url(\"data:image/svg+xml," + urllib.parse.quote(doodle, safe='') + "\")"

CSS = f"""
.wa-screen{{position:relative;background-color:#EFEAE2;background-image:{bg};background-size:132px 132px;display:flex;flex-direction:column}}
.wa-head{{position:relative;background:transparent;color:#111B21;display:flex;align-items:center;gap:9px;padding:30px 12px 8px 10px;box-shadow:none}}
.wa-status{{position:absolute;top:8px;left:26px;right:20px;display:flex;justify-content:space-between;align-items:center;font-family:-apple-system,'SF Pro Text','Instrument Sans',system-ui,sans-serif;font-size:12px;font-weight:600;color:#111B21;pointer-events:none}}
.wa-sys{{display:inline-flex;align-items:center;gap:4px;font-size:10.5px;font-weight:700}}
.wa-back{{width:32px;height:32px;border-radius:50%;background:rgba(255,255,255,0.92);box-shadow:0 1px 3px rgba(11,20,26,0.12);display:inline-flex;align-items:center;justify-content:center;flex:0 0 auto}}
.wa-name{{flex:1;min-width:0;font-family:-apple-system,'SF Pro Text','Instrument Sans',system-ui,sans-serif;font-size:14.5px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.wa-out,.wa-in{{position:relative;padding:6px 9px 5px 10px;max-width:86%;box-sizing:border-box;box-shadow:0 1px 0.5px rgba(11,20,26,0.10)}}
.wa-out{{align-self:flex-end;background:#DCF8C6;border-radius:15px 15px 4px 15px;display:flex;flex-wrap:wrap;align-items:flex-end;column-gap:8px}}
.wa-in{{align-self:flex-start;background:#FFFFFF;border-radius:15px 15px 15px 4px;display:flex;flex-direction:column;gap:1px}}
.wa-out::after{{content:"";position:absolute;bottom:0;right:-5px;width:10px;height:10px;background:radial-gradient(circle at 100% 0,transparent 9px,#DCF8C6 9.5px)}}
.wa-in::after{{content:"";position:absolute;bottom:0;left:-5px;width:10px;height:10px;background:radial-gradient(circle at 0 0,transparent 9px,#FFFFFF 9.5px)}}
.wa-act{{border-top:1px solid #E9EDEF;color:#1F8F4E;font-weight:500;padding:8px;display:flex;align-items:center;justify-content:center;gap:6px;margin:5px -9px -5px -10px}}
.wa-bar{{display:flex;align-items:center;gap:9px;padding:6px 10px 14px;background:rgba(246,245,243,0.96)}}
.wa-plus{{flex:0 0 auto;display:inline-flex}}
.wa-field{{flex:1;min-width:0;height:30px;background:#FFFFFF;border:1px solid #E3E1DD;border-radius:999px;padding:0 6px 0 12px;display:flex;align-items:center;justify-content:flex-end;box-sizing:border-box;box-shadow:none;color:transparent;font-size:0}}
.wa-mic{{width:32px;height:32px;border-radius:50%;background:#25B35A;display:flex;align-items:center;justify-content:center;flex:0 0 auto}}
.wa-tick{{display:inline-block;vertical-align:-1px}}
"""
SYS = ('<svg width="15" height="10" viewBox="0 0 17 11" aria-hidden="true"><rect x="0" y="7" width="3" height="4" rx="1" fill="#111B21"/><rect x="4.5" y="5" width="3" height="6" rx="1" fill="#111B21"/><rect x="9" y="2.5" width="3" height="8.5" rx="1" fill="#111B21"/><rect x="13.5" y="0" width="3" height="11" rx="1" fill="#111B21" fill-opacity="0.3"/></svg>'
 '<span>5G</span>'
 '<svg width="24" height="12" viewBox="0 0 26 13" aria-hidden="true"><rect x="0.5" y="0.5" width="22" height="12" rx="3.6" fill="#111B21" fill-opacity="0.18"/><rect x="2" y="2" width="15" height="9" rx="2.4" fill="#111B21"/><path d="M24 4.5v4c.8-.3 1.3-1.1 1.3-2s-.5-1.7-1.3-2z" fill="#111B21" fill-opacity="0.4"/></svg>')
BACK = '<span class="wa-back" aria-hidden="true"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#111B21" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M15 4l-8 8 8 8"/></svg></span>'
PLUS = '<span class="wa-plus" aria-hidden="true"><svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="#111B21" stroke-width="2" stroke-linecap="round"><path d="M12 4v16M4 12h16"/></svg></span>'
STICKER = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#111B21" stroke-width="1.9" stroke-linejoin="round" aria-hidden="true"><path d="M20.5 12.5V8a4.5 4.5 0 0 0-4.5-4.5H8A4.5 4.5 0 0 0 3.5 8v8A4.5 4.5 0 0 0 8 20.5h4.5z"/><path d="M12.5 20.5v-3.5a4.5 4.5 0 0 1 4.5-4.5h3.5"/></svg>'
CAM = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#111B21" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="flex:0 0 auto"><path d="M4 8h3l1.8-2.5h6.4L17 8h3a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1z"/><circle cx="12" cy="13" r="3.6"/></svg>'
MIC = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="3" width="6" height="11" rx="3"></rect><path d="M5 11a7 7 0 0 0 14 0M12 18v3"></path></svg>'
TICK = '<svg class="wa-tick" width="15" height="10" viewBox="0 0 16 11" aria-hidden="true"><path d="M11.1 1.2L5 7.8 2.4 5.2 1.3 6.3 5 10l7.2-7.7zM14.6 1.2L8.5 7.8l-.7-.7-1.1 1.2L8.5 10l7.2-7.7z" fill="#667781"/></svg>'
REPLY = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#1F8F4E" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 7L4 12l5 5"/><path d="M4 12h10a6 6 0 0 1 6 6"/></svg>'

# eski kuralları sil, yenilerini ekle
for sel in ['.wa-screen{', '.wa-head{', '.wa-out,.wa-in{', '.wa-out{', '.wa-in{', '.wa-out::after{', '.wa-in::after{', '.wa-act{', '.wa-bar{', '.wa-field{', '.wa-mic{']:
    s, n = re.subn(r'^' + re.escape(sel) + r'[^\n]*\n', '', s, count=1, flags=re.M); assert n == 1, sel
s = s.replace('.notch{', CSS.strip() + '\n.notch{', 1)

def screen(m):
    block = m.group(0)
    times = re.findall(r'class="wa-meta">(\d\d:\d\d)', block)
    clock = times[-1] if times else '09:41'
    big = 'height: 640px' in block
    av = 34 if big else 30
    head = (f'<div class="wa-head">'
            f'<span class="notch" aria-hidden="true"></span>'
            f'<span class="wa-status" aria-hidden="true"><span>{clock}</span><span class="wa-sys">{SYS}</span></span>'
            f'{BACK}<img src="{logo}" alt="" style="width: {av}px; height: {av}px; border-radius: 50%; object-fit: cover; flex: 0 0 auto">'
            f'<span class="wa-name">SporTakip</span></div>')
    block = re.sub(r'<div class="wa-head".*?</div>\n?<div class="wa-msgs"', head + '\n<div class="wa-msgs"', block, count=1, flags=re.S)
    block = re.sub(r'<div class="wa-bar">.*?</div>',
                   f'<div class="wa-bar" aria-hidden="true">{PLUS}<span class="wa-field">{STICKER}</span>{CAM}<span class="wa-mic">{MIC}</span></div>',
                   block, count=1, flags=re.S)
    block = re.sub(r'(<div class="wa-out">(?:(?!</div>).)*?<span class="wa-meta">)(\d\d:\d\d)(</span>)', lambda x: x.group(1) + x.group(2) + TICK + x.group(3), block, flags=re.S)
    block = re.sub(r'<span class="wa-act">', '<span class="wa-act">' + REPLY, block)
    return block

s, n = re.subn(r'<div class="wa-screen".*?<div class="wa-bar">.*?</div>', screen, s, flags=re.S)
print('ekran:', n)
open(p, 'w', encoding='utf8').write(s)
