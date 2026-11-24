"""Scarica le icone dichiarate da alcuni siti, per scegliere a mano il logo giusto."""
import re, sys, urllib.request, urllib.parse, pathlib, html
out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0 Safari/537.36"}
def get(u):
    with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=20) as r: return r.read(3_000_000), r.geturl()
for site in sys.argv[2:]:
    if re.search(r"\.(png|svg|ico|webp|jpg)(\?|$)", site, re.I):
        try:
            d, _ = get(site); n = out / re.sub(r"[^a-z0-9.]+", "_", site.lower())[-80:]; n.write_bytes(d); print(n.name, len(d), site)
        except Exception as e: print("x", site, e)
        continue
    try:
        b, base = get(site); t = b.decode("utf-8", "ignore")
    except Exception as e:
        print(site, e); continue
    urls = set(re.findall(r'<link[^>]+href="([^"]+\.(?:png|svg|ico|webp)[^"]*)"', t, re.I))
    urls |= set(re.findall(r'<meta[^>]+content="([^"]+\.(?:png|svg|jpg|webp)[^"]*)"', t, re.I))
    urls |= set(re.findall(r'<img[^>]+src="([^"]*logo[^"]*)"', t, re.I))
    for p in ("/apple-touch-icon.png", "/favicon.ico", "/favicon.svg"): urls.add(p)
    for i, u in enumerate(sorted(urls)):
        u = urllib.parse.urljoin(base, html.unescape(u))
        try:
            d, _ = get(u); ext = (re.search(r"\.(png|svg|ico|webp|jpg)", u, re.I) or [None, "bin"])[1]
            n = out / f"{urllib.parse.urlparse(site).netloc}_{i}.{ext.lower()}"; n.write_bytes(d); print(n.name, len(d), u)
        except Exception as e: print("x", u, e)
