from storage.services_repo import get_all_services
from storage.block_repo      import get_blocked
from storage.timeblock_repo import get_blocked_slots

def build_services_menu(to_whatsapp_id):
    services = get_all_services()
    buttons = [
        {
          "type": "reply",
          "reply": {"id": svc["id"], "title": svc["title"]}
        }
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
    blocked = get_blocked(service_id)
    rows = [
      {"id": f"day_{key}", "title": name}
      for key, name in weekdays
      if key not in blocked
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

def build_times_menu(to_whatsapp_id, service_id, day_key):
    # Ejemplo: franjas de 09:00 a 18:00 cada hora
    all_slots = [f"{h:02d}:00" for h in range(9,19)]
    blocked = get_blocked_slots(service_id, day_key)
    rows = [
      {"id": f"time_{slot}", "title": slot}
      for slot in all_slots if slot not in blocked
    ]
    return {
      "messaging_product":"whatsapp",
      "to":f"whatsapp:+{to_whatsapp_id}",
      "type":"interactive",
      "interactive":{
        "type":"list",
        "body":{"text":f"Has elegido {day_key.capitalize()}. Ahora, elige la hora:"},
        "action":{
          "button":"Ver horas",
          "sections":[{"title": "Horas disponibles", "rows": rows}]
        }
      }
    }

def build_confirmation_message(to_whatsapp_id, service_id, day_key):
    return {
      "messaging_product": "whatsapp",
      "to": f"whatsapp:+{to_whatsapp_id}",
      "type": "text",
      "text": {
        "body": (
          f"Has reservado {service_id} el "
          f"{day_key.capitalize()}. Día bloqueado para futuras reservas."
        )
      }
    }
