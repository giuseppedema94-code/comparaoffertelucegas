#!/usr/bin/env python3
"""Loghi dei fornitori, serviti dal nostro dominio in img/loghi/<dominio>.png.

Per ogni dominio raccoglie più fonti (icona "apple-touch-icon" del sito, icone dichiarate
nella pagina, Google, DuckDuckGo, favicon.ico), tiene l'immagine più grande e la salva
come PNG 128x128 con sfondo trasparente. I loghi sotto i 96 pixel vengono ricercati una
volta a settimana, finché non se ne trova uno migliore. Aggiunge il campo "lg" alle offerte.
"""
import concurrent.futures as cf
import datetime as dt
import html
import io
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

from PIL import Image

try:
    import cairosvg  # facoltativo: permette di usare anche le icone SVG dei siti
except Exception:
    cairosvg = None

R = Path(__file__).resolve().parent.parent
DIR = R / "img" / "loghi"
DIR.mkdir(parents=True, exist_ok=True)
STATO = DIR / "stato.json"  # dominio -> {"px": lato originale, "data": ultimo tentativo}
stato = json.loads(STATO.read_text()) if STATO.exists() else {}
oggi = dt.date.today()
LATO = 128
BUONO = 96
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"}


def dominio(u):
    if not u:
        return None
    if not u.startswith("http"):
        u = "https://" + u
    h = urlparse(u).netloc.lower().split(":")[0].split(".")
    return ".".join(h[-2:]) if len(h) >= 2 else None


def get(u, n=600_000):
    req = urllib.request.Request(u, headers=UA)
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.status, r.read(n), r.geturl()


def apri(b):
    """Restituisce un'immagine PIL (il frame più grande per gli .ico) o None."""
    if len(b) < 100:
        return None
    if b.lstrip()[:5].lower().startswith((b"<svg", b"<?xml")) and cairosvg:
        try:
            b = cairosvg.svg2png(bytestring=b, output_width=512)
        except Exception:
            return None
    try:
        im = Image.open(io.BytesIO(b))
        if im.format == "ICO":
            dims = sorted(im.ico.sizes(), key=lambda s: s[0] * s[1])
            if dims:
                im.size = dims[-1]
        im.load()
        return im.convert("RGBA")
    except Exception:
        return None


def pieno(im):
    """Quota di pixel visibili e non bianchi: scarta icone vuote o quasi bianche."""
    px = im.convert("RGBA").resize((64, 64)).getdata()
    return sum(1 for r, g, b, a in px if a > 40 and not (r > 235 and g > 235 and b > 235)) / 4096


def candidati(d):
    """Restituisce (icone, loghi): icone del sito e immagini del logo nella testata."""
    host = f"www.{d}" if d.count(".") == 1 else d
    icone, loghi = [], []
    try:
        st, b, fin = get(f"https://{host}/")
        t = b.decode("utf-8", "replace")
        for tag in re.findall(r"<link[^>]+>", t, re.I):
            if re.search(r'rel=["\'][^"\']*(apple-touch-icon|icon)', tag, re.I):
                h = re.search(r'href=["\']([^"\']+)', tag)
                if h:
                    icone.append(urllib.parse.urljoin(fin, html.unescape(h.group(1))))
        for tag in re.findall(r"<img[^>]+>", t, re.I)[:80]:
            if re.search(r"logo", tag, re.I):
                h = re.search(r'\ssrc=["\']([^"\']+)', tag)
                if h and not h.group(1).startswith("data:"):
                    loghi.append(urllib.parse.urljoin(fin, html.unescape(h.group(1))))
        icone += [urllib.parse.urljoin(fin, "/apple-touch-icon.png"), urllib.parse.urljoin(fin, "/favicon.ico")]
    except Exception:
        icone += [f"https://{host}/apple-touch-icon.png", f"https://{host}/favicon.ico"]
    icone += [f"https://www.google.com/s2/favicons?domain={d}&sz=256", f"https://icons.duckduckgo.com/ip3/{d}.ico"]
    return list(dict.fromkeys(icone)), list(dict.fromkeys(loghi))[:4]


def salva(im, f):
    w, h = im.size
    # taglia i bordi trasparenti o bianchi
    mask = Image.eval(im.convert("RGBA").split()[3], lambda a: 255 if a > 40 else 0)
    chiaro = im.convert("L").point(lambda v: 0 if v > 235 else 255)
    bb = Image.composite(chiaro, Image.new("L", im.size, 0), mask).getbbox()
    if bb and (bb[2] - bb[0]) > 8 and (bb[3] - bb[1]) > 8:
        m = max(2, round(max(bb[2] - bb[0], bb[3] - bb[1]) * 0.04))
        im = im.crop((max(0, bb[0] - m), max(0, bb[1] - m), min(w, bb[2] + m), min(h, bb[3] + m)))
        w, h = im.size
    if max(w, h) < 28 or pieno(im) < 0.02:
        return False  # troppo piccolo o quasi invisibile su sfondo bianco: meglio l'iniziale
    k = min(LATO / w, LATO / h)
    if k != 1:  # adatto al riquadro: il browser lo mostra a 40 px, quindi resta nitido
        im = im.resize((max(1, round(w * k)), max(1, round(h * k))), Image.LANCZOS)
    tela = Image.new("RGBA", (LATO, LATO), (0, 0, 0, 0))
    tela.paste(im, ((LATO - im.width) // 2, (LATO - im.height) // 2), im)
    tela.save(f, optimize=True)
    return True


def cerca(d):
    f = DIR / f"{d}.png"
    s = stato.get(d, {})
    if f.exists() and s.get("px", 0) >= BUONO:
        return
    if s.get("data") and (oggi - dt.date.fromisoformat(s["data"])).days < 7:
        return
    migliore, lato = None, s.get("px", 0) if f.exists() else 0
    vecchio = DIR / f"{d}.ico"  # logo già scaricato con la versione precedente
    if vecchio.exists() and not f.exists():
        im = apri(vecchio.read_bytes())
        if im is not None and pieno(im) >= 0.01:
            migliore, lato = im, min(im.size)
    icone, loghi = candidati(d)

    def scarica_img(u):
        try:
            st, b, _ = get(u)
        except Exception:
            return None
        if st != 200:
            return None
        im = apri(b)
        return im if im is not None and pieno(im) >= 0.01 else None

    for u in icone:
        im = scarica_img(u)
        if im is not None and min(im.size) > lato and min(im.size) >= 16:
            migliore, lato = im, min(im.size)
        if lato >= 180:
            break
    if lato < BUONO:  # icone piccole: provo il logo nella testata del sito (spesso SVG, quindi nitido)
        for u in loghi:
            im = scarica_img(u)
            if im is not None and max(im.size) >= 120:
                migliore, lato = im, max(BUONO, min(im.size))
                break
    if migliore is not None and not salva(migliore, f):
        f.unlink(missing_ok=True)
        lato = 0
    stato[d] = {"px": lato, "data": oggi.isoformat()}


file_offerte = [R / "data" / n for n in ("luce.json", "gas.json", "dual.json")]
marchi = json.loads((R / "data" / "marchi.json").read_text()) if (R / "data" / "marchi.json").exists() else {}
nome_dom = {v: k for k, v in marchi.items()}
domini = set()
for p in file_offerte:
    if p.exists():
        for o in json.loads(p.read_text())["offerte"]:
            domini.add(dominio(o.get("u")) or nome_dom.get(o.get("v")))
for n in ("internet.json", "internet_auto.json"):
    p = R / "data" / n
    if p.exists():
        d = json.loads(p.read_text())
        righe = d if isinstance(d, list) else d.get("internet", []) + d.get("bundle", [])
        domini |= {dominio(x.get("url")) for x in righe}
domini.discard(None)

with cf.ThreadPoolExecutor(16) as ex:
    list(ex.map(cerca, sorted(domini)))
STATO.write_text(json.dumps(stato, indent=0, sort_keys=True))
for vecchio in DIR.glob("*.ico"):
    vecchio.unlink()
(DIR / "mancanti.json").unlink(missing_ok=True)

ci = {f.stem for f in DIR.glob("*.png")}
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
buoni = sum(1 for d in ci if stato.get(d, {}).get("px", 0) >= BUONO)
print(f"loghi: {len(ci)} su {len(domini)} domini, {buoni} in buona qualità (>= {BUONO} px)")
