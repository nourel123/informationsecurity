from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

PASSIVE_HEADERS = [
    "User-Agent", "Accept-Language", "Accept", "Accept-Encoding",
    "Sec-CH-UA", "Sec-CH-UA-Platform", "Sec-CH-UA-Mobile",
    "Sec-Fetch-Site", "Sec-Fetch-Mode", "Sec-Fetch-Dest",
    "Upgrade-Insecure-Requests", "DNT", "Sec-GPC", "Referer", "Connection",
]

@app.route("/")
def home():
    passive = {h: request.headers.get(h, "— not sent —") for h in PASSIVE_HEADERS}
    passive["IP address"] = request.remote_addr
    passive["HTTP method"] = request.method

    print("\n========== NEW VISIT (passive) ==========")
    for name, value in passive.items():
        print(f"{name:28}: {value}")
    print("=========================================\n")

    return render_template("index.html", passive=passive)

@app.route("/collect", methods=["POST"])
def collect():
    data = request.get_json(silent=True) or {}

    if data.get("type") == "active":
        print("\n---------- ACTIVE FEATURES ----------")
        for name, value in data.get("features", {}).items():
            print(f"{name:22}: {value}")
        print("-------------------------------------\n")
    elif data.get("type") == "typing":
            print("\n---------- TYPING BEHAVIOUR ----------")
            print(f"{'Total time':22}: {data.get('typingTime')} s")
            print(f"{'Typing speed':22}: {data.get('typingSpeed')} WPM")
            print(f"{'Corrections':22}: {data.get('corrections')}")
            print(f"{'Sentence length':22}: {data.get('sentenceLength')} characters")
            print("--------------------------------------\n")

    return jsonify(ok=True)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)