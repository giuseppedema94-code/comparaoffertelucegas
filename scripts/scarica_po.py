"""Scarica gli open data del Portale Offerte tramite il relay a Milano (Google Cloud Run)
e li salva in grezzi/AAAAMMGG/*.gz, nel formato letto da aggiorna.py.
Variabili d'ambiente: RELAY_URL, RELAY_KEY."""
import gzip, os, re, sys, urllib.parse, urllib.request
from pathlib import Path

URL, KEY = os.environ["RELAY_URL"].rstrip("/"), os.environ["RELAY_KEY"]
SCHEMI = {
    "offerte_luce_placet": r"PO_Offerte_E_PLACET_(\d{8})\.csv",
    "offerte_gas_placet": r"PO_Offerte_G_PLACET_(\d{8})\.csv",
    "parametri_luce": r"PO_Parametri_E_(\d{8})\.csv",
    "parametri_gas": r"PO_Parametri_G_(\d{8})\.csv",
    "offerte_luce_ml": r"PO_Offerte_E_MLIBERO_(\d{8})\.xml",
    "offerte_gas_ml": r"PO_Offerte_G_MLIBERO_(\d{8})\.xml",
    "offerte_dual_ml": r"PO_Offerte_D_MLIBERO_(\d{8})\.xml",
}


def relay(path: str) -> bytes:
    req = urllib.request.Request(f"{URL}?p={urllib.parse.quote(path)}", headers={"x-relay-key": KEY})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()  # gzip


pagina = gzip.decompress(relay("/portaleOfferte/it/open-data.page")).decode("utf-8", "ignore")
link = [urllib.parse.urlparse(h).path for h in re.findall(r'href="([^"]+)"', pagina)]
trovati, data = {}, None
for nome, schema in SCHEMI.items():
    for p in link:
        m = re.search(schema + "$", p)
        if m:
            trovati[nome], data = p, m.group(1)
            break
if len(trovati) < len(SCHEMI):
    sys.exit(f"File mancanti sulla pagina Open Data: {set(SCHEMI) - set(trovati)}")
dest = Path(sys.argv[1] if len(sys.argv) > 1 else "grezzi") / data
dest.mkdir(parents=True, exist_ok=True)
for nome, p in trovati.items():
    (dest / f"{nome}.gz").write_bytes(relay(p))
    print("ok", nome)
prezzi = next((p for p in link if "/cms/documents/" in p and p.endswith(".csv")), None)
if prezzi:
    (dest / "prezzi_storici.csv.gz").write_bytes(relay(prezzi))
print("Open data del", data)
