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

CSS_NET = """.lg{position:relative;flex:0 0 auto;width:30px;height:30px;border-radius:8px;background:#fff;border:1px solid var(--line);display:inline-flex;align-items:center;justify-content:center;font:700 13px 'Schibsted Grotesk',sans-serif;color:#14161A;overflow:hidden}
.lg img{position:absolute;inset:3px;width:calc(100% - 6px);height:calc(100% - 6px);object-fit:contain;background:#fff}
.pk .op{display:flex;align-items:center;gap:8px}
.seg{display:flex;background:var(--soft);border-radius:12px;padding:4px}
.segn a{font:600 15px 'Schibsted Grotesk',sans-serif;padding:10px 20px;border-radius:9px;color:var(--ink);text-decoration:none}
.segn a[aria-current=page]{background:var(--accbg);color:#fff}
@media (max-width:520px){.segn a{padding:10px 11px;font-size:14px}}
:root[data-c=lg]{--acc:#F5C518;--accbg:#F5C518;--accbar:#F5C518}:root[data-c=lg] .segn a[aria-current=page]{color:#14161A}
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
    nav = (f'<nav class="seg segn" aria-label="Confronti"><a href="/"{on("luce")}>Luce</a><a href="/#gas"{on("gas")}>Gas</a>'
           f'<a href="/luce-e-gas/"{on("lg")}>Luce + gas</a><a href="/internet/"{on("net")}>Internet</a></nav>')
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
    if c == "net":
        s = re.sub(r'<img class="geco ic-bolt"[^>]*><img class="geco ic-flame"[^>]*>',
                   '<img class="geco" src="/img/geco-net.svg" width="40" height="40" alt="">', s)
    return s


def scrivi(path, corpo, script=""):
    out = R / path.strip("/") / "index.html"
    out.parent.mkdir(exist_ok=True)
    js = f"<script>\n(function(){{\nvar $=function(id){{return document.getElementById(id)}};\ndocument.addEventListener('error',function(e){{var t=e.target;if(t&&t.tagName==='IMG'&&t.closest('.lg'))t.remove()}},true);\n{tema}\n{script}\n}})();\n</script>\n"
    out.write_text(corpo + "</main>" + piede + js + "</body>\n</html>\n", encoding="utf-8")


# ---------- luce + gas ----------
LG_JS = r"""
var num=function(n,d){return n.toLocaleString('it-IT',{minimumFractionDigits:d,maximumFractionDigits:d})};
var eur=function(n){return num(n,2)+' €'};
var esc=function(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})};
var safe=function(u){return /^https:\/\//.test(u||'')?u:null};
var logo=function(o){var d=o.lg&&/^[a-z0-9.-]+$/.test(o.lg)?o.lg:null;return '<span class="lg" aria-hidden="true">'+esc((o.v||'?').charAt(0).toUpperCase())+(d?'<img src="/img/loghi/'+d+'.ico" alt="" loading="lazy">':'')+'</span>'};
function accLuce(y,al){var m=y/12,e=m<=220?Math.min(m,150):Math.max(0,150-(m-220));return (m-e)*12*al}
function costo(o,c,y,R){var r=R[c],acc=c==='luce'?accLuce(y,r.acc):0;return (1+r.iva)*(o.fx+o.p*y-(o.s||0)+r.rf+r.rv*y+acc)/12}
var D={};
function render(){
  var yl=Math.max(0,+$('ql').value||0)*12,yg=Math.max(0,+$('qg').value||0)*12,rai=$('rai').checked?90/12:0;
  var R=D.dual.reg;
  var rows=D.dual.offerte.map(function(o){var l=costo(o.l,'luce',yl,R)+rai,g=costo(o.g,'gas',yg,R);return {o:o,l:l,g:g,t:l+g}}).sort(function(a,b){return a.t-b.t});
  function migliore(d,c,y){var b=null;d.offerte.forEach(function(o){if(o.ok===false)return;if(o.min!=null&&y<o.min||o.max!=null&&y>o.max)return;var x=costo(o,c,y,R);if(!b||x<b.x)b={o:o,x:x}});return b}
  var bl=migliore(D.luce,'luce',yl),bg=migliore(D.gas,'gas',yg);
  if(bl&&bg){var sep=bl.x+rai+bg.x;$('sep').innerHTML='<strong>'+eur(sep)+' al mese</strong><span>Luce: '+esc(bl.o.v)+', '+esc(bl.o.n)+' ('+eur(bl.x+rai)+')</span><span>Gas: '+esc(bg.o.v)+', '+esc(bg.o.n)+' ('+eur(bg.x)+')</span>'+(rows.length?'<span>'+(rows[0].t>sep?'Conviene più di un pacchetto unico: il più economico ('+esc(rows[0].o.v)+', '+eur(rows[0].t)+') costa '+eur(rows[0].t-sep)+' al mese in più.':'Il pacchetto unico più economico ('+esc(rows[0].o.v)+', '+eur(rows[0].t)+') costa '+eur(sep-rows[0].t)+' al mese in meno: conviene il pacchetto.')+'</span>':'')}
  var h='<thead><tr><th>#</th><th>Fornitore e pacchetto</th><th class="n">Luce</th><th class="n">Gas</th><th class="n">Totale al mese</th></tr></thead><tbody>';
  rows.forEach(function(x,i){var o=x.o,u=safe(o.u),tipo=o.t==='f'?'fisso'+(o.d>=12&&o.d<99?' '+(o.d%12?o.d+' mesi':o.d/12+(o.d===12?' anno':' anni')):''):'variabile';
    h+='<tr'+(i===0?' class="first"':'')+'><td class="c-pos">'+(i+1)+'</td><td class="c-op"><div class="op">'+logo(o)+esc(o.v)+'</div><div>'+(u?'<a href="'+esc(u)+'" target="_blank" rel="nofollow noopener">'+esc(o.n)+'</a>':esc(o.n))+'</div><div class="nt">Prezzo '+tipo+(o.pen?' · costo di uscita anticipata':'')+'</div></td><td class="n c-x" data-l="Luce">'+eur(x.l)+'</td><td class="n c-x" data-l="Gas">'+eur(x.g)+'</td><td class="n tot c-pr">'+eur(x.t)+'</td></tr>'});
  $('tab').innerHTML=h+'</tbody>';
  $('cnt').textContent=rows.length+' pacchetti di '+D.dual.fornitori+' fornitori';
}
Promise.all(['dual','luce','gas'].map(function(k){return fetch('/data/'+k+'.json',{cache:'no-cache'}).then(function(r){return r.json()})})).then(function(a){D.dual=a[0];D.luce=a[1];D.gas=a[2];
  ['ql','qg','rai'].forEach(function(id){$(id).addEventListener('input',render)});render();
  $('fsrc').textContent='Fonte: ARERA, Portale Offerte, open data del '+D.dual.data_open_data.split('-').reverse().join('/')+'.'});
"""

corpo = testata("/luce-e-gas/", "Offerte luce e gas insieme: pacchetti a confronto",
                "Le offerte luce e gas in un unico contratto dagli open data ARERA, con la spesa sui tuoi consumi e il confronto con le migliori offerte separate.",
                "lg", "/img/geco-luce.svg")
corpo += """<main class="wrap pg">
<h1 class="h">Offerte luce e gas insieme</h1>
<section class="card"><h2 class="h" style="margin:0 0 8px;font-size:22px">I tuoi consumi al mese</h2>
<div class="inp"><label>Luce <input type="number" id="ql" value="225" min="0" step="10" inputmode="numeric"> kWh</label><label>Gas <input type="number" id="qg" value="90" min="0" step="5" inputmode="numeric"> Smc</label><label><input type="checkbox" id="rai" checked> Canone RAI</label></div>
<p class="src">Cliente residente, contatore da 3 kW. Spesa con imposte, stimata come nella <a href="/">classifica principale</a>.</p></section>
<section class="card"><h2 class="h" style="margin:0 0 4px;font-size:22px">Luce e gas da fornitori diversi</h2><div class="best2" id="sep">—</div></section>
<section class="card"><h2 class="h" style="margin:0 0 8px;font-size:22px">Pacchetti luce + gas <span class="src" id="cnt"></span></h2>
<div class="scroll" role="region" aria-label="Pacchetti luce e gas" tabindex="0"><table class="pk" id="tab"></table></div></section>
<section class="card txt"><h2 class="h">Conviene il pacchetto unico?</h2>
<p>Un'offerta dual lega luce e gas allo stesso venditore: una sola bolletta e, a volte, uno sconto. Non è detto che costi meno di due offerte separate scelte ciascuna al prezzo più basso, per questo le mettiamo a confronto qui sopra.</p>
<p>Se un domani vuoi cambiare solo la luce o solo il gas, controlla nella scheda dell'offerta se lo sconto del pacchetto si perde.</p></section>
"""
scrivi("/luce-e-gas/", corpo, LG_JS)

# ---------- internet ----------
net = json.loads((R / "data" / "internet.json").read_text(encoding="utf-8"))
e = lambda s: H.escape(str(s), quote=True)


def logo(nome, url):
    from urllib.parse import urlparse
    d = ".".join(urlparse(url or "").netloc.lower().split(".")[-2:]) if url else ""
    img = f'<img src="/img/loghi/{e(d)}.ico" alt="" loading="lazy">' if d and (R / "img" / "loghi" / f"{d}.ico").exists() else ""
    return f'<span class="lg" aria-hidden="true">{e(nome.strip()[:1].upper())}{img}</span>'
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
tr = []
for i, x in enumerate(righe):
    nome = f'<a href="{e(x["url"])}" target="_blank" rel="nofollow noopener">{e(x["offerta"])}</a>' if x.get("url") else e(x["offerta"])
    dopo = f'poi {n2(x["prezzo_dopo"])}' + (f' dopo {x["mesi_promo"]} mesi' if x.get("mesi_promo") else "") if x.get("prezzo_dopo") and x["prezzo_dopo"] != x["prezzo_mese"] else ""
    tec = (x.get("tecnologia") or "").upper()
    cat = "fwa" if "FWA" in tec else "ftth" if "FTTH" in tec else "altro"
    area = f'<span class="ar">Solo {e(x["area"])}</span> ' if x.get("area") else ""
    tr.append(f'<tr data-cat="{cat}" data-reg="{1 if x.get("area") else 0}"{" class=\"first\"" if i == 0 else ""}><td class="c-pos">{i + 1}</td><td class="c-op"><div class="op">{logo(x["operatore"], x.get("url"))}{e(x["operatore"])}</div><div>{nome}</div>'
              f'<div class="nt">{area}{e(x.get("nota") or "")}{dl(x)}</div></td><td class="c-x" data-l="Tecnologia">{e(x.get("tecnologia") or "—")}{", " + e(x["velocita"]) if x.get("velocita") else ""}</td>'
              f'<td class="n tot c-pr">{n2(x["prezzo_mese"])}<div class="nt">{dopo}</div></td><td class="n c-x" data-l="Attivazione">{n2(x.get("attivazione"))}</td><td class="c-x" data-l="Modem">{e(x.get("modem") or "—")}</td></tr>')
bt = []
for x in net["bundle"]:
    nome = f'<a href="{e(x["url"])}" target="_blank" rel="nofollow noopener">{e(x["offerta"])}</a>' if x.get("url") else e(x["offerta"])
    bt.append(f'<tr><td class="c-op"><div class="op">{logo(x["fornitore"], x.get("url"))}{e(x["fornitore"])}</div><div>{nome}</div><div class="nt">{e(x["nota"])}</div></td><td class="c-x">{e(x["vantaggio"])}</td><td class="n tot c-pr">{n2(x["prezzo_fibra_mese"])}</td></tr>')

corpo = testata("/internet/", "Offerte fibra e internet casa a confronto",
                "Le offerte fibra per la casa dei principali operatori, ordinate per canone mensile, e i pacchetti energia più internet dei fornitori di luce e gas.",
                "net", "/img/geco-net.svg")
corpo += f"""<main class="wrap pg">
<h1 class="h">Offerte fibra e internet casa</h1>
<section class="card"><h2 class="h" style="margin:0 0 8px;font-size:22px">Internet casa, dal canone più basso <span class="src" id="ncnt"></span></h2>
<div class="flt" role="group" aria-label="Filtra"><button type="button" data-t="tutte" aria-pressed="true">Tutte</button><button type="button" data-t="ftth" aria-pressed="false">Fibra FTTH</button><button type="button" data-t="fwa" aria-pressed="false">FWA senza linea</button><label><input type="checkbox" id="noreg"> Nascondi offerte regionali</label></div>
<div class="scroll" role="region" aria-label="Offerte internet casa" tabindex="0"><table class="pk" id="nt">
<thead><tr><th>#</th><th>Operatore e offerta</th><th>Tecnologia</th><th class="n">Al mese</th><th class="n">Attivazione</th><th>Modem</th></tr></thead><tbody>
{''.join(tr)}
</tbody></table></div>
<p class="src">Prezzi letti ogni giorno in automatico dalle pagine ufficiali degli operatori, ultimo controllo il {ver}. Velocità e tecnologia dipendono dalla copertura del tuo indirizzo: verificala sul sito dell'operatore prima di attivare.</p></section>
<section class="card xs"><h2 class="h" style="margin:0 0 4px;font-size:22px">Quanto spenderesti oggi per luce e gas</h2>
<p class="src" style="margin:0">Le offerte più convenienti di oggi per una casa con 225 kWh di luce e 90 Smc di gas al mese, imposte e canone RAI inclusi.</p>
<div class="rw"><div class="bx"><div class="l">Luce</div><strong id="xl">—</strong><span id="xln"></span></div><div class="bx"><div class="l">Gas</div><strong id="xg">—</strong><span id="xgn"></span></div></div>
<div class="cta"><a href="/">Confronta la luce</a><a href="/#gas">Confronta il gas</a><a href="/luce-e-gas/">Pacchetti luce + gas</a></div></section>
<section class="card"><h2 class="h" style="margin:0 0 8px;font-size:22px">Pacchetti energia + internet</h2>
<div class="scroll" role="region" aria-label="Pacchetti energia e internet" tabindex="0"><table class="pk">
<thead><tr><th>Fornitore e offerta</th><th>Vantaggio</th><th class="n">Fibra al mese</th></tr></thead><tbody>
{''.join(bt)}
</tbody></table></div>
<p class="src">Il prezzo della luce e del gas di questi fornitori lo trovi nella <a href="/">classifica luce e gas</a>.</p></section>
<section class="card txt"><h2 class="h">Come leggere il confronto</h2>
<p>Per luce e gas usiamo gli open data ufficiali di ARERA. Per internet non esiste una banca dati pubblica delle offerte: ogni mattina leggiamo i prezzi direttamente dalle pagine degli operatori. Prima di attivare, controlla comunque prezzo e condizioni sulla pagina dell'offerta.</p>
<p>Oltre al canone guarda tre cose: quanto dura il prezzo promozionale, il costo di attivazione e quanto paghi se disdici prima del vincolo.</p></section>
"""
NET_JS = r"""
var T='tutte';function flt(){var n=0,rr=document.querySelectorAll('#nt tbody tr');rr.forEach(function(r){var ok=(T==='tutte'||r.dataset.cat===T)&&!($('noreg').checked&&r.dataset.reg==='1');r.hidden=!ok;if(ok)n++});$('ncnt').textContent=n+' offerte';document.querySelectorAll('.flt button').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.t===T)})}
document.querySelectorAll('.flt button').forEach(function(b){b.addEventListener('click',function(){T=b.dataset.t;flt()})});$('noreg').addEventListener('change',flt);flt();
var eur=function(n){return n.toLocaleString('it-IT',{minimumFractionDigits:2,maximumFractionDigits:2})+' € al mese'};
fetch('/data/top.json',{cache:'no-cache'}).then(function(r){return r.json()}).then(function(d){
  var l=d.luce[0],g=d.gas[0];$('xl').textContent=eur(l.m);$('xln').textContent=l.v+', '+l.n;$('xg').textContent=eur(g.m);$('xgn').textContent=g.v+', '+g.n;});
"""
scrivi("/internet/", corpo, NET_JS)
print("pagine generate")
