#!/usr/bin/env python3
"""Card day page. page.json + courses.json + photos.json -> index.html (+ preview.html).
Run: python3 build.py   (also exec'd by course-picker/engine/extract.py: module-level COURSES and PH)"""
import json, html, re
from urllib.parse import quote

PH = json.load(open('photos.json'))
PAGE = json.load(open('page.json'))
COURSES = json.load(open('courses.json'))

E = html.escape
q = lambda s: quote(s, safe='')
RARE = {'A': '◆', 'B': '●', 'C': '★'}
CRED = PH['_credits']
N = len(COURSES)
NN = str(N).zfill(2)
SITE = 'https://yukitchy.github.io/pokemon-cards-nintendo-day/'
META_Q = PAGE['meet_place'] + ', Tokyo'


def gmap(query):
    return 'https://www.google.com/maps/search/?api=1&query=' + q(query)


def route(stops):
    u = 'https://www.google.com/maps/dir/?api=1&origin=' + q(stops[0]) + '&destination=' + q(stops[-1])
    if len(stops) > 2:
        u += '&waypoints=' + '%7C'.join(q(s) for s in stops[1:-1])
    return u + '&travelmode=transit'


def use(sym, cls='ic'):
    return f'<svg class="{cls}" aria-hidden="true" focusable="false"><use href="#{sym}"/></svg>'


BALL_FAVICON = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'><defs><clipPath id='c'><circle cx='32' cy='32' r='29'/></clipPath></defs>"
                "<circle cx='32' cy='32' r='29' fill='#ffffff'/><g clip-path='url(#c)'><g transform='rotate(-22 32 32)'><rect x='-20' y='-20' width='104' height='52' fill='#e3262e'/>"
                "<rect x='-20' y='28' width='104' height='8' fill='#0e1a3a'/></g></g><circle cx='32' cy='32' r='29' fill='none' stroke='#0e1a3a' stroke-width='4'/>"
                "<circle cx='32' cy='32' r='8' fill='#ffffff' stroke='#0e1a3a' stroke-width='4'/></svg>")
FAVICON = 'data:image/svg+xml,' + quote(BALL_FAVICON, safe="/:=' ")

SPRITE = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>
<linearGradient id="g-holo" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ff8fb1"/><stop offset=".25" stop-color="#ffd76e"/><stop offset=".5" stop-color="#8dffb8"/><stop offset=".75" stop-color="#78d6ff"/><stop offset="1" stop-color="#b9a0ff"/></linearGradient>
<pattern id="p-dots" width="14" height="14" patternUnits="userSpaceOnUse"><circle cx="7" cy="7" r="2.2" fill="#0e1a3a" opacity=".18"/></pattern>
<clipPath id="cl-ball"><circle cx="32" cy="32" r="29"/></clipPath>
<symbol id="i-ball" viewBox="0 0 64 64"><circle cx="32" cy="32" r="29" fill="#ffffff"/>
<g clip-path="url(#cl-ball)"><g transform="rotate(-22 32 32)"><rect x="-20" y="-20" width="104" height="52" fill="#e3262e"/><rect x="-20" y="28" width="104" height="8" fill="#0e1a3a"/></g></g>
<path d="M14 22a21 21 0 0 1 12-9" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round" opacity=".8"/>
<circle cx="32" cy="32" r="29" fill="none" stroke="#0e1a3a" stroke-width="3.5"/>
<circle cx="32" cy="32" r="8.5" fill="#ffffff" stroke="#0e1a3a" stroke-width="3.5"/><circle cx="32" cy="32" r="3" fill="#0e1a3a"/></symbol>
<symbol id="i-orb" viewBox="0 0 64 64"><ellipse cx="32" cy="32" rx="30" ry="9" transform="rotate(-24 32 32)" fill="none" stroke="#0e1a3a" stroke-width="3"/>
<circle cx="32" cy="32" r="21" fill="#1f56b5" stroke="#0e1a3a" stroke-width="3.5"/>
<circle cx="32" cy="32" r="13" fill="#ffffff" stroke="#0e1a3a" stroke-width="2.5"/><circle cx="32" cy="32" r="5.5" fill="#1f56b5" stroke="#0e1a3a" stroke-width="2.5"/>
<circle cx="54" cy="17" r="3.5" fill="#0e1a3a"/></symbol>
<symbol id="i-slab" viewBox="0 0 48 64"><rect x="2" y="2" width="44" height="60" rx="6" fill="#ffffff" stroke="#0e1a3a" stroke-width="3"/>
<rect x="7" y="7" width="34" height="8" rx="2" fill="#0e1a3a"/>
<rect x="8" y="20" width="32" height="38" rx="3" fill="#1f56b5" stroke="#0e1a3a" stroke-width="2.5"/>
<rect x="8" y="38" width="32" height="5" fill="url(#g-holo)"/><circle cx="24" cy="29" r="5" fill="none" stroke="#0e1a3a" stroke-width="2.5"/></symbol>
<symbol id="a-ball" viewBox="0 0 400 300"><rect width="400" height="300" fill="#ffffff"/><rect width="400" height="300" fill="url(#p-dots)"/>
<circle cx="200" cy="150" r="112" fill="#c3d4f2"/><circle cx="200" cy="150" r="134" fill="none" stroke="#0e1a3a" stroke-width="3" stroke-dasharray="2 10" stroke-linecap="round"/>
<use href="#i-ball" x="118" y="68" width="164" height="164"/></symbol>
<symbol id="a-orb" viewBox="0 0 400 300"><rect width="400" height="300" fill="#ffffff"/><rect width="400" height="300" fill="url(#p-dots)"/>
<circle cx="200" cy="150" r="112" fill="#1f56b5" opacity=".28"/><circle cx="200" cy="150" r="134" fill="none" stroke="#0e1a3a" stroke-width="3" stroke-dasharray="2 10" stroke-linecap="round"/>
<use href="#i-orb" x="108" y="58" width="184" height="184"/></symbol>
<symbol id="a-slab" viewBox="0 0 400 300"><rect width="400" height="300" fill="#ffffff"/><rect width="400" height="300" fill="url(#p-dots)"/>
<circle cx="200" cy="150" r="112" fill="#1f56b5" opacity=".28"/><circle cx="200" cy="150" r="134" fill="none" stroke="#0e1a3a" stroke-width="3" stroke-dasharray="2 10" stroke-linecap="round"/>
<use href="#i-slab" x="119" y="22" width="162" height="216"/></symbol>
</defs></svg>'''

CSS = r'''
:root{
  --bg:#eaf0fa; --ink:#0e1a3a; --mute:#4a5878; --blue:#1f56b5; --red:#e3262e; --paper:#ffffff;
  --holo:linear-gradient(115deg,#ff8fb1 0%,#ffd76e 22%,#8dffb8 45%,#78d6ff 68%,#b9a0ff 88%,#ff8fb1 100%);
  --cond:'Barlow Condensed','Arial Narrow',Impact,sans-serif;
  --body:'Barlow','Helvetica Neue',Arial,sans-serif;
  --mono:'IBM Plex Mono',ui-monospace,Menlo,monospace;
  --cw:clamp(130px,36vw,222px);
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--body);font-size:17px;line-height:1.55;overflow-x:hidden}
button{font:inherit;color:inherit}
a{color:var(--ink)}
img{display:block;max-width:100%}
.wrap{max-width:1160px;margin:0 auto;padding:0 20px}
.nb{word-break:keep-all;overflow-wrap:normal}
.sheet{display:none}
.ic{width:1em;height:1em;flex:none}

/* hero */
.hero{display:grid;grid-template-columns:1.15fr .85fr;gap:24px;align-items:center;padding:36px 0 20px}
.kicker{font-family:var(--mono);font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--mute);margin:0 0 14px}
h1{font-family:var(--cond);font-weight:900;text-transform:uppercase;line-height:.92;letter-spacing:-.005em;font-size:clamp(46px,8.4vw,112px);margin:0;word-break:keep-all;overflow-wrap:normal}
.stat{display:inline-block;margin:22px 0 0;padding:6px 12px;background:var(--red);color:#fff;font-family:var(--mono);font-weight:600;font-size:clamp(15px,2.3vw,20px);letter-spacing:.02em}
.lead{max-width:34em;margin:18px 0 0;font-size:19px}
.facts{margin:22px 0 0;padding:0;list-style:none;font-family:var(--mono);font-size:13px;border-top:2px solid var(--ink)}
.facts li{display:flex;gap:14px;padding:8px 0;border-bottom:1px solid rgba(14,26,58,.25)}
.facts b{width:64px;flex:none;text-transform:uppercase;letter-spacing:.1em;font-weight:500;color:var(--mute)}

/* dividers + strips */
.dv{display:flex;align-items:center;gap:14px;margin:34px 0 0}
.dv i{flex:1;height:2px;background:var(--ink)}
.dv svg{width:34px;height:34px}
.strip{height:10px;border-radius:99px;background:radial-gradient(circle,var(--ink) 2px,transparent 2.5px) 0 0/12px 10px repeat-x;opacity:.55;margin:0 0 16px}
.corner{width:22px;height:22px;border-radius:50%;border:1.5px solid var(--ink);background:repeating-radial-gradient(circle at 50% 50%,var(--ink) 0 1.5px,var(--blue) 1.5px 4.5px);flex:none}

/* shared card pieces */
.card{background:var(--blue);border-radius:14px;padding:8px;aspect-ratio:5/7;box-shadow:0 1px 0 rgba(14,26,58,.5),0 10px 22px -10px rgba(14,26,58,.45)}
.face{height:100%;background:var(--paper);border-radius:8px;display:flex;flex-direction:column;padding:8px;gap:6px;min-height:0;overflow:hidden}
.band{display:flex;justify-content:space-between;align-items:center;gap:6px;font-family:var(--mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase}
.art{flex:1;min-height:56px;border-radius:5px;border:2px solid var(--ink);position:relative;overflow:hidden;background:var(--blue)}
.art img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.art-holo::after{content:"";position:absolute;inset:0;background:repeating-linear-gradient(45deg,rgba(255,255,255,.28) 0 2px,transparent 2px 9px),var(--holo);background-size:auto,220% 100%;mix-blend-mode:soft-light;opacity:.85;animation:sheen 1.6s .5s ease-out 1 both}
@keyframes sheen{from{background-position:0 0,100% 0}to{background-position:0 0,0 0}}
.foot{display:flex;justify-content:space-between;align-items:center;font-family:var(--mono);font-size:11px;font-weight:600}
.rare{letter-spacing:.2em}

/* fan */
.fanbox{position:relative}
.fan{position:relative;height:calc(var(--cw)*1.4 + 36px);width:100%}
.fan .card{position:absolute;left:50%;bottom:0;width:var(--cw);margin-left:calc(var(--cw)/-2);transform-origin:50% 100%;transform:translateX(var(--x)) rotate(var(--r));animation:fanIn .8s ease-out 1 both}
.fan .c1{--x:calc(var(--cw)*-.44);--r:-12deg;z-index:1}
.fan .c2{--x:0px;--r:0deg;z-index:3;animation-delay:.1s;background:var(--holo)}
.fan .c3{--x:calc(var(--cw)*.44);--r:12deg;z-index:2;animation-delay:.2s}
.fan .nm{font-family:var(--cond);font-weight:900;text-transform:uppercase;font-size:clamp(16px,3.6vw,26px);line-height:1}
.herball{position:absolute;right:-4px;top:-6px;width:clamp(56px,9vw,92px);height:clamp(56px,9vw,92px);z-index:4;filter:drop-shadow(0 6px 8px rgba(14,26,58,.3));animation:pop .7s .5s cubic-bezier(.3,1.6,.5,1) 1 both}
@keyframes fanIn{from{transform:translateX(0) rotate(0deg) translateY(28px);opacity:0}}
@keyframes pop{from{transform:scale(.3) rotate(-40deg);opacity:0}}

/* plan cards */
.sec-head{display:flex;justify-content:space-between;align-items:baseline;gap:12px;padding-top:14px;margin:0 0 18px;font-family:var(--mono);font-size:13px;letter-spacing:.1em;text-transform:uppercase}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
.pc{display:block;width:100%;border:0;text-align:left;cursor:pointer;transition:transform .15s;-webkit-tap-highlight-color:transparent}
.pc:hover{transform:translateY(-4px)}
.pc:focus-visible{outline:3px solid var(--ink);outline-offset:3px}
.pc[aria-expanded="true"]{background:var(--holo)}
.pc .nm{font-family:var(--cond);font-weight:900;text-transform:uppercase;font-size:clamp(22px,2.1vw,28px);line-height:1;margin:2px 0 0}
.pc .tag{font-size:13px;line-height:1.3;color:var(--mute);margin:0}
.moves{display:grid;grid-template-columns:1fr 1fr;border:1.5px solid var(--ink);border-radius:4px;font-family:var(--mono);font-size:11px}
.moves span{padding:5px 8px}
.moves span+span{border-left:1.5px solid var(--ink)}
.moves b{font-weight:600}
.open-hint{font-family:var(--mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase}
.pc .band>span:first-child{display:flex;align-items:center;gap:7px}

/* panel */
.panel{margin-top:26px;background:var(--paper);border:3px solid var(--blue);border-radius:14px;padding:26px;outline:0;scroll-margin-top:12px}
.panel[hidden]{display:none}
.ph{display:flex;flex-wrap:wrap;justify-content:space-between;gap:10px 24px;align-items:flex-end}
.ph h2{font-family:var(--cond);font-weight:900;text-transform:uppercase;font-size:clamp(32px,5vw,56px);line-height:.95;margin:0;word-break:keep-all;overflow-wrap:normal}
.ph .no{display:flex;align-items:center;gap:8px;font-family:var(--mono);font-size:13px;letter-spacing:.1em;color:var(--mute);margin:0 0 8px}
.ph .no .ic{width:26px;height:26px}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:0;padding:0;list-style:none}
.chips li{font-family:var(--mono);font-size:12px;border:1.5px solid var(--ink);border-radius:99px;padding:2px 10px}
.why{margin:16px 0 0;max-width:44em}
.mv{margin:20px 0 0;padding:0;list-style:none;border-top:2px solid var(--ink)}
.mv>li{display:grid;grid-template-columns:84px minmax(0,1fr) 250px;gap:8px 20px;padding:16px 0;border-bottom:1px solid rgba(14,26,58,.25);align-items:start}
.cost{font-family:var(--mono);font-weight:600;font-size:15px;background:var(--ink);color:#fff;border-radius:99px;padding:3px 0;text-align:center;width:84px}
.mn{font-family:var(--cond);font-weight:800;text-transform:uppercase;font-size:24px;line-height:1.05;margin:2px 0 0}
.fx{margin:6px 0 0;color:#2c281d}
.lk{display:flex;flex-wrap:wrap;gap:0 18px;margin:4px 0 0}
.lk a,.ln,.links a{display:inline-flex;align-items:center;min-height:44px;font-family:var(--mono);font-size:14px;font-weight:600}
.shot{margin:0}
.shot .pic{aspect-ratio:4/3;width:100%;border:2px solid var(--ink);border-radius:5px;overflow:hidden;background:var(--blue)}
.shot img,.shot svg{width:100%;height:100%;object-fit:cover;display:block}
.shot figcaption{font-family:var(--mono);font-size:11px;line-height:1.4;color:var(--mute);margin-top:5px}
.notes{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:22px}
.notes h3,.lh{font-family:var(--mono);font-weight:500;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--mute);margin:0 0 4px}
.notes p{margin:0}
.links{margin-top:18px}
.links ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:0 22px}
.route{display:inline-flex;align-items:center;min-height:48px;margin-top:14px;padding:0 18px;background:var(--ink);color:var(--paper);font-family:var(--mono);font-size:14px;font-weight:600;text-decoration:none;border-radius:6px}

/* questionnaire */
.qz{margin-top:6px}
.qcard{background:var(--blue);border-radius:14px;padding:8px;box-shadow:0 1px 0 rgba(14,26,58,.5),0 10px 22px -10px rgba(14,26,58,.45)}
.qface{background:var(--paper);border-radius:8px;padding:24px;display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr);gap:20px 36px}
.qface h2{font-family:var(--cond);font-weight:900;text-transform:uppercase;font-size:clamp(32px,4.4vw,52px);line-height:.95;margin:10px 0 10px}
.qface .qintro{margin:0;color:#2c281d}
.qface .ic.qb{width:44px;height:44px}
.qf{display:grid;gap:18px}
.qf label,.qf legend{display:block;font-family:var(--mono);font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--mute);margin:0 0 6px;padding:0}
.qf fieldset{border:0;margin:0;padding:0;min-width:0}
.qf input[type=text],.qf textarea{width:100%;min-height:48px;padding:10px 12px;font:inherit;font-size:16px;color:var(--ink);background:#fff;border:2px solid var(--ink);border-radius:6px}
.qf textarea{min-height:120px;resize:vertical}
.qf input[type=text]:focus-visible,.qf textarea:focus-visible{outline:3px solid var(--ink);outline-offset:2px;background:#ffffff}
.qf ::placeholder{color:#7a705a;opacity:1}
.opts{display:flex;flex-wrap:wrap;gap:8px}
.opts input{position:absolute;opacity:0;width:1px;height:1px}
.opts label{display:inline-flex;align-items:center;justify-content:center;min-height:44px;min-width:56px;padding:0 16px;margin:0;border:2px solid var(--ink);border-radius:99px;background:#fff;color:var(--ink);font-size:14px;letter-spacing:.04em;cursor:pointer;text-transform:none;font-weight:600}
.opts input:checked+label{background:var(--red);color:#fff;border-color:var(--red)}
.opts input:focus-visible+label{outline:3px solid var(--ink);outline-offset:3px}
.qbtns{display:flex;flex-wrap:wrap;gap:10px 12px;align-items:center}
.qbtn{min-height:48px;padding:0 22px;border:2px solid var(--ink);border-radius:8px;font-family:var(--mono);font-weight:600;font-size:15px;cursor:pointer;background:var(--paper)}
.qbtn.pri{background:var(--ink);color:var(--paper)}
.qbtn:focus-visible{outline:3px solid var(--ink);outline-offset:3px}
.qstat{font-family:var(--mono);font-size:13px;min-height:1.4em;margin:0}
.qnote{font-size:14px;color:var(--mute);margin:0}
.hid{position:absolute;left:-9999px;top:0;width:1px;height:1px;opacity:0}

/* meet + footer */
.meet{display:grid;grid-template-columns:.8fr 1.2fr;gap:28px;align-items:start}
.meet h2{font-family:var(--cond);font-weight:900;text-transform:uppercase;font-size:clamp(32px,4.4vw,52px);line-height:.95;margin:0 0 10px}
.meet p{margin:0 0 14px}
.map{width:100%;height:320px;border:2px solid var(--ink);border-radius:8px;background:#e8dfc6}
.reply{margin:0;padding:30px 0 40px;display:flex;flex-wrap:wrap;gap:20px 40px;justify-content:space-between;align-items:flex-end}
.reply h2{font-family:var(--cond);font-weight:900;text-transform:uppercase;font-size:clamp(32px,5.2vw,64px);line-height:.95;margin:0;max-width:12em}
.reply p{margin:10px 0 0;color:var(--mute);max-width:36em}
.pdf{min-height:52px;padding:0 24px;background:var(--red);color:#fff;border:2px solid var(--ink);border-radius:8px;font-family:var(--mono);font-weight:600;font-size:15px;cursor:pointer}
.pdf:focus-visible{outline:3px solid var(--ink);outline-offset:3px}
.cred{margin:0 0 48px;font-size:13px;color:var(--mute)}
.cred summary{cursor:pointer;min-height:44px;display:flex;align-items:center;font-family:var(--mono);font-weight:600;color:var(--ink)}
.cred ul{margin:4px 0 0;padding-left:18px}
.cred li{margin:4px 0}
.cred a{color:var(--ink)}

@media (max-width:860px){
  .hero{grid-template-columns:1fr;padding-top:28px}
  .cards{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:14px;margin:0 -20px;padding:6px 20px 14px;scroll-padding:0 20px;-webkit-overflow-scrolling:touch}
  .cards .pc{flex:0 0 76vw;max-width:340px;scroll-snap-align:start}
  .pc .nm{font-size:26px}
  .mv>li{grid-template-columns:84px minmax(0,1fr)}
  .mv .shot{grid-column:1/-1;max-width:420px}
  .notes{grid-template-columns:1fr}
  .meet{grid-template-columns:1fr}
  .qface{grid-template-columns:1fr;padding:18px 14px}
  .panel{padding:20px 16px}
  .map{height:260px}
  .herball{right:6px}
}
@media (prefers-reduced-motion:reduce){
  .fan .card,.art-holo::after,.herball{animation:none}
  .pc{transition:none}
}

/* print: only the compact sheet */
@page{size:A4;margin:11mm}
@media print{
  body{background:#fff;font-size:9pt;line-height:1.35;color:#000;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  .screen{display:none!important}
  .sheet{display:block}
  .sheet h1{font-size:20pt;margin:0 0 3pt;line-height:1}
  .sheet .meta{margin:0 0 5pt;font-size:9pt}
  .sheet .meta b{font-family:var(--mono);font-size:9pt;font-weight:600}
  .sheet .mp{border:1px solid #000;border-left:5pt solid var(--blue);padding:3pt 7pt;margin:0 0 5pt}
  .sheet .mp p{margin:0}
  .sheet h2{font-family:var(--cond);font-weight:900;text-transform:uppercase;font-size:13pt;line-height:1.1;margin:6pt 0 1pt;border-bottom:1.5pt solid #000;break-after:avoid}
  .sheet table{width:100%;border-collapse:collapse}
  .sheet tr{break-inside:avoid}
  .sheet td{padding:1.5pt 0;border-bottom:.5pt solid #999;vertical-align:top;font-size:9pt;line-height:1.25}
  .sheet td.t{width:34pt;font-family:var(--mono);font-weight:600;font-size:9pt}
  .sheet td.p{width:118pt;font-weight:600;padding-right:6pt}
  .sheet .u{display:block;font-family:var(--mono);font-size:9pt;color:#333;word-break:break-all}
  .sheet .ft{margin:6pt 0 0;font-size:9pt;line-height:1.3}
  .sheet .qs{break-inside:avoid;margin-top:6pt}
  .sheet .qs p{margin:3pt 0 0;font-size:9pt}
  .sheet .qs .ln1{height:22pt;border-bottom:.6pt solid #000}
  .sheet .qs .bx{display:inline-block;width:8pt;height:8pt;border:1pt solid #000;margin:0 3pt 0 8pt;vertical-align:-1pt}
}
'''

JS = r'''
(function(){
  var cards=[].slice.call(document.querySelectorAll('.pc'));
  var rm=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function show(id,scroll){
    cards.forEach(function(b){
      var on=b.dataset.plan===id, p=document.getElementById('detail-'+b.dataset.plan);
      p.hidden=!on; b.setAttribute('aria-expanded',on?'true':'false');
      b.querySelector('.open-hint').textContent=on?'Open':'Tap to open';
    });
    if(scroll)document.getElementById('detail-'+id).scrollIntoView({block:'start',behavior:rm?'auto':'smooth'});
  }
  cards.forEach(function(b){b.addEventListener('click',function(){
    show(b.dataset.plan,window.innerWidth<=860);history.replaceState(null,'','#detail-'+b.dataset.plan);});});
  function fromHash(){var m=location.hash.match(/^#detail-([A-Z])$/);return m&&document.getElementById('detail-'+m[1])?m[1]:null;}
  window.addEventListener('hashchange',function(){var h=fromHash();if(h)show(h,true);});
  var h=fromHash();show(h||cards[0].dataset.plan,false);
  if(h)setTimeout(function(){document.getElementById('detail-'+h).scrollIntoView();},80);
})();
(function(){
  var TO='icchan417@gmail.com',SUB='Plan choice and questions';
  function v(id){var x=(document.getElementById(id).value||'').trim();return x||'-';}
  function body(){
    var r=document.querySelector('input[name="qplan"]:checked');
    return 'Plan: '+(r?r.value:'-')+'\n\n1. Favourite Pokémon: '+v('q-fav')+'\n\n2. Cards I am looking for: '+v('q-cards')+'\n\n3. Shops to visit or skip: '+v('q-shops')+'\n\n';
  }
  document.getElementById('q-mail').addEventListener('click',function(){
    window.location.href='mailto:'+TO+'?subject='+encodeURIComponent(SUB)+'&body='+encodeURIComponent(body());
  });
  var st=document.getElementById('q-stat');
  function ok(){st.textContent='Copied. Paste it into your reply.';}
  function fallback(t){
    var a=document.getElementById('q-hid');a.value=t;a.focus();a.select();
    try{if(document.execCommand('copy'))ok();}catch(e){}
  }
  document.getElementById('q-copy').addEventListener('click',function(){
    var t=body();
    if(navigator.clipboard&&navigator.clipboard.writeText){
      navigator.clipboard.writeText(t).then(ok,function(){fallback(t);});
    }else fallback(t);
  });
})();
'''


def photo_fig(step):
    d = step[3]
    if d.get('img'):
        c = CRED[d['img']]
        cap = c['alt'] + ('. ' + c['note'] if c['note'] else '.')
        return (f'<figure class="shot"><div class="pic"><img src="{E(c["src"])}" alt="{E(c["alt"])}" loading="lazy"></div>'
                f'<figcaption>{E(cap)}</figcaption></figure>')
    art = d.get('art')
    if art:
        return f'<figure class="shot"><div class="pic"><svg viewBox="0 0 400 300" aria-hidden="true" focusable="false"><use href="#a-{art}"/></svg></div></figure>'
    return ''


def step_li(s):
    t, name, desc, d = s
    links = ''
    if d.get('url'):
        links += f'<a href="{E(d["url"])}" target="_blank" rel="noopener">Official page &#8599;</a>'
    if d.get('maps'):
        links += f'<a href="{gmap(d["maps"])}" target="_blank" rel="noopener">Map &#8599;</a>'
    return (f'<li><span class="cost">{E(t)}</span><div><h3 class="mn nb">{E(name)}</h3><p class="fx">{E(desc)}</p>'
            f'<p class="lk">{links}</p></div>{photo_fig(s)}</li>')


def fan_card(c, i):
    th = PH[c['id']]['card']
    return (f'<div class="card c{i + 1}"><div class="face"><div class="band"><span>Plan {c["id"]}</span><span>{RARE[c["id"]]}</span></div>'
            f'<div class="art"><img src="{E(th["thumb"])}" alt="" loading="eager"></div><div class="nm">Plan {c["id"]}</div>'
            f'<div class="foot"><span>{c["id"]}/{NN}</span><span class="rare">{RARE[c["id"]]}</span></div></div></div>')


def plan_card(c):
    th = PH[c['id']]['card']
    return (f'<button type="button" class="card pc" id="pc-{c["id"]}" data-plan="{c["id"]}" aria-expanded="false" aria-controls="detail-{c["id"]}">'
            f'<span class="face"><span class="band"><span><span class="corner"></span>Plan {c["id"]}</span><span class="open-hint">Tap to open</span></span>'
            f'<span class="art"><img src="{E(th["thumb"])}" alt="{E(th["title"])}" loading="lazy"></span>'
            f'<span class="nm nb">{E(c["name"])}</span><span class="tag">{E(c["tag"])}</span>'
            f'<span class="moves"><span>Steps <b>{len(c["steps"])}</b></span><span>Stops <b>{len(c["stops"])}</b></span></span>'
            f'<span class="foot"><span>{c["id"]}/{NN}</span><span class="rare">{RARE[c["id"]]}</span></span></span></button>')


def panel(c):
    chips = ''.join(f'<li>{E(x)}</li>' for x in c['chips'])
    links = ''.join(f'<li><a href="{E(u)}" target="_blank" rel="noopener">{E(t)} &#8599;</a></li>' for t, u in c['links'])
    return (f'<section class="panel" id="detail-{c["id"]}" tabindex="-1" hidden aria-labelledby="ph-{c["id"]}">'
            f'<div class="strip"></div>'
            f'<div class="ph"><div><p class="no">{use("i-ball")}PLAN {c["id"]}/{NN} {RARE[c["id"]]}</p><h2 id="ph-{c["id"]}">{E(c["name"])}</h2></div>'
            f'<ul class="chips">{chips}</ul></div>'
            f'<p class="why">{E(c["why"])}</p>'
            f'<ol class="mv">{"".join(step_li(s) for s in c["steps"])}</ol>'
            f'<div class="notes"><div><h3>Getting around</h3><p>{E(c["moves"])}</p></div><div><h3>Good for</h3><p>{E(c["good"])}</p></div>'
            f'<div><h3>Keep in mind</h3><p>{E(c["mind"])}</p></div></div>'
            f'<div class="links"><h3 class="lh">Links</h3><ul>{links}</ul></div>'
            f'<a class="route" href="{route(c["stops"])}" target="_blank" rel="noopener">Open the whole route in Google Maps &#8599;</a></section>')


def quest():
    opts = ''.join(f'<input type="radio" name="qplan" id="qp-{i}" value="{E(v)}"><label for="qp-{i}">{E(l)}</label>'
                   for i, (v, l) in enumerate([(c['id'], c['id']) for c in COURSES] + [('Not sure yet', 'Not sure yet')]))
    return (f'<section class="qz" aria-labelledby="qh"><div class="qcard"><div class="qface"><div>{use("i-ball", "ic qb")}'
            f'<h2 id="qh">Before the day: three quick questions</h2>'
            f'<p class="qintro">Answering takes one or two minutes. It helps your guide plan the stops around you.</p></div>'
            f'<div class="qf"><fieldset><legend>Plan I would like</legend><div class="opts">{opts}</div></fieldset>'
            f'<div><label for="q-fav">Which Pok&eacute;mon do you like most?</label><input type="text" id="q-fav" autocomplete="off"></div>'
            f'<div><label for="q-cards">Which cards are you looking for?</label><textarea id="q-cards" placeholder="Card name, set or card number, and the condition or PSA grade you prefer. Add photos by attaching them to your reply."></textarea></div>'
            f'<div><label for="q-shops">Shops you want to visit, and shops you want to skip</label><textarea id="q-shops"></textarea></div>'
            f'<div class="qbtns"><button type="button" class="qbtn pri" id="q-mail">Reply by email</button>'
            f'<button type="button" class="qbtn" id="q-copy">Copy my answers</button></div>'
            f'<p class="qstat" id="q-stat" role="status" aria-live="polite"></p>'
            f'<p class="qnote">If the email button does nothing, use Copy my answers and paste into a reply to the email you received.</p>'
            f'<textarea class="hid" id="q-hid" tabindex="-1" aria-hidden="true"></textarea>'
            f'</div></div></div></section>')


def credits():
    seen = []
    for c in COURSES:
        for s in c['steps']:
            k = s[3].get('img')
            if k and k not in seen:
                seen.append(k)
    li = ''.join(
        f'<li><a href="{E(CRED[k]["page"])}" target="_blank" rel="noopener">{E(CRED[k]["title"])}</a>, by {E(CRED[k]["artist"])} '
        f'({E(CRED[k]["lic"])}), via Wikimedia Commons</li>' for k in seen)
    return f'<details class="cred"><summary>Photo credits</summary><ul>{li}</ul></details>'


def sheet_q():
    lines = '<div class="ln1"></div>' * 3
    qs = ''.join(f'<p><b>{n}. {E(t)}</b></p>{lines}' for n, t in
                 [(1, 'Which Pokémon do you like most?'), (2, 'Which cards are you looking for?'),
                  (3, 'Shops you want to visit, and shops you want to skip')])
    boxes = ''.join(f'<span class="bx"></span>{E(l)}' for l in [c['id'] for c in COURSES] + ['Not sure'])
    return (f'<div class="qs"><h2>Before the day: three quick questions</h2><p><b>Plan I would like:</b>{boxes}</p>{qs}</div>')


def sheet():
    rows = ''
    for c in COURSES:
        tr = ''
        for t, name, desc, d in c['steps']:
            u = f'<span class="u">{E(d["url"])}</span>' if d.get('url') else ''
            tr += f'<tr><td class="t">{E(t)}</td><td class="p">{E(name)}</td><td>{E(desc)}{u}</td></tr>'
        rows += f'<h2>Plan {c["id"]}: {E(c["name"])}</h2><table><tbody>{tr}</tbody></table>'
    facts = ' &nbsp;|&nbsp; '.join(f'<b>{E(a)}</b> {E(b)}' for a, b in PAGE['facts'])
    return (f'<section class="sheet" aria-hidden="true"><h1>{E(PAGE["h1"])}</h1><p class="meta">{facts}</p>'
            f'<div class="mp"><p><b>{E(PAGE["meet_place"])}</b></p><p>{E(PAGE["meet_text"])} {E(PAGE["meet_hint"])}</p></div>'
            f'{rows}{sheet_q()}<p class="ft">{E(PAGE["footer"])}</p></section>')


time_txt = next(v for k, v in PAGE['facts'] if k == 'Length')
start = re.search(r'\d{1,2}:\d{2}', PAGE['meet_sub']).group(0)
facts_li = ''.join(f'<li><b>{E(a)}</b><span>{E(b)}</span></li>' for a, b in PAGE['facts'])
dot = PAGE['footer'].index('. ') + 1
r1, r2 = PAGE['footer'][:dot], PAGE['footer'][dot:].strip()
mq = q(META_Q)
DV = f'<div class="dv" aria-hidden="true"><i></i>{use("i-ball", "")}<i></i></div>'

HEAD = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(PAGE["title"])}</title>
<meta name="robots" content="noindex">
<meta name="description" content="{E(PAGE["og_desc"])}">
<meta property="og:title" content="{E(PAGE["title"])}">
<meta property="og:description" content="{E(PAGE["og_desc"])}">
<meta property="og:type" content="website">
<meta property="og:image" content="{SITE}og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="{SITE}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(PAGE["title"])}">
<meta name="twitter:description" content="{E(PAGE["og_desc"])}">
<meta name="twitter:image" content="{SITE}og.jpg">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800;900&family=Barlow:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
<noscript><style>.panel[hidden]{{display:block}}</style></noscript>
</head>
<body>
{SPRITE}
<main class="wrap screen">
  <section class="hero">
    <div>
      <p class="kicker">{E(PAGE["kicker"])}</p>
      <h1>{E(PAGE["h1"])}</h1>
      <p class="stat">{N} plans &middot; {E(time_txt)}</p>
      <p class="lead">{E(PAGE["lead"])}</p>
      <ul class="facts">{facts_li}</ul>
    </div>
    <div class="fanbox"><div class="fan" aria-hidden="true">{"".join(fan_card(c, i) for i, c in enumerate(COURSES))}</div>{use("i-ball", "herball")}</div>
  </section>

  {DV}
  <div class="sec-head" style="margin-top:14px"><span>{N} cards in the deck</span><span>Tap one to open it</span></div>
  <div class="cards">{"".join(plan_card(c) for c in COURSES)}</div>
  <div id="panels">{"".join(panel(c) for c in COURSES)}</div>

  {DV}
  {quest()}

  {DV}
  <div class="sec-head" style="margin-top:14px"><span>Where we meet</span><span>{E(start)}</span></div>
  <section class="meet">
    <div>
      <h2>{E(PAGE["meet_place"])}</h2>
      <p>{E(PAGE["meet_text"])}</p>
      <p>{E(PAGE["meet_hint"])}</p>
      <a class="ln" href="{gmap(META_Q)}" target="_blank" rel="noopener">Open in Google Maps &#8599;</a>
    </div>
    <iframe class="map" src="https://maps.google.com/maps?q={mq}&amp;output=embed" title="Map of the meeting point" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
  </section>

  {DV}
  <section class="reply">
    <div>
      <h2>{E(r1)}</h2>
      <p>{E(r2)}</p>
    </div>
    <button class="pdf" type="button" onclick="window.print()">Save as PDF</button>
  </section>
  {credits()}
</main>
{sheet()}
<script>{JS}</script>
@@DEVBAR@@</body></html>
'''

open('index.html', 'w').write(HEAD.replace('@@DEVBAR@@', ''))
open('preview.html', 'w').write(HEAD.replace(
    '@@DEVBAR@@', '<script>window.DEVBAR_FORCE=1</script><script src="devbar.js?v=3"></script>'))
print('written', len(HEAD), '-> index.html + preview.html')
