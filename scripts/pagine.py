#!/usr/bin/env python3
"""Genera le pagine /luce-e-gas/ e /internet/ partendo dalla testata di /psv/.

Uso: python3 scripts/pagine.py   (poi python3 scripts/csp.py)
I dati internet stanno in data/internet.json e si aggiornano a mano.
"""
import html as H
import json
import re
from pathlib import Path

R = Path(__file__).resolve().parent.parent
BASE = "https://comparaoffertelucegas.it"
tpl = (R / "psv" / "index.html").read_text(encoding="utf-8")
testa = tpl[: tpl.index('<main')]
piede = tpl[tpl.index('</main>') + len('</main>'): tpl.index('<script>\n(function(){')]
tema = re.search(r"\(function\(\)\{var modes=.*?show\(\)\}\)\(\);", tpl, re.S).group(0)

CSS_NET = """.t-luce:hover:not([aria-pressed=true]):not([aria-current]){background:rgba(245,197,24,.25)!important;color:var(--ink)!important}
.t-gas:hover:not([aria-pressed=true]):not([aria-current]){background:rgba(198,91,124,.22)!important;color:var(--ink)!important}
.t-lg:hover:not([aria-current]){background:linear-gradient(90deg,rgba(245,197,24,.25),rgba(198,91,124,.22))!important;color:var(--ink)!important}
.t-net:hover:not([aria-current]){background:rgba(46,155,230,.2)!important;color:var(--ink)!important}
.seg button,.seg a{transition:background-color .15s}
.oc{transition:border-color .15s,box-shadow .15s,transform .15s}
.oc:hover{border-color:var(--accbar);box-shadow:0 8px 22px rgba(0,0,0,.08);transform:translateY(-2px)}
@media (prefers-reduced-motion:reduce){.oc,.oc:hover{transition:none;transform:none}}
:root[data-c=lg] .oc:not(.first):hover{border-color:transparent;background:linear-gradient(var(--card),var(--card)) padding-box,var(--grad) border-box}
.lgh{display:grid;grid-template-columns:1fr 1.15fr;gap:16px;margin-bottom:16px}.lgh .card{margin:0}
.lga h2{margin:0 0 14px;font-size:22px}.lgq{display:flex;align-items:center;justify-content:space-between;gap:12px;margin:0 0 10px}.lgq label{font:700 17px 'Schibsted Grotesk',sans-serif}
.lgst{display:flex;align-items:center;gap:8px}.pm{width:44px;height:44px;border-radius:12px;border:1px solid var(--bd);background:var(--card);color:var(--ink);font:600 22px 'Schibsted Grotesk',sans-serif;cursor:pointer;touch-action:manipulation}.pm:hover{border-color:var(--ink)}
.lgv input::-webkit-outer-spin-button,.lgv input::-webkit-inner-spin-button{-webkit-appearance:none;margin:0}.lgv input[type=number]{-moz-appearance:textfield}
.lgv{display:flex;align-items:baseline;gap:8px;border:2px solid var(--bd);border-radius:14px;padding:6px 14px;background:var(--soft)}.lgv input{width:96px;border:0;background:transparent;font:800 30px 'Schibsted Grotesk',sans-serif;color:var(--ink);text-align:right}.lgv input:focus{outline:none}.lgv:focus-within{border-color:var(--ink)}.lgv span{color:var(--mut);font-weight:600}
.prof{display:flex;align-items:center;gap:6px;flex-wrap:wrap;font-size:13px;color:var(--mut);margin:12px 0 8px}.prof button{font:600 13px 'Schibsted Grotesk',sans-serif;padding:5px 10px;border-radius:8px;border:1px solid var(--bd);background:transparent;color:var(--ink2);cursor:pointer}.prof button:hover{border-color:var(--ink)}
.lgr{display:flex;align-items:center;gap:6px;font-size:14px;color:var(--ink2)}.lgr span{font-size:12.5px;color:var(--mut)}
.lgb1{position:relative;background:#14161A;color:#fff;border-radius:20px;padding:24px;overflow:hidden}.lgb1::before{content:'';position:absolute;top:0;left:0;right:0;height:4px;background:linear-gradient(90deg,#F5C518,#C65B7C)}
.lbk{font:800 12.5px 'Schibsted Grotesk',sans-serif;letter-spacing:.08em;text-transform:uppercase;background:linear-gradient(90deg,#F5C518,#E58CA8);-webkit-background-clip:text;background-clip:text;color:transparent}
.lbt{font:700 19px 'Schibsted Grotesk',sans-serif;margin-top:6px}.lbm{margin:6px 0 10px;white-space:nowrap}.lbm strong{font:800 54px/1 'Schibsted Grotesk',sans-serif;letter-spacing:-.03em}.lbm span{font:700 20px 'Schibsted Grotesk',sans-serif;color:#C9CCD1}
.lgr1{display:grid;grid-template-columns:70px 1fr auto;align-items:center;gap:10px;padding:9px 0;border-top:1px solid rgba(255,255,255,.12)}.lgr1 .k{font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:#9AA0A8}.lgl{display:flex;align-items:center;gap:10px;font-size:13.5px;color:#C9CCD1}.lgl strong{color:#fff;font-size:15px}.lgl .lgb{width:38px;height:38px;font-size:16px}.lgp{font-weight:800;font-size:16px;white-space:nowrap}
.lbs{color:#4ADE80;font-weight:700;font-size:14.5px;margin:10px 0 0}
.lbb{display:flex;gap:10px;flex-wrap:wrap;margin-top:14px}.lgbtn{display:inline-flex;align-items:center;gap:6px;background:linear-gradient(90deg,#F5C518,#C65B7C);color:#14161A;font:800 14.5px 'Schibsted Grotesk',sans-serif;padding:11px 16px;border-radius:12px;text-decoration:none}.lgbtn:after{content:'›';font-size:19px;line-height:1}
@media (max-width:860px){.lgh{grid-template-columns:1fr}.lbm strong{font-size:44px}.lgr1{grid-template-columns:56px 1fr auto}}
.oc{border:1px solid var(--line);border-radius:16px;background:var(--card);margin:0 0 12px;overflow:hidden}.oc[hidden]{display:none}
.oc.first{border:2px solid var(--accbar);box-shadow:0 6px 18px rgba(0,0,0,.06)}
.oc-h{display:flex;align-items:center;gap:12px;padding:14px 18px;border-bottom:1px solid var(--line)}.oc.first .oc-h{background:var(--first)}
.oc-n{font:800 15px 'Schibsted Grotesk',sans-serif;color:var(--mut);width:22px}
.lgb{position:relative;flex:0 0 auto;width:52px;height:52px;border-radius:12px;background:#fff;border:1px solid var(--line);display:inline-flex;align-items:center;justify-content:center;font:800 22px 'Schibsted Grotesk',sans-serif;color:#14161A;overflow:hidden}
.lgb img{position:absolute;inset:6px;width:calc(100% - 12px);height:calc(100% - 12px);object-fit:contain;background:#fff}
.oc-t{min-width:0;flex:1}.oc-v{font:800 18px 'Schibsted Grotesk',sans-serif}.oc-o{font-size:14.5px;color:var(--ink2);margin-top:2px}.oc-o a{color:var(--ink2)}
.oc-tg{display:flex;gap:6px;flex-wrap:wrap;justify-content:flex-end}
.tg{font:700 12px 'Schibsted Grotesk',sans-serif;padding:5px 9px;border-radius:7px;white-space:nowrap}
.tg-f{background:#14161A;color:#fff}.tg-v{background:#DBEAFE;color:#1E3A8A}.tg-w{background:#FFEDD5;color:#9A3412}.tg-s{background:transparent;border:1px solid var(--bd);color:var(--ink2)}
.tg-ftth{background:#14161A;color:#fff}.tg-fwa{background:#E0F2FE;color:#075985}.tg-altro{background:#E7E9E4;color:#3A3F47}
.st-A{background:#DCFCE7;color:#166534}.st-B{background:#ECFCCB;color:#3F6212}.st-C{background:#FEF9C3;color:#854D0E}.st-D{background:#FFE4E6;color:#9F1239}
.oc-b{display:grid;grid-template-columns:1.4fr 1fr auto;align-items:center}
.oc-d{margin:0;padding:14px 18px;display:grid;grid-template-columns:1fr 1fr;gap:8px 18px;border-right:1px solid var(--line)}
.oc-d div{display:flex;flex-direction:column}.oc-d div.w{grid-column:1/-1}.oc-d dt{font-size:12px;color:var(--mut);text-transform:uppercase;letter-spacing:.04em}.oc-d dd{margin:2px 0 0;font-weight:700;font-size:15px}.oc-d dd.nt{font-weight:400;font-size:13.5px;color:var(--ink2);white-space:normal;overflow:visible;text-overflow:clip;max-width:none}
.oc-p{text-align:center;padding:14px 18px;border-right:1px solid var(--line)}
.oc-m{white-space:nowrap}.oc-m strong{font:800 46px/1 'Schibsted Grotesk',sans-serif;letter-spacing:-.03em}.oc-m span{font:700 18px 'Schibsted Grotesk',sans-serif}
.oc-y{color:var(--mut);font-size:14px;margin-top:4px}.oc-dd{font-size:13.5px;font-weight:700;color:#B45309;margin-top:4px;white-space:nowrap}.oc-dd.top1{color:#15803d}
.oc-a{padding:14px 18px;display:flex;flex-direction:column;gap:8px;align-items:stretch}
.oc-btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;background:var(--accbg);color:#fff!important;font:800 15px 'Schibsted Grotesk',sans-serif;padding:13px 18px;border-radius:12px;text-decoration:none;white-space:nowrap}.oc-btn:after{content:'›';font-size:20px;line-height:1}.oc-btn:hover{filter:brightness(.94)}
@media (max-width:760px){.oc-h{flex-wrap:wrap;padding:12px 14px}.oc-tg{width:100%;justify-content:flex-start}.oc-b{grid-template-columns:minmax(0,1fr) auto}.oc-d{grid-column:1/-1;border-right:0;border-bottom:1px solid var(--line);padding:12px 14px}.oc-p{text-align:left;border-right:0;padding:12px 14px}.oc-a{padding:12px 14px 12px 0}.oc-m strong{font-size:34px}.oc-m span{font-size:16px}.oc-btn{padding:12px 14px;font-size:14px}.lgb{width:46px;height:46px}}
:root[data-c=lg]{--grad:linear-gradient(90deg,#F5C518,#C65B7C);--first:#FDF1E4}
:root[data-c=lg] header.top::before{background:var(--grad)}
:root[data-c=lg] .w-luce{background:linear-gradient(90deg,#F5C518,#DD904A);-webkit-background-clip:text;background-clip:text;color:transparent!important}
:root[data-c=lg] .w-gas{background:linear-gradient(90deg,#DD904A,#C65B7C);-webkit-background-clip:text;background-clip:text;color:transparent!important}
:root[data-c=lg] .segn a[aria-current=page]{background:var(--grad);color:#14161A}
:root[data-c=lg] .oc.first{border:2px solid transparent;background:linear-gradient(var(--card),var(--card)) padding-box,var(--grad) border-box}
:root[data-c=lg] .oc.first .oc-h{background:linear-gradient(90deg,#FEF6D8,#F9E5EC)}
:root[data-c=lg] .oc-btn{background:var(--grad);color:#14161A!important}
.lgbtn.bl,:root[data-c=lg] .oc-btn.bl{background:#F5C518;color:#14161A!important}.lgbtn.bg,:root[data-c=lg] .oc-btn.bg{background:#C65B7C;color:#fff!important}
@media (prefers-color-scheme:dark){:root[data-c=lg]:not([data-theme=light]) .oc.first .oc-h{background:linear-gradient(90deg,#3a3110,#3a1f29)}}
:root[data-c=lg][data-theme=dark] .oc.first .oc-h{background:linear-gradient(90deg,#3a3110,#3a1f29)}
.lg{position:relative;flex:0 0 auto;width:30px;height:30px;border-radius:8px;background:#fff;border:1px solid var(--line);display:inline-flex;align-items:center;justify-content:center;font:700 13px 'Schibsted Grotesk',sans-serif;color:#14161A;overflow:hidden}
.lg img{position:absolute;inset:3px;width:calc(100% - 6px);height:calc(100% - 6px);object-fit:contain;background:#fff}
.pk .op{display:flex;align-items:center;gap:8px}
.seg{display:flex;background:var(--soft);border-radius:12px;padding:4px}
.segn a{font:600 15px 'Schibsted Grotesk',sans-serif;padding:10px 20px;border-radius:9px;color:var(--ink);text-decoration:none}
.segn a[aria-current=page]{background:var(--accbg);color:#fff}
@media (max-width:520px){.segn a{padding:10px 11px;font-size:14px}}
:root[data-c=lg]{--acc:#F5C518;--accbg:#F5C518;--accbar:#F5C518}
.flt{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:6px 0 10px}.flt button{font:600 14px 'Schibsted Grotesk',sans-serif;padding:7px 12px;border-radius:8px;border:1px solid var(--bd);background:transparent;color:var(--ink);cursor:pointer}.flt button[aria-pressed=true]{background:var(--ink);color:var(--bg);border-color:var(--ink)}.flt label{font-size:14px;display:flex;gap:6px;align-items:center;margin-left:4px}
.ar{display:inline-block;font-size:11.5px;font-weight:700;background:var(--soft);border:1px solid var(--line);border-radius:6px;padding:0 6px;margin-right:4px;color:var(--ink2)}.pk tr[hidden]{display:none}
.xs{border:2px solid var(--acc)}.xs .rw{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:10px}
.xs .bx{background:var(--soft);border-radius:14px;padding:14px}.xs .bx .l{font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:var(--mut)}
.xs .bx strong{display:block;font-size:24px;margin:4px 0}.xs .bx span{font-size:13.5px;color:var(--ink2)}
.xs .cta{display:flex;gap:10px;flex-wrap:wrap;margin-top:14px}.xs .cta a{font:700 14px 'Schibsted Grotesk',sans-serif;padding:10px 14px;border-radius:9px;text-decoration:none;background:var(--ink);color:var(--bg)}
.xs .cta a+a{background:transparent;color:var(--ink);border:1px solid var(--bd)}
@media (max-width:520px){.xs .rw{grid-template-columns:1fr}}
:root[data-c=net]{--acc:#2E9BE6;--accbg:#2E9BE6;--accbar:#2E9BE6;--first:#E3F1FB}
:root[data-c=net] .w-luce,:root[data-c=net] .w-gas{color:var(--ink)}
@media (prefers-color-scheme:dark){:root[data-c=net]:not([data-theme=light]){--acc:#5AB4F0;--first:#14283a}}
:root[data-c=net][data-theme=dark]{--acc:#5AB4F0;--first:#14283a}
.pk{width:100%;border-collapse:collapse;font-size:14.5px}.pk th{font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:var(--mut);text-align:left;padding:10px 8px;border-bottom:1px solid var(--line)}
.pk td{padding:12px 8px;border-bottom:1px solid var(--line);vertical-align:top}.pk td.n{text-align:right;white-space:nowrap;font-variant-numeric:proportional-nums}
.pk tr.first td{background:var(--first)}.pk .op{font-weight:700}.pk .nt{font-size:12.5px;color:var(--mut);margin-top:4px;max-width:46ch;white-space:normal;overflow:visible;text-overflow:clip}.pk td{font-variant-numeric:proportional-nums}
.pk .tot{font-weight:800;font-size:17px}.pk a{color:var(--ink)}
.inp{display:flex;flex-wrap:wrap;gap:12px 24px;align-items:center;margin:4px 0 0}.inp label{display:flex;align-items:center;gap:8px;font-weight:600}
.inp input[type=number]{width:96px;font:600 16px 'Schibsted Grotesk',sans-serif;padding:8px 10px;border:1px solid var(--bd);border-radius:10px;background:var(--card);color:var(--ink)}
.best2{display:grid;gap:4px;margin-top:6px}.best2 strong{font-size:22px}
.txt{margin-top:16px}.txt h2{margin:0 0 8px;font-size:22px}.txt p{margin:10px 0 0;line-height:1.55;max-width:72ch}
.pg .card+.card{margin-top:16px}
@media (max-width:520px){.pg h1{font-size:30px}}
@media (max-width:640px){
.pk thead{display:none}.pk,.pk tbody{display:block}
.pk tr{display:grid;grid-template-columns:1fr auto;gap:6px 14px;padding:14px 2px;border-bottom:1px solid var(--line)}
.pk tr.first{background:var(--first);border-radius:12px;padding:14px 12px}.pk tr.first td{background:none}
.pk td{display:block;padding:0;border:0}.pk td.n{text-align:right}
.pk .c-pos{display:none}.pk .c-op{grid-column:1}.pk .c-pr{grid-column:2;grid-row:1}
.pk .c-x{grid-column:1/-1;font-size:13.5px;color:var(--ink2);text-align:left!important}
.pk .c-x[data-l]::before{content:attr(data-l) ": ";color:var(--mut)}
}
"""


def testata(path, title, desc, c, icon):
    s = testa
    on = lambda k: ' aria-current="page"' if k == c else ""
    nav = (f'<nav class="seg segn" aria-label="Confronti"><a class="t-luce" href="/"{on("luce")}>Luce</a><a class="t-gas" href="/#gas"{on("gas")}>Gas</a>'
           f'<a class="t-lg" href="/luce-e-gas/"{on("lg")}>Luce + gas</a><a class="t-net" href="/internet/"{on("net")}>Internet</a></nav>')
    s = s.replace('<a class="theme-btn" href="/" style="text-decoration:none">Confronta offerte</a>', nav)
    s = re.sub(r'<html lang="it" data-c="[^"]*">', f'<html lang="it" data-c="{c}">', s)
    s = re.sub(r"<title>.*?</title>", f"<title>{H.escape(title, quote=False)}</title>", s)
    for k in ('name="description"', 'property="og:description"'):
        s = re.sub(rf'(<meta {k} content=")[^"]*', lambda m: m.group(1) + H.escape(desc), s)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + H.escape(title), s)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + BASE + path, s)
    s = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + BASE + path, s)
    s = re.sub(r'(<link rel="icon" href=")[^"]*', lambda m: m.group(1) + icon, s)
    s = s.replace("\n</style>", "\n" + CSS_NET + "</style>", 1)
    if c in ("net", "lg"):
        s = re.sub(r'(<img class="geco [^>]*>)+',
                   f'<img class="geco ic-bolt" src="/img/geco-{c}.svg" width="40" height="40" alt=""><img class="geco ic-bolt dk" src="/img/geco-{c}-dark.svg" width="40" height="40" alt="">', s, count=1)
    return s


def scrivi(path, corpo, script=""):
    out = R / path.strip("/") / "index.html"
    out.parent.mkdir(exist_ok=True)
    js = f"<script>\n(function(){{\nvar $=function(id){{return document.getElementById(id)}};\ndocument.addEventListener('error',function(e){{var t=e.target;if(t&&t.tagName==='IMG'&&t.closest('.lg,.lgb'))t.remove()}},true);\n['click','auxclick','contextmenu'].forEach(function(ev){{document.addEventListener(ev,function(e){{var a=e.target.closest&&e.target.closest('a[href^=http]');if(!a||a.dataset.u)return;a.dataset.u=1;try{{var x=new URL(a.href);if(/comparaoffertelucegas|ilportaleofferte/.test(x.hostname))return;x.searchParams.set('utm_source','comparaoffertelucegas.it');x.searchParams.set('utm_medium','referral');x.searchParams.set('utm_campaign',location.pathname.replace(/\\//g,'')||'home');a.href=x.toString()}}catch(_){{}}}},true)}});\n{tema}\n{script}\n}})();\n</script>\n"
    out.write_text(corpo + "</main>" + piede + js + "</body>\n</html>\n", encoding="utf-8")


# ---------- luce + gas ----------
LG_JS = r"""
var num=function(n,d){return n.toLocaleString('it-IT',{minimumFractionDigits:d,maximumFractionDigits:d})};
var eur=function(n){return num(n,2)+' €'};
var esc=function(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})};
var safe=function(u){return /^https:\/\//.test(u||'')?u:null};
var big=function(v){var c=Math.round(v*100);return '<strong>'+Math.floor(c/100)+'</strong><span>,'+String(c%100).padStart(2,'0')+' €/mese</span>'};
var logoB=function(o){var d=o.lg&&/^[a-z0-9.-]+$/.test(o.lg)?o.lg:null;return '<span class="lgb" aria-hidden="true">'+esc((o.v||'?').charAt(0).toUpperCase())+(d?'<img src="/img/loghi/'+d+'.png" alt="" loading="lazy">':'')+'</span>'};
function accLuce(y,al){var m=y/12,e=m<=220?Math.min(m,150):Math.max(0,150-(m-220));return (m-e)*12*al}
function costo(o,c,y,R){var r=R[c],acc=c==='luce'?accLuce(y,r.acc):0;return (1+r.iva)*(o.fx+o.p*y-(o.s||0)+r.rf+r.rv*y+acc)/12}
var D={};
function render(){
  var yl=Math.max(0,+$('ql').value||0)*12,yg=Math.max(0,+$('qg').value||0)*12,rai=$('rai').checked?90/12:0;
  var R=D.dual.reg;
  var ok=function(o,y){return o.ok!==false&&!(o.min!=null&&y<o.min||o.max!=null&&y>o.max)};
  var rows=D.dual.offerte.map(function(o){var l=costo(o.l,'luce',yl,R)+rai,g=costo(o.g,'gas',yg,R);return {o:o,l:l,g:g,t:l+g,k:'c'}});
  var bestBy=function(d,c,y){var m={};d.offerte.forEach(function(o){if(!ok(o,y))return;var x=costo(o,c,y,R);if(!m[o.v]||x<m[o.v].x)m[o.v]={o:o,x:x}});return m};
  var ML=bestBy(D.luce,'luce',yl),MG=bestBy(D.gas,'gas',yg);
  Object.keys(ML).forEach(function(v){if(!MG[v])return;var L=ML[v].o,G=MG[v].o,l=ML[v].x+rai,g=MG[v].x;
    rows.push({k:'s',l:l,g:g,t:l+g,o:{v:v,n:'Luce: '+L.n+' · Gas: '+G.n,u:null,t:L.t==='f'&&G.t==='f'?'f':'v',d:Math.min(L.d||0,G.d||0),pen:L.pen||G.pen,lg:L.lg||G.lg,l:{pd:L.pd!=null?L.pd:L.p},g:{pd:G.pd!=null?G.pd:G.p},L:L,G:G}})});
  rows.sort(function(a,b){return a.t-b.t});
  function migliore(d,c,y){var b=null;d.offerte.forEach(function(o){if(o.ok===false)return;if(o.min!=null&&y<o.min||o.max!=null&&y>o.max)return;var x=costo(o,c,y,R);if(!b||x<b.x)b={o:o,x:x}});return b}
  var bl=migliore(D.luce,'luce',yl),bg=migliore(D.gas,'gas',yg);
  if(bl&&bg){var sep=bl.x+rai+bg.x,pk=rows[0],vince=!pk||sep<=pk.t,lnk=function(o,t,c){var u=safe(o.u)||safe(o.us),k=/luce$/.test(t)?' bl':/gas$/.test(t)?' bg':'';return u?'<a class="lgbtn'+k+'" href="'+esc(u)+'" target="_blank" rel="nofollow noopener">'+t+'</a>':'<a class="lgbtn'+k+'" href="/?q='+encodeURIComponent(o.v)+'#'+(c||'luce')+'">'+t+'</a>'};
    var riga=function(k,x,o){return '<div class="lgr1"><span class="k">'+k+'</span><span class="lgl">'+logoB(o)+'<span><strong>'+esc(o.v)+'</strong><br>'+esc(o.n)+'</span></span><span class="lgp">'+eur(x)+'</span></div>'};
    $('best').innerHTML=vince
      ?'<div class="lbk">La soluzione più conveniente oggi</div><div class="lbt">Luce e gas da due fornitori diversi</div><div class="lbm">'+big(sep)+'</div>'+riga('Luce',bl.x+rai,bl.o)+riga('Gas',bg.x,bg.o)
        +(pk?'<div class="lbs">Risparmi '+eur(pk.t-sep)+' al mese rispetto al miglior fornitore unico per luce e gas ('+esc(pk.o.v)+', '+eur(pk.t)+')</div>':'')+'<div class="lbb">'+lnk(bl.o,'Offerta luce','luce')+lnk(bg.o,'Offerta gas','gas')+'</div>'
      :'<div class="lbk">La soluzione più conveniente oggi</div><div class="lbt">Luce e gas con '+esc(pk.o.v)+'</div><div class="lbm">'+big(pk.t)+'</div>'+riga('Pacchetto',pk.t,pk.o)
        +'<div class="lbs">Risparmi '+eur(sep-pk.t)+' al mese rispetto a luce e gas da fornitori diversi ('+eur(sep)+')</div><div class="lbb">'+(pk.k==='s'?lnk(pk.o.L,'Offerta luce','luce')+lnk(pk.o.G,'Offerta gas','gas'):lnk(pk.o,'Vai all\'offerta'))+'</div>'}
  var stab=function(o){return o.t!=='f'?'D':(o.d>=36&&o.d<99?'A':o.d>=24&&o.d<99?'B':'C')};
  var bt=function(o,t,c){var u=safe(o.u)||safe(o.us),k=/luce$/.test(t)?' bl':/gas$/.test(t)?' bg':'';return '<a class="oc-btn'+k+'" href="'+(u?esc(u)+'" target="_blank" rel="nofollow noopener':'/?q='+encodeURIComponent(o.v)+'#'+c)+'">'+t+'</a>'};
  var h='',top=rows.length?rows[0].t:0;
  rows.forEach(function(x,i){var o=x.o,u=safe(o.u),tipo=o.t==='f'?'Fisso'+(o.d>=12&&o.d<99?' · '+(o.d%12?o.d+' mesi':o.d/12+(o.d===12?' anno':' anni')):''):'Variabile';
    h+='<article class="oc'+(i===0?' first':'')+'"><div class="oc-h"><span class="oc-n">'+(i+1)+'</span>'+logoB(o)+'<div class="oc-t"><div class="oc-v">'+esc(o.v)+'</div><div class="oc-o">'+(u?'<a href="'+esc(u)+'" target="_blank" rel="nofollow noopener">'+esc(o.n)+'</a>':esc(o.n))+'</div></div>'
     +'<div class="oc-tg"><span class="tg '+(o.t==='f'?'tg-f':'tg-v')+'">'+tipo+'</span><span class="tg st-'+stab(o)+'">Stabilità '+stab(o)+'</span>'+(x.k==='c'?'<span class="tg tg-s" title="Un unico contratto per luce e gas">Offerta congiunta</span>':'<span class="tg tg-s" title="Due contratti separati con lo stesso fornitore">Due contratti</span>')+(o.pen?'<span class="tg tg-w">Penale di uscita</span>':'')+'</div></div>'
     +'<div class="oc-b"><dl class="oc-d"><div><dt>Luce</dt><dd>'+eur(x.l)+' al mese</dd></div><div><dt>Gas</dt><dd>'+eur(x.g)+' al mese</dd></div><div><dt>Energia luce</dt><dd>'+num(o.l.pd,4)+' €/kWh</dd></div><div><dt>Energia gas</dt><dd>'+num(o.g.pd,4)+' €/Smc</dd></div></dl>'
     +'<div class="oc-p"><div class="oc-m">'+big(x.t)+'</div><div class="oc-y">luce + gas</div>'+(i===0?'<div class="oc-dd top1">La più conveniente</div>':'<div class="oc-dd">+'+eur(x.t-top)+' al mese</div>')+'</div>'
     +'<div class="oc-a">'+(x.k==='s'?bt(o.L,'Offerta luce','luce')+bt(o.G,'Offerta gas','gas'):bt(o,'Vai all\'offerta','luce'))+'</div></div></article>'});
  $('tab').innerHTML=h;
  var nc=rows.filter(function(x){return x.k==='c'}).length;$('cnt').textContent=(rows.length-nc)+' fornitori con luce e gas, '+nc+' offerte congiunte';
}
Promise.all(['dual','luce','gas'].map(function(k){return fetch('/data/'+k+'.json',{cache:'no-cache'}).then(function(r){return r.json()})})).then(function(a){D.dual=a[0];D.luce=a[1];D.gas=a[2];
  ['ql','qg','rai'].forEach(function(id){$(id).addEventListener('input',render)});
  document.querySelectorAll('.pm').forEach(function(b){b.addEventListener('click',function(){var i=$(b.dataset.t);i.value=Math.max(0,(+i.value||0)+(+b.dataset.d));render()})});
  var PF={1:[125,40],2:[185,75],4:[270,115]};document.querySelectorAll('[data-pf]').forEach(function(b){b.addEventListener('click',function(){$('ql').value=PF[b.dataset.pf][0];$('qg').value=PF[b.dataset.pf][1];render()})});render();
  $('fsrc').textContent='Fonte: ARERA, Portale Offerte, open data del '+D.dual.data_open_data.split('-').reverse().join('/')+'.'});
"""

corpo = testata("/luce-e-gas/", "Offerte luce e gas insieme: pacchetti a confronto",
                "Le offerte luce e gas in un unico contratto dagli open data ARERA, con la spesa sui tuoi consumi e il confronto con le migliori offerte separate.",
                "lg", "/img/geco-lg.svg")
corpo += """<main class="wrap pg">
<h1 class="h">Offerte luce e gas insieme</h1>
<section class="lgh">
<div class="card lga"><h2 class="h">I tuoi consumi al mese</h2>
<div class="lgq"><label for="ql">Luce</label><div class="lgst"><button type="button" class="pm" data-t="ql" data-d="-10" aria-label="Diminuisci il consumo di luce">−</button><div class="lgv"><input type="number" id="ql" value="225" min="0" step="10" inputmode="numeric"><span>kWh</span></div><button type="button" class="pm" data-t="ql" data-d="10" aria-label="Aumenta il consumo di luce">+</button></div></div>
<div class="lgq"><label for="qg">Gas</label><div class="lgst"><button type="button" class="pm" data-t="qg" data-d="-5" aria-label="Diminuisci il consumo di gas">−</button><div class="lgv"><input type="number" id="qg" value="90" min="0" step="5" inputmode="numeric"><span>Smc</span></div><button type="button" class="pm" data-t="qg" data-d="5" aria-label="Aumenta il consumo di gas">+</button></div></div>
<div class="prof" role="group" aria-label="Consumo tipo"><span>Non hai la bolletta?</span><button type="button" data-pf="1">Single</button><button type="button" data-pf="2">Coppia</button><button type="button" data-pf="4">Famiglia di 4</button></div>
<label class="lgr"><input type="checkbox" id="rai" checked> Canone RAI <span>(90 €/anno)</span></label>
<p class="src">Cliente residente, contatore da 3 kW. Spesa con imposte, stimata come nella <a href="/">classifica principale</a>.</p></div>
<div class="lgb1" id="best" aria-live="polite">Caricamento offerte…</div>
</section>
<section class="card"><h2 class="h" style="margin:0 0 8px;font-size:22px">Luce e gas con un solo fornitore <span class="src" id="cnt"></span></h2>
<div id="tab"></div></section>
<section class="card txt"><h2 class="h">Conviene il pacchetto unico?</h2>
<p>Un'offerta dual lega luce e gas allo stesso venditore: una sola bolletta e, a volte, uno sconto. Non è detto che costi meno di due offerte separate scelte ciascuna al prezzo più basso, per questo le mettiamo a confronto qui sopra.</p>
<p>Se un domani vuoi cambiare solo la luce o solo il gas, controlla nella scheda dell'offerta se lo sconto del pacchetto si perde.</p></section>
"""
scrivi("/luce-e-gas/", corpo, LG_JS)

# ---------- internet ----------
net = json.loads((R / "data" / "internet.json").read_text(encoding="utf-8"))
e = lambda s: H.escape(str(s), quote=True)


def logo(nome, url, cls="lg"):
    from urllib.parse import urlparse
    d = ".".join(urlparse(url or "").netloc.lower().split(".")[-2:]) if url else ""
    img = f'<img src="/img/loghi/{e(d)}.png" alt="" loading="lazy">' if d and (R / "img" / "loghi" / f"{d}.png").exists() else ""
    return f'<span class="{cls}" aria-hidden="true">{e(nome.strip()[:1].upper())}{img}</span>'
n2 = lambda v: f"{v:.2f}".replace(".", ",") + " €" if v is not None else "—"
ver = net["verificato"].split("-")
ver = f"{int(ver[2])}/{ver[1]}/{ver[0]}"
import datetime as _dt
auto = json.loads((R / "data" / "internet_auto.json").read_text(encoding="utf-8"))
fresco = lambda x: not x.get("letto") or (_dt.date.fromisoformat(net["verificato"]) - _dt.date.fromisoformat(x["letto"])).days <= 7
righe = sorted([x for x in net["internet"] + [a for a in auto if not a["bundle"]] if fresco(x)], key=lambda x: x["prezzo_mese"])
net["bundle"] = net["bundle"] + [{"fornitore": a["operatore"], "offerta": a["offerta"], "vantaggio": a["nota"], "prezzo_fibra_mese": a["prezzo_mese"], "url": a["url"], "nota": (f"Poi {a['prezzo_dopo']:.2f} €".replace(".", ",") + (f" dopo {a['mesi_promo']} mesi." if a.get("mesi_promo") else ".")) if a.get("prezzo_dopo") and a["prezzo_dopo"] != a["prezzo_mese"] else ""} for a in auto if a["bundle"] and fresco(a)]
vecchio = lambda x: x.get("letto") and x["letto"] < net["verificato"]
dl = lambda x: f' Prezzo letto il {int(x["letto"][8:])}/{x["letto"][5:7]}.' if vecchio(x) else ""
def eur_big(v):
    c = round(v * 100)
    return f'<strong>{c // 100}</strong><span>,{c % 100:02d} €/mese</span>'


def scheda(x, i, top, bundle=False):
    nome = f'<a href="{e(x["url"])}" target="_blank" rel="nofollow noopener">{e(x["offerta"])}</a>' if x.get("url") else e(x["offerta"])
    op = x.get("operatore") or x.get("fornitore")
    pm = x.get("prezzo_mese", x.get("prezzo_fibra_mese"))
    tec = (x.get("tecnologia") or "").upper()
    cat = "fwa" if "FWA" in tec else "ftth" if "FTTH" in tec else "altro"
    tags = (f'<span class="tg tg-{cat}">{e(x["tecnologia"])}</span>' if x.get("tecnologia") else "") + (f'<span class="tg tg-s">Solo {e(x["area"])}</span>' if x.get("area") else "")
    dati = []
    if x.get("velocita"): dati.append(("Velocità", e(x["velocita"]), ""))
    if x.get("attivazione") is not None: dati.append(("Attivazione", n2(x["attivazione"]), ""))
    if x.get("modem"): dati.append(("Modem", e(x["modem"]), ""))
    if bundle and x.get("vantaggio"): dati.append(("Vantaggio", e(x["vantaggio"]), "w"))
    if x.get("nota"): dati.append(("Condizioni", e(x["nota"][:1].upper()+x["nota"][1:]) + dl(x), "w"))
    dd = "".join(f'<div class="{w}"><dt>{k}</dt><dd{" class=nt" if k in ("Condizioni", "Vantaggio") else ""}>{v}</dd></div>' for k, v, w in dati)
    dopo = (f'poi {n2(x["prezzo_dopo"])}' + (f' dopo {x["mesi_promo"]} mesi' if x.get("mesi_promo") else "")) if x.get("prezzo_dopo") and x["prezzo_dopo"] != pm else ""
    diff = "" if bundle else ('<div class="oc-dd top1">Il canone più basso</div>' if i == 0 else f'<div class="oc-dd">+{n2(pm - top)} al mese</div>')
    btn = f'<a class="oc-btn" href="{e(x["url"])}" target="_blank" rel="nofollow noopener">Vai all\'offerta</a>' if x.get("url") else ""
    num = "" if bundle else f'<span class="oc-n">{i + 1}</span>'
    first = " first" if (i == 0 and not bundle) else ""
    return (f'<article class="oc{first}" data-cat="{cat}" data-reg="{1 if x.get("area") else 0}"><div class="oc-h">{num}{logo(op, x.get("url"), "lgb")}'
            f'<div class="oc-t"><div class="oc-v">{e(op)}</div><div class="oc-o">{nome}</div></div><div class="oc-tg">{tags}</div></div>'
            f'<div class="oc-b"><dl class="oc-d">{dd}</dl><div class="oc-p"><div class="oc-m">{eur_big(pm)}</div>'
            f'{f"<div class=oc-y>{dopo}</div>" if dopo else ""}{diff}</div><div class="oc-a">{btn}</div></div></article>')


top = righe[0]["prezzo_mese"] if righe else 0
tr = [scheda(x, i, top) for i, x in enumerate(righe)]
bt = [scheda(x, 0, 0, bundle=True) for x in sorted(net["bundle"], key=lambda b: b["prezzo_fibra_mese"])]

corpo = testata("/internet/", "Offerte fibra e internet casa a confronto",
                "Le offerte fibra per la casa dei principali operatori, ordinate per canone mensile, e i pacchetti energia più internet dei fornitori di luce e gas.",
                "net", "/img/geco-net.svg")
corpo += f"""<main class="wrap pg">
<h1 class="h">Offerte fibra e internet casa</h1>
<section class="card"><h2 class="h" style="margin:0 0 8px;font-size:22px">Internet casa, dal canone più basso <span class="src" id="ncnt"></span></h2>
<div class="flt" role="group" aria-label="Filtra"><button type="button" data-t="tutte" aria-pressed="true">Tutte</button><button type="button" data-t="ftth" aria-pressed="false">Fibra FTTH</button><button type="button" data-t="fwa" aria-pressed="false">FWA senza linea</button><label><input type="checkbox" id="noreg"> Nascondi offerte regionali</label></div>
<div id="nt">
{''.join(tr)}
</div>
<p class="src">Prezzi letti ogni giorno in automatico dalle pagine ufficiali degli operatori, ultimo controllo il {ver}. Velocità e tecnologia dipendono dalla copertura del tuo indirizzo: verificala sul sito dell'operatore prima di attivare.</p></section>
<section class="card xs"><h2 class="h" style="margin:0 0 4px;font-size:22px">Quanto spenderesti oggi per luce e gas</h2>
<p class="src" style="margin:0">Le offerte più convenienti di oggi per una casa con 225 kWh di luce e 90 Smc di gas al mese, imposte e canone RAI inclusi.</p>
<div class="rw"><div class="bx"><div class="l">Luce</div><strong id="xl">—</strong><span id="xln"></span></div><div class="bx"><div class="l">Gas</div><strong id="xg">—</strong><span id="xgn"></span></div></div>
<div class="cta"><a href="/">Confronta la luce</a><a href="/#gas">Confronta il gas</a><a href="/luce-e-gas/">Pacchetti luce + gas</a></div></section>
<section class="card"><h2 class="h" style="margin:0 0 8px;font-size:22px">Pacchetti energia + internet</h2>
<div>
{''.join(bt)}
</div>
<p class="src">Il prezzo della luce e del gas di questi fornitori lo trovi nella <a href="/">classifica luce e gas</a>.</p></section>
<section class="card txt"><h2 class="h">Come leggere il confronto</h2>
<p>Per luce e gas usiamo gli open data ufficiali di ARERA. Per internet non esiste una banca dati pubblica delle offerte: ogni mattina leggiamo i prezzi direttamente dalle pagine degli operatori. Prima di attivare, controlla comunque prezzo e condizioni sulla pagina dell'offerta.</p>
<p>Oltre al canone guarda tre cose: quanto dura il prezzo promozionale, il costo di attivazione e quanto paghi se disdici prima del vincolo.</p></section>
"""
NET_JS = r"""
var T='tutte';function flt(){var n=0,rr=document.querySelectorAll('#nt article');rr.forEach(function(r){var ok=(T==='tutte'||r.dataset.cat===T)&&!($('noreg').checked&&r.dataset.reg==='1');r.hidden=!ok;if(ok)n++});$('ncnt').textContent=n+' offerte';document.querySelectorAll('.flt button').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.t===T)})}
document.querySelectorAll('.flt button').forEach(function(b){b.addEventListener('click',function(){T=b.dataset.t;flt()})});$('noreg').addEventListener('change',flt);flt();
var eur=function(n){return n.toLocaleString('it-IT',{minimumFractionDigits:2,maximumFractionDigits:2})+' € al mese'};
fetch('/data/top.json',{cache:'no-cache'}).then(function(r){return r.json()}).then(function(d){
  var l=d.luce[0],g=d.gas[0];$('xl').textContent=eur(l.m);$('xln').textContent=l.v+', '+l.n;$('xg').textContent=eur(g.m);$('xgn').textContent=g.v+', '+g.n;});
"""
scrivi("/internet/", corpo, NET_JS)
print("pagine generate")


# ---------- classifiche per ricerca (pagine statiche, rigenerate a ogni aggiornamento) ----------
TIPO_Y = {"luce": 2700, "gas": 1080}
U = {"luce": "kWh", "gas": "Smc"}
CSS_CL = """.tg-g{background:#D1FAE5;color:#065F46}.tg-p{background:#E7E9E4;color:#3A3F47}
.intro{font-size:16.5px;line-height:1.55;color:var(--ink2);max-width:72ch;margin:6px 0 0}.intro strong{color:var(--ink)}
.cta1{display:inline-flex;margin-top:14px;background:var(--accbg);color:#14161A;font:800 15px 'Schibsted Grotesk',sans-serif;padding:13px 18px;border-radius:12px;text-decoration:none}
html[data-c=gas] .cta1{color:#fff}.cta1{width:max-content;max-width:100%;align-self:flex-start}.cta1+.card{margin-top:16px}.cta1:hover{filter:brightness(.94)}
.altre{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}.altre a{border:1px solid var(--bd);border-radius:99px;padding:9px 14px;font-weight:600;font-size:14px;color:var(--ink);text-decoration:none}.altre a:hover{border-color:var(--ink)}
"""


def spesa(o, c, reg):
    y = TIPO_Y[c]
    if c == "luce":
        m = y / 12
        e = min(m, 150) if m <= 220 else max(0, 150 - (m - 220))
        acc = (m - e) * 12 * reg["acc"]
    else:
        acc = 0 if y <= reg["accSoglia"] else reg["accRif"] * y
    a = (1 + reg["iva"]) * (o["fx"] + o["p"] * y - (o.get("s") or 0) + reg["rf"] + reg["rv"] * y + acc)
    return a / 12 + (90 / 12 if c == "luce" else 0)


def stab(o):
    if o["t"] != "f":
        return "D"
    d = o.get("d") or 0
    return "A" if 36 <= d < 99 else "B" if 24 <= d < 99 else "C"


def durata(o):
    d = o.get("d") or 0
    if o["t"] != "f":
        return "Variabile"
    if 12 <= d < 99:
        return "Fisso · " + (f"{d} mesi" if d % 12 else f"{d // 12} anno" if d == 12 else f"{d // 12} anni")
    return "Fisso"


def link_ok(u):
    u = (u or "").strip()
    if u and not re.match(r"^https?://", u, re.I):
        u = "https://" + u
    return u if re.match(r"^https?://[^\s\"'<>]+$", u) else None


def scheda_en(x, i, top, c):
    o, m = x
    e = lambda s: H.escape(str(s))
    lg = o.get("lg") if re.match(r"^[a-z0-9.-]+$", o.get("lg") or "") else None
    logo_ = f'<span class="lgb" aria-hidden="true">{e((o["v"] or "?").strip()[:1].upper())}' + (f'<img src="/img/loghi/{lg}.png" alt="" loading="lazy">' if lg else "") + "</span>"
    s = stab(o)
    tags = (f'<span class="tg {"tg-f" if o["t"] == "f" else "tg-v"}">{durata(o)}</span><span class="tg st-{s}">Stabilità {s}</span>'
            + ('<span class="tg tg-g">Verde</span>' if o.get("vd") else "") + ('<span class="tg tg-p">PLACET</span>' if o.get("pl") else "")
            + ('<span class="tg tg-w">Penale di uscita</span>' if o.get("pen") else ""))
    pd = o["pd"] if o.get("pd") is not None else o["p"]
    dd = (f'<div><dt>Energia</dt><dd>{n4(pd)} €/{U[c]}</dd></div><div><dt>Quota fissa</dt><dd>{n2(o["fx"] / 12)} al mese</dd></div>'
          + (f'<div><dt>Offerta valida fino al</dt><dd>{"/".join(reversed(o["sc"][:10].split("-")))}</dd></div>' if o.get("sc") else ""))
    u, us = link_ok(o.get("u")), link_ok(o.get("us"))
    btn = (f'<a class="oc-btn" href="{e(u)}" target="_blank" rel="nofollow noopener">Vai all\'offerta</a>' if u else
           f'<a class="oc-btn" href="{e(us)}" target="_blank" rel="nofollow noopener">Sito del fornitore</a>' if us else
           '<a class="oc-btn" href="https://www.ilportaleofferte.it/portaleOfferte/" target="_blank" rel="noopener">Portale ARERA</a>')
    diff = '<div class="oc-dd top1">La più conveniente</div>' if i == 0 else f'<div class="oc-dd">+{n2(m - top)} al mese</div>'
    return (f'<article class="oc{" first" if i == 0 else ""}"><div class="oc-h"><span class="oc-n">{i + 1}</span>{logo_}'
            f'<div class="oc-t"><div class="oc-v">{e(o["v"])}</div><div class="oc-o">{e(o["n"])}</div></div><div class="oc-tg">{tags}</div></div>'
            f'<div class="oc-b"><dl class="oc-d">{dd}</dl><div class="oc-p"><div class="oc-m">{eur_big(m)}</div><div class="oc-y">{n0(m * 12)} l\'anno</div>{diff}</div>'
            f'<div class="oc-a">{btn}</div></div></article>')


def n2(v):
    return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") + " €"


def n0(v):
    return f"{v:,.0f}".replace(",", ".") + " €"


def n4(v):
    return f"{v:.4f}".replace(".", ",")


CLASSIFICHE = [
    ("offerte-luce-prezzo-fisso", "luce", lambda o: o["t"] == "f", "f=f", "Offerte luce a prezzo fisso",
     "a prezzo fisso",
     ["Con un'offerta a prezzo fisso il costo dell'energia resta uguale per la durata scritta nel contratto, di solito 12, 24 o 36 mesi. Le altre voci della bolletta (trasporto, oneri di sistema e imposte) le decidono ARERA e lo Stato e possono cambiare.",
      "Prima della scadenza il venditore deve mandarti le nuove condizioni con almeno tre mesi di anticipo. Se non scegli un'altra offerta, passi al nuovo prezzo: segna la data e confronta di nuovo."]),
    ("offerte-gas-prezzo-fisso", "gas", lambda o: o["t"] == "f", "c=gas&f=f", "Offerte gas a prezzo fisso",
     "a prezzo fisso",
     ["Con un'offerta a prezzo fisso il costo del gas al metro cubo (Smc) resta uguale per la durata scritta nel contratto, di solito 12, 24 o 36 mesi. Trasporto, oneri e imposte li decidono ARERA e lo Stato e possono cambiare.",
      "Il prezzo fisso conta di più d'inverno, quando con il riscaldamento si consuma gran parte del gas dell'anno."]),
    ("offerte-luce-variabili", "luce", lambda o: o["t"] != "f", "f=v", "Offerte luce a prezzo variabile",
     "a prezzo variabile",
     ["Il prezzo segue ogni mese il PUN, il prezzo all'ingrosso dell'elettricità, più uno spread del venditore che resta fisso. Per stimare la spesa usiamo le quotazioni del PUN per i prossimi 12 mesi: se il mercato scende paghi meno, se sale paghi di più.",
      'Il valore di oggi e l\'andamento degli ultimi mesi sono nella pagina <a href="/prezzo-energia-oggi/">PUN oggi</a>.']),
    ("offerte-gas-variabili", "gas", lambda o: o["t"] != "f", "c=gas&f=v", "Offerte gas a prezzo variabile",
     "a prezzo variabile",
     ["Il prezzo segue ogni mese il PSV, il prezzo all'ingrosso del gas in Italia, più uno spread del venditore che resta fisso. Per stimare la spesa usiamo le quotazioni del PSV per i prossimi 12 mesi.",
      'Il valore mensile e l\'andamento sono nella pagina <a href="/psv/">prezzo gas PSV</a>.']),
    ("offerte-luce-senza-penale", "luce", lambda o: o.get("pen") is False, "np=1", "Offerte luce senza penale di uscita",
     "senza penale di uscita",
     ["Nel mercato libero puoi cambiare fornitore quando vuoi e il cambio è gratuito. Alcune offerte, di solito a prezzo fisso, chiedono però un costo se esci prima della scadenza.",
      "Qui ci sono solo le offerte che nella scheda ARERA non prevedono questo costo. Prima di firmare controlla comunque le condizioni contrattuali."]),
    ("offerte-gas-senza-penale", "gas", lambda o: o.get("pen") is False, "c=gas&np=1", "Offerte gas senza penale di uscita",
     "senza penale di uscita",
     ["Nel mercato libero puoi cambiare fornitore quando vuoi e il cambio è gratuito. Alcune offerte gas, di solito a prezzo fisso, chiedono però un costo se esci prima della scadenza.",
      "Qui ci sono solo le offerte che nella scheda ARERA non prevedono questo costo. Prima di firmare controlla comunque le condizioni contrattuali."]),
    ("offerte-luce-energia-verde", "luce", lambda o: o.get("vd"), "vd=1", "Offerte luce con energia verde",
     "con energia verde",
     ["Energia verde vuol dire che il venditore copre i tuoi consumi con Garanzie d'Origine, i certificati che attestano la produzione da fonti rinnovabili. Dalla presa esce la stessa corrente di prima: cambia quanta energia rinnovabile il venditore compra per te.",
      "Spesso costa quanto un'offerta normale: confronta il prezzo prima di scegliere."]),
    ("offerte-luce-placet", "luce", lambda o: o.get("pl"), "q=placet", "Offerte luce PLACET",
     "PLACET",
     ["Le offerte PLACET (Prezzo Libero A Condizioni Equiparate di Tutela) hanno le condizioni contrattuali fissate da ARERA, uguali per tutti i venditori. Ogni venditore sceglie solo il prezzo, fisso o variabile, che vale 12 mesi.",
      "Sono utili come riferimento: se un'offerta costa più della PLACET dello stesso venditore, chiediti cosa paghi in più."]),
    ("offerte-gas-placet", "gas", lambda o: o.get("pl"), "c=gas&q=placet", "Offerte gas PLACET",
     "PLACET",
     ["Le offerte PLACET (Prezzo Libero A Condizioni Equiparate di Tutela) hanno le condizioni contrattuali fissate da ARERA, uguali per tutti i venditori. Ogni venditore sceglie solo il prezzo, fisso o variabile, che vale 12 mesi.",
      "Sono utili come riferimento: se un'offerta costa più della PLACET dello stesso venditore, chiediti cosa paghi in più."]),
]

DATI = {c: json.loads((R / "data" / f"{c}.json").read_text(encoding="utf-8")) for c in ("luce", "gas")}
for slug, c, flt, qs, titolo, agg, testo in CLASSIFICHE:
    d = DATI[c]
    y = TIPO_Y[c]
    ok = [o for o in d["offerte"] if o.get("ok", True) and o.get("s") is not None and flt(o)
          and (o.get("min") is None or y >= o["min"]) and (o.get("max") is None or y <= o["max"])]
    righe = sorted(((o, spesa(o, c, d["reg"])) for o in ok), key=lambda x: x[1])
    if not righe:
        continue
    forn = len({o["v"] for o, _ in righe})
    data = "/".join(reversed(d["data_open_data"].split("-")))
    b, bm = righe[0]
    cons = "225 kWh di luce al mese, contatore da 3 kW, imposte e canone RAI inclusi" if c == "luce" else "90 Smc di gas al mese, imposte incluse"
    desc = f"{len(righe)} offerte {c} {agg} di {forn} fornitori, dagli open data ARERA del {data}, ordinate per spesa mensile stimata."
    corpo = testata(f"/{slug}/", f"{titolo}: classifica di oggi", desc, c, f"/img/geco-{c}.svg").replace("</style>", CSS_CL + "</style>", 1)
    ld = {"@context": "https://schema.org", "@type": "ItemList", "name": titolo, "numberOfItems": min(20, len(righe)),
          "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": f'{o["v"]}, {o["n"]}'} for i, (o, _) in enumerate(righe[:20])]}
    corpo = corpo.replace("</head>", '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>\n</head>", 1)
    altre = "".join(f'<a href="/{s2}/">{t2}</a>' for s2, _, _, _, t2, _, _ in CLASSIFICHE if s2 != slug)
    corpo += f"""<main class="wrap pg">
<h1 class="h">{titolo}</h1>
<p class="intro">Oggi ci sono <strong>{len(righe)} offerte {agg}</strong> di {forn} fornitori. Con {cons}, la più conveniente è <strong>{H.escape(b["v"])}</strong> ({H.escape(b["n"])}) a <strong>{n2(bm)} al mese</strong>.</p>
<a class="cta1" href="/?{qs}">Calcola sui tuoi consumi</a>
<section class="card"><h2 class="h" style="margin:0 0 8px;font-size:22px">Le 20 più convenienti</h2>
{''.join(scheda_en(x, i, bm, c) for i, x in enumerate(righe[:20]))}
<p class="src">Open data del Portale Offerte di ARERA del {data}. Spesa stimata per {cons}. Le offerte variabili sono stimate con le quotazioni dei prossimi 12 mesi.</p></section>
<section class="card txt"><h2 class="h">Come funzionano</h2>{''.join(f"<p>{p}</p>" for p in testo)}</section>
<section class="card txt"><h2 class="h">Altre classifiche</h2><div class="altre"><a href="/">Tutte le offerte luce</a><a href="/#gas">Tutte le offerte gas</a>{altre}</div></section>
"""
    scrivi(f"/{slug}/", corpo, "")
print("classifiche generate")
