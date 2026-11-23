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
import urllib.parse
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


import datetime as _dt
import html as _html
import re as _re

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"}
MANCANTI = DIR / "mancanti.json"
mancanti = json.loads(MANCANTI.read_text()) if MANCANTI.exists() else {}
oggi = _dt.date.today()


def get(u, n=400_000):
    req = urllib.request.Request(u, headers=UA)
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.status, r.headers.get("Content-Type", ""), r.read(n), r.geturl()


def immagine(b, ct):
    if len(b) < 100 or b.lstrip()[:1] == b"<":  # niente SVG o HTML: il .ico deve essere un'immagine raster
        return False
    if b[:4] in (b"\x89PNG", b"\x00\x00\x01\x00", b"GIF8") or b[:3] == b"\xff\xd8\xff" or b[:4] == b"RIFF":
        return True
    return "image" in ct and "svg" not in ct


def scarica(d):
    f = DIR / f"{d}.ico"
    if f.exists():
        return
    ult = mancanti.get(d)
    if ult and (oggi - _dt.date.fromisoformat(ult)).days < 7:
        return  # già cercato da poco senza risultato
    fonti = [f"https://icons.duckduckgo.com/ip3/{d}.ico", f"https://www.google.com/s2/favicons?domain={d}&sz=128"]
    try:  # icone dichiarate dal sito stesso
        st, ct, b, fin = get(f"https://www.{d}/" if d.count(".") == 1 else f"https://{d}/")
        t = b.decode("utf-8", "replace")
        for m in _re.finditer(r"<link[^>]+>", t, _re.I):
            tag = m.group(0)
            if _re.search(r'rel=["\'][^"\']*(apple-touch-icon|icon)', tag, _re.I):
                h = _re.search(r'href=["\']([^"\']+)', tag)
                if h and not h.group(1).lower().endswith(".svg"):
                    fonti.append(urllib.parse.urljoin(fin, _html.unescape(h.group(1))))
        fonti.append(urllib.parse.urljoin(fin, "/favicon.ico"))
    except Exception:
        fonti.append(f"https://{d}/favicon.ico")
    for u in fonti:
        try:
            st, ct, b, _ = get(u, 200_000)
            if st == 200 and immagine(b, ct):
                f.write_bytes(b)
                mancanti.pop(d, None)
                return
        except Exception:
            continue
    mancanti[d] = oggi.isoformat()


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
# fornitori senza link nelle offerte: dominio dall'elenco dei marchi (dominio -> nome)
marchi = json.loads((R / "data" / "marchi.json").read_text()) if (R / "data" / "marchi.json").exists() else {}
nome_dom = {v: k for k, v in marchi.items()}
domini |= {nome_dom[o.get("v")] for p in file_offerte if p.exists() for o in json.loads(p.read_text())["offerte"] if not o.get("u") and o.get("v") in nome_dom}
domini.discard(None)
with cf.ThreadPoolExecutor(16) as ex:
    list(ex.map(scarica, sorted(domini)))
MANCANTI.write_text(json.dumps(mancanti, indent=0, sort_keys=True))
ci = {f.stem for f in DIR.glob("*.ico")}
# fornitori senza link: uso il dominio di un'altra offerta dello stesso fornitore
per_nome = {n: d for n, d in nome_dom.items() if d in ci}
for p in file_offerte:
    if p.exists():
        for o in json.loads(p.read_text())["offerte"]:
            x = dominio(o.get("u"))
            if x in ci:
                per_nome.setdefault(o.get("v"), x)
for p in file_offerte:
    if p.exists():
        d = json.loads(p.read_text())
        for o in d["offerte"]:
            x = dominio(o.get("u"))
            x = x if x in ci else per_nome.get(o.get("v"))
            if x:
                o["lg"] = x
            else:
                o.pop("lg", None)
        p.write_text(json.dumps(d, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"loghi: {len(ci)} disponibili su {len(domini)} domini")
