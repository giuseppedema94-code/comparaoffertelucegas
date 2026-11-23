"""Riepilogo quotidiano via mail: GoatCounter + Clarity (+ Google Analytics se configurato).
Segreti richiesti: GC_TOKEN, GMAIL_USER, GMAIL_APP_PASSWORD. Facoltativi: CLARITY_TOKEN, GA_PROPERTY, GA_KEY (JSON account di servizio)."""
import datetime as dt, json, os, smtplib, ssl, urllib.parse, urllib.request
from email.mime.text import MIMEText
from zoneinfo import ZoneInfo

GC = "https://comparaoffertelucegas.goatcounter.com/api/v0"
oggi = dt.datetime.now(ZoneInfo("Europe/Rome")).date()
ieri, altro = oggi - dt.timedelta(days=1), oggi - dt.timedelta(days=2)
E_ = os.environ.get


def get(url, tok, **q):
    req = urllib.request.Request(url + ("?" + urllib.parse.urlencode(q) if q else ""),
                                 headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json", "User-Agent": "report"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def n(x):
    return f"{x:,}".replace(",", ".")


def var(a, b):
    if not b:
        return ""
    p = round((a - b) / b * 100)
    return f" ({'+' if p >= 0 else ''}{p}% rispetto a due giorni fa)"


righe, err = [], []
# --- GoatCounter
try:
    t = E_("GC_TOKEN")
    rng = lambda d: {"start": str(d), "end": str(d)}
    tot = get(GC + "/stats/total", t, **rng(ieri))
    tot2 = get(GC + "/stats/total", t, **rng(altro))
    v, v2 = tot.get("total", 0), tot2.get("total", 0)
    hits = get(GC + "/stats/hits", t, limit=50, **rng(ieri)).get("hits", [])
    pag = [h for h in hits if not h.get("event")]
    ev = [h for h in hits if h.get("event") and str(h.get("path", "")).startswith("esce-")]
    ref = get(GC + "/stats/toprefs", t, limit=6, **rng(ieri)).get("stats", [])
    c = lambda h: h.get("count", h.get("count_unique", 0))
    righe.append(f"<h3>Visite</h3><p><b>{n(v)}</b> pagine viste{var(v, v2)}.</p>")
    if ev:
        righe.append(f"<p><b>{n(sum(c(h) for h in ev))}</b> clic verso i fornitori: " +
                     ", ".join(f"{h['path'][5:]} {c(h)}" for h in sorted(ev, key=c, reverse=True)[:8]) + ".</p>")
    if pag:
        righe.append("<p>Pagine: " + ", ".join(f"{h['path']} {c(h)}" for h in sorted(pag, key=c, reverse=True)[:6]) + ".</p>")
    if ref:
        righe.append("<p>Provenienza: " + ", ".join(f"{r.get('name') or 'diretto'} {r.get('count', 0)}" for r in ref) + ".</p>")
except Exception as e:
    err.append(f"GoatCounter: {e}")
# --- Clarity (ultime 24 ore)
if E_("CLARITY_TOKEN"):
    try:
        d = get("https://www.clarity.ms/export-data/api/v1/project-live-insights", E_("CLARITY_TOKEN"), numOfDays=1)
        m = {x.get("metricName"): (x.get("information") or [{}])[0] for x in d}
        tr = m.get("Traffic", {})
        val = lambda k: next((m.get(k, {}).get(f) for f in ("sessionsCount", "subTotal", "pagesViews") if m.get(k, {}).get(f) is not None), "0")
        righe.append(f"<h3>Comportamento (Clarity, ultime 24 ore)</h3><p>{tr.get('totalSessionCount', 0)} sessioni registrate, "
                     f"{tr.get('distinctUserCount', 0)} utenti. Clic a vuoto in {val('DeadClickCount')} sessioni, clic ripetuti per frustrazione in {val('RageClickCount')}, "
                     f"ritorni rapidi alla pagina precedente in {val('QuickbackClick')}. Scorrimento medio {m.get('ScrollDepth', {}).get('averageScrollDepth', '?')}%.</p>")
    except Exception as e:
        err.append(f"Clarity: {e}")
# --- Google Analytics (facoltativo)
if E_("GA_PROPERTY") and E_("GA_KEY"):
    try:
        from google.analytics.data_v1beta import BetaAnalyticsDataClient
        from google.analytics.data_v1beta.types import DateRange, Metric, RunReportRequest
        from google.oauth2 import service_account
        cr = service_account.Credentials.from_service_account_info(json.loads(E_("GA_KEY")))
        r = BetaAnalyticsDataClient(credentials=cr).run_report(RunReportRequest(
            property="properties/" + E_("GA_PROPERTY"), date_ranges=[DateRange(start_date=str(ieri), end_date=str(ieri))],
            metrics=[Metric(name=x) for x in ("activeUsers", "newUsers", "averageSessionDuration", "engagementRate")]))
        if r.rows:
            a, nu, dur, eng = (x.value for x in r.rows[0].metric_values)
            righe.append(f"<h3>Google Analytics (chi ha accettato i cookie)</h3><p>{a} utenti, di cui {nu} nuovi. "
                         f"Durata media {round(float(dur))} secondi, coinvolgimento {round(float(eng) * 100)}%.</p>")
    except Exception as e:
        err.append(f"Google Analytics: {e}")

if err:
    righe.append("<p style='color:#a33'>Non letti: " + "; ".join(err) + "</p>")
corpo = (f"<div style='font:15px/1.5 -apple-system,Segoe UI,sans-serif;color:#14161A;max-width:620px'>"
         f"<h2 style='margin:0 0 4px'>comparaoffertelucegas.it</h2><p style='color:#666;margin:0 0 12px'>Riepilogo del {ieri.strftime('%d/%m/%Y')}</p>"
         + "".join(righe) +
         "<p style='color:#666;font-size:13px'>Dettagli: <a href='https://comparaoffertelucegas.goatcounter.com'>GoatCounter</a>, "
         "<a href='https://clarity.microsoft.com'>Clarity</a>, <a href='https://analytics.google.com'>Analytics</a></p></div>")
msg = MIMEText(corpo, "html", "utf-8")
msg["Subject"] = f"Sito luce e gas: riepilogo del {ieri.strftime('%d/%m')}"
msg["From"] = msg["To"] = E_("GMAIL_USER")
if os.environ.get("SOLO_STAMPA"):
    print(corpo)
else:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as s:
        s.login(E_("GMAIL_USER"), E_("GMAIL_APP_PASSWORD"))
        s.send_message(msg)
    print("inviata")
