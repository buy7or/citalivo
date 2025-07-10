# app.py
from flask import Flask, request, jsonify
import config
from handlers.time_handler import prompt_time, handle_time, prompt_period
from handlers.verify import handle_verification
from handlers.service_handler import new_user, handle_selection
from state_store import get_state

app = Flask(__name__)

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        return handle_verification(request.args)

    data = request.get_json()

    for entry in data.get("entry", []):
        for change in entry.get("changes", []):
            for msg in change.get("value", {}).get("messages", []):
                wa_id = msg.get("from")
                if not wa_id:
                    continue

                state = get_state(wa_id)
                if not state:
                    new_user(wa_id)
                    continue

                # 1) Servicio
                if state["step"] == "awaiting_service":
                    # ¿Es un botón válido?
                    if msg.get("type") == "interactive" and msg["interactive"].get("button_reply"):
                        svc_id = msg["interactive"]["button_reply"]["id"]
                        handle_selection(wa_id, svc_id)
                    else:
                        # Respuesta no válida: avisamos y reenviamos menú
                        from whatsapp_client import send_message
                        from sender import build_services_menu
                        send_message({
                            "messaging_product": "whatsapp",
                            "to": f"whatsapp:+{wa_id}",
                            "type": "text",
                            "text": {"body": "❗️Por favor, selecciona un servicio usando los botones.",}
                        })
                        send_message(build_services_menu(wa_id))
                        # seguimos en mismo estado
                        from state_store import set_state
                        set_state(wa_id, {"step": "awaiting_service"})
                    continue

                # 2) Día
                if state["step"] == "awaiting_day" and msg.get("type") == "interactive":
                    raw_id = msg["interactive"]["list_reply"]["id"]
                    day_key = raw_id.replace("day_", "")
                    svc_id = state["service"]
                    prompt_period(wa_id, svc_id, day_key)
                    continue

                # 3) Mañana o tarde
                if state["step"] == "awaiting_period" and msg.get("type") == "interactive":
                    period = msg["interactive"]["button_reply"]["id"].replace("period_", "")
                    svc_id = state["service"]
                    day_key = state["day"]
                    prompt_time(wa_id, svc_id, day_key, period)
                    continue

                # 4) Hora concreta
                if state["step"] == "awaiting_time" and msg.get("type") == "interactive":
                    slot = msg["interactive"]["list_reply"]["id"].replace("time_", "")
                    svc_id = state["service"]
                    day_key = state["day"]
                    handle_time(wa_id, svc_id, day_key, slot)
                    continue

    return jsonify(status="received"), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
