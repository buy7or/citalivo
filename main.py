import json
import logging
from flask import Flask, request, jsonify
from sender import send_hola_mundo

# Cargar configuración desde config.json
with open("config.json") as f:
    config = json.load(f)

PHONE_NUMBER_ID = config["phone_number_id"]
ACCESS_TOKEN = config["access_token"]
VERIFY_TOKEN = config["verify_token"]

WH_API_URL = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# Inicializar app Flask
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge"), 200
        return "Forbidden", 403

    data = request.get_json()
    entries = data.get("entry", [])

    for entry in entries:
        for change in entry.get("changes", []):
            messages = change.get("value", {}).get("messages", [])
            for msg in messages:
                whatsapp_id = msg.get("from")
                if whatsapp_id:
                    try:
                        send_hola_mundo(whatsapp_id, WH_API_URL, HEADERS)
                        app.logger.info(f"Mensaje enviado a {whatsapp_id}")
                    except Exception as e:
                        app.logger.error(f"Error al enviar mensaje: {e}")
    return jsonify(status="received"), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
