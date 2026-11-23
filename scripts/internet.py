#!/usr/bin/env python3
"""Aggiorna data/internet.json leggendo i prezzi dalle pagine ufficiali degli operatori.

Gira ogni giorno in GitHub Actions (workflow internet.yml), senza AI: per ogni offerta
c'è una regola (espressione regolare) sul testo della pagina. Se la regola non trova
il prezzo, l'offerta resta con i valori dell'ultima lettura riuscita e la data vecchia.
"""
import datetime as dt
import gzip
import html
import json
import re
import sys
import urllib.request
from pathlib import Path

R = Path(__file__).resolve().parent.parent
FILE = R / "data" / "internet.json"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"
E = r"(\d{1,3},\d{2})"


def scarica(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "it-IT,it;q=0.9", "Accept": "text/html,*/*"})
    with urllib.request.urlopen(req, timeout=40) as r:
        b = r.read()
        if r.headers.get("Content-Encoding") == "gzip":
            b = gzip.decompress(b)
    return b.decode("utf-8", "replace")


def testo(raw: str) -> str:
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return re.sub(r"\s+", " ", t).replace("​", "")


def f(s: str) -> float:
    return float(s.replace(",", "."))


def eur(v: float) -> str:
    return f"{v:.2f}".replace(".", ",")


# Ogni regola riceve (testo pulito, html grezzo) e restituisce i campi aggiornati o None.
def windtre(t, raw):
    m = re.search(r"Con una linea Mobile WINDTRE Fibra fino a [\d,]+ Gbps " + E + r" ?€/mese per (\d+) ann[oi] poi " + E, t)
    return m and {"prezzo_mese": f(m[1]), "mesi_promo": int(m[2]) * 12, "prezzo_dopo": f(m[3])}


def sky(t, raw):
    m = re.search(r'"price":\{"price":"' + E + r'","old":"[^"]*","per":"al mese per (\d+) mesi"', raw)
    return m and {"prezzo_mese": f(m[1]), "mesi_promo": int(m[2]), "nota": f"Solo con un abbonamento Sky TV. Prezzo per {m[2]} mesi."}


def eolo(t, raw):
    m = re.search(r"canone mensile dell'offerta di " + E + "€", t)
    a = re.search(r"è di " + E + r"€ al posto di", t)
    return m and {"prezzo_mese": f(m[1]), **({"attivazione": f(a[1])} if a else {})}


def aruba(t, raw):
    m = re.search(r"base senza router Fibra Aruba.{0,80}?" + E + r" € / mese \(IVA inclusa\) Costo di attivazione iniziale " + E, t)
    return m and {"prezzo_mese": f(m[1]), "attivazione": f(m[2])}


def poste(t, raw):
    m = re.search(r"costo mensile dell'offerta è " + E + " €", t)
    a = re.search(r"costo di attivazione di PosteCasa Ultraveloce Start è di " + E, t)
    return m and {"prezzo_mese": f(m[1]), **({"attivazione": f(a[1])} if a else {})}


def tim(t, raw):
    m = re.search(r"TIM WiFi Casa " + E + r"€/mese anziché " + E + r"€ \(con domiciliazione\)", t)
    return m and {"prezzo_mese": f(m[1]), "nota": f"{m[1]} € con addebito su conto, altrimenti {m[2]} €. Vincolo 24 mesi."}


def fastweb(t, raw):
    m = re.search(r"Fastweb Casa Start Fibra ultraveloce " + E + r" € al mese " + E + r" ?€/mese se aggiungi", t)
    return m and {"prezzo_mese": f(m[1]), "nota": f"{m[2]} € con una SIM Fastweb Mobile."}


def enel(t, raw):
    m = re.search(r"cliente Luce e Gas Prezzo\* ?" + E + r" ?€/Mese invece di " + E, t)
    d = re.search(r"scontato a [\d,]+ ?€/mese per i primi (\d+) mesi", t)
    if not m:
        return None
    mesi = d[1] if d else None
    return {"prezzo_fibra_mese": f(m[1]),
            "vantaggio": f"Canone ridotto da {m[2]} € a {m[1]} € se hai luce e gas con Enel" + (f", per {mesi} mesi" if mesi else ""),
            "nota": f"Prezzo pieno {m[2]} €. Lo sconto si perde se chiudi il contratto luce o gas."}


def windtre_bundle(t, raw):
    x = windtre(t, raw)
    return x and {"prezzo_fibra_mese": x["prezzo_mese"], "nota": f"Poi {eur(x['prezzo_dopo'])} € dopo {x['mesi_promo']} mesi. Serve una linea mobile WindTre."}


REGOLE = {"WindTre": windtre, "Sky": sky, "Eolo": eolo, "Aruba": aruba, "Poste": poste, "TIM": tim, "Fastweb": fastweb}
REGOLE_BUNDLE = {"Enel Energia": enel, "WindTre": windtre_bundle}


def main() -> int:
    d = json.loads(FILE.read_text(encoding="utf-8"))
    oggi = dt.date.today().isoformat()
    cache, esito = {}, []
    for lista, regole in (("internet", REGOLE), ("bundle", REGOLE_BUNDLE)):
        for x in d[lista]:
            nome = x.get("operatore") or x.get("fornitore")
            regola = regole.get(nome)
            if not regola or not x.get("url"):
                continue
            try:
                if x["url"] not in cache:
                    raw = scarica(x["url"])
                    cache[x["url"]] = (testo(raw), raw)
                nuovo = regola(*cache[x["url"]])
            except Exception as e:  # pagina irraggiungibile: tengo i valori precedenti
                nuovo = None
                print(f"{nome}: errore {e!r}"[:200], file=sys.stderr)
            if nuovo:
                cambi = {k: (x.get(k), v) for k, v in nuovo.items() if x.get(k) != v}
                x.update(nuovo)
                x["letto"] = oggi
                esito.append(f"{lista}/{nome}: ok" + (f" {cambi}" if cambi else ""))
            else:
                esito.append(f"{lista}/{nome}: regola non trovata, resta il dato del {x.get('letto', d.get('verificato'))}")
    # offerte con regola generica (data/internet_auto.json): aggiorno solo il canone mensile
    auto = json.loads((R / "data" / "internet_auto.json").read_text(encoding="utf-8"))
    for x in auto:
        try:
            if x["url"] not in cache:
                raw = scarica(x["url"])
                cache[x["url"]] = (testo(raw), raw)
            m = re.search(x["regex"], cache[x["url"]][0])
        except Exception as e:
            m = None
            print(f"{x['operatore']}: errore {e!r}"[:200], file=sys.stderr)
        if m:
            v = f(m.group(1))
            if v != x["prezzo_mese"]:
                esito.append(f"auto/{x['operatore']} {x['offerta']}: {x['prezzo_mese']} -> {v}")
                if x.get("prezzo_dopo") == x["prezzo_mese"]:
                    x["prezzo_dopo"] = v
                x["prezzo_mese"] = v
            x["letto"] = oggi
        else:
            esito.append(f"auto/{x['operatore']} {x['offerta']}: regola non trovata")
    (R / "data" / "internet_auto.json").write_text(json.dumps(auto, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    ok = sum(1 for x in auto if x.get("letto") == oggi)
    esito.append(f"auto: {ok}/{len(auto)} lette oggi")
    date = [x.get("letto") for k in ("internet", "bundle") for x in d[k] if x.get("letto")]
    if date:
        d["verificato"] = max(date)
    FILE.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("\n".join(esito))
    return 0


if __name__ == "__main__":
    sys.exit(main())
