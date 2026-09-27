from flask import Flask, render_template, request, make_response
from datetime import datetime
import secrets

app = Flask(__name__)

LOG = []          # in-memory: every request the tracker ever received

@app.route("/track")
def track():
    # 1. Who is this browser?
    tid = request.cookies.get("tid")
    is_new = tid is None
    if is_new:
        tid = secrets.token_hex(8)

    # 2. What did the embedding page tell us?
    publisher = request.args.get("publisher", "unknown")
    page = request.args.get("page", "unknown")
    referer = request.headers.get("Referer")

    # 3. Record it
    entry = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "tid": tid,
        "publisher": publisher,
        "page": page,
        "referer": referer,
    }
    LOG.append(entry)
    print(f"[{entry['time']}] tid={tid} new={is_new} "
          f"{publisher} → {page} | Referer: {referer}")

    # 4. Respond, tagging the browser if it's new
    response = make_response(render_template("tracker.html", tid=tid))
    if is_new:
        response.set_cookie("tid", tid, max_age=60 * 60 * 24 * 365)
    return response


@app.route("/profile")
def profile():
    profiles = {}
    for e in LOG:
        profiles.setdefault(e["tid"], []).append(e)

    html = ["<h1>Profiles reconstructed by tracker-one</h1>"]
    for tid, events in profiles.items():
        html.append(f"<h2>Browser {tid} — {len(events)} events</h2><ol>")
        for e in events:
            html.append(f"<li>{e['time']} — <b>{e['publisher']}</b> → {e['page']}</li>")
        html.append("</ol>")
    return "\n".join(html)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=9000, debug=True)
