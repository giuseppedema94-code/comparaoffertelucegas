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
.lgst{flex:0 1 auto;min-width:0}.lgv{min-width:0}.lgv input{font-variant-numeric:tabular-nums;padding:0}
@media (max-width:520px){.lgq{gap:8px}.lgq label{flex:0 0 46px}.lgst{flex:1 1 auto;justify-content:flex-end}.lgv{flex:1 1 auto;padding:6px 10px;gap:5px;justify-content:flex-end}.lgv input{flex:1 1 auto;width:0;min-width:0;font-size:26px}.lgv span{font-size:13px}.pm{flex:0 0 40px;width:40px;height:44px}}
@media (max-width:360px){.lgv input{font-size:22px}.lgv{padding:6px 8px}.pm{flex:0 0 36px;width:36px}.lgq label{flex:0 0 40px;font-size:15px}}
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
.lgb{position:relative;flex:0 0 auto;width:76px;height:76px;border-radius:16px;background:#fff;border:1px solid var(--line);display:inline-flex;align-items:center;justify-content:center;font:800 30px 'Schibsted Grotesk',sans-serif;color:#14161A;overflow:hidden}
.lgb img{position:absolute;inset:7px;width:calc(100% - 14px);height:calc(100% - 14px);object-fit:contain;background:#fff}
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
@media (max-width:760px){.oc-h{flex-wrap:wrap;padding:12px 14px}.oc-tg{width:100%;justify-content:flex-start}.oc-b{grid-template-columns:minmax(0,1fr) auto}.oc-d{grid-column:1/-1;border-right:0;border-bottom:1px solid var(--line);padding:12px 14px}.oc-p{text-align:left;border-right:0;padding:12px 14px}.oc-a{padding:12px 14px 12px 0}.oc-m strong{font-size:34px}.oc-m span{font-size:16px}.oc-btn{padding:12px 14px;font-size:14px}.lgb{width:62px;height:62px;border-radius:14px}}
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
.claim{display:block;padding:0 4px 20px}
.claim .cl-h{font-size:clamp(34px,5.4vw,60px);line-height:1.04;letter-spacing:-.02em;margin:0 0 10px;font-weight:900}
.claim .cl-s{font-size:18px;line-height:1.45;color:var(--ink2);margin:0 0 16px}.cl-s strong{color:var(--ink)}
.cl-n{font-size:13.5px;line-height:1.45;color:var(--mut);margin:18px 0 0;max-width:70ch}.cl-h sup{font-size:.45em;vertical-align:.9em;margin-left:2px}
@media (max-width:700px){.claim{padding:14px 18px 8px}.cl-s{font-size:16px;margin-bottom:8px}.cl-n{padding:0 18px}}
.oc-cmp{font:600 14px 'Schibsted Grotesk',sans-serif;padding:10px 12px;border-radius:10px;border:1px solid var(--bd);background:transparent;color:var(--ink2);cursor:pointer}.oc-cmp:hover{border-color:var(--ink);color:var(--ink)}
.chip{border:1px solid var(--bd);cursor:pointer;font:600 13px 'Schibsted Grotesk',sans-serif;padding:10px 14px;border-radius:99px;background:var(--card);color:var(--ink)}
#cdlg{border:0;border-radius:16px;padding:20px;max-width:560px;width:calc(100% - 24px);background:var(--card);color:var(--ink)}#cdlg::backdrop{background:rgba(0,0,0,.5)}
.cdh{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:10px}.cdh h2{margin:0;font-size:22px}
.ctab{width:100%;border-collapse:collapse;font-size:14.5px;table-layout:fixed;margin-top:12px}.ctab th,.ctab td{padding:9px 8px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top;overflow-wrap:anywhere}.ctab th{color:var(--mut);font-weight:600;width:32%}.ctab td.w{color:var(--ok);font-weight:700}.ctab thead td{font-weight:800;font-size:15px}
#cmine .note{font-size:14px;color:var(--ink2);line-height:1.45}
.mia-f{display:grid;gap:10px}.mia-f label{display:grid;gap:4px;font-size:13px;color:var(--mut)}
.mia-in{display:flex;align-items:center;gap:6px;border:1px solid var(--bd);border-radius:10px;padding:0 10px;background:var(--soft)}.mia-in:focus-within{border-color:var(--ink)}
.mia-in input{flex:1;min-width:0;width:0;border:0;background:transparent;font:700 18px 'Schibsted Grotesk',sans-serif;color:var(--ink);padding:9px 0;outline:0}.mia-in span{font-size:13px;color:var(--mut);white-space:nowrap}
.mia-r{margin:0;padding:10px 12px;border-radius:10px;background:var(--first);font-size:14px;line-height:1.45}
.mia-row{margin:6px 0;padding:10px 14px;border:2px dashed var(--accbar);border-radius:14px;font-size:14px;display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap}.mia-row strong{font-size:16px}
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
.per{display:flex;justify-content:flex-start;gap:6px;margin:0 0 12px}.per button{font:600 14px 'Schibsted Grotesk',sans-serif;padding:6px 14px;border-radius:8px;border:1px solid var(--line);background:transparent;color:var(--ink2);cursor:pointer;min-height:36px}.per button[aria-pressed=true]{background:var(--ink);color:var(--bg);border-color:var(--ink)}
"""


def testata(path, title, desc, c, icon):
    s = testa
    on = lambda k: ' aria-current="page"' if k == c else ""
    nav = (f'<nav class="seg segn" aria-label="Confronti"><a class="t-luce" href="/"{on("luce")}>Luce</a><a class="t-gas" href="/#gas"{on("gas")}>Gas</a>'
           f'<a class="t-lg" href="/luce-e-gas/"{on("lg")}>Luce + gas</a><a class="t-net" href="/internet/"{on("net")}>Internet</a></nav>')
    s = s.replace('<a class="cmp-link" href="/">Confronta offerte</a>', nav)
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
var PMv=function(){return PER==='b'?2:1},PLv=function(){return PER==='b'?' a bimestre':' al mese'};
var big=function(v){var c=Math.round(v*PMv()*100);return '<strong>'+Math.floor(c/100)+'</strong><span>,'+String(c%100).padStart(2,'0')+(PER==='b'?' €/bimestre':' €/mese')+'</span>'};
var logoB=function(o){var d=o.lg&&/^[a-z0-9.-]+$/.test(o.lg)?o.lg:null;return '<span class="lgb" aria-hidden="true">'+esc((o.v||'?').charAt(0).toUpperCase())+(d?'<img src="/img/loghi/'+d+'.png" alt="" loading="lazy">':'')+'</span>'};
function accLuce(y,al){var m=y/12,e=m<=220?Math.min(m,150):Math.max(0,150-(m-220));return (m-e)*12*al}
function costo(o,c,y,R){var r=R[c],acc=c==='luce'?accLuce(y,r.acc):0;return (1+r.iva)*(o.fx+o.p*y-(o.s||0)+r.rf+r.rv*y+acc)/12}
var D={};
var PER='m';
var PF_={m:1,b:2,a:12},PS_={m:1,b:2,a:10};
function setPer(x){if(x===PER)return;var f=PF_[x]/PF_[PER];['ql','qg'].forEach(function(id){var i=$(id),st=id==='ql'?10:5;i.value=Math.round((+i.value||0)*f);i.step=st*PS_[x]});
  document.querySelectorAll('.pm').forEach(function(b){var s=b.dataset.t==='ql'?10:5;b.dataset.d=(+b.dataset.d<0?-1:1)*s*PS_[x]});
  PER=x;document.querySelectorAll('.per button').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.p===x)});render()}
function render(){
  var k=12/PF_[PER],yl=Math.max(0,+$('ql').value||0)*k,yg=Math.max(0,+$('qg').value||0)*k,rai=$('rai').checked?9:0;
  var R=D.dual.reg;
  var FN=$('ofn').checked,ok=function(o,y){return o.ok!==false&&(!FN||o.fn)&&!(o.min!=null&&y<o.min||o.max!=null&&y>o.max)};
  var rows=D.dual.offerte.filter(function(o){return !FN||o.fn}).map(function(o){var l=costo(o.l,'luce',yl,R)+rai,g=costo(o.g,'gas',yg,R);return {o:o,l:l,g:g,t:l+g,k:'c'}});
  var bestBy=function(d,c,y){var m={};d.offerte.forEach(function(o){if(!ok(o,y))return;var x=costo(o,c,y,R);if(!m[o.v]||x<m[o.v].x)m[o.v]={o:o,x:x}});return m};
  var ML=bestBy(D.luce,'luce',yl),MG=bestBy(D.gas,'gas',yg);
  Object.keys(ML).forEach(function(v){if(!MG[v])return;var L=ML[v].o,G=MG[v].o,l=ML[v].x+rai,g=MG[v].x;
    rows.push({k:'s',l:l,g:g,t:l+g,o:{v:v,n:'Luce: '+L.n+' · Gas: '+G.n,u:null,t:L.t==='f'&&G.t==='f'?'f':'v',d:Math.min(L.d||0,G.d||0),pen:L.pen||G.pen,lg:L.lg||G.lg,l:{pd:L.pd!=null?L.pd:L.p,fx:L.fx},g:{pd:G.pd!=null?G.pd:G.p,fx:G.fx},L:L,G:G}})});
  rows.sort(function(a,b){return a.t-b.t});
  function migliore(d,c,y){var b=null;d.offerte.forEach(function(o){if(o.ok===false||FN&&!o.fn)return;if(o.min!=null&&y<o.min||o.max!=null&&y>o.max)return;var x=costo(o,c,y,R);if(!b||x<b.x)b={o:o,x:x}});return b}
  var bl=migliore(D.luce,'luce',yl),bg=migliore(D.gas,'gas',yg);
  if(bl&&bg){var sep=bl.x+rai+bg.x,pk=rows[0],vince=!pk||sep<=pk.t,lnk=function(o,t,c){var u=safe(o.u)||safe(o.us),k=/luce$/.test(t)?' bl':/gas$/.test(t)?' bg':'';return u?'<a class="lgbtn'+k+'" href="'+esc(u)+'" target="_blank" rel="nofollow noopener">'+t+'</a>':'<a class="lgbtn'+k+'" href="/?q='+encodeURIComponent(o.v)+'#'+(c||'luce')+'">'+t+'</a>'};
    var riga=function(k,x,o){return '<div class="lgr1"><span class="k">'+k+'</span><span class="lgl">'+logoB(o)+'<span><strong>'+esc(o.v)+'</strong><br>'+esc(o.n)+'</span></span><span class="lgp">'+eur(x*PMv())+'</span></div>'};
    $('best').innerHTML=vince
      ?'<div class="lbk">La soluzione più conveniente oggi</div><div class="lbt">Luce e gas da due fornitori diversi</div><div class="lbm">'+big(sep)+'</div>'+riga('Luce',bl.x+rai,bl.o)+riga('Gas',bg.x,bg.o)
        +(pk?'<div class="lbs">Risparmi '+eur((pk.t-sep)*PMv())+PLv()+' rispetto al miglior fornitore unico per luce e gas ('+esc(pk.o.v)+', '+eur(pk.t*PMv())+')</div>':'')+'<div class="lbb">'+lnk(bl.o,'Offerta luce','luce')+lnk(bg.o,'Offerta gas','gas')+'</div>'
      :'<div class="lbk">La soluzione più conveniente oggi</div><div class="lbt">Luce e gas con '+esc(pk.o.v)+'</div><div class="lbm">'+big(pk.t)+'</div>'+riga('Pacchetto',pk.t,pk.o)
        +'<div class="lbs">Risparmi '+eur((sep-pk.t)*PMv())+PLv()+' rispetto a luce e gas da fornitori diversi ('+eur(sep*PMv())+')</div><div class="lbb">'+(pk.k==='s'?lnk(pk.o.L,'Offerta luce','luce')+lnk(pk.o.G,'Offerta gas','gas'):lnk(pk.o,'Vai all\'offerta'))+'</div>'}
  var stab=function(o){return o.t!=='f'?'D':(o.d>=36&&o.d<=240?'A':o.d>=24&&o.d<=240?'B':'C')};
  var bt=function(o,t,c){var u=safe(o.u)||safe(o.us),k=/luce$/.test(t)?' bl':/gas$/.test(t)?' bg':'';return '<a class="oc-btn'+k+'" href="'+(u?esc(u)+'" target="_blank" rel="nofollow noopener':'/?q='+encodeURIComponent(o.v)+'#'+c)+'">'+t+'</a>'};
  var h='',top=rows.length?rows[0].t:0,qs=($('lgs').value||'').trim().toLowerCase(),vis=qs?rows.filter(function(x){return (x.o.v+' '+x.o.n).toLowerCase().indexOf(qs)>=0}):rows;
  if(!vis.length)h='<p class="src">Nessuna offerta per &laquo;'+esc(qs)+'&raquo;.</p>';
  vis.forEach(function(x,j){var i=rows.indexOf(x);var o=x.o,u=safe(o.u),tipo=o.t==='f'?'Fisso'+(o.d>=12&&o.d<=240?' · '+(o.d%12?o.d+' mesi':o.d/12+(o.d===12?' anno':' anni')):''):'Variabile';
    h+='<article class="oc'+(i===0?' first':'')+'"><div class="oc-h"><span class="oc-n">'+(i+1)+'</span>'+logoB(o)+'<div class="oc-t"><div class="oc-v">'+esc(o.v)+'</div><div class="oc-o">'+(u?'<a href="'+esc(u)+'" target="_blank" rel="nofollow noopener">'+esc(o.n)+'</a>':esc(o.n))+'</div></div>'
     +'<div class="oc-tg"><span class="tg '+(o.t==='f'?'tg-f':'tg-v')+'">'+tipo+'</span><span class="tg st-'+stab(o)+'">Stabilità '+stab(o)+'</span>'+(x.k==='c'?'<span class="tg tg-s" title="Un unico contratto per luce e gas">Offerta congiunta</span>':'<span class="tg tg-s" title="Due contratti separati con lo stesso fornitore">Due contratti</span>')+(o.pen?'<span class="tg tg-w">Penale di uscita</span>':'')+'</div></div>'
     +'<div class="oc-b"><dl class="oc-d"><div><dt>Luce</dt><dd>'+eur(x.l*PMv())+PLv()+'</dd></div><div><dt>Gas</dt><dd>'+eur(x.g*PMv())+PLv()+'</dd></div><div><dt>Energia luce</dt><dd>'+num(o.l.pd,4)+' €/kWh</dd></div><div><dt>Energia gas</dt><dd>'+num(o.g.pd,4)+' €/Smc</dd></div><div><dt>Quota fissa luce</dt><dd>'+eur(o.l.fx/12)+' al mese</dd></div><div><dt>Quota fissa gas</dt><dd>'+eur(o.g.fx/12)+' al mese</dd></div></dl>'
     +'<div class="oc-p"><div class="oc-m">'+big(x.t)+'</div><div class="oc-y">luce + gas</div>'+(i===0?'<div class="oc-dd top1">La più conveniente</div>':'<div class="oc-dd">+'+eur((x.t-top)*PMv())+PLv()+'</div>')+'</div>'
     +'<div class="oc-a">'+(x.k==='s'?bt(o.L,'Offerta luce','luce')+bt(o.G,'Offerta gas','gas'):bt(o,'Vai all\'offerta','luce'))+'</div></div></article>'});
  $('tab').innerHTML=h;
  var mg=function(n){return String(n).replace(/\B(?=(\d{3})+(?!\d))/g,'.')},bst=Math.min(bl&&bg?bl.x+rai+bg.x:Infinity,rows.length?rows[0].t:Infinity);
  if(isFinite(bst))$('clp').textContent=Math.floor(bst)+'\u00a0€';
  $('clc').textContent=mg(['luce','gas','dual'].reduce(function(a,k){return a+D[k].offerte.filter(function(o){return o.ok!==false}).length},0));
  var ql=Math.round(yl/12),qg=Math.round(yg/12),sg=ql===125&&qg===40,hh=D.dual.generato?new Date(D.dual.generato).toLocaleTimeString('it-IT',{timeZone:'Europe/Rome',hour:'2-digit',minute:'2-digit'}):'';
  $('cln').textContent='*La soluzione più economica'+(hh?' alle '+hh:'')+' per '+(sg?'una persona sola (':'')+mg(ql)+' kWh di luce e '+mg(qg)+' Smc di gas al mese'+(sg?')':'')+', con imposte, oneri'+(rai?' e canone RAI':'')+'. Cambia con il tuo consumo.';
  var nc=rows.filter(function(x){return x.k==='c'}).length;$('cnt').textContent=(rows.length-nc)+' fornitori con luce e gas, '+nc+' offerte congiunte';
}
Promise.all(['dual','luce','gas'].map(function(k){return fetch('/data/'+k+'.json',{cache:'no-cache'}).then(function(r){return r.json()})})).then(function(a){D.dual=a[0];D.luce=a[1];D.gas=a[2];
  ['ql','qg','rai','lgs'].forEach(function(id){$(id).addEventListener('input',render)});$('ofn').addEventListener('change',render);
  document.querySelectorAll('.pm').forEach(function(b){b.addEventListener('click',function(){var i=$(b.dataset.t);i.value=Math.max(0,(+i.value||0)+(+b.dataset.d));render()})});
  document.querySelectorAll('.per button').forEach(function(b){b.addEventListener('click',function(){setPer(b.dataset.p)})});
  var PF={1:[125,40],2:[185,75],4:[270,115]};document.querySelectorAll('[data-pf]').forEach(function(b){b.addEventListener('click',function(){var k=PF_[PER];$('ql').value=PF[b.dataset.pf][0]*k;$('qg').value=PF[b.dataset.pf][1]*k;render()})});render();
  $('fsrc').textContent='Fonte: ARERA, Portale Offerte, open data del '+D.dual.data_open_data.split('-').reverse().join('/')+'.'});
"""

corpo = testata("/luce-e-gas/", "Offerte luce e gas insieme: pacchetti a confronto",
                "Le offerte luce e gas in un unico contratto dagli open data ARERA, con la spesa sui tuoi consumi e il confronto con le migliori offerte separate.",
                "lg", "/img/geco-lg.svg")
corpo += """<main class="wrap pg">
<section class="claim" aria-label="In breve"><h1 class="cl-h h">Offerte luce e gas da <span id="clp">…</span><sup>*</sup> al mese.</h1>
<p class="cl-s">Tutte le <strong id="clc">…</strong> offerte luce e gas del Portale ARERA, anche congiunte, sempre aggiornate.</p></section>
<section class="lgh">
<div class="card lga"><h2 class="h">I tuoi consumi</h2>
<div class="per" role="group" aria-label="Periodo del consumo"><button type="button" data-p="m" aria-pressed="true">Mensile</button><button type="button" data-p="b" aria-pressed="false">Bimestrale</button><button type="button" data-p="a" aria-pressed="false">Annuo</button></div>
<div class="lgq"><label for="ql">Luce</label><div class="lgst"><button type="button" class="pm" data-t="ql" data-d="-10" aria-label="Diminuisci il consumo di luce">−</button><div class="lgv"><input type="number" id="ql" value="125" min="0" step="10" inputmode="numeric"><span>kWh</span></div><button type="button" class="pm" data-t="ql" data-d="10" aria-label="Aumenta il consumo di luce">+</button></div></div>
<div class="lgq"><label for="qg">Gas</label><div class="lgst"><button type="button" class="pm" data-t="qg" data-d="-5" aria-label="Diminuisci il consumo di gas">−</button><div class="lgv"><input type="number" id="qg" value="40" min="0" step="5" inputmode="numeric"><span>Smc</span></div><button type="button" class="pm" data-t="qg" data-d="5" aria-label="Aumenta il consumo di gas">+</button></div></div>
<div class="prof" role="group" aria-label="Consumo tipo"><span>Non hai la bolletta?</span><button type="button" data-pf="1">Single</button><button type="button" data-pf="2">Coppia</button><button type="button" data-pf="4">Famiglia di 4</button></div>
<label class="lgr"><input type="checkbox" id="rai" checked> Canone RAI <span>(90 €/anno)</span></label>
<label class="lgr"><input type="checkbox" id="ofn"> Solo fornitori certificati</label>
<p class="src">Cliente residente, contatore da 3 kW. Spesa con imposte, stimata come nella <a href="/">classifica principale</a>.</p></div>
<div class="lgb1" id="best" aria-live="polite">Caricamento offerte…</div>
</section>
<section class="card"><h2 class="h" style="margin:0 0 8px;font-size:22px">Luce e gas con un solo fornitore <span class="src" id="cnt"></span></h2>
<input type="search" class="search" id="lgs" placeholder="Cerca fornitore o offerta, es. Enel" aria-label="Cerca fornitore o offerta" style="width:100%;margin:0 0 12px"><div id="tab"></div></section>
<section class="card txt"><h2 class="h">Conviene il pacchetto unico?</h2>
<p>Un'offerta dual lega luce e gas allo stesso venditore: una sola bolletta e, a volte, uno sconto. Non è detto che costi meno di due offerte separate scelte ciascuna al prezzo più basso, per questo le mettiamo a confronto qui sopra.</p>
<p>Se un domani vuoi cambiare solo la luce o solo il gas, controlla nella scheda dell'offerta se lo sconto del pacchetto si perde.</p></section>
<p class="cl-n" id="cln"></p>
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
    diff = "" if bundle else ('<div class="oc-dd top1">La più conveniente</div>' if i == 0 else f'<div class="oc-dd">+{n2(pm - top)} al mese</div>')
    btn = f'<a class="oc-btn" href="{e(x["url"])}" target="_blank" rel="nofollow noopener">Vai all\'offerta</a>' if x.get("url") else ""
    if not bundle: btn += '<button type="button" class="oc-cmp">Confronta con il tuo</button>'
    num = "" if bundle else f'<span class="oc-n">{i + 1}</span>'
    first = " first" if (i == 0 and not bundle) else ""
    return (f'<article class="oc{first}" data-pm="{pm:.2f}" data-cat="{cat}" data-reg="{1 if x.get("area") else 0}"><div class="oc-h">{num}{logo(op, x.get("url"), "lgb")}'
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
<section class="claim" aria-label="In breve"><h1 class="cl-h h">Offerte internet da {int(top)}&nbsp;€<sup>*</sup> al mese.</h1>
<p class="cl-s">Tutte le <strong>{len(righe)}</strong> offerte fibra e FWA dei principali operatori, sempre aggiornate.</p></section>
<section class="card"><h2 class="h" style="margin:0 0 8px;font-size:22px">Internet casa, risparmia fino all'ultimo centesimo <span class="src" id="ncnt"></span></h2>
<div class="flt" role="group" aria-label="Filtra"><button type="button" data-t="tutte" aria-pressed="true">Tutte</button><button type="button" data-t="ftth" aria-pressed="false">Fibra FTTH</button><button type="button" data-t="fwa" aria-pressed="false">FWA senza linea</button><label><input type="checkbox" id="noreg"> Nascondi offerte regionali</label></div>
<input type="search" class="search" id="ns" placeholder="Cerca fornitore o offerta, es. Iliad" aria-label="Cerca fornitore o offerta" style="width:100%;margin:0 0 12px">
<div id="nt">
{''.join(tr)}
</div>
<dialog id="cdlg" aria-labelledby="cdh"><div class="cdh"><h2 class="h" id="cdh">Il tuo abbonamento a confronto</h2><button type="button" class="chip" id="cclose">Chiudi</button></div>
<div class="mia-f"><label><span>Quanto paghi oggi</span><span class="mia-in"><input id="mq" inputmode="decimal" autocomplete="off" placeholder="29,90"><span>€/mese</span></span></label></div><div id="cmine"></div></dialog>
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
<p class="cl-n">*Il canone al mese più basso tra le offerte in elenco.</p>
<section class="card txt"><h2 class="h">Come leggere il confronto</h2>
<p>Per luce e gas usiamo gli open data ufficiali di ARERA. Per internet non esiste una banca dati pubblica delle offerte: ogni mattina leggiamo i prezzi direttamente dalle pagine degli operatori. Prima di attivare, controlla comunque prezzo e condizioni sulla pagina dell'offerta.</p>
<p>Oltre al canone guarda tre cose: quanto dura il prezzo promozionale, il costo di attivazione e quanto paghi se disdici prima del vincolo.</p></section>
"""
NET_JS = r"""
var MQ='',CUR=null;try{MQ=localStorage.getItem('mia-net')||''}catch(e){}
var fe=function(n){return n.toLocaleString('it-IT',{minimumFractionDigits:2,maximumFractionDigits:2})+' €'};
var mv=function(){var v=parseFloat(String(MQ).replace(/\s|€/g,'').replace(',','.'));return v>0&&v<300?v:null};
function mia(){var o=document.querySelector('.mia-row');if(o)o.remove();var v=mv();if(v==null)return;
  var vis=[].slice.call(document.querySelectorAll('#nt article')).filter(function(a){return !a.hidden});
  var d=document.createElement('div');d.className='mia-row';d.innerHTML='<span>Il tuo abbonamento</span><strong>'+fe(v)+' al mese</strong>';
  var nx=vis.filter(function(a){return +a.dataset.pm>=v-0.005})[0];if(nx)nx.parentNode.insertBefore(d,nx);else if(vis.length)vis[vis.length-1].after(d)}
function tab(){var el=$('cmine'),v=mv(),a=CUR;if(!a)return;if(v==null){el.innerHTML='';return}var pm=+a.dataset.pm,w=Math.abs(pm-v)<0.005?-1:pm<v?0:1;
  var c=function(i,t){return '<td'+(w===i?' class="w"':'')+'>'+t+'</td>'},nm=a.querySelector('.oc-v').textContent,of=a.querySelector('.oc-o').textContent;
  var vis=[].slice.call(document.querySelectorAll('#nt article')).filter(function(x){return !x.hidden}),n=vis.filter(function(x){return +x.dataset.pm<v-0.005}).length,df=v-pm;
  el.innerHTML='<table class="ctab"><thead><tr><th></th><td>'+nm+'<br><span style="font-weight:500;color:var(--ink2)">'+of+'</span></td><td>Il tuo</td></tr></thead><tbody><tr><th>Canone al mese</th>'+c(0,fe(pm))+c(1,fe(v))+'</tr><tr><th>All\'anno</th>'+c(0,fe(pm*12))+c(1,fe(v*12))+'</tr></tbody></table>'
   +'<p class="note">'+(Math.abs(df)<0.005?'Costano uguale.':df>0?'Con '+nm+' risparmi '+fe(df)+' al mese, '+Math.round(df*12)+' € all\'anno.':'Il tuo abbonamento costa '+fe(-df)+' in meno al mese.')+' '+(n?n+(n===1?' offerta in elenco costa':' offerte in elenco costano')+' meno del tuo.':'Nessuna offerta in elenco costa meno del tuo.')+'</p>'}
document.addEventListener('click',function(e){var b=e.target.closest('.oc-cmp');if(!b)return;CUR=b.closest('article');$('mq').value=MQ;tab();var dl=$('cdlg');if(dl.showModal)dl.showModal();else dl.setAttribute('open','');if(!MQ)$('mq').focus()});
$('cclose').addEventListener('click',function(){$('cdlg').close()});$('cdlg').addEventListener('click',function(e){if(e.target===$('cdlg'))$('cdlg').close()});
var T='tutte';function flt(){var n=0,rr=document.querySelectorAll('#nt article');rr.forEach(function(r){var q=($('ns').value||'').trim().toLowerCase(),ok=(T==='tutte'||r.dataset.cat===T)&&!($('noreg').checked&&r.dataset.reg==='1')&&(!q||r.textContent.toLowerCase().indexOf(q)>=0);r.hidden=!ok;if(ok)n++});mia();$('ncnt').textContent=n+' offerte';document.querySelectorAll('.flt button').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.t===T)})}
document.querySelectorAll('.flt button').forEach(function(b){b.addEventListener('click',function(){T=b.dataset.t;flt()})});$('noreg').addEventListener('change',flt);$('ns').addEventListener('input',flt);$('mq').addEventListener('input',function(e){MQ=e.target.value.slice(0,8);try{localStorage.setItem('mia-net',MQ)}catch(_){}mia();tab()});flt();
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
    return a / 12 + (9 if c == "luce" else 0)


def stab(o):
    if o["t"] != "f":
        return "D"
    d = o.get("d") or 0
    return "A" if 36 <= d <= 240 else "B" if 24 <= d <= 240 else "C"


def durata(o):
    d = o.get("d") or 0
    if o["t"] != "f":
        return "Variabile"
    if 12 <= d <= 240:
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
            f'<div class="oc-b"><dl class="oc-d">{dd}</dl><div class="oc-p"><div class="oc-m">{eur_big(m)}</div><div class="oc-y">{n0(m * 12 - (18 if c == "luce" else 0))} l\'anno</div>{diff}</div>'
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
    mese = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"][int(d["data_open_data"].split("-")[1]) - 1] + " " + d["data_open_data"][:4]
    desc = (f"La più conveniente oggi è {b['v']} a {n2(bm)} al mese. {len(righe)} offerte {c} {agg} di {forn} fornitori "
            f"dagli open data ARERA del {data}, ordinate per spesa. Nessuna registrazione, nessuna telefonata.")
    corpo = testata(f"/{slug}/", f"{titolo} {mese}: da {n2(bm)} al mese", desc, c, f"/img/geco-{c}.svg").replace("</style>", CSS_CL + "</style>", 1)
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
<section class="card txt"><h2 class="h">Altre classifiche</h2><div class="altre"><a href="/">Tutte le offerte luce</a><a href="/#gas">Tutte le offerte gas</a><a href="/fornitori/">Fornitori a confronto</a>{altre}</div></section>
"""
    scrivi(f"/{slug}/", corpo, "")
print("classifiche generate")


# ---------- pagine per fornitore (/offerte-<fornitore>/) ----------
FORNITORI = [  # (slug, nome mostrato, nomi nel campo v)
    ("octopus-energy", "Octopus Energy", ["Octopus Energy"]),
    ("enel", "Enel", ["Enel"]),
    ("eni-plenitude", "Eni Plenitude", ["Eni Plenitude"]),
    ("a2a", "A2A Energia", ["A2A Energia"]),
    ("edison", "Edison Energia", ["Edison Energia"]),
    ("iren", "Iren", ["Iren"]),
    ("sorgenia", "Sorgenia", ["Sorgenia"]),
    ("eon", "E.ON", ["E.ON"]),
    ("engie", "Engie", ["Engie"]),
    ("hera", "Hera Comm", ["Hera Comm"]),
    ("acea", "Acea Energia", ["Acea Energia"]),
    ("pulsee", "Pulsee (Axpo)", ["Pulsee (Axpo)", "Axpo Italia"]),
    ("illumia", "Illumia", ["Illumia"]),
    ("optima", "Optima Italia", ["Optima Italia"]),
    ("alperia", "Alperia", ["Alperia"]),
    ("sinergas", "Sinergas", ["Sinergas"]),
    ("lifegate-energy", "LifeGate Energy", ["LIFEGATE Energy"]),
    ("nen", "NeN", ["NeN (YADA)"]),
    ("estra", "Estra", ["Estra", "Estra Energie"]),
    ("poste-energia", "Poste Energia", ["Poste Energia", "Postepay"]),
    ("wind-tre-luce-gas", "WindTre Luce e Gas", ["Wind TRE Luce E GAS"]),
    ("fastweb-energia", "Fastweb Energia", ["Fastweb"]),
    ("audax", "Audax Energia", ["Audax Energía"]),
    ("cva-energie", "CVA Energie", ["CVA Energie"]),
    ("enostra", "ènostra", ["Enostra"]),
]


def _valide(c):
    d = DATI[c]; y = TIPO_Y[c]
    ok = [o for o in d["offerte"] if o.get("ok", True) and o.get("s") is not None
          and (o.get("min") is None or y >= o["min"]) and (o.get("max") is None or y <= o["max"])]
    return sorted(((o, spesa(o, c, d["reg"])) for o in ok), key=lambda x: x[1])


_TUTTE = {c: _valide(c) for c in ("luce", "gas")}
_fatti = []
for slug, nome, nomi in FORNITORI:
    per = {c: [x for x in _TUTTE[c] if x[0]["v"] in nomi] for c in ("luce", "gas")}
    if not per["luce"] and not per["gas"]:
        continue
    d = DATI["luce"]
    data = "/".join(reversed(d["data_open_data"].split("-")))
    mesi = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"]
    mese = mesi[int(d["data_open_data"].split("-")[1]) - 1] + " " + d["data_open_data"][:4]
    parti, frasi = [], []
    for c in ("luce", "gas"):
        r = per[c]
        if not r:
            continue
        b, bm = r[0]
        best = _TUTTE[c][0][1]
        pos = next(i for i, x in enumerate(_TUTTE[c]) if x[0]["v"] in nomi) + 1
        cons = "225 kWh al mese, contatore da 3 kW, imposte e canone RAI inclusi" if c == "luce" else "90 Smc al mese, imposte incluse"
        frasi.append(f"{c} da {n2(bm)} al mese")
        parti.append(f'<section class="card"><h2 class="h" style="margin:0 0 8px;font-size:22px">Offerte {c} {H.escape(nome)} ({len(r)})</h2>'
                     f'<p class="intro">La più conveniente è <strong>{H.escape(b["n"])}</strong>, {n2(bm)} al mese con {cons}. '
                     f'Su {len(_TUTTE[c])} offerte {c} del mercato libero è al {pos}° posto'
                     + (f'; la più conveniente di tutte costa {n2(best)} al mese.' if pos > 1 else ', la più conveniente di oggi.') + '</p>'
                     + "".join(scheda_en(x, i, bm, c) for i, x in enumerate(r[:12]))
                     + (f'<p class="src">Ci sono altre {len(r) - 12} offerte {c} {H.escape(nome)}: le trovi nel <a href="/?q={H.escape(nome.split(" ")[0].lower())}{"&c=gas" if c == "gas" else ""}">confronto completo</a>.</p>' if len(r) > 12 else "")
                     + "</section>")
    tit = f"Offerte {nome} luce e gas {mese}: prezzi e confronto"
    desc = (f"Le offerte {nome} di oggi dagli open data ARERA: " + ", ".join(frasi) +
            ". Prezzo, quota fissa, durata e penali, confrontati con tutto il mercato libero.")
    c0 = "luce" if per["luce"] else "gas"
    corpo = testata(f"/offerte-{slug}/", tit, desc, c0, f"/img/geco-{c0}.svg").replace("</style>", CSS_CL + "</style>", 1)
    faq = []
    for c in ("luce", "gas"):
        if per[c]:
            b, bm = per[c][0]
            faq.append((f"Qual è l'offerta {c} {nome} più conveniente oggi?", f"{b['n']}, con una spesa stimata di {n2(bm)} al mese (open data ARERA del {data})."))
    faq.append((f"{nome} conviene?", f"Dipende dai consumi. Confronta le offerte {nome} con le altre del mercato libero inserendo i tuoi consumi nel comparatore: la classifica cambia ogni giorno."))
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
                                                        {"@type": "ListItem", "position": 2, "name": "Fornitori", "item": BASE + "/fornitori/"},
                                                        {"@type": "ListItem", "position": 3, "name": nome, "item": BASE + f"/offerte-{slug}/"}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]}
    corpo = corpo.replace("</head>", '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>\n</head>", 1)
    corpo += (f'<main class="wrap pg"><h1 class="h">Offerte {H.escape(nome)} luce e gas</h1>'
              f'<p class="intro">Tutte le offerte {H.escape(nome)} pubblicate sul Portale Offerte di ARERA, con la spesa stimata e il confronto con gli altri fornitori. Dati del {data}.</p>'
              f'<a class="cta1" href="/">Confronta con tutte le offerte</a>' + "".join(parti)
              + '<section class="card txt"><h2 class="h">Domande frequenti</h2>' + "".join(f"<h3>{H.escape(q)}</h3><p>{H.escape(a)}</p>" for q, a in faq) + "</section>"
              + '<section class="card txt"><h2 class="h">Altri fornitori</h2><div class="altre">'
              + "".join(f'<a href="/offerte-{s2}/">{H.escape(n2_)}</a>' for s2, n2_, _ in FORNITORI if s2 != slug) + "</div></section>\n")
    scrivi(f"/offerte-{slug}/", corpo, "")
    _fatti.append((slug, nome, per))

# hub
d = DATI["luce"]; data = "/".join(reversed(d["data_open_data"].split("-")))
righe = "".join(f'<tr><th><a href="/offerte-{s}/">{H.escape(n)}</a></th><td>{len(p["luce"])}</td><td>{n2(p["luce"][0][1]) if p["luce"] else "–"}</td>'
                f'<td>{len(p["gas"])}</td><td>{n2(p["gas"][0][1]) if p["gas"] else "–"}</td></tr>' for s, n, p in sorted(_fatti, key=lambda x: x[2]["luce"][0][1] if x[2]["luce"] else 9e9))
corpo = testata("/fornitori/", "Fornitori luce e gas a confronto: offerte e prezzi di oggi",
                f"I principali fornitori di luce e gas del mercato libero ({len(_fatti)}) messi a confronto con gli open data ARERA: numero di offerte e spesa più bassa per luce e gas.",
                "luce", "/img/geco-luce.svg").replace("</style>", CSS_CL + "</style>", 1)
corpo += (f'<main class="wrap pg"><h1 class="h">Fornitori luce e gas a confronto</h1>'
          f'<p class="intro">Per ogni fornitore: quante offerte ha oggi sul Portale Offerte ARERA e quanto costa la più conveniente, per luce (225 kWh al mese) e gas (90 Smc al mese). Dati del {data}.</p>'
          f'<section class="card"><div class="scroll" tabindex="0"><style>.fz td{{white-space:nowrap}}</style><table class="itab fz"><thead><tr><th>Fornitore</th><th>Offerte luce</th><th>Luce da</th><th>Offerte gas</th><th>Gas da</th></tr></thead><tbody>{righe}</tbody></table></div></section>\n')
scrivi("/fornitori/", corpo, "")
_sm = (R / "sitemap.xml").read_text(encoding="utf-8")
_nuovi = ["/fornitori/"] + [f"/offerte-{s}/" for s, _, _ in _fatti]
_add = "".join(f"  <url><loc>{BASE}{u}</loc><changefreq>daily</changefreq></url>\n" for u in _nuovi if f"<loc>{BASE}{u}</loc>" not in _sm)
if _add:
    (R / "sitemap.xml").write_text(_sm.replace("</urlset>", _add + "</urlset>"), encoding="utf-8")
print("fornitori generati:", len(_fatti))


# ---------- quanto costa la potenza del contatore (/potenza-contatore/) ----------
def _pot():
    r = DATI["luce"]["reg"]; qp, al, iva = r["qp"], r["acc"], r["iva"]
    data = "/".join(reversed(DATI["luce"]["data_open_data"].split("-")))
    def acc(y, kw):
        m = y / 12; g = 150 if kw <= 1.5 else 220
        e = 0 if kw > 3 else (min(m, 150) if m <= g else max(0, 150 - (m - g)))
        return (m - e) * 12 * al
    def extra(kw, y):
        return (1 + iva) * (qp * (kw - 3) + acc(y, kw) - acc(y, 3))
    kws = [3.5, 4, 4.5, 5, 6]
    righe = "".join(f"<tr><th>{str(k).replace('.', ',')} kW</th><td>+{n2(extra(k, 1800))}</td><td>+{n2(extra(k, 2700))}</td><td>+{n2(extra(k, 2700) / 12)}</td></tr>" for k in kws)
    e45 = extra(4.5, 2700)
    tit = "Contatore 3 kW o 4,5 kW: quanto costa di più in bolletta"
    desc = (f"Passare da 3 a 4,5 kW costa circa {n0(e45)} l'anno in più in bolletta con 2.700 kWh di consumo, IVA inclusa. "
            "Tabella per ogni potenza con le tariffe ARERA in vigore e calcolatore sui tuoi consumi.")
    faq = [("Quanto costa passare da 3 a 4,5 kW?", f"In bolletta circa {n0(e45)} l'anno in più con 2.700 kWh di consumo (IVA inclusa): {n2(qp * 1.5 * (1 + iva))} di quota potenza più le accise che oltre i 3 kW si pagano anche sui primi kWh. A questo si aggiunge una volta il contributo per l'aumento di potenza, che dipende dal distributore."),
           ("Perché oltre i 3 kW pago più accise?", "Per le abitazioni di residenza con potenza fino a 3 kW i primi 150 kWh al mese sono esenti da accisa. Sopra i 3 kW l'esenzione non spetta."),
           ("Quanto costa ogni kW in più?", f"La quota potenza ARERA vale {n2(qp)} per kW all'anno, {n2(qp * (1 + iva))} con l'IVA al 10%.")]
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    corpo = testata("/potenza-contatore/", tit, desc, "luce", "/img/geco-luce.svg").replace("</style>", CSS_CL + "</style>", 1)
    corpo = corpo.replace("</head>", '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>\n</head>", 1)
    corpo += (f'<main class="wrap pg"><h1 class="h">Contatore 3 kW o 4,5 kW: quanto costa di più</h1>'
              f'<p class="intro">Ogni kW di potenza in più costa <strong>{n2(qp * (1 + iva))} l\'anno</strong> di quota potenza, IVA inclusa. In più, oltre i 3 kW perdi l\'esenzione dall\'accisa sui primi 150 kWh al mese. Con 2.700 kWh l\'anno, passare a 4,5 kW costa circa <strong>{n0(e45)} l\'anno</strong> in più.</p>'
              '<section class="card"><h2 class="h" style="margin:0 0 8px;font-size:22px">Calcola sui tuoi consumi</h2>'
              '<p><label>Consumo annuo (kWh) <input id="pk" type="number" min="0" step="100" value="2700" inputmode="numeric" style="max-width:140px"></label> '
              '<label>Potenza <select id="pw"><option>3,5</option><option>4</option><option selected>4,5</option><option>5</option><option>6</option></select> kW</label></p>'
              '<p class="intro" id="pr" style="margin:8px 0 0"></p></section>'
              f'<section class="card"><h2 class="h" style="margin:0 0 8px;font-size:22px">Costo in più rispetto a 3 kW</h2><div class="scroll" tabindex="0"><table class="itab fz"><thead><tr><th>Potenza</th><th>1.800 kWh/anno</th><th>2.700 kWh/anno</th><th>Al mese (2.700 kWh)</th></tr></thead><tbody>{righe}</tbody></table></div>'
              f'<p class="src">Abitazione di residenza, IVA 10%. Quota potenza ({n2(qp)} per kW all\'anno) e accise ({str(al).replace(".", ",")} €/kWh) dalle tariffe ARERA in vigore al {data}. Non include il contributo una tantum per l\'aumento di potenza.</p></section>'
              '<section class="card txt"><h2 class="h">Domande frequenti</h2>' + "".join(f"<h3>{H.escape(q)}</h3><p>{H.escape(a)}</p>" for q, a in faq) + "</section>"
              '<section class="card txt"><h2 class="h">Confronta le offerte</h2><div class="altre"><a href="/">Tutte le offerte luce</a><a href="/offerte-luce-prezzo-fisso/">Luce prezzo fisso</a><a href="/fornitori/">Fornitori a confronto</a></div></section>\n')
    js = ("var QP=%s,AL=%s,IVA=%s;function acc(y,kw){var m=y/12,g=kw<=1.5?150:220,e=kw>3?0:(m<=g?Math.min(m,150):Math.max(0,150-(m-g)));return (m-e)*12*AL}"
          "function f(n){return n.toLocaleString('it-IT',{minimumFractionDigits:2,maximumFractionDigits:2})+' €'}"
          "function up(){var y=+$('pk').value||0,kw=parseFloat($('pw').value.replace(',','.')),x=(1+IVA)*(QP*(kw-3)+acc(y,kw)-acc(y,3));"
          "$('pr').innerHTML='Con '+y.toLocaleString('it-IT')+' kWh l\\'anno, a '+$('pw').value+' kW paghi <strong>'+f(x)+' l\\'anno in più</strong> ('+f(x/12)+' al mese) rispetto a 3 kW.'}"
          "$('pk').addEventListener('input',up);$('pw').addEventListener('change',up);up();") % (qp, al, iva)
    scrivi("/potenza-contatore/", corpo, js)
    sm = (R / "sitemap.xml").read_text(encoding="utf-8")
    if f"<loc>{BASE}/potenza-contatore/</loc>" not in sm:
        (R / "sitemap.xml").write_text(sm.replace("</urlset>", f"  <url><loc>{BASE}/potenza-contatore/</loc><changefreq>monthly</changefreq></url>\n</urlset>"), encoding="utf-8")
    print("potenza contatore:", n2(e45))
_pot()


# ---------- costo kWh, elettrodomestici, calcolo bolletta ----------
def _kwh():
    d = DATI["luce"]; r = d["reg"]; y = TIPO_Y["luce"]
    data = "/".join(reversed(d["data_open_data"].split("-")))
    tutte = _TUTTE["luce"]
    best_o, best_m = tutte[0]
    med_o, med_m = tutte[len(tutte) // 2]
    pb = best_o["pd"] if best_o.get("pd") is not None else best_o["p"]
    pm = med_o["pd"] if med_o.get("pd") is not None else med_o["p"]
    marg = lambda pp: (1 + r["iva"]) * (pp + r["rv"] + r["acc"])  # costo di 1 kWh in più, tutto incluso
    tot = lambda m: (m - 9) * 12 / y  # costo medio per kWh, tutto incluso, senza canone RAI
    mb, mm = marg(pb), marg(pm)
    sm = (R / "sitemap.xml").read_text(encoding="utf-8")
    def addsm(u):
        nonlocal sm
        if f"<loc>{BASE}{u}</loc>" not in sm:
            sm = sm.replace("</urlset>", f"  <url><loc>{BASE}{u}</loc><changefreq>daily</changefreq></url>\n</urlset>")
    def pagina(path, tit, desc, h1, intro, sezioni, faq, js):
        ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
        corpo = testata(path, tit, desc, "luce", "/img/geco-luce.svg").replace("</style>", CSS_CL + ".pg label{display:block;margin:10px 0;font-weight:600}.pg label input,.pg label select{display:block;margin-top:4px;font:inherit;font-weight:400;padding:8px 10px;border:1px solid var(--bd);border-radius:8px;background:var(--card);color:var(--ink)}</style>", 1)
        corpo = corpo.replace("</head>", '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>\n</head>", 1)
        corpo += (f'<main class="wrap pg"><h1 class="h">{h1}</h1><p class="intro">{intro}</p>' + sezioni
                  + '<section class="card txt"><h2 class="h">Domande frequenti</h2>' + "".join(f"<h3>{H.escape(q)}</h3><p>{H.escape(a)}</p>" for q, a in faq) + "</section>"
                  + '<section class="card txt"><h2 class="h">Vedi anche</h2><div class="altre"><a href="/">Confronta le offerte luce</a><a href="/costo-kwh/">Costo del kWh oggi</a><a href="/consumo-elettrodomestici/">Consumo elettrodomestici</a><a href="/calcolo-bolletta-luce/">Calcolo bolletta luce</a><a href="/potenza-contatore/">Contatore 3 o 4,5 kW</a><a href="/fornitori/">Fornitori a confronto</a></div></section>\n')
        scrivi(path, corpo, js)
        addsm(path)
    n4e = lambda v: f"{v:.3f}".replace(".", ",") + " €"
    fonte = f'<p class="src">Prezzi delle offerte dal Portale Offerte ARERA, tariffe di rete, oneri e accise ARERA in vigore. Dati del {data}. Abitazione di residenza, 3 kW, IVA 10%.</p>'
    # 1) costo kWh
    pagina("/costo-kwh/", f"Costo kWh luce oggi: {n4e(mb)} tutto incluso con l'offerta più conveniente",
           f"Quanto costa oggi un kWh di luce, tasse comprese: {n4e(mb)} con l'offerta più conveniente, {n4e(mm)} con un'offerta nella media. Dati ARERA del {data}.",
           "Quanto costa un kWh di luce oggi",
           f"Ogni kWh che consumi in più costa oggi <strong>{n4e(mb)}</strong> con l'offerta più conveniente ({H.escape(best_o['v'])}) e <strong>{n4e(mm)}</strong> con un'offerta nella media del mercato, tutto compreso: energia, trasporto, oneri, accise e IVA.",
           '<section class="card"><h2 class="h" style="margin:0 0 8px;font-size:22px">Il prezzo del kWh in bolletta</h2><div class="scroll" tabindex="0"><table class="itab fz"><thead><tr><th></th><th>Offerta più conveniente</th><th>Offerta media</th></tr></thead><tbody>'
           f'<tr><th>Prezzo energia del venditore</th><td>{n4e(pb)}</td><td>{n4e(pm)}</td></tr>'
           f'<tr><th>Ogni kWh in più, tutto incluso</th><td>{n4e(mb)}</td><td>{n4e(mm)}</td></tr>'
           f'<tr><th>Costo medio per kWh con 2.700 kWh l\'anno (quote fisse comprese)</th><td>{n4e(tot(best_m))}</td><td>{n4e(tot(med_m))}</td></tr>'
           '</tbody></table></div>' + fonte + '</section>',
           [("Quanto costa un kWh di luce oggi?", f"Tutto incluso, {n4e(mb)} con l'offerta più conveniente e {n4e(mm)} con un'offerta nella media (dati ARERA del {data})."),
            ("Perché il prezzo del kWh in bolletta è più alto di quello dell'offerta?", "Al prezzo dell'energia del venditore si aggiungono trasporto e gestione del contatore, oneri di sistema, accise e IVA, che decidono ARERA e lo Stato e sono uguali per tutti i venditori."),
            ("Che differenza c'è tra costo del kWh in più e costo medio?", "Il costo del kWh in più conta solo le voci che crescono con i consumi: serve per sapere quanto costa usare un elettrodomestico. Il costo medio divide tutta la bolletta per i kWh consumati, quindi comprende anche le quote fisse.")],
           "")
    # 2) elettrodomestici
    js = ("var MB=%s,MM=%s;function f(n){return n.toLocaleString('it-IT',{minimumFractionDigits:2,maximumFractionDigits:2})+' €'}"
          "function up(){var k=+$('ek').value||0;$('er').innerHTML='Con '+k.toLocaleString('it-IT')+' kWh l\\'anno spendi <strong>'+f(k*MB)+' l\\'anno</strong> con l\\'offerta più conveniente e '+f(k*MM)+' con un\\'offerta nella media ('+f(k*MB/12)+' – '+f(k*MM/12)+' al mese).'}"
          "function up2(){var k=+$('ck').value||0,n=+$('cn').value||0;$('cr').innerHTML='Un ciclo costa <strong>'+f(k*MB)+'</strong> ('+f(k*MM)+' con un\\'offerta media); con '+n+' cicli a settimana spendi '+f(k*MB*n*52)+' l\\'anno.'}"
          "$('ek').addEventListener('input',up);$('ck').addEventListener('input',up2);$('cn').addEventListener('input',up2);up();up2();") % (round(mb, 5), round(mm, 5))
    pagina("/consumo-elettrodomestici/", "Quanto costa un elettrodomestico in bolletta: calcolo dall'etichetta energetica",
           f"Calcola quanto ti costano frigorifero, lavatrice o lavastoviglie: inserisci i kWh dell'etichetta energetica. Prezzo del kWh di oggi {n4e(mb)} tutto incluso, dati ARERA.",
           "Quanto costa un elettrodomestico in bolletta",
           f"Il consumo è scritto sull'etichetta energetica: in kWh all'anno per frigoriferi e congelatori, in kWh ogni 100 cicli per lavatrici e lavastoviglie. Moltiplicato per il prezzo del kWh di oggi, <strong>{n4e(mb)}</strong> tutto incluso con l'offerta più conveniente, dà il costo in bolletta.",
           '<section class="card"><h2 class="h" style="margin:0 0 8px;font-size:22px">Frigorifero, congelatore, TV</h2>'
           '<p><label>Consumo dall\'etichetta (kWh all\'anno) <input id="ek" type="number" min="0" step="10" value="200" inputmode="numeric" style="max-width:140px"></label></p><p class="intro" id="er" style="margin:8px 0 0"></p></section>'
           '<section class="card"><h2 class="h" style="margin:0 0 8px;font-size:22px">Lavatrice e lavastoviglie</h2>'
           '<p><label>kWh per ciclo <input id="ck" type="number" min="0" step="0.05" value="0.7" inputmode="decimal" style="max-width:120px"></label> '
           '<label>Cicli a settimana <input id="cn" type="number" min="0" step="1" value="4" inputmode="numeric" style="max-width:90px"></label></p>'
           '<p class="note">Sull\'etichetta trovi i kWh per 100 cicli: dividi per 100. Es. 70 kWh/100 cicli = 0,7 kWh per ciclo.</p><p class="intro" id="cr" style="margin:8px 0 0"></p>' + fonte + '</section>',
           [("Come calcolo quanto consuma un elettrodomestico?", "Prendi i kWh dall'etichetta energetica e moltiplicali per il prezzo del kWh tutto incluso. Per lavatrici e lavastoviglie l'etichetta indica i kWh ogni 100 cicli."),
            ("Quale prezzo del kWh usate?", f"Il costo di ogni kWh in più con tutte le voci della bolletta: {n4e(mb)} con l'offerta più conveniente e {n4e(mm)} con un'offerta nella media, aggiornato ogni giorno con i dati ARERA.")],
           js)
    # 3) calcolo bolletta
    js = ("var R=%s,PM=%s,FM=%s;function f(n){return n.toLocaleString('it-IT',{minimumFractionDigits:2,maximumFractionDigits:2})+' €'}"
          "function acc(y,kw){var m=y/12,g=kw<=1.5?150:220,e=kw>3?0:(m<=g?Math.min(m,150):Math.max(0,150-(m-g)));return (m-e)*12*R.acc}"
          "function up(){var km=+$('bk').value||0,kw=parseFloat($('bw').value.replace(',','.')),p=+String($('bp').value).replace(',','.')||0,fx=+String($('bf').value).replace(',','.')||0,y=km*12;"
          "var en=p*y+fx*12,rete=R.rf+R.qp*(kw-3)+R.rv*y,a=acc(y,kw),iva=(en+rete+a)*R.iva,tot=en+rete+a+iva;"
          "var row=function(t,v){return '<tr><th>'+t+'</th><td>'+f(v/12)+'</td><td>'+f(v)+'</td></tr>'};"
          "$('bt').innerHTML=row('Energia e quota fissa del venditore',en)+row('Trasporto, contatore e oneri di sistema',rete)+row('Accise',a)+row('IVA 10%%',iva)+'<tr class=\"tot\"><th><b>Totale (senza canone RAI)</b></th><td><b>'+f(tot/12)+'</b></td><td><b>'+f(tot)+'</b></td></tr>'}"
          "['bk','bw','bp','bf'].forEach(function(i){$(i).addEventListener('input',up)});up();") % (json.dumps(r), round(pm, 4), round(med_o["fx"] / 12, 2))
    pagina("/calcolo-bolletta-luce/", "Calcolo bolletta luce: quanto pagherai, voce per voce",
           "Calcola la bolletta della luce dai tuoi consumi: energia, trasporto, oneri, accise e IVA, con le tariffe ARERA in vigore. Gratis, senza registrazione.",
           "Calcolo della bolletta luce",
           "Inserisci i consumi e le condizioni della tua offerta (le trovi in bolletta o nella scheda dell'offerta): il calcolo usa le tariffe di rete, gli oneri e le accise in vigore. I valori proposti sono quelli di un'offerta nella media di oggi.",
           '<section class="card"><p><label>Consumo al mese (kWh) <input id="bk" type="number" min="0" step="10" value="225" inputmode="numeric" style="max-width:120px"></label> '
           '<label>Potenza <select id="bw"><option>3</option><option>3,5</option><option>4</option><option>4,5</option><option>5</option><option>6</option></select> kW</label></p>'
           f'<p><label>Prezzo energia (€/kWh) <input id="bp" type="number" min="0" step="0.001" value="{round(pm, 4)}" inputmode="decimal" style="max-width:120px"></label> '
           f'<label>Quota fissa venditore (€/mese) <input id="bf" type="number" min="0" step="0.5" value="{round(med_o["fx"] / 12, 2)}" inputmode="decimal" style="max-width:110px"></label></p>'
           '<div class="scroll" tabindex="0"><table class="ctab dtab"><thead><tr><th></th><td>Al mese</td><td>All\'anno</td></tr></thead><tbody id="bt"></tbody></table></div>' + fonte
           + '<p class="note">Il canone RAI (90 € l\'anno, 9 € al mese da gennaio a ottobre) si aggiunge in bolletta.</p></section>',
           [("Come si calcola la bolletta della luce?", "Si sommano la spesa per l'energia del venditore (prezzo per kWh e quota fissa), il trasporto e gli oneri di sistema decisi da ARERA, le accise e l'IVA al 10% per le abitazioni."),
            ("Quanto costa la luce al mese per una famiglia?", f"Con 225 kWh al mese (2.700 l'anno) e un contatore da 3 kW, oggi si va da {n2(best_m)} al mese con l'offerta più conveniente a {n2(med_m)} con un'offerta nella media, canone RAI compreso.")],
           js)
    (R / "sitemap.xml").write_text(sm, encoding="utf-8")
    print("kwh:", n4e(mb), n4e(mm))
_kwh()


# ---------- sitemap con data di aggiornamento ----------
_oggi = _dt.date.today().isoformat()
_sm = (R / "sitemap.xml").read_text(encoding="utf-8")
_sm = re.sub(r"\s*<lastmod>[^<]*</lastmod>", "", _sm)
_sm = re.sub(r"(<loc>[^<]*</loc>)", r"\1<lastmod>" + _oggi + "</lastmod>", _sm)
(R / "sitemap.xml").write_text(_sm, encoding="utf-8")


# --- Titolo e descrizione della home con mese e offerta luce più conveniente del giorno (per i clic da Google su "offerte luce")
def _home():
    d = DATI["luce"]; y = TIPO_Y["luce"]
    ok = [o for o in d["offerte"] if o.get("ok", True) and o.get("s") is not None
          and (o.get("min") is None or y >= o["min"]) and (o.get("max") is None or y <= o["max"])]
    if not ok:
        return
    o, m = min(((o, spesa(o, "luce", d["reg"])) for o in ok), key=lambda x: x[1])
    mesi = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"]
    mese = mesi[int(d["data_open_data"].split("-")[1]) - 1] + " " + d["data_open_data"][:4]
    t = f"Offerte luce e gas {mese}: le più convenienti di oggi, da {n2(m)} al mese"
    ds = (f"Offerte luce e gas di oggi dagli open data ARERA: la luce più conveniente è {o['v']} a {n2(m)} al mese. "
          "Spesa, prezzo, quota fissa e scadenza. Nessuna registrazione, nessuna telefonata.")
    p = R / "index.html"; s = p.read_text(encoding="utf-8")
    s = re.sub(r"<title>.*?</title>", f"<title>{H.escape(t, quote=False)}</title>", s, count=1)
    for k in ('name="description"', 'property="og:description"'):
        s = re.sub(r'(<meta ' + k + r' content=")[^"]*', lambda mm: mm.group(1) + H.escape(ds), s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda mm: mm.group(1) + H.escape(t), s, count=1)
    p.write_text(s, encoding="utf-8")
    print("home:", t)
_home()
