"""Aggiorna il meta Content-Security-Policy in ogni pagina HTML con gli hash degli script inline.
Da rilanciare dopo ogni modifica a uno <script> inline:  python3 scripts/csp.py"""
import base64, hashlib, re
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
EST = "https://*.goatcounter.com https://*.google-analytics.com https://*.analytics.google.com https://*.googletagmanager.com https://*.clarity.ms https://c.bing.com"
BASE = ("default-src 'self'; script-src 'self' https://gc.zgo.at https://www.googletagmanager.com https://*.clarity.ms {h}; style-src 'self' 'unsafe-inline'; "
        "font-src 'self'; img-src 'self' data: " + EST + "; connect-src 'self' " + EST + "; "
        "object-src 'none'; base-uri 'none'; form-action 'none'; upgrade-insecure-requests")

for f in sorted(RADICE.glob("**/index.html")):
    if "grezzi" in f.parts:
        continue
    s = f.read_text(encoding="utf-8")
    s = re.sub(r'\s*<meta http-equiv="Content-Security-Policy"[^>]*>', "", s)
    s = re.sub(r'\s*<meta name="referrer"[^>]*>', "", s)
    s = re.sub(r'\s*<script src="/js/stat.js" defer></script>', "", s)
    s = re.sub(r'\s*<link rel="manifest"[^>]*>\s*<script src="/js/pwa.js" defer></script>', "", s)
    s = s.replace("</head>", '<script src="/js/stat.js" defer></script>\n<link rel="manifest" href="/manifest.webmanifest">\n<script src="/js/pwa.js" defer></script>\n</head>', 1)
    hashes = []
    for m in re.finditer(r"<script(?![^>]*\bsrc=)(?![^>]*ld\+json)[^>]*>(.*?)</script>", s, re.S):
        hashes.append("'sha256-" + base64.b64encode(hashlib.sha256(m.group(1).encode()).digest()).decode() + "'")
    meta = f'<meta http-equiv="Content-Security-Policy" content="{BASE.format(h=" ".join(hashes))}">\n<meta name="referrer" content="strict-origin-when-cross-origin">'
    s = s.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n' + meta, 1) if '<meta charset="utf-8">' in s else re.sub(r"(<head[^>]*>)", r"\1\n" + meta, s, count=1)
    f.write_text(s, encoding="utf-8")
    print(f.relative_to(RADICE), len(hashes), "script")
