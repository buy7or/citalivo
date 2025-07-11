import json

def load_config():
    with open("data/config.json", encoding="utf-8") as f:
        return json.load(f)

_cfg = load_config()
PHONE_NUMBER_ID = _cfg["phone_number_id"]
ACCESS_TOKEN    = _cfg["access_token"]
VERIFY_TOKEN    = _cfg["verify_token"]
WH_API_URL      = f"https://graph.facebook.com/v23.0/{PHONE_NUMBER_ID}/messages"
HEADERS         = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}