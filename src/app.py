from flask import Flask, request, jsonify
import config

from handlers.verify          import handle_verification
from handlers.service_handler import new_user, handle_selection
from handlers.day_handler     import handle_day
from state_store              import get_state

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

                if state["step"] == "awaiting_service" and msg.get("type") == "interactive":
                    svc_id = msg["interactive"]["button_reply"]["id"]
                    handle_selection(wa_id, svc_id)
                    continue

                if state["step"] == "awaiting_day" and msg.get("type") == "interactive":
                    raw_id = msg["interactive"]["list_reply"]["id"]
                    day_key = raw_id.replace("day_", "")
                    svc_id  = state["service"]
                    handle_day(wa_id, svc_id, day_key)
                    continue

    return jsonify(status="received"), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
