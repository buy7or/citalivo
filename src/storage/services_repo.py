import json
import os

_PATH = "data/services.json"

def get_all_services():
    if not os.path.exists(_PATH):
        return []
    with open(_PATH, encoding="utf-8") as f:
        return json.load(f)
