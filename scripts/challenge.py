#!/usr/bin/env python3
"""Fa verificare il calcolo dei costi ad altre AI gratuite, solo su richiesta.

Non gira nei workflow automatici. Le chiavi si leggono da ~/.ai_keys
(righe NOME=valore) o dalle variabili d'ambiente:
  GEMINI_API_KEY      aistudio.google.com/apikey (gratis)
  GROQ_API_KEY        console.groq.com/keys (gratis: GPT-OSS di OpenAI, Qwen)
  OPENROUTER_API_KEY  openrouter.ai/keys (modelli ":free")
  MISTRAL_API_KEY     console.mistral.ai (piano Experiment gratuito)
  XAI_API_KEY         console.x.ai (Grok, crediti se disponibili)
Uso: python3 scripts/challenge.py [luce|gas]
Risposte salvate in challenge/AAAA-MM-GG-<commodity>.md (fuori da git).
"""
import json, os, re, ssl, sys, urllib.request, datetime, pathlib, concurrent.futures as cf

ROOT = pathlib.Path(__file__).resolve().parent.parent
KEYS = pathlib.Path.home() / ".ai_keys"
if KEYS.exists():
    for r in KEYS.read_text().splitlines():
        if "=" in r and not r.startswith("#"):
            k, v = r.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

CA = pathlib.Path.home() / ".ccr/ca-bundle.crt"
CTX = ssl.create_default_context(cafile=str(CA)) if CA.exists() else ssl.create_default_context()


def post(url, body, headers):
    req = urllib.request.Request(url, json.dumps(body).encode(), {"Content-Type": "application/json", "User-Agent": "comparaofferte-challenge/1.0", **headers})
    with urllib.request.urlopen(req, timeout=300, context=CTX) as r:
        return json.load(r)


def openai_like(url, key, model):
    def f(p):
        d = post(url, {"model": model, "messages": [{"role": "user", "content": p}], "temperature": 0.2},
                 {"Authorization": "Bearer " + key})
        return d["choices"][0]["message"]["content"]
    return f


def gemini(key):
    def f(p):
        d = post("https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent",
                 {"contents": [{"parts": [{"text": p}]}]}, {"x-goog-api-key": key})
        return "".join(x.get("text", "") for x in d["candidates"][0]["content"]["parts"] if not x.get("thought"))
    return f


def providers():
    e = os.environ.get
    p = {}
    if e("GEMINI_API_KEY"): p["Gemini 3.5 Flash"] = gemini(e("GEMINI_API_KEY"))
    if e("GROQ_API_KEY"):
        g = "https://api.groq.com/openai/v1/chat/completions"
        p["GPT-OSS 120B di OpenAI (Groq)"] = openai_like(g, e("GROQ_API_KEY"), "openai/gpt-oss-120b")
        p["Qwen 3.8 (Groq)"] = openai_like(g, e("GROQ_API_KEY"), "qwen/qwen3.8-27b")
    if e("OPENROUTER_API_KEY"):
        o = "https://openrouter.ai/api/v1/chat/completions"
        p["Nemotron 3 Ultra di NVIDIA (OpenRouter)"] = openai_like(o, e("OPENROUTER_API_KEY"), "nvidia/nemotron-3-ultra-550b-a55b:free")
    if e("MISTRAL_API_KEY"): p["Mistral Small"] = openai_like("https://api.mistral.ai/v1/chat/completions", e("MISTRAL_API_KEY"), "mistral-small-latest")
    if e("XAI_API_KEY"): p["Grok"] = openai_like("https://api.x.ai/v1/chat/completions", e("XAI_API_KEY"), "grok-3-mini")
    return p


def prompt(c):
    d = json.load(open(ROOT / "data" / f"{c}.json"))
    html = (ROOT / "index.html").read_text()
    js = re.search(r"function accLuce.*?\nfunction compute\(\)\{.*?\n\}", html, re.S).group(0)
    q = 2700 if c == "luce" else 1080
    ex = []
    for o in d["offerte"][:3] + d["offerte"][-2:]:
        r = d["reg"]
        if r and o.get("s") is not None:
            m = q / 12
            e = min(m, 150) if m <= 220 else max(0, 150 - (m - 220))
            acc = (m - e) * 12 * r["acc"] if r.get("acc") else (0 if q <= r["accSoglia"] else r["accRif"] * q)
            a = (1 + r["iva"]) * (o["fx"] + o["p"] * q - o["s"] + r["rf"] + r["rv"] * q + acc)
        else:
            a = o["A"] + o["B"] * q if o.get("A") is not None else o["fx"] + o["p"] * q
        ex.append({k: o.get(k) for k in ("v", "n", "t", "fx", "p", "pd", "s", "ds", "A", "B")} | {"costo_mese_sito": round(a / 12, 2)})
    return f"""Sei un revisore esperto del mercato libero energia italiano (dati Portale Offerte ARERA).
Il sito comparaoffertelucegas.it stima la spesa mensile per {c} con consumo annuo {q} {'kWh' if c == 'luce' else 'Smc'}.
Campi: fx quota fissa €/anno dell'offerta, p prezzo energia netto sconti €/unità, pd prezzo lordo, s sconto €/anno, ds sconto mostrato.
Oneri regolati usati per tutte le offerte (reg): {json.dumps(d['reg'])} (rf €/anno fissi rete+oneri, rv €/unità: per il gas include già trasporto, oneri e accise medie; iva, acc = accisa €/kWh con esenzione residenti 150 kWh/mese e recupero sopra 220).
Funzione JS usata:
{js}
Esempi calcolati dal sito:
{json.dumps(ex, ensure_ascii=False, indent=1)}

Compito: 1) ricalcola i costi degli esempi e segnala differenze; 2) indica componenti mancanti o sbagliate
(accise, IVA, oneri di sistema, trasporto, canone RAI, bonus, scaglioni, prezzi indicizzati PUN/PSV); 3) proponi
correzioni concrete. Rispondi in italiano, conciso, elenco puntato, con numeri. Se non sei sicuro dillo."""


def main():
    c = sys.argv[1] if len(sys.argv) > 1 else "luce"
    p = providers()
    if not p:
        sys.exit("Nessuna chiave trovata: aggiungile in ~/.ai_keys")
    pr = prompt(c)
    out = ROOT / "challenge"
    out.mkdir(exist_ok=True)
    f = out / f"{datetime.date.today()}-{c}.md"
    with cf.ThreadPoolExecutor() as ex:
        res = {n: ex.submit(fn, pr) for n, fn in p.items()}
        txt = [f"# Challenge calcolo {c} — {datetime.date.today()}\n"]
        for n, fu in res.items():
            try:
                txt.append(f"## {n}\n\n{fu.result()}\n")
            except Exception as e:
                txt.append(f"## {n}\n\nERRORE: {e}\n")
    f.write_text("\n".join(txt))
    print(f)


if __name__ == "__main__":
    main()
