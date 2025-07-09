import json
import logging
import requests
from flask import Flask, request, jsonify

from sender import (
    send_services_menu,
    send_weekdays_menu,
    block_day
)

# Carga configuración
def load_config():
    with open("data/config.json") as f:
        return json.load(f)

config = load_config()
PHONE_NUMBER_ID = config["phone_number_id"]
ACCESS_TOKEN    = config["access_token"]
VERIFY_TOKEN    = config["verify_token"]
WH_API_URL      = f"https://graph.facebook.com/v23.0/{PHONE_NUMBER_ID}/messages"
HEADERS         = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
user_states = {}

@app.route("/webhook", methods=["GET","POST"])
def webhook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge"), 200
        return "Forbidden", 403

    data = request.get_json()
    
    for entry in data.get("entry", []):
        for change in entry.get("changes", []):
            for msg in change.get("value", {}).get("messages", []):
                wa_id = msg.get("from")
                if not wa_id:
                    continue
                state = user_states.get(wa_id, {})

                # Paso 1: envía servicios
                if not state:
                    logging.info("Enviar servicios")
                    send_services_menu(wa_id, WH_API_URL, HEADERS)
                    user_states[wa_id] = {"step": "awaiting_service"}
                    continue

                # Paso 2: usuario elige servicio
                if state.get("step") == "awaiting_service" and msg.get("type") == "interactive":
                    svc_id = msg["interactive"]["button_reply"]["id"]
                    user_states[wa_id] = {"step": "awaiting_day", "service": svc_id}
                    send_weekdays_menu(wa_id, svc_id, WH_API_URL, HEADERS)
                    continue

                # Paso 3: usuario elige día de la semana
                if state.get("step") == "awaiting_day" and msg.get("type") == "interactive":
                    day_key = msg["interactive"]["list_reply"]["id"].replace("day_", "")
                    svc_id = state["service"]
                    # Bloquear día y confirmar
                    block_day(svc_id, day_key)
                    # Confirmación al usuario
                    payload = {
                        "messaging_product": "whatsapp",
                        "to": f"whatsapp:+{wa_id}",
                        "type": "text",
                        "text": {"body": f"Has reservado {svc_id} el {day_key.capitalize()}. Día bloqueado para futuras reservas."}
                    }
                    requests.post(WH_API_URL, json=payload, headers=HEADERS)
                    user_states.pop(wa_id)
                    continue

    return jsonify(status="received"), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)