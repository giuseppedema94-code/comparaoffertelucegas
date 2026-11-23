#!/usr/bin/env python3
"""Sonda manuale: verifica i siti candidati dei fornitori senza link (nome presente nella home)."""
import concurrent.futures as cf, html, json, re, sys, urllib.request, pathlib
OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
C = json.loads((pathlib.Path(__file__).parent / "siti_candidati.json").read_text())
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/131.0 Safari/537.36"}
def prova(nome, dom):
    for u in (f"https://www.{dom}/", f"https://{dom}/"):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=20) as r:
                t = html.unescape(r.read(800_000).decode("utf-8", "replace")).lower()
                fin = r.geturl()
            parole = [w for w in re.findall(r"[a-z0-9]{3,}", nome.lower()) if w not in ("energia", "energie", "gas", "luce", "spa", "srl", "power", "and")]
            ok = sum(1 for w in parole if w in t)
            return {"url": fin, "parole": parole, "trovate": ok, "luce_gas": ("luce" in t or "energia" in t)}
        except Exception as e:
            err = repr(e)[:100]
    return {"errore": err}
res = {}
with cf.ThreadPoolExecutor(16) as ex:
    fut = {(n, d): ex.submit(prova, n, d) for n, ds in C.items() for d in ds}
    for (n, d), f in fut.items():
        res.setdefault(n, {})[d] = f.result()
(OUT / "siti.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
print("ok")
