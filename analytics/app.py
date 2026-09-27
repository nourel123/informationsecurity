from flask import Flask, request, make_response
from datetime import datetime

app = Flask(__name__)

LOG = []

# 1x1 transparent GIF — the classic tracking pixel
PIXEL = (b'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!'
         b'\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00'
         b'\x00\x02\x02D\x01\x00;')


@app.route("/collect")
def collect():
    entry = {
        "time":   datetime.now().strftime("%H:%M:%S"),
        "aid":    request.args.get("aid"),
        "site":   request.args.get("site"),
        "page":   request.args.get("page"),
        "title":  request.args.get("title"),
        "event":  request.args.get("event", "pageview"),
        "target": request.args.get("target"),
        "lang":   request.args.get("lang"),
        "screen": request.args.get("screen"),
        "tz":     request.args.get("tz"),
        # what the BROWSER added by itself:
        "referer": request.headers.get("Referer"),
        "cookies_received": request.headers.get("Cookie"),
        "ip":      request.remote_addr,
    }
    LOG.append(entry)

    print(f"[{entry['time']}] aid={entry['aid']}  site={entry['site']}  "
          f"page={entry['page']}  event={entry['event']}")
    print(f"           Referer: {entry['referer']}")
    print(f"           Cookie header received: {entry['cookies_received']}")

    response = make_response(PIXEL)
    response.headers["Content-Type"] = "image/gif"
    return response


@app.route("/profile")
def profile():
    by_aid = {}
    for e in LOG:
        by_aid.setdefault(e["aid"], []).append(e)

    html = ["<h1>Profiles held by analytics.test</h1>",
            f"<p>{len(LOG)} events, <b>{len(by_aid)} distinct identifiers</b></p>"]
    for aid, events in by_aid.items():
        sites = sorted({e["site"] for e in events})
        html.append(f"<h2>aid = {aid}</h2>")
        html.append(f"<p>seen on: <b>{', '.join(sites)}</b></p><ol>")
        for e in events:
            html.append(f"<li>{e['time']} — {e['site']}{e['page']} "
                        f"[{e['event']}] {e['target'] or ''}</li>")
        html.append("</ol>")
    return "\n".join(html)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=9100, debug=True)