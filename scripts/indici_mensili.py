"""Aggiorna data/indici.json: PSV mensile (CMEM, media mensile PSV day ahead) dalla pagina ARERA,
PUN dei nuovi mesi come media giornaliera zona Nord da data/elettricita.json."""
import html, json, re, urllib.request

URL = "https://www.arera.it/area-operatori/prezzi-e-tariffe/valore-cmemm-vulnerabili"
MESI = ["gennaio","febbraio","marzo","aprile","maggio","giugno","luglio","agosto","settembre","ottobre","novembre","dicembre"]
req = urllib.request.Request(URL, headers={"User-Agent": "comparaoffertelucegas.it (aggiornamento dati)"})
s = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "ignore")
psv = {}
for tb in re.findall(r"<table.*?</table>", s, re.S):
    anno = None
    for r in re.findall(r"<tr.*?</tr>", tb, re.S):
        c = [html.unescape(re.sub(r"<[^>]+>", "", x)).strip() for x in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", r, re.S)]
        if c and re.fullmatch(r"20\d\d", c[0]): anno = c[0]; continue
        if anno and c and c[0].lower() in MESI and len(c) >= 4 and c[3]:
            psv[f"{anno}-{MESI.index(c[0].lower())+1:02d}"] = float(c[3].replace(".", "").replace(",", "."))
if len(psv) < 12: raise SystemExit("Tabella CMEM non letta")

d = json.load(open("data/indici.json"))
righe = {r["m"]: r for r in d["serie"]}
el = json.load(open("data/elettricita.json"))
gg = {}
for x in el["serie"]: gg.setdefault(x["d"][:7], []).append(x["v"])
for m, v in psv.items():
    if m < "2024-01": continue
    r = righe.setdefault(m, {"m": m})
    r["psv"] = round(v, 6)
    if "pun" not in r and len(gg.get(m, [])) >= 25:
        r["pun"] = round(sum(gg[m]) / len(gg[m]), 6)
d["serie"] = [righe[k] for k in sorted(righe) if "pun" in righe[k] and "psv" in righe[k]]
d["fonte"] = "PSV: ARERA, CMEM (media mensile PSV day ahead). PUN: ARERA fino a ottobre 2026, poi media zona Nord (Energy-Charts)."
json.dump(d, open("data/indici.json", "w"), separators=(",", ":"))
print("ultimo mese:", d["serie"][-1])
