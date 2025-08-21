from flask import Flask, jsonify, send_from_directory, request
import os
from scraper import scrape_all

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), "..", "static"), static_url_path="/static")

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/search")
def search():
    sort = request.args.get("sort","price")
    order = request.args.get("order","asc")
    q = request.args.get("q","")
    items = scrape_all(q)
    keymap = {"price":"price_eur","thc":"thc_percent","yield":"yield_grams","duration":"days"}
    key = keymap.get(sort, "price_eur")
    items = [r for r in items if not q or q.lower() in r["name"].lower()]
    items.sort(key=lambda x: (x.get(key) is None, x.get(key)), reverse=(order=="desc"))
    return jsonify(items)

@app.route("/<path:path>")
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    app.run(debug=True)
