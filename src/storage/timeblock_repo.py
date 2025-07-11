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

def get_blocked_slots(day):
    data = _load()
    return data.get(day, [])

def is_slot_available(day, slot) -> bool:
    """
    Devuelve True si la franja 'slot' NO está aún reservada en el día 'day'.
    """
    data = _load()
    # extraemos las franjas ya reservadas
    reserved = {item["slot"] for item in data.get(day, [])}
    return slot not in reserved



def add_block_slot(day, slot, phone):
    data = _load()
    raw = data.get(day, [])

    # Añadimos sólo si la franja NO existe ya
    if not any(item["slot"] == slot for item in raw):
        raw.append({"slot": slot, "phone": phone})

    # Ordenamos por hora
    raw = sorted(raw, key=lambda x: x["slot"])
    data[day] = raw
    _save(data)

    # Si están bloqueadas todas las franjas de 09:00 a 18:00…
    all_slots = {f"{h:02d}:00" for h in range(9, 19)}
    reserved = {item["slot"] for item in raw}
    if all_slots.issubset(reserved):
        add_block(day)
