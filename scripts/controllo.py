"""Controllo di salute del sito, senza AI. Esce con errore (e GitHub manda una mail) se qualcosa non va."""
import datetime as dt
import json
import os
import sys
import urllib.request
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
SITO = "https://comparaoffertelucegas.it"
problemi = []


def get(url, headers=None, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": "controllo comparaoffertelucegas", **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read()


oggi = dt.date.today()

# 1. pagine online e HTTPS
for pagina in ("/", "/prezzo-energia-oggi/", "/psv/", "/data/luce.json", "/data/gas.json", "/sitemap.xml"):
    try:
        st, corpo = get(SITO + pagina)
        if st != 200 or len(corpo) < 200:
            problemi.append(f"{pagina}: HTTP {st}, {len(corpo)} byte")
    except Exception as e:
        problemi.append(f"{pagina}: {e}")
try:
    urllib.request.urlopen("http://comparaoffertelucegas.it/", timeout=20)
except Exception as e:
    problemi.append(f"redirect http->https: {e}")

# 2. dati offerte: freschi e plausibili
limiti = {"luce": (0.03, 1.0, 500), "gas": (0.2, 3.0, 300)}
for c, (pmin, pmax, nmin) in limiti.items():
    d = json.loads((RADICE / "data" / f"{c}.json").read_text(encoding="utf-8"))
    o = d.get("offerte") or []
    data = dt.date.fromisoformat(d.get("rilevazione", "2000-01-01")[:10])
    if (oggi - data).days > 3:
        problemi.append(f"{c}: dati fermi al {data}")
    if len(o) < nmin:
        problemi.append(f"{c}: solo {len(o)} offerte")
    strani = [x["n"] for x in o if not (pmin <= x.get("p", 0) <= pmax) or not (0 <= x.get("fx", 0) <= 600)]
    if strani:
        problemi.append(f"{c}: {len(strani)} offerte con prezzi fuori scala, es. {strani[:3]}")
    senza_nome = sum(1 for x in o if not x.get("v") or x["v"] == "Fornitore")
    if senza_nome > 20:
        problemi.append(f"{c}: {senza_nome} offerte senza nome fornitore")

# 3. PUN e PSV aggiornati
el = json.loads((RADICE / "data" / "elettricita.json").read_text(encoding="utf-8"))
ultimo = max((g.get("d") or g.get("data") or "") for g in el.get("giorni", el.get("serie", [])) if isinstance(g, dict)) if isinstance(el, dict) else ""
if ultimo and (oggi - dt.date.fromisoformat(ultimo[:10])).days > 4:
    problemi.append(f"PUN: ultimo dato {ultimo}")

# 4. relay Milano vivo
url, chiave = os.environ.get("RELAY_URL"), os.environ.get("RELAY_KEY")
if url and chiave:
    try:
        st, corpo = get(url + "?p=/portaleOfferte/it/open-data.page", {"x-relay-key": chiave}, 90)
        if st != 200 or len(corpo) < 1000:
            problemi.append(f"relay: HTTP {st}")
    except Exception as e:
        problemi.append(f"relay: {e}")
    try:
        get(url + "?p=/portaleOfferte/it/open-data.page", timeout=60)
        problemi.append("relay: risponde anche senza chiave!")
    except urllib.error.HTTPError as e:
        if e.code != 401:
            problemi.append(f"relay senza chiave: HTTP {e.code} (atteso 401)")
    except Exception:
        pass

# 5. intestazioni di sicurezza nelle pagine
for f in RADICE.glob("**/index.html"):
    if "grezzi" not in f.parts and "Content-Security-Policy" not in f.read_text(encoding="utf-8"):
        problemi.append(f"{f.relative_to(RADICE)}: manca la CSP")

try:
    import datetime as _dt
    _v = json.loads((RADICE / "data" / "internet.json").read_text())["verificato"]
    if (_dt.date.today() - _dt.date.fromisoformat(_v)).days > 3:
        problemi.append(f"internet: prezzi fermi al {_v}")
except Exception as e:
    problemi.append(f"internet.json: {e}")

if problemi:
    print("PROBLEMI:\n- " + "\n- ".join(problemi))
    sys.exit(1)
print("tutto ok")
