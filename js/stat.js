/* Statistiche e consenso cookie (banner: orestbida/cookieconsent v3.3.0, licenza MIT, in /js/cc). */
(function(){
var CFG={gc:'comparaoffertelucegas',ga:'G-707BNRZX3Z',clarity:'zi8k13rov1'};
var d=document,w=window;
function js(src,attrs,cb){var s=d.createElement('script');s.async=true;s.src=src;for(var k in attrs||{})s.setAttribute(k,attrs[k]);if(cb)s.onload=cb;d.head.appendChild(s)}
/* GoatCounter: senza cookie, conta tutte le visite */
if(CFG.gc){js('https://gc.zgo.at/count.js',{'data-goatcounter':'https://'+CFG.gc+'.goatcounter.com/count'});
  d.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href^="http"]');if(!a)return;try{var h=new URL(a.href).hostname;if(/comparaoffertelucegas/.test(h))return;
    w.goatcounter&&w.goatcounter.count&&w.goatcounter.count({path:'esce-'+h.replace(/^www\./,''),title:location.pathname,event:true})}catch(_){}},true)}
var on={};
function ga(){if(on.ga||!CFG.ga)return;on.ga=1;w.dataLayer=w.dataLayer||[];w.gtag=function(){w.dataLayer.push(arguments)};w.gtag('js',new Date());w.gtag('config',CFG.ga);js('https://www.googletagmanager.com/gtag/js?id='+CFG.ga)}
function clarity(){if(on.cl||!CFG.clarity)return;on.cl=1;w.clarity=w.clarity||function(){(w.clarity.q=w.clarity.q||[]).push(arguments)};js('https://www.clarity.ms/tag/'+CFG.clarity);w.clarity('consentv2',{ad_Storage:'denied',analytics_Storage:'granted'})}
function applica(){var C=w.CookieConsent;if(C.acceptedService('ga','analytics'))ga();if(C.acceptedService('clarity','analytics'))clarity()}
function avvia(){
  var l=d.createElement('link');l.rel='stylesheet';l.href='/js/cc/cookieconsent.css';d.head.appendChild(l);
  var st=d.createElement('style');st.textContent='#cc-main{--cc-font-family:"Schibsted Grotesk",system-ui,sans-serif;--cc-modal-border-radius:16px;--cc-btn-border-radius:12px;--cc-btn-primary-bg:var(--accbg,#F5C518);--cc-btn-primary-color:#14161A;--cc-btn-primary-border-color:var(--accbg,#F5C518);--cc-btn-primary-hover-bg:var(--accbg,#F5C518);--cc-btn-primary-hover-color:#14161A;--cc-btn-primary-hover-border-color:var(--accbg,#F5C518);--cc-btn-secondary-bg:transparent;--cc-btn-secondary-color:var(--ink,#14161A);--cc-btn-secondary-border-color:var(--bd,#cfd2cc);--cc-btn-secondary-hover-bg:transparent;--cc-btn-secondary-hover-color:var(--ink,#14161A);--cc-btn-secondary-hover-border-color:var(--ink,#14161A);--cc-toggle-on-bg:var(--ink,#14161A)}#cc-main .cm__btn,#cc-main .pm__btn{font-weight:800}#cc-main .cm__btn:not(.cm__btn--secondary):hover,#cc-main .pm__btn:not(.pm__btn--secondary):hover{filter:brightness(.94)}html[data-c=gas] #cc-main{--cc-btn-primary-color:#fff;--cc-btn-primary-hover-color:#fff}.cc--darkmode #cc-main{--cc-btn-secondary-color:#E8EAED;--cc-btn-secondary-border-color:#5a5f68;--cc-btn-secondary-hover-color:#fff;--cc-btn-secondary-hover-border-color:#E8EAED;--cc-toggle-on-bg:#E8EAED}';
  var H=d.documentElement,dk=function(){var t=H.getAttribute('data-theme');H.classList.toggle('cc--darkmode',t==='dark'||(t!=='light'&&matchMedia('(prefers-color-scheme: dark)').matches))};dk();new MutationObserver(dk).observe(H,{attributes:true,attributeFilter:['data-theme']});d.head.appendChild(st);
  js('/js/cc/cookieconsent.umd.js',null,function(){
    w.CookieConsent.run({
      revision:1,cookie:{name:'cc_cookie',expiresAfterDays:182},
      guiOptions:{consentModal:{layout:'box',position:'bottom center',equalWeightButtons:false},preferencesModal:{layout:'box',equalWeightButtons:false}},
      onConsent:applica,onChange:function(){applica();var C=w.CookieConsent;if((on.ga&&!C.acceptedService('ga','analytics'))||(on.cl&&!C.acceptedService('clarity','analytics')))location.reload()},
      categories:{necessary:{enabled:true,readOnly:true},
        analytics:{autoClear:{cookies:[{name:/^_ga/},{name:/^_cl(ck|sk)$/},{name:'CLID'}],reloadPage:false},
          services:{ga:{label:'Google Analytics'},clarity:{label:'Microsoft Clarity'}}}},
      language:{default:'it',translations:{it:{
        consentModal:{label:'Consenso sui cookie',title:'Consenso sui cookie',
          description:'Utilizziamo i cookie per far funzionare questo sito e capire come viene utilizzato. I cookie analitici si attivano solo con il tuo consenso.',
          acceptAllBtn:'Accetta tutto',acceptNecessaryBtn:'Rifiuta tutto',showPreferencesBtn:'Gestisci preferenze',
          footer:'<a href="/privacy/">Informativa sulla privacy</a>'},
        preferencesModal:{title:'Centro preferenze per il consenso',acceptAllBtn:'Accetta tutto',acceptNecessaryBtn:'Rifiuta tutto',savePreferencesBtn:'Salva le preferenze',closeIconLabel:'Chiudi la finestra',serviceCounterLabel:'Servizi',
          sections:[{title:'Utilizzo dei cookie',description:'Utilizziamo i cookie per far funzionare questo sito e migliorare la tua esperienza. Qui sotto puoi scegliere quali categorie consentire e modificare la tua scelta in qualsiasi momento. Per maggiori dettagli, leggi la nostra <a href="/privacy/" class="cc__link">Informativa sulla privacy</a>.'},
            {title:'Cookie strettamente necessari <span class="pm__badge">Sempre attivi</span>',description:'Questi cookie sono indispensabili per il corretto funzionamento del sito, ad esempio per ricordare il tema scelto e le tue preferenze sui cookie. Non possono essere disattivati.',linkedCategory:'necessary'},
            {title:'Cookie analitici',description:'Questi cookie raccolgono informazioni su come i visitatori utilizzano il sito, come le pagine visitate e il tempo trascorso su di esse, per aiutarci a migliorarlo.',linkedCategory:'analytics',
              cookieTable:{headers:{name:'Nome',service:'Servizio',description:'Descrizione',exp:'Durata'},body:[
                {name:'_ga, _ga_*',service:'Google Analytics',description:'Distingue i visitatori e le visite',exp:'fino a 2 anni'},
                {name:'_clck, _clsk',service:'Microsoft Clarity',description:'Collega le pagine della stessa visita',exp:'da 1 giorno a 1 anno'}]}},
            {title:'Ulteriori informazioni',description:'Per qualsiasi domanda sulla nostra politica sui cookie o sulle tue scelte, <a class="cc__link" href="mailto:info@comparaoffertelucegas.it">contattaci</a>.'}]}}}}
    });
    var f=d.querySelector('footer');if(f&&!d.getElementById('ckl')){var p=d.createElement('p');p.style.margin='8px 0 0';p.innerHTML='<a href="#" id="ckl" data-cc="show-preferencesModal">Preferenze cookie</a>';f.appendChild(p);
      d.getElementById('ckl').addEventListener('click',function(e){e.preventDefault();w.CookieConsent.showPreferences()})}
  })}
if(CFG.ga||CFG.clarity){if(d.readyState==='loading')d.addEventListener('DOMContentLoaded',avvia);else avvia()}
})();
