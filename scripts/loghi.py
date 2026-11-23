#!/usr/bin/env python3
"""Scarica i loghi dei fornitori una volta sola e li serve dal nostro dominio.

Prima il browser li chiedeva a icons.duckduckgo.com: alcuni browser o estensioni lo
bloccano e i loghi sparivano. Qui li salviamo in img/loghi/<dominio>.ico e aggiungiamo
il campo "lg" alle offerte che hanno un logo.
"""
import concurrent.futures as cf
import json
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

R = Path(__file__).resolve().parent.parent
DIR = R / "img" / "loghi"
DIR.mkdir(parents=True, exist_ok=True)


def dominio(u):
    if not u:
        return None
    if not u.startswith("http"):
        u = "https://" + u
    h = urlparse(u).netloc.lower().split(":")[0].split(".")
    return ".".join(h[-2:]) if len(h) >= 2 else None


def scarica(d):
    f = DIR / f"{d}.ico"
    if f.exists():
        return
    try:
        req = urllib.request.Request(f"https://icons.duckduckgo.com/ip3/{d}.ico", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            b = r.read(200_000)
            if r.status == 200 and len(b) > 100:
                f.write_bytes(b)
    except Exception:
        pass  # 404 = nessun logo: resta l'iniziale


file_offerte = [R / "data" / n for n in ("luce.json", "gas.json", "dual.json")]
domini = set()
for p in file_offerte:
    if p.exists():
        domini |= {dominio(o.get("u")) for o in json.loads(p.read_text())["offerte"]}
for n in ("internet.json", "internet_auto.json"):
    p = R / "data" / n
    if p.exists():
        d = json.loads(p.read_text())
        righe = d if isinstance(d, list) else d.get("internet", []) + d.get("bundle", [])
        domini |= {dominio(x.get("url")) for x in righe}
domini.discard(None)
with cf.ThreadPoolExecutor(16) as ex:
    list(ex.map(scarica, sorted(domini)))
ci = {f.stem for f in DIR.glob("*.ico")}
for p in file_offerte:
    if p.exists():
        d = json.loads(p.read_text())
        for o in d["offerte"]:
            x = dominio(o.get("u"))
            if x in ci:
                o["lg"] = x
            else:
                o.pop("lg", None)
        p.write_text(json.dumps(d, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"loghi: {len(ci)} disponibili su {len(domini)} domini")
