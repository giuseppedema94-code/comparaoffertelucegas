"""Avvisa Bing e gli altri motori IndexNow che le pagine sono cambiate (gratis, senza account)."""
import json, re, urllib.request
from pathlib import Path
R = Path(__file__).resolve().parent.parent
KEY = "d58d4fe82f9245001e2fbbe4f970f98a"
urls = re.findall(r"<loc>([^<]+)</loc>", (R / "sitemap.xml").read_text(encoding="utf-8"))
body = json.dumps({"host": "comparaoffertelucegas.it", "key": KEY,
                   "keyLocation": f"https://comparaoffertelucegas.it/{KEY}.txt", "urlList": urls}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                             headers={"Content-Type": "application/json; charset=utf-8"})
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        print("IndexNow", r.status, len(urls), "pagine")
except Exception as e:
    print("IndexNow non riuscito:", e)
