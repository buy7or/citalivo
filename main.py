import json
import logging
from flask import Flask, request, jsonify
from sender import send_quick_replies, send_hola_mundo, send_adios_mundo

# Carga config...
with open("config.json") as f:
    config = json.load(f)
PHONE_NUMBER_ID = config["phone_number_id"]
ACCESS_TOKEN    = config["access_token"]
VERIFY_TOKEN    = config["verify_token"]

WH_API_URL = f"https://graph.facebook.com/v23.0/{PHONE_NUMBER_ID}/messages"
HEADERS    = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge"), 200
        return "Forbidden", 403

    data = request.get_json()

    for entry in data.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            # Incoming messages or button replies
            for msg in value.get("messages", []):
                wa_id = msg.get("from")
                if not wa_id: 
                    continue

                # Si es respuesta a Quick Reply
                if msg.get("type") == "interactive":
                    interactive = msg["interactive"]
                    if interactive.get("type") == "button_reply":
                        btn_id = interactive["button_reply"]["id"]
                        if btn_id == "opt_hola":
                            send_hola_mundo(wa_id, WH_API_URL, HEADERS)
                        elif btn_id == "opt_adios":
                            send_adios_mundo(wa_id, WH_API_URL, HEADERS)
                        continue

                # Si no es interacción, enviamos el menú
                send_quick_replies(wa_id, WH_API_URL, HEADERS)

    return jsonify(status="received"), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
