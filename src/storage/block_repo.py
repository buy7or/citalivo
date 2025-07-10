#storage/block_repo
import json
import os

_PATH = "data/blocked_days.json"

def _load():
    if not os.path.exists(_PATH):
        return {}
    with open(_PATH, encoding="utf-8") as f:
        return json.load(f)

def _save(data):
    with open(_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_blocked(service_id):
    data = _load()
    return data.get(service_id, [])

def add_block(service_id, day):
    data = _load()
    days = set(data.get(service_id, []))
    days.add(day)
    data[service_id] = list(days)
    _save(data)
