"""Scarica gli open data del Portale Offerte (ARERA / Acquirente Unico) e genera
data/luce.json e data/gas.json per il sito.

Per ogni offerta si stima il costo della parte vendita a due livelli di consumo e se ne
ricavano una quota fissa (euro/anno) e un prezzo marginale (euro/kWh o euro/Smc).
Il browser calcola cosi la spesa per qualsiasi consumo senza altri dati.

Lettura dei file e calcolo: libreria portale-offerte-mcp di Marco Patti (licenza MIT).
"""

from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

from portale_offerte_mcp.archivio import Archivio
from portale_offerte_mcp import costi

RADICE = Path(__file__).resolve().parent.parent
DATI = RADICE / "data"

# Due consumi annui per ricavare quota fissa e prezzo marginale.
PUNTI = {"luce": (1200.0, 3600.0), "gas": (400.0, 1600.0)}


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


def genera(archivio: Archivio, commodity: str, cambio: dict) -> dict:
    offerte, _ = archivio.cerca(commodity=commodity, tipo_cliente="domestico", residente=True)
    parametri = archivio.parametri.get(commodity, {})
    valori, riferimento = archivio.valori_indici("ultimo_mese")
    a, b = PUNTI[commodity]
    righe, visti = [], set()
    for o in offerte:
        if o.get("sottoscrivibile_singolarmente") is False:
            continue
        sa = costi.stima(o, a, parametri, valori, riferimento)
        sb = costi.stima(o, b, parametri, valori, riferimento)
        ca, cb = sa["costo_vendita_anno"], sb["costo_vendita_anno"]
        prezzo = (cb - ca) / (b - a)
        fisso = ca - prezzo * a
        if prezzo <= 0:
            continue
        chiave = (o["piva"], o["codice"])
        if chiave in visti:
            continue
        visti.add(chiave)
        pen, pen_testo = penale(o)
        contatti = o.get("contatti") or {}
        cv = cambio.get(o["piva"]) or cambio.get((o.get("venditore") or "").upper()) or {}
        righe.append({
            "v": (o.get("venditore") or "").strip(),
            "n": (o.get("nome") or "").strip(),
            "c": o["codice"],
            "t": "f" if o.get("tipo_prezzo") == "fisso" else ("v" if o.get("tipo_prezzo") == "variabile" else "a"),
            "pl": o.get("fonte") == "PLACET",
            "fx": round(fisso, 2),
            "p": round(prezzo, 5),
            "d": o.get("durata_mesi"),
            "pen": pen,
            "penT": pen_testo,
            "z": zona(archivio, o),
            "u": contatti.get("pagina_offerta") or contatti.get("sito"),
            "min": o.get("consumo_min"),
            "max": o.get("consumo_max"),
            "ok": bool(sa.get("stima_completa")),
            "cl": cv.get("stato"),
            "clT": cv.get("nota"),
        })
    righe.sort(key=lambda r: r["fx"] + r["p"] * (2700 if commodity == "luce" else 1100))
    return {
        "commodity": commodity,
        "data_open_data": archivio.giornata.data.isoformat(),
        "generato": dt.datetime.now(dt.timezone.utc).isoformat(timespec="minutes"),
        "indici": riferimento,
        "fornitori": len({r["v"] for r in righe}),
        "offerte": righe,
    }


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
    for commodity in ("luce", "gas"):
        dati = genera(archivio, commodity, cambio)
        if len(dati["offerte"]) < 20:
            print(f"{commodity}: solo {len(dati['offerte'])} offerte, file non aggiornato", file=sys.stderr)
            return 1
        (DATI / f"{commodity}.json").write_text(json.dumps(dati, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        print(f"{commodity}: {len(dati['offerte'])} offerte, {dati['fornitori']} fornitori, dati del {dati['data_open_data']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
