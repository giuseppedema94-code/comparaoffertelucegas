# comparaoffertelucegas.it

Classifica di tutte le offerte luce e gas per le famiglie, dagli open data del Portale Offerte (ARERA / Acquirente Unico).

- `scripts/aggiorna.py` scarica gli open data e genera `data/luce.json` e `data/gas.json`.
- La GitHub Action `aggiorna-dati` lo esegue alle 00:00 e alle 12:00 ora italiana.
- `data/cambio-offerta.json`: verifica manuale del cambio offerta libero, per P.IVA venditore: `{"PIVA": {"stato": "si|no", "nota": "...", "fonte": "url"}}`.

Lettura dei file e stima dei costi: [portale-offerte-mcp](https://github.com/marcopa84/PortaleOfferteEnergiaMCP) (MIT).
