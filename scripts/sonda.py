#!/usr/bin/env python3
"""Sonda manuale (workflow sonda-internet): scarica le pagine offerte degli operatori
e salva l'HTML grezzo più un riepilogo, per capire da dove estrarre i prezzi."""
import json, re, sys, urllib.request, pathlib, gzip
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "sonde"); OUT.mkdir(parents=True, exist_ok=True)
URLS = {
 "tim_offerta": "https://www.tim.it/fisso-e-mobile/fibra-e-adsl/fibra-internet-casa",
 "tim_trasparenza": "https://www.tim.it/assistenza/trasparenza-tariffaria/trasparenza-tariffaria-delle-offerte-di-linea-fissa",
 "fastweb_offerta": "https://www.fastweb.it/adsl-fibra-ottica/fastweb-casa-start/",
 "fastweb_lista": "https://www.fastweb.it/adsl-fibra-ottica/",
 "fastweb_trasparenza": "https://www.fastweb.it/trasparenza-tariffaria/",
 "vodafone_casa": "https://www.vodafone.it/privati/fibra-adsl-telefono.html",
 "vodafone_trasparenza": "https://www.vodafone.it/privati/area-legale/trasparenza-tariffaria.html",
 "windtre_offerta": "https://www.windtre.it/offerte-fibra/",
 "windtre_trasparenza": "https://www.windtre.it/trasparenza-tariffaria/",
 "iliad_fibra": "https://www.iliad.it/offerta-iliadbox-fibra-domotica.html",
 "iliad_prezzi": "https://www.iliad.it/brochure-prezzi-fibra.html",
 "sky_wifi": "https://www.sky.it/sky-wifi-fibra",
 "tiscali": "https://casa.tiscali.it/",
 "eolo": "https://www.eolo.it/offerte-internet-casa/eolo-fibra",
 "aruba": "https://fibra.aruba.it/offerte-fibra-casa.aspx",
 "poste": "https://www.poste.it/fibra/postecasa-ultraveloce-start",
 "enel_fibra": "https://www.enel.it/it-it/offerte-fibra",
}
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"
rep = {}
for k, u in URLS.items():
    r = {"url": u}
    try:
        req = urllib.request.Request(u, headers={"User-Agent": UA, "Accept-Language": "it-IT,it;q=0.9", "Accept": "text/html,*/*"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            b = resp.read()
            if resp.headers.get("Content-Encoding") == "gzip": b = gzip.decompress(b)
            r["status"] = resp.status; r["final"] = resp.geturl(); r["type"] = resp.headers.get("Content-Type")
        t = b.decode("utf-8", "replace")
        (OUT / f"{k}.html").write_text(t, encoding="utf-8")
        r["bytes"] = len(b)
        r["jsonld"] = len(re.findall(r"application/ld\+json", t))
        r["next_data"] = "__NEXT_DATA__" in t
        r["nuxt"] = "__NUXT__" in t
        r["prezzi"] = sorted(set(re.findall(r"\d{1,2},\d{2}\s?(?:€|&euro;|euro)", t)))[:25]
        r["pdf"] = sorted(set(re.findall(r'href="([^"]+\.pdf)"', t)))[:40]
        r["api"] = sorted(set(re.findall(r'["\'](/[a-zA-Z0-9_\-/]*api[a-zA-Z0-9_\-/.?=&]*)["\']', t)))[:20]
    except Exception as e:
        r["errore"] = repr(e)[:300]
    rep[k] = r
(OUT / "riepilogo.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({k: (v.get("status"), v.get("bytes"), v.get("errore", "")[:80]) for k, v in rep.items()}, indent=1))
