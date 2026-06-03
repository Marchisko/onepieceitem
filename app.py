import os
import requests as req
from flask import Flask, jsonify, request

app = Flask(__name__)

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def supabase_get(table, params=""):
    url = f"{SUPABASE_URL}/rest/v1/{table}?{params}"
    r = req.get(url, headers=HEADERS)
    return r.json()

@app.route("/")
def health():
    return jsonify({"status": "ok", "app": "OnePieceItem API"})

@app.route("/api/cards")
def get_cards():
    params = []
    name = request.args.get("name")
    set_id = request.args.get("set_id")
    rarity = request.args.get("rarity")
    limit = request.args.get("limit", "50")
    offset = request.args.get("offset", "0")
    if name: params.append(f"name=ilike.*{name}*")
    if set_id: params.append(f"set_id=eq.{set_id}")
    if rarity: params.append(f"rarity=eq.{rarity}")
    params.append(f"limit={limit}&offset={offset}")
    data = supabase_get("cards", "&".join(params))
    return jsonify({"cards": data})

@app.route("/api/cards/<card_id>")
def get_card(card_id):
    data = supabase_get("cards", f"id=eq.{card_id}")
    return jsonify(data[0] if data else {})

@app.route("/api/sets")
def get_sets():
    data = supabase_get("sets", "order=id")
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
