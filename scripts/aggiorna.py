"""Scarica gli open data del Portale Offerte (ARERA / Acquirente Unico) e genera
data/luce.json e data/gas.json per il sito.

Per ogni offerta si stima il costo della parte vendita a due livelli di consumo e se ne
ricavano una quota fissa (euro/anno) e un prezzo marginale (euro/kWh o euro/Smc).
Il browser calcola cosi la spesa per qualsiasi consumo senza altri dati.

Lettura dei file e calcolo: libreria portale-offerte-mcp di Marco Patti (licenza MIT).
"""

from __future__ import annotations

import re
from urllib.parse import urlparse

import datetime as dt
import hashlib
import json
import os
import sys
from pathlib import Path

from portale_offerte_mcp.archivio import Archivio
from portale_offerte_mcp import costi

RADICE = Path(__file__).resolve().parent.parent
DATI = RADICE / "data"

# Due consumi annui per ricavare quota fissa e prezzo marginale.
PUNTI = {"luce": (1200.0, 3600.0), "gas": (400.0, 1600.0)}

# Componenti regolate (uguali per tutte le offerte), cliente domestico residente.
# Luce: quote fisse di rete e potenza 3 kW (€/anno), qp quota potenza €/kW/anno (ARERA 2026, del. 575/2025), parte variabile rete+oneri+dispacciamento (€/kWh), accise, IVA 10%.
# Gas: rete+oneri+accise medie (€/Smc) e IVA media, dal confronto con le bollette tipo a 1.400 Smc.
REG = {
    "luce": {"rf": 94.2, "rv": 0.06461, "iva": 0.10, "accSoglia": 1800, "accRif": 44.49 / 3200, "acc": 0.0227, "qp": 23.52},
    "gas": {"rf": 0, "rv": 0.474, "iva": 0.183, "accSoglia": 1e9, "accRif": 0},
}




RISERVATE_FILE = DATI / "riservate.json"
RISERVATE_RE = re.compile(r"\bresti\b|fedel|retention|win.?back|rinnov[oi](?![a-z])", re.I)


def riservata(o: dict) -> bool:
    """Offerte solo per clienti già attivi (fedeltà, rinnovi, win-back): non le mostriamo."""
    nome = (o.get("nome") or "").strip()
    if RISERVATE_RE.search(nome.replace("_", " ")):
        return True
    try:
        lista = json.loads(RISERVATE_FILE.read_text(encoding="utf-8"))["nomi"]
    except Exception:
        lista = []
    return nome.lower() in {x.lower() for x in lista}

NUM_ANNI = {"due": 2, "tre": 3, "quattro": 4, "cinque": 5, "sei": 6, "sette": 7, "otto": 8, "nove": 9, "dieci": 10}


def durata(o):
    """Mesi di prezzo bloccato. ARERA usa -1 per 'non indicata': in quel caso la ricaviamo dal nome, se c'è."""
    d = o.get("durata_mesi")
    if d not in (None, -1, 0):
        return d
    n = (o.get("nome") or "").lower()
    m = re.search(r"\b(\d{1,2}|" + "|".join(NUM_ANNI) + r")\s*anni\b", n)
    if m:
        a = m.group(1)
        return (int(a) if a.isdigit() else NUM_ANNI[a]) * 12
    for k, a in NUM_ANNI.items():
        if re.search(r"\b" + k + r"\b", n):
            return a * 12
    m = re.search(r"(?<![a-z\d])(\d{1,2})\s*y\b", n)
    if m:
        return int(m.group(1)) * 12
    m = re.search(r"(?<![\d.,])(12|18|24|30|36|48|60)(?![\d.,%])\s*(mesi)?", n)
    if m and o.get("tipo_prezzo") == "fisso":
        return int(m.group(1))
    return d

def penale(offerta: dict) -> tuple[bool, str | None]:
    for c in offerta.get("condizioni") or []:
        tip = c.get("tipologia") or ""
        if tip == "oneri di recesso anticipato" or (tip == "recesso" and c.get("limitante")):
            testo = (c.get("descrizione") or "").strip()
            return True, testo[:280] or None
    return False, None


def zona(archivio: Archivio, offerta: dict) -> str | None:
    if Archivio.nazionale(offerta):
        return None
    try:
        return archivio.descrivi_zone(offerta)[:120]
    except Exception:
        return "solo alcune zone"


MARCHI_FILE = Path(__file__).resolve().parent.parent / "data" / "marchi.json"
SUFFISSI = re.compile(r"[\s,]*\b(S\.?\s?P\.?\s?A|S\.?\s?R\.?\s?L|S\.?\s?A\.?\s?S|S\.?\s?N\.?\s?C|SOCIETA'?\s+.*|SOC\.?\s+COOP.*|UNIPERSONALE|A SOCIO UNICO|IN FORMA ABBREVIATA.*)\.?\b.*$", re.I)


def dominio(url: str | None) -> str | None:
    if not url:
        return None
    h = urlparse(url if "://" in url else "https://" + url).netloc.lower()
    return h[4:] if h.startswith("www.") else (h or None)


def bello(testo: str) -> str:
    testo = re.sub(r"\s+", " ", testo).strip(" .,-")
    if testo and sum(c.isupper() for c in testo) > 0.7 * sum(c.isalpha() for c in testo):
        testo = " ".join(w if (len(w) <= 3 and w.isalpha() and w not in ("DI", "DEL", "E")) or any(ch.isdigit() for ch in w) else w.capitalize() for w in testo.split())
    return testo


def marchio(o: dict, marchi: dict) -> str:
    contatti = o.get("contatti") or {}
    for u in (contatti.get("sito"), contatti.get("pagina_offerta")):
        d = dominio(u)
        if d and d in marchi:
            return marchi[d]
    v = (o.get("venditore") or "").strip()
    if v:
        return bello(SUFFISSI.sub("", v)) or bello(v)
    d = dominio(contatti.get("sito") or contatti.get("pagina_offerta"))
    if d:
        return d.split(".")[-2].replace("-", " ").title() if d.count(".") else d
    return "Fornitore"


def senza_doppioni(o: dict) -> dict:
    """Se una componente ha una riga generica e anche righe a scaglioni, la libreria le somma: tengo solo gli scaglioni."""
    comp = []
    for c in o.get("componenti") or []:
        prezzi = c.get("prezzi") or []
        scaglioni = [x for x in prezzi if x.get("consumo_da") is not None or x.get("consumo_a") is not None]
        if scaglioni and len(scaglioni) < len(prezzi):
            c = {**c, "prezzi": scaglioni}
        comp.append(c)
    return {**o, "componenti": comp}


def link(u: str | None) -> str | None:
    u = (u or "").strip()
    if not u or " " in u or "." not in u:
        return None
    return u if u.lower().startswith(("http://", "https://")) else "https://" + u.lstrip("/")


def link_vivi(dati: list[dict]) -> None:
    """Toglie i link che non rispondono (dominio inesistente, 404, timeout)."""
    import concurrent.futures as cf
    import urllib.request
    urls = {r["u"] for d in dati for r in d["offerte"] if r.get("u")}

    def ok(u: str) -> bool:
        for metodo in ("HEAD", "GET"):
            try:
                req = urllib.request.Request(u, method=metodo, headers={"User-Agent": "Mozilla/5.0 (comparaoffertelucegas.it)"})
                with urllib.request.urlopen(req, timeout=12) as r:
                    return r.status < 400
            except urllib.error.HTTPError as e:
                if e.code in (403, 405, 429, 503):  # siti che bloccano i bot: li considero vivi
                    return True
                if metodo == "GET":
                    return False
            except Exception:
                if metodo == "GET":
                    return False
        return False

    with cf.ThreadPoolExecutor(32) as ex:
        stato = dict(zip(urls, ex.map(ok, urls)))
    morti = [u for u, v in stato.items() if not v]
    print(f"link: {len(urls)} controllati, {len(morti)} non raggiungibili")
    for d in dati:
        for r in d["offerte"]:
            if r.get("u") and not stato.get(r["u"], True):
                del r["u"]


def genera(archivio: Archivio, commodity: str, cambio: dict) -> dict:
    offerte, _ = archivio.cerca(commodity=commodity, tipo_cliente="domestico", residente=True)
    parametri = archivio.parametri.get(commodity, {})
    valori, riferimento = archivio.valori_indici("ultimo_mese")
    a, b = PUNTI[commodity]
    righe, visti = [], set()
    marchi = json.loads(MARCHI_FILE.read_text()) if MARCHI_FILE.exists() else {}
    oggi = dt.date.today().isoformat()
    pmax = 1.0 if commodity == "luce" else 3.0
    for o in offerte:
        if o.get("sottoscrivibile_singolarmente") is False or riservata(o):
            continue
        o = senza_doppioni(o)
        sa = costi.stima(o, a, parametri, valori, riferimento)
        sb = costi.stima(o, b, parametri, valori, riferimento)
        ca, cb = sa["costo_vendita_anno"], sb["costo_vendita_anno"]
        # sconti separati: quota fissa e prezzo mostrati lordi, sconto a parte
        za = (sa.get("voci") or {}).get("sconti") or 0
        zb = (sb.get("voci") or {}).get("sconti") or 0
        z_var = (zb - za) / (b - a)
        z_fix = za - z_var * a
        prezzo_lordo = ((cb - zb) - (ca - za)) / (b - a)
        fisso = (ca - za) - prezzo_lordo * a
        prezzo = prezzo_lordo + z_var
        if prezzo <= 0 or prezzo > pmax or not (0 <= fisso <= 600):
            continue
        if zona(archivio, o):
            continue  # offerte solo per alcune regioni: il sito non chiede il CAP
        fine_ = o.get("data_fine")
        if fine_ and str(fine_)[:10] < oggi:
            continue
        chiave = (o["piva"], o["codice"])
        if chiave in visti:
            continue
        visti.add(chiave)
        pen, pen_testo = penale(o)
        contatti = o.get("contatti") or {}
        cv = cambio.get(o["piva"]) or cambio.get((o.get("venditore") or "").upper()) or {}
        voci = sb.get("voci") or {}
        sconto = round(-z_fix, 2)
        durata_sconto = None
        for sc_ in o.get("sconti") or []:
            dm = (sc_.get("periodo") or {}).get("durata_mesi")
            if dm and not [c for c in sc_.get("condizioni", []) if c.get("codice") not in (None, "00")]:
                durata_sconto = f"per {dm} mesi"
                break
        fine = o.get("data_fine")
        verde = any(k.get("macroarea") == "06" and k.get("tipologia") == "01" for k in o.get("componenti") or [])
        righe.append({
            "id": hashlib.md5(f"{o['piva']}|{o['codice']}".encode()).hexdigest()[:8],
            "vd": True if verde else None,
            "v": marchio(o, marchi),
            "n": bello(o.get("nome") or ""),
            "c": o["codice"],
            "t": "f" if o.get("tipo_prezzo") == "fisso" else "v",
            "pl": o.get("fonte") == "PLACET",
            "fx": round(fisso, 2),
            "p": round(prezzo, 5),
            "pd": round(prezzo_lordo, 5),
            "s": sconto if sconto > 0.5 else 0,
            "ds": sconto if sconto > 0.5 else 0,
            "dsT": durata_sconto,
            "sc": str(fine)[:10] if fine else None,
            "d": durata(o),
            "nt": None,
            "pen": pen,
            "penT": pen_testo,
            "z": zona(archivio, o),
            "u": link(contatti.get("pagina_offerta") or contatti.get("sito")),
            "min": o.get("consumo_min"),
            "max": o.get("consumo_max"),
            "ok": bool(sa.get("stima_completa")),
            "cl": cv.get("stato"),
            "clT": cv.get("nota"),
        })
    righe.sort(key=lambda r: (not r["ok"], r["fx"] + r["p"] * (2700 if commodity == "luce" else 1100)))
    return {
        "reg": REG[commodity],
        "fonte": "arera",
        "rilevazione": archivio.giornata.data.isoformat(),
        "commodity": commodity,
        "data_open_data": archivio.giornata.data.isoformat(),
        "generato": dt.datetime.now(dt.timezone.utc).isoformat(timespec="minutes"),
        "indici": riferimento,
        "idx": round(valori.get("PUN" if commodity == "luce" else "PSV") or 0, 5),
        "fornitori": len({r["v"] for r in righe}),
        "offerte": [{k: v for k, v in r.items() if v is not None and k not in ("c", "min", "max")} for r in righe],
    }


def prezzi(o: dict, commodity: str, parametri: dict, valori, riferimento) -> dict | None:
    """Quota fissa, prezzo e sconto annuo di una singola offerta (stessa logica di genera)."""
    a, b = PUNTI[commodity]
    sa = costi.stima(o, a, parametri, valori, riferimento)
    sb = costi.stima(o, b, parametri, valori, riferimento)
    ca, cb = sa["costo_vendita_anno"], sb["costo_vendita_anno"]
    za = (sa.get("voci") or {}).get("sconti") or 0
    zb = (sb.get("voci") or {}).get("sconti") or 0
    z_var = (zb - za) / (b - a)
    z_fix = za - z_var * a
    pd_ = ((cb - zb) - (ca - za)) / (b - a)
    fx = (ca - za) - pd_ * a
    p_ = pd_ + z_var
    pmax = 1.0 if commodity == "luce" else 3.0
    if p_ <= 0 or p_ > pmax or not (0 <= fx <= 600):
        return None
    sc = round(-z_fix, 2)
    return {"fx": round(fx, 2), "p": round(p_, 5), "pd": round(pd_, 5), "s": sc if sc > 0.5 else 0,
            "t": "f" if o.get("tipo_prezzo") == "fisso" else "v", "ok": bool(sa.get("stima_completa") and sb.get("stima_completa"))}


def genera_dual(archivio: Archivio) -> dict:
    """Pacchetti luce + gas: ogni offerta dual rimanda a un'offerta luce e una gas collegate."""
    duali, _ = archivio.cerca(commodity="dual", tipo_cliente="domestico", residente=True)
    valori, riferimento = archivio.valori_indici("ultimo_mese")
    per_codice = {}
    for c in ("luce", "gas"):
        tutte, _ = archivio.cerca(commodity=c, tipo_cliente="domestico", residente=True)
        for o in tutte:
            per_codice[(c, o["piva"], o["codice"])] = o
    marchi = json.loads(MARCHI_FILE.read_text()) if MARCHI_FILE.exists() else {}
    oggi = dt.date.today().isoformat()
    righe, visti = [], set()
    for d in duali:
        fine = d.get("data_fine")
        if fine and str(fine)[:10] < oggi:
            continue
        if zona(archivio, d):
            continue
        cg = d.get("offerte_congiunte") or {}
        parti = {}
        for c in ("luce", "gas"):
            for cod in cg.get(c) or []:
                o = per_codice.get((c, d["piva"], cod))
                if o and not zona(archivio, o):
                    x = prezzi(senza_doppioni(o), c, archivio.parametri.get(c, {}), valori, riferimento)
                    if x:
                        parti[c] = x
                        break
        if len(parti) < 2:
            continue
        chiave = (d["piva"], d["codice"])
        if chiave in visti or riservata(d):
            continue
        visti.add(chiave)
        pen, pen_testo = penale(d)
        contatti = d.get("contatti") or {}
        righe.append({
            "v": marchio(d, marchi),
            "n": bello(d.get("nome") or ""),
            "t": "f" if d.get("tipo_prezzo") == "fisso" else "v",
            "d": durata(d),
            "sc": str(fine)[:10] if fine else None,
            "pen": pen,
            "u": link(contatti.get("pagina_offerta") or contatti.get("sito")),
            "l": parti["luce"],
            "g": parti["gas"],
        })
    return {
        "reg": REG,
        "data_open_data": archivio.giornata.data.isoformat(),
        "generato": dt.datetime.now(dt.timezone.utc).isoformat(timespec="minutes"),
        "fornitori": len({r["v"] for r in righe}),
        "offerte": [{k: v for k, v in r.items() if v is not None} for r in righe],
    }


def migliori(luce: dict, gas: dict, n: int = 3) -> dict:
    """Prime offerte per consumi tipici (225 kWh e 90 Smc al mese), per le pagine che non caricano tutta la classifica."""
    def acc_luce(y, al):
        m = y / 12
        e = min(m, 150) if m <= 220 else max(0, 150 - (m - 220))
        return (m - e) * 12 * al

    def mese(o, c, y):
        r = REG[c]
        acc = acc_luce(y, r["acc"]) if c == "luce" else 0
        return (1 + r["iva"]) * (o["fx"] + o["p"] * y - (o.get("s") or 0) + r["rf"] + r["rv"] * y + acc) / 12 + (90 / 12 if c == "luce" else 0)

    out = {}
    for c, d, y in (("luce", luce, 2700), ("gas", gas, 1080)):
        ok = [o for o in d["offerte"] if o.get("ok", True)]
        top = sorted(ok, key=lambda o: mese(o, c, y))[:n]
        out[c] = [{"v": o["v"], "n": o["n"], "t": o["t"], "m": round(mese(o, c, y), 2)} for o in top]
    out["consumi"] = {"luce_kwh_mese": 225, "gas_smc_mese": 90}
    out["data_open_data"] = luce["data_open_data"]
    return out


def mese_tipo(o: dict, c: str) -> float:
    """Spesa mensile con consumo tipo (225 kWh o 90 Smc al mese), come nel sito."""
    y = 2700 if c == "luce" else 1080
    r = REG[c]
    acc = 0
    if c == "luce":
        m = y / 12
        e = min(m, 150) if m <= 220 else max(0, 150 - (m - 220))
        acc = (m - e) * 12 * r["acc"]
    return (1 + r["iva"]) * (o["fx"] + o["p"] * y - (o.get("s") or 0) + r["rf"] + r["rv"] * y + acc) / 12


def storico(c: str, dati: dict) -> None:
    """Salva la spesa tipo di ogni offerta giorno per giorno (ultimi 35 giorni) e
    aggiunge a ogni offerta la variazione rispetto a 7 giorni prima (campo "tr")."""
    f = DATI / "storico" / f"{c}.json"
    f.parent.mkdir(exist_ok=True)
    st = json.loads(f.read_text()) if f.exists() else {"giorni": [], "v": {}}
    oggi = dt.date.today().isoformat()
    if st["giorni"] and st["giorni"][-1] == oggi:
        st["giorni"].pop()
        for k in st["v"]:
            st["v"][k] = st["v"][k][:len(st["giorni"])]
    n = len(st["giorni"])
    st["giorni"].append(oggi)
    attuali = {o["id"]: round(mese_tipo(o, c), 2) for o in dati["offerte"]}
    for k, v in attuali.items():
        st["v"].setdefault(k, [None] * n).append(v)
    for k in st["v"]:
        if len(st["v"][k]) < n + 1:
            st["v"][k].append(None)
    if len(st["giorni"]) > 35:
        st["giorni"] = st["giorni"][-35:]
        st["v"] = {k: v[-35:] for k, v in st["v"].items()}
    st["v"] = {k: v for k, v in st["v"].items() if any(x is not None for x in v)}
    # confronto con 7 giorni fa (o il giorno più vecchio disponibile, almeno 2 giorni fa)
    g = st["giorni"]
    oggi_d = dt.date.fromisoformat(oggi)
    rif = [i for i, d in enumerate(g) if 2 <= (oggi_d - dt.date.fromisoformat(d)).days <= 7]
    for o in dati["offerte"]:
        o.pop("tr", None)
        if not rif:
            continue
        serie = st["v"].get(o["id"], [])
        vecchio = next((serie[i] for i in rif if i < len(serie) and serie[i] is not None), None)
        if vecchio is not None:
            dv = round(attuali[o["id"]] - vecchio, 2)
            if abs(dv) >= 0.5:
                o["tr"] = dv
    f.write_text(json.dumps(st, separators=(",", ":")), encoding="utf-8")


def prepara_cache(grezzi: Path) -> None:
    """Il Portale Offerte blocca i server di GitHub: i file arrivano gia scaricati
    (cartella grezzi/AAAAMMGG con i .gz) e vengono messi nella cache della libreria."""
    import shutil
    from portale_offerte_mcp import sorgenti

    giorni = sorted(p for p in grezzi.iterdir() if p.is_dir() and p.name.isdigit()) if grezzi.is_dir() else []
    if not giorni:
        return
    ultimo = giorni[-1]
    cache = sorgenti.cartella_cache()
    dest = cache / "giornaliero" / ultimo.name
    dest.mkdir(parents=True, exist_ok=True)
    for f in ultimo.glob("*.gz"):
        if f.name == "prezzi_storici.csv.gz":
            shutil.copy(f, cache / f.name)
        else:
            shutil.copy(f, dest / f.name)


def main() -> int:
    DATI.mkdir(exist_ok=True)
    if len(sys.argv) > 1:
        prepara_cache(Path(sys.argv[1]))
    percorso_cambio = DATI / "cambio-offerta.json"
    cambio = json.loads(percorso_cambio.read_text(encoding="utf-8")) if percorso_cambio.exists() else {}
    archivio = Archivio()
    archivio.assicura(forza=True)
    tutti = {}
    for commodity in ("luce", "gas"):
        dati = genera(archivio, commodity, cambio)
        if len(dati["offerte"]) < 20:
            print(f"{commodity}: solo {len(dati['offerte'])} offerte, file non aggiornato", file=sys.stderr)
            return 1
        tutti[commodity] = dati
    duale = genera_dual(archivio)
    if os.environ.get("CONTROLLA_LINK"):
        link_vivi(list(tutti.values()) + [duale])
    for commodity, dati in tutti.items():
        storico(commodity, dati)
        (DATI / f"{commodity}.json").write_text(json.dumps(dati, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        print(f"{commodity}: {len(dati['offerte'])} offerte, {dati['fornitori']} fornitori, dati del {dati['data_open_data']}")
    (DATI / "top.json").write_text(json.dumps(migliori(tutti["luce"], tutti["gas"]), ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    if len(duale["offerte"]) >= 5:
        (DATI / "dual.json").write_text(json.dumps(duale, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        print(f"dual: {len(duale['offerte'])} pacchetti")
    return 0


if __name__ == "__main__":
    sys.exit(main())
