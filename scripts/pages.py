import re,os
s=open('index.html').read()
css=re.search(r'<style>.*?</style>',s,re.S).group(0)
themeinit=re.search(r'<script>try\{var t=localStorage.*?</script>',s,re.S).group(0)
logo=re.search(r'<a class="logo h" href="/">.*?</a>',s,re.S).group(0)
extra='''<style>
.pg{padding:28px 0 64px;display:flex;flex-direction:column;gap:18px}
.pg h1{margin:0;font-size:32px;letter-spacing:-.02em}
.kpi{display:flex;flex-wrap:wrap;gap:12px}
.kpi .card{flex:1 1 180px;padding:18px}
.kpi .l{font-size:13px;font-weight:700;color:var(--mut)}
.kpi .v{font:700 34px 'Space Grotesk',sans-serif;margin-top:4px}
.kpi .s{font-size:13px;color:var(--ink3)}
.src{font-size:12px;color:var(--mut)}
.back{font-weight:600;font-size:14px}
</style>'''
def page(path,c,title,desc,h1,body,js):
    html=f'''<!DOCTYPE html>
<html lang="it" data-c="{c}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://comparaoffertelucegas.it/{path}/">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://comparaoffertelucegas.it/og.png">
<meta property="og:url" content="https://comparaoffertelucegas.it/{path}/">
<meta name="theme-color" content="#14161A">
{themeinit}
<link rel="icon" href="/{'favicon.svg' if c=='luce' else 'favicon-gas.svg'}" type="image/svg+xml">
<link rel="preload" href="/fonts/inter.woff2" as="font" type="font/woff2" crossorigin>
<link href="/fonts/fonts.css" rel="stylesheet">
{css}
{extra}
</head>
<body>
<header class="top"><div class="wrap">{logo}
<div class="hdr-r"><a class="theme-btn" href="/" style="text-decoration:none">Confronta offerte</a><button class="theme-btn" id="theme-toggle" type="button" aria-label="Cambia tema">Tema: auto</button></div>
</div></header>
<main class="wrap pg">
<h1 class="h">{h1}</h1>
{body}
</main>
<footer><div class="wrap"><span id="fsrc"></span><a href="/">comparaoffertelucegas.it</a></div></footer>
<script>
(function(){{
var $=function(id){{return document.getElementById(id)}};
var num=function(n,d){{return n.toLocaleString('it-IT',{{minimumFractionDigits:d,maximumFractionDigits:d}})}};
var MESI=['gen','feb','mar','apr','mag','giu','lug','ago','set','ott','nov','dic'];
var fd=function(s){{var p=s.split('-');return p.length===3?(+p[2])+' '+MESI[+p[1]-1]:MESI[+p[1]-1]+' '+p[0]}};
(function(){{var modes=['auto','light','dark'],nomi={{auto:'auto',light:'chiaro',dark:'scuro'}},b=$('theme-toggle'),r=document.documentElement;
var m=Math.max(0,modes.indexOf(r.getAttribute('data-theme')||'auto'));var show=function(){{b.textContent='Tema: '+nomi[modes[m]]}};
b.addEventListener('click',function(){{m=(m+1)%3;if(modes[m]==='auto')r.removeAttribute('data-theme');else r.setAttribute('data-theme',modes[m]);try{{modes[m]==='auto'?localStorage.removeItem('tema'):localStorage.setItem('tema',modes[m])}}catch(e){{}}show()}});show()}})();
function chart(el,pts,lab,dec){{var n=pts.length,W=800,H=230,P=40;if(!n)return;
var mx=Math.max.apply(null,pts)*1.08,mn=Math.min(0,Math.min.apply(null,pts));
var X=function(i){{return P+i*(W-P-10)/Math.max(1,n-1)}},Y=function(v){{return H-24-(v-mn)/(mx-mn)*(H-40)}};
var g='';for(var t=0;t<=4;t++){{var v=mn+(mx-mn)*t/4,y=Y(v).toFixed(1);g+='<line x1="'+P+'" x2="'+(W-10)+'" y1="'+y+'" y2="'+y+'" stroke="var(--line)"/><text x="'+(P-6)+'" y="'+(+y+4)+'" text-anchor="end" font-size="11" fill="var(--mut)">'+num(v,2)+'</text>'}}
var lb='';var step=Math.max(1,Math.ceil(n/6));for(var i=0;i<n;i+=step)lb+='<text x="'+X(i).toFixed(1)+'" y="'+(H-6)+'" text-anchor="middle" font-size="11" fill="var(--mut)">'+lab[i]+'</text>';
var p=pts.map(function(v,i){{return X(i).toFixed(1)+','+Y(v).toFixed(1)}}).join(' ');
el.innerHTML='<svg viewBox="0 0 '+W+' '+H+'" role="img">'+g+lb+'<polyline points="'+p+'" fill="none" stroke="var(--accbg)" stroke-width="3" stroke-linejoin="round"/><circle cx="'+X(n-1).toFixed(1)+'" cy="'+Y(pts[n-1]).toFixed(1)+'" r="5" fill="var(--accbg)"/></svg>'}}
{js}
}})();
</script>
</body>
</html>
'''
    os.makedirs(path,exist_ok=True); open(path+'/index.html','w').write(html)

# electricity page
page('prezzo-energia-oggi','luce','PUN oggi: prezzo energia elettrica (zona Nord) | comparaoffertelucegas',
'Prezzo dell\'energia elettrica di oggi e domani sul mercato del giorno prima, andamento degli ultimi mesi.',
'PUN oggi',
'''<section class="kpi">
<div class="card"><div class="l" id="l1">Oggi</div><div class="v" id="v1">—</div><div class="s">€/kWh, media del giorno</div></div>
<div class="card"><div class="l" id="l2">Domani</div><div class="v" id="v2">—</div><div class="s" id="s2">€/kWh</div></div>
<div class="card"><div class="l" id="l3">Media del mese</div><div class="v" id="v3">—</div><div class="s">€/kWh</div></div>
</section>
<section class="card"><h2 class="h" style="margin:0 0 8px;font-size:22px">Oggi ora per ora</h2><div id="ch0"></div></section>
<section class="card"><h2 class="h" style="margin:0 0 8px;font-size:22px">Ultimi 120 giorni</h2><div id="ch1"></div>
<div class="scroll"><table class="itab" id="tab"></table></div>
<p class="src">Prezzo del mercato del giorno prima, zona Nord, riferimento per il PUN. Prezzo all'ingrosso, non la tariffa in bolletta.</p></section>''',
'''fetch('/data/elettricita.json',{cache:'no-cache'}).then(function(r){return r.json()}).then(function(d){
var se=d.serie,n=se.length,oggi=new Date().toLocaleDateString('sv-SE',{timeZone:'Europe/Rome'});
var past0=se.filter(function(x){return x.d<oggi}),t0=se.filter(function(x){return x.d===oggi})[0],o=t0||past0[past0.length-1],dom=se.filter(function(x){return x.d>oggi})[0]||null;
$('l1').textContent=(t0?'Oggi, ':'Ultimo dato, ')+fd(o.d);$('v1').textContent=num(o.v,4);
if(dom){$('l2').textContent='Domani, '+fd(dom.d);$('v2').textContent=num(dom.v,4);var dv=(dom.v-o.v)/o.v*100;$('s2').innerHTML='€/kWh <span class="dl '+(dv>0?'up':'down')+'">'+(dv>0?'▲':'▼')+' '+Math.abs(dv).toFixed(0)+'%</span>'}else{$('v2').textContent='dalle 13';}
var cm=oggi.slice(0,7),l30=se.filter(function(x){return x.d.slice(0,7)===cm&&x.d<=oggi});if(!l30.length)l30=se.filter(function(x){return x.d<=o.d}).slice(-30);$('l3').textContent='Media '+fd(cm);$('v3').textContent=num(l30.reduce(function(a,x){return a+x.v},0)/l30.length,4);
var h=d.orario[o.d]||d.orario[oggi]||[];if(!h.length)$('ch0').parentNode.style.display='none';chart($('ch0'),h,h.map(function(_,i){return i+':00'}));
var past=se.filter(function(x){return x.d<=o.d});chart($('ch1'),past.map(function(x){return x.v}),past.map(function(x){return fd(x.d)}));
$('tab').innerHTML='<thead><tr><th>Giorno</th><th>Media €/kWh</th><th>Min</th><th>Max</th></tr></thead><tbody>'+se.slice().reverse().slice(0,30).map(function(x){return '<tr><td>'+fd(x.d)+(x.d>oggi?' (domani)':'')+'</td><td>'+num(x.v,4)+'</td><td>'+num(x.min,4)+'</td><td>'+num(x.max,4)+'</td></tr>'}).join('')+'</tbody>';
$('fsrc').textContent='Dati: Energy-Charts (Fraunhofer ISE), Bundesnetzagentur | SMARD.de, CC BY 4.0.';
});''')

# gas page
page('psv','gas','Prezzo gas PSV: valore e andamento mensile | comparaoffertelucegas',
'Prezzo del gas PSV in €/Smc, ultimo valore ufficiale e andamento mese per mese dal 2024.',
'Prezzo gas PSV',
'''<section class="kpi">
<div class="card"><div class="l" id="l1">Ultimo mese</div><div class="v" id="v1">—</div><div class="s" id="s1">€/Smc</div></div>
<div class="card"><div class="l">Media 12 mesi</div><div class="v" id="v2">—</div><div class="s">€/Smc</div></div>
</section>
<section class="card"><h2 class="h" style="margin:0 0 8px;font-size:22px">Andamento mensile</h2><div id="ch1"></div>
<div class="scroll"><table class="itab" id="tab"></table></div>
<p class="src">Media mensile del PSV usata da ARERA per le offerte. Un valore giornaliero ufficiale e gratuito non esiste.</p></section>''',
'''fetch('/data/indici.json',{cache:'no-cache'}).then(function(r){return r.json()}).then(function(d){
var se=d.serie,n=se.length,l=se[n-1],p=se[n-2];
$('l1').textContent='PSV '+fd(l.m);$('v1').textContent=num(l.psv,4);var dv=(l.psv-p.psv)/p.psv*100;$('s1').innerHTML='€/Smc <span class="dl '+(dv>0?'up':'down')+'">'+(dv>0?'▲':'▼')+' '+Math.abs(dv).toFixed(0)+'%</span>';
var y=se.slice(-12);$('v2').textContent=num(y.reduce(function(a,x){return a+x.psv},0)/y.length,4);
chart($('ch1'),se.map(function(x){return x.psv}),se.map(function(x){return fd(x.m)}));
$('tab').innerHTML='<thead><tr><th>Mese</th><th>PSV €/Smc</th></tr></thead><tbody>'+se.slice().reverse().map(function(x){return '<tr><td>'+fd(x.m)+'</td><td>'+num(x.psv,4)+'</td></tr>'}).join('')+'</tbody>';
$('fsrc').textContent='Fonte: ARERA, Portale Offerte, open data.';
});''')
print('ok')
