from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return f"<h1>scheme = {request.scheme}</h1><p>secure = {request.is_secure}</p>"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=7000, debug=True, ssl_context="adhoc")