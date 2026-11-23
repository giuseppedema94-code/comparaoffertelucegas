#!/usr/bin/env python3
"""Sonda manuale (workflow sonda-internet): per ogni operatore prova gli URL candidati e
i link "fibra/internet/offerte" della home, e salva testo e prezzi trovati.
Serve solo a scoprire le pagine da cui leggere i prezzi; non gira tutti i giorni."""
import concurrent.futures as cf, gzip, html, json, re, sys, urllib.parse, urllib.request, pathlib
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "sonde"); OUT.mkdir(parents=True, exist_ok=True)
OPS = json.loads((pathlib.Path(__file__).parent / "sonda_operatori.json").read_text())
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"
P = re.compile(r"\d{1,3}[,.]\d{2}\s?(?:€|euro)", re.I)

def get(u):
    req = urllib.request.Request(u, headers={"User-Agent": UA, "Accept-Language": "it-IT,it;q=0.9", "Accept": "text/html,*/*"})
    with urllib.request.urlopen(req, timeout=25) as r:
        b = r.read(3_000_000)
        if r.headers.get("Content-Encoding") == "gzip": b = gzip.decompress(b)
        return r.status, r.geturl(), b.decode("utf-8", "replace")

def testo(raw):
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t)))

def prova(u):
    try:
        st, fin, raw = get(u)
        t = testo(raw)
        return {"url": u, "status": st, "final": fin, "prezzi": len(P.findall(t)), "esempi": P.findall(t)[:12],
                "fibra": len(re.findall(r"fibra|FTTH|Gbit|Gbps|Mbps", t, re.I)), "raw": raw, "testo": t}
    except Exception as e:
        return {"url": u, "errore": repr(e)[:160]}

def operatore(o):
    res = []
    viste = set()
    for u in o["url"]:
        r = prova(u); viste.add(u); res.append(r)
    # link interessanti dalla home del dominio
    dom = urllib.parse.urlparse(o["url"][0]).netloc if o["url"] else None
    if dom:
        h = prova(f"https://{dom}/"); res.append(h)
        if h.get("raw"):
            base = h["final"]
            links = re.findall(r'href="([^"#]+)"', h["raw"])
            cand = []
            for l in links:
                a = urllib.parse.urljoin(base, html.unescape(l))
                if re.search(r"fibra|internet|offert|casa|connettiv|ftth|wifi", a, re.I) and urllib.parse.urlparse(a).netloc.endswith(dom.split(".", 1)[-1]) and a not in viste and not a.endswith((".pdf", ".jpg", ".png")):
                    cand.append(a); viste.add(a)
            for a in cand[:6]:
                res.append(prova(a))
    best = sorted([r for r in res if r.get("testo")], key=lambda r: (r["prezzi"] > 0) * (r["fibra"] + r["prezzi"]), reverse=True)
    for i, r in enumerate(best[:3]):
        (OUT / f"{o['k']}_{i}.txt").write_text(r["final"] + "\n" + r["testo"][:200000], encoding="utf-8")
    return {"k": o["k"], "nome": o["nome"], "tipo": o["tipo"], "area": o["area"],
            "pagine": [{k: v for k, v in r.items() if k not in ("raw", "testo")} for r in res]}

with cf.ThreadPoolExecutor(16) as ex:
    rep = list(ex.map(operatore, OPS))
(OUT / "riepilogo.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
print(sum(1 for o in rep for p in o["pagine"] if p.get("prezzi")), "pagine con prezzi")
