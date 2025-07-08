import json
import logging
from flask import Flask, request, jsonify
from sender import (
    send_quick_replies,
    send_hola_mundo,
    send_adios_mundo,
)

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

def handle_user_response(wa_id: str, msg: dict):
    """
    Procesa la respuesta del usuario y llama a la función correspondiente del sender.
    """
    msg_type = msg.get("type")

    # Respuesta a un botón interactivo
    if msg_type == "interactive":
        interactive = msg["interactive"]
        if interactive.get("type") == "button_reply":
            btn_id = interactive["button_reply"]["id"]
            if btn_id == "opt_hola":
                send_hola_mundo(wa_id, WH_API_URL, HEADERS)
                return
            if btn_id == "opt_adios":
                send_adios_mundo(wa_id, WH_API_URL, HEADERS)
                return

    # Si no es interacción o no se reconoce, enviamos el menú por defecto
    send_quick_replies(wa_id, WH_API_URL, HEADERS)

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
            for msg in value.get("messages", []):
                wa_id = msg.get("from")
                if not wa_id:
                    continue

                handle_user_response(wa_id, msg)

    return jsonify(status="received"), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
