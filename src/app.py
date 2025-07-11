# app.py
from flask import Flask, request, jsonify
from handlers.time_handler import handle_time
from handlers.period_handler import handle_period
from handlers.day_handler import handle_day
from utils.verify import handle_verification
from handlers.service_handler import new_user, handle_selection
from storage.state_store import get_state

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
                if not state and msg.get("type") == "text":
                    new_user(wa_id)
                    continue

                # 1) Servicio
                if state["step"] == "awaiting_service":
                    handle_selection(wa_id, msg)
                    continue

                # 2) Día
                if state["step"] == "awaiting_day":
                    handle_day(wa_id,msg)
                    continue

                # 3) Mañana o tarde
                if state["step"] == "awaiting_period":
                    handle_period(wa_id,msg)
                    continue

                # 4) Hora concreta
                if state["step"] == "awaiting_time":
                    handle_time(wa_id,msg)
                    continue

    return jsonify(status="received"), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
