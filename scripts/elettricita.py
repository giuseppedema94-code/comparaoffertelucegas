"""Prezzi elettrici del giorno prima, zona Nord Italia, da Energy-Charts (Fraunhofer ISE).
Licenza dei dati IT-North: CC BY 4.0, Bundesnetzagentur | SMARD.de (campo license_info).
Scrive data/elettricita.json con medie giornaliere (ultimi 120 giorni) e profilo orario di oggi e domani."""
import datetime as dt, json, sys, urllib.request
from collections import defaultdict
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Europe/Rome")
URL = "https://api.energy-charts.info/price?bzn=IT-North&start={s}&end={e}"

def get(s, e):
    with urllib.request.urlopen(URL.format(s=s, e=e), timeout=60) as r:
        return json.load(r)

oggi = dt.datetime.now(TZ).date()
d = get((oggi - dt.timedelta(days=120)).isoformat(), (oggi + dt.timedelta(days=1)).isoformat())
lic = d.get("license_info", "")
if "CC BY" not in lic:
    print("Licenza non CC BY:", lic); sys.exit(1)
giorni, ore = defaultdict(list), defaultdict(lambda: defaultdict(list))
for t, p in zip(d["unix_seconds"], d["price"]):
    if p is None: continue
    x = dt.datetime.fromtimestamp(t, TZ)
    giorni[x.date().isoformat()].append(p)
    ore[x.date().isoformat()][x.hour].append(p)
serie = [{"d": k, "v": round(sum(v) / len(v) / 1000, 5), "min": round(min(v) / 1000, 5), "max": round(max(v) / 1000, 5)}
         for k, v in sorted(giorni.items()) if len(v) >= 20]
ultimo = max([k for k in ore if k <= oggi.isoformat()], default=None)
chiavi = {ultimo, oggi.isoformat(), (oggi + dt.timedelta(days=1)).isoformat()} - {None}
prof = {k: [round(sum(ore[k][h]) / len(ore[k][h]) / 1000, 5) for h in sorted(ore[k])] for k in chiavi if k in ore}
out = {"zona": "IT-North", "unita": "€/kWh", "licenza": lic, "generato": dt.datetime.now(TZ).isoformat(timespec="minutes"), "serie": serie, "orario": prof}
json.dump(out, open("data/elettricita.json", "w"), separators=(",", ":"))
print(len(serie), "giorni; ultimo", serie[-1])
