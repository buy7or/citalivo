import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Valores escritos directamente
PHONE_NUMBER_ID = "698125916724321"  # tu Phone Number ID
ACCESS_TOKEN    = "EAAXOfSwnZAZBABPEOf0VkEJpdSs2kc9goEQZBaOtbKzfQyYJTMnDMjENETSsu7loPiWYesyrwELL42rw5HgjPGxz4GKMcK9oKwRznjqviIjw7kY8znz5YLnLgMFKnaI5Ovo97tYDfTCFXXo4jADcyrZB0TBVA9lEom7j7wWo45eOoZBli935ebXd7kYyQN9u0FxJr3sipSNrXW197tgeJnRHYtbQJN8Ni8MtZC1QEJwc9B3WUZD"
VERIFY_TOKEN    = "mi_token_personal"  # el token que configures en Facebook

WH_API_URL = f"https://graph.facebook.com/v23.0/{PHONE_NUMBER_ID}/messages"
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def send_hola_mundo(to_whatsapp_id: str):
    payload = {
        "messaging_product": "whatsapp",
        "to": to_whatsapp_id,
        "type": "text",
        "text": { "body": "¡Hola Mundo!" }
    }
    resp = requests.post(WH_API_URL, json=payload, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        hub_verify = request.args.get("hub.verify_token")
        challenge  = request.args.get("hub.challenge")
        if hub_verify == VERIFY_TOKEN:
            return challenge, 200
        return "Forbidden", 403

    data = request.get_json()
    for entry in data.get("entry", []):
        for change in entry.get("changes", []):
            for msg in change.get("value", {}).get("messages", []):
                whatsapp_id = msg["from"]
                to_whatsapp = f"whatsapp:+{whatsapp_id}"
                try:
                    send_hola_mundo(to_whatsapp)
                except Exception as e:
                    app.logger.error(f"Error enviando Hola Mundo: {e}")
    return jsonify(status="received"), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
