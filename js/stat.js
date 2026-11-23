/* Statistiche e consenso cookie. Inserire gli ID quando gli account sono pronti. */
(function(){
var CFG={gc:'comparaoffertelucegas',ga:'G-707BNRZX3Z',clarity:'zi8k13rov1'};
var K='cc',SEI_MESI=182*864e5,d=document,w=window;
function get(){try{var v=JSON.parse(localStorage.getItem(K)||'null');if(v&&Date.now()-v.t<SEI_MESI)return v.s}catch(e){}return null}
function set(s){try{localStorage.setItem(K,JSON.stringify({s:s,t:Date.now()}))}catch(e){}}
function js(src,attrs){var s=d.createElement('script');s.async=true;s.src=src;for(var k in attrs||{})s.setAttribute(k,attrs[k]);d.head.appendChild(s)}
/* GoatCounter: senza cookie, conta tutte le visite */
if(CFG.gc){js('https://gc.zgo.at/count.js',{'data-goatcounter':'https://'+CFG.gc+'.goatcounter.com/count'});
  d.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href^="http"]');if(!a)return;try{var h=new URL(a.href).hostname;if(/comparaoffertelucegas/.test(h))return;
    w.goatcounter&&w.goatcounter.count&&w.goatcounter.count({path:'esce-'+h.replace(/^www\./,''),title:location.pathname,event:true})}catch(_){}},true)}
var conCookie=CFG.ga||CFG.clarity;
function attiva(){
  if(CFG.ga){w.dataLayer=w.dataLayer||[];w.gtag=function(){w.dataLayer.push(arguments)};w.gtag('js',new Date());w.gtag('config',CFG.ga);js('https://www.googletagmanager.com/gtag/js?id='+CFG.ga)}
  if(CFG.clarity){w.clarity=w.clarity||function(){(w.clarity.q=w.clarity.q||[]).push(arguments)};js('https://www.clarity.ms/tag/'+CFG.clarity);w.clarity('consentv2',{ad_Storage:'denied',analytics_Storage:'granted'})}}
function pulisci(){d.cookie.split(';').forEach(function(c){var n=c.split('=')[0].trim();if(/^(_ga|_gid|_clck|_clsk|CLID|MUID)/.test(n)){['',';domain=.'+location.hostname,';domain='+location.hostname].forEach(function(dm){d.cookie=n+'=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/'+dm})}})}
function banner(){if(d.getElementById('ckb'))return;
  var st=d.createElement('style');st.textContent='#ckb{position:fixed;left:16px;right:16px;bottom:16px;z-index:90;max-width:560px;margin:0 auto;background:var(--card,#fff);color:var(--ink,#14161A);border:1px solid var(--bd,#ddd);border-radius:16px;padding:16px 18px;box-shadow:0 10px 40px rgba(0,0,0,.22);font:15px/1.45 "Schibsted Grotesk",system-ui,sans-serif}#ckb p{margin:0 0 12px}#ckb a{color:inherit}#ckb .b{display:flex;gap:10px}#ckb button{flex:1;min-height:44px;border-radius:12px;font:700 15px "Schibsted Grotesk",system-ui,sans-serif;cursor:pointer;border:2px solid var(--ink,#14161A)}#ckb .n{background:transparent;color:var(--ink,#14161A)}#ckb .y{background:transparent;color:var(--ink,#14161A)}';
  d.head.appendChild(st);var b=d.createElement('div');b.id='ckb';b.setAttribute('role','dialog');b.setAttribute('aria-label','Cookie');
  b.innerHTML='<p>Usiamo cookie di '+[CFG.ga&&'Google Analytics',CFG.clarity&&'Microsoft Clarity'].filter(Boolean).join(' e ')+' per capire quali pagine e funzioni del sito servono di più. Si attivano solo se accetti. Dettagli nella <a href="/privacy/">privacy</a>.</p><div class="b"><button type="button" class="n">Rifiuta</button><button type="button" class="y">Accetta</button></div>';
  d.body.appendChild(b);
  b.querySelector('.y').onclick=function(){set('si');b.remove();attiva()};
  b.querySelector('.n').onclick=function(){var era=get()==='si';set('no');b.remove();if(era){pulisci();location.reload()}}}
function link(){var f=d.querySelector('footer');if(!f||d.getElementById('ckl'))return;var p=d.createElement('p');p.style.margin='8px 0 0';
  p.innerHTML='<a href="#" id="ckl">Preferenze cookie</a>';f.appendChild(p);d.getElementById('ckl').onclick=function(e){e.preventDefault();banner()}}
if(conCookie){var s=get();if(s==='si')attiva();
  var avvia=function(){link();if(!s)banner()};if(d.readyState==='loading')d.addEventListener('DOMContentLoaded',avvia);else avvia()}
})();
