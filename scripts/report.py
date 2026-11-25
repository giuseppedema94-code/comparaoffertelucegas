"""Riepilogo quotidiano via mail: GoatCounter + Clarity (+ Google Analytics se configurato).
Segreti richiesti: GC_TOKEN, MAIL_USER, MAIL_PASSWORD (casella Aruba del sito). Facoltativi: CLARITY_TOKEN, GA_PROPERTY, GA_KEY (JSON account di servizio)."""
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


def credenziali(scopes):
    """Account di servizio: da GA_KEY se presente, altrimenti dal collegamento GitHub-Google senza chiavi (google-github-actions/auth)."""
    if E_("GA_KEY"):
        from google.oauth2 import service_account
        return service_account.Credentials.from_service_account_info(json.loads(E_("GA_KEY")), scopes=scopes)
    import google.auth
    return google.auth.default(scopes=scopes)[0]


GOOGLE = bool(E_("GA_KEY") or E_("GOOGLE_APPLICATION_CREDENTIALS"))
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
                     f"ritorni rapidi alla pagina precedente in {val('QuickbackClick')}. Errori JavaScript in {val('ScriptErrorCount')} sessioni." + (f" Scorrimento medio {round(sd)}%." if (sd := m.get('ScrollDepth', {}).get('averageScrollDepth')) is not None else "") + "</p>")
    except Exception as e:
        err.append(f"Clarity: {e}")
# --- Google Analytics (facoltativo)
if E_("GA_PROPERTY") and GOOGLE:
    try:
        from google.analytics.data_v1beta import BetaAnalyticsDataClient
        from google.analytics.data_v1beta.types import DateRange, Metric, RunReportRequest
        cr = credenziali(["https://www.googleapis.com/auth/analytics.readonly"])
        r = BetaAnalyticsDataClient(credentials=cr).run_report(RunReportRequest(
            property="properties/" + E_("GA_PROPERTY"), date_ranges=[DateRange(start_date=str(ieri), end_date=str(ieri))],
            metrics=[Metric(name=x) for x in ("activeUsers", "newUsers", "averageSessionDuration", "engagementRate")]))
        if r.rows:
            a, nu, dur, eng = (x.value for x in r.rows[0].metric_values)
            righe.append(f"<h3>Google Analytics (chi ha accettato i cookie)</h3><p>{a} utenti, di cui {nu} nuovi. "
                         f"Durata media {round(float(dur))} secondi, coinvolgimento {round(float(eng) * 100)}%.</p>")
    except Exception as e:
        err.append(f"Google Analytics: {e}")

# --- Search Console, tutti i siti (dati con 2-3 giorni di ritardo: ultimi 7 giorni disponibili contro i 7 precedenti)
SITI = [("comparaoffertelucegas.it", "sc-domain:comparaoffertelucegas.it"), ("stipendioccnl.it", "sc-domain:stipendioccnl.it"),
        ("vestitiperanimali.it", "sc-domain:vestitiperanimali.it"), ("superocchiali.it", "sc-domain:superocchiali.it")]
sezioni = {}
if GOOGLE:
    try:
        from google.auth.transport.requests import AuthorizedSession
        ses = AuthorizedSession(credenziali(["https://www.googleapis.com/auth/webmasters.readonly"]))
        fine = oggi - dt.timedelta(days=3)

        def q(prop, a, b, **extra):
            u = "https://searchconsole.googleapis.com/webmasters/v3/sites/" + urllib.parse.quote(prop, safe="") + "/searchAnalytics/query"
            r = ses.post(u, json={"startDate": str(a), "endDate": str(b), **extra}, timeout=60)
            r.raise_for_status()
            return r.json().get("rows", [])

        for nome, prop in SITI:
            try:
                a = q(prop, fine - dt.timedelta(days=6), fine)
                b = q(prop, fine - dt.timedelta(days=13), fine - dt.timedelta(days=7))
                cur, pre = (a[0] if a else {}), (b[0] if b else {})
                top = q(prop, fine - dt.timedelta(days=6), fine, dimensions=["query"], rowLimit=5)
                txt = (f"<p><b>{n(int(cur.get('clicks', 0)))}</b> clic e <b>{n(int(cur.get('impressions', 0)))}</b> impressioni su Google"
                       + var(cur.get('impressions', 0), pre.get('impressions', 0)).replace('due giorni fa', 'la settimana prima')
                       + (f", posizione media {cur['position']:.1f}" if cur.get('position') else "")
                       + f" ({(fine - dt.timedelta(days=6)).strftime('%d/%m')}-{fine.strftime('%d/%m')}).</p>")
                if top:
                    txt += "<p>Ricerche: " + ", ".join(f"{r['keys'][0]} ({int(r['impressions'])})" for r in top) + ".</p>"
                sezioni[nome] = txt
            except Exception as e:
                sezioni[nome] = f"<p style='color:#a33'>Search Console non letto: {e}</p>"
    except Exception as e:
        err.append(f"Search Console: {e}")

if err:
    righe.append("<p style='color:#a33'>Non letti: " + "; ".join(err) + "</p>")
box = lambda nome, html: f"<h2 style='margin:24px 0 4px;font-size:19px'>{nome}</h2>" + html
blocchi = box("comparaoffertelucegas.it", sezioni.get("comparaoffertelucegas.it", "") + "".join(righe))
for nome, _ in SITI[1:]:
    blocchi += box(nome, sezioni.get(nome, "<p style='color:#666'>Search Console non configurato.</p>"))
corpo = (f"<div style='font:15px/1.5 -apple-system,Segoe UI,sans-serif;color:#14161A;max-width:620px'>"
         f"<h1 style='margin:0 0 4px;font-size:22px'>I tuoi siti</h1><p style='color:#666;margin:0 0 12px'>Riepilogo del {ieri.strftime('%d/%m/%Y')}</p>"
         + blocchi +
         "<p style='color:#666;font-size:13px'>Dettagli: <a href='https://search.google.com/search-console'>Search Console</a>, "
         "<a href='https://comparaoffertelucegas.goatcounter.com'>GoatCounter</a>, "
         "<a href='https://clarity.microsoft.com'>Clarity</a>, <a href='https://analytics.google.com'>Analytics</a></p></div>")
if E_("GITHUB_STEP_SUMMARY"):
    with open(E_("GITHUB_STEP_SUMMARY"), "a", encoding="utf-8") as f:
        f.write(corpo)
# Invio: Gmail (GMAIL_USER + password per le app) se configurato, altrimenti la casella Aruba
if (E_("GMAIL_USER") or "").strip() and (E_("GMAIL_APP_PASSWORD") or "").strip():
    server, utente, pw = "smtp.gmail.com", E_("GMAIL_USER").strip(), E_("GMAIL_APP_PASSWORD").replace(" ", "").strip()
else:
    server, utente, pw = "smtps.aruba.it", (E_("MAIL_USER") or "").strip(), (E_("MAIL_PASSWORD") or "").strip()
msg = MIMEText(corpo, "html", "utf-8")
msg["Subject"] = f"I tuoi siti: riepilogo del {ieri.strftime('%d/%m')}"
msg["From"] = "Report siti <" + utente + ">"
msg["To"] = E_("MAIL_TO", "") or utente
if os.environ.get("SOLO_STAMPA"):
    print(corpo)
else:
    if not (utente and pw):
        raise SystemExit("Credenziali mail mancanti nei secret: il report e solo nel riepilogo di GitHub Actions")
    with smtplib.SMTP_SSL(server, 465, context=ssl.create_default_context()) as s:
        s.login(utente, pw)
        s.send_message(msg)
    print("inviata")
