# sender.py
from storage.services_repo import get_all_services
from storage.block_repo import get_blocked
from storage.timeblock_repo import get_blocked_slots

def build_services_menu(to_whatsapp_id):
    services = get_all_services()
    buttons = [
        {"type": "reply", "reply": {"id": svc["id"], "title": svc["title"]}}
        for svc in services
    ]
    return {
        "messaging_product": "whatsapp",
        "to": f"whatsapp:+{to_whatsapp_id}",
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": "¡Bienvenido! Elige un servicio:"},
            "action": {"buttons": buttons}
        }
    }

def build_weekdays_menu(to_whatsapp_id, service_id):
    weekdays = [
        ("lunes","Lunes"), ("martes","Martes"),
        ("miercoles","Miércoles"),
        ("jueves","Jueves"), ("viernes","Viernes"),
    ]
    blocked = get_blocked()
    rows = [
        {"id": f"day_{key}", "title": name}
        for key, name in weekdays if key not in blocked
    ]
    return {
        "messaging_product": "whatsapp",
        "to": f"whatsapp:+{to_whatsapp_id}",
        "type": "interactive",
        "interactive": {
            "type": "list",
            "body": {"text": "Elige el día de la semana:"},
            "action": {
                "button": "Ver días",
                "sections": [{"title": "Semana laboral", "rows": rows}]
            }
        }
    }
def build_period_menu(wa_id):
  return {
        "messaging_product": "whatsapp",
        "to": f"whatsapp:+{wa_id}",
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": "¿Prefieres turno de mañana o de tarde?"},
            "action": {
                "buttons": [
                    {"type":"reply", "reply":{"id":"period_morning",   "title":"Mañana"}},
                    {"type":"reply", "reply":{"id":"period_afternoon", "title":"Tarde"}}
                ]
            }
        }
    }


def build_times_menu(to_whatsapp_id, service_id, day_key, period):
    # franjas de 09:00 a 18:00
    all_slots = [f"{h:02d}:00" for h in range(9, 19)]
    blocked = get_blocked_slots(day_key)

    # Filtrar según mañana (<13h) o tarde (>=13h)
    if period == "morning":
        slots = [s for s in all_slots if int(s.split(":")[0]) < 13]
    else:
        slots = [s for s in all_slots if int(s.split(":")[0]) >= 13]

    available = [s for s in slots if s not in blocked]
    rows = [{"id": f"time_{slot}", "title": slot} for slot in available]

    return {
        "messaging_product": "whatsapp",
        "to": f"whatsapp:+{to_whatsapp_id}",
        "type": "interactive",
        "interactive": {
            "type": "list",
            "body": {"text": f"Has elegido {day_key.capitalize()} ({'mañana' if period=='morning' else 'tarde'}). Ahora, elige la hora:"},
            "action": {
                "button": "Ver horas",
                "sections": [{"title": "Horas disponibles", "rows": rows}]
            }
        }
    }

def build_confirmation_message(wa_id, service_id, day_key, slot):
    text = f"✅ ¡Listo! Reservado *{service_id}* el *{day_key.capitalize()}* a las *{slot}*."
    payload = {
        "messaging_product": "whatsapp",
        "to": f"whatsapp:+{wa_id}",
        "type": "text",
        "text": {"body": text}
    }
    return payload

