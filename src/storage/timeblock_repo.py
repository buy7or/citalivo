# storage/timeblock_repo.py
import json, os
from storage.block_repo import add_block

_PATH = "data/blocked_slots.json"

def _load():
    # Si no existe o está vacío, devolvemos {}
    if not os.path.exists(_PATH) or os.path.getsize(_PATH) == 0:
        return {}
    try:
        with open(_PATH, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Si el contenido está corrupto, lo ignoramos y reiniciamos
        return {}

def _save(d):
    with open(_PATH, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

def get_blocked_slots(service_id, day):
    data = _load()
    return data.get(service_id, {}).get(day, [])

def add_block_slot(service_id, day, slot):
    data = _load()
    svc = data.setdefault(service_id, {})
    slots = set(svc.setdefault(day, []))
    slots.add(slot)
    svc[day] = sorted(slots)
    _save(data)

     # Comprobamos si ya están todas las franjas de 09:00 a 18:00
    all_slots = {f"{h:02d}:00" for h in range(9, 19)}
    if all_slots.issubset(slots):
        # bloqueamos el día completo para futuras selecciones
        add_block(service_id, day)
