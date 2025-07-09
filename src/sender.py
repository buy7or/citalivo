from storage.services_repo import get_all_services
from storage.block_repo      import get_blocked

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
