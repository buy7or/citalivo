# handlers/time_handler.py
from whatsapp_client     import send_message
from sender              import build_times_menu, build_confirmation_message
from storage.timeblock_repo import add_block_slot
from state_store         import clear_state

def prompt_time(wa_id, service_id, day_key):
    """Envía el menú de horas y actualiza estado."""
    payload = build_times_menu(wa_id, service_id, day_key)
    send_message(payload)
    from state_store import set_state
    set_state(wa_id, {"step":"awaiting_time", "service":service_id, "day":day_key})

def handle_time(wa_id, service_id, day_key, slot):
    """Bloquea la hora y confirma."""
    add_block_slot(service_id, day_key, slot)
    # Usa el mismo build_confirmation_message o uno nuevo
    text = f"Reservado {service_id} el {day_key.capitalize()} a las {slot}."
    payload = {
      "messaging_product":"whatsapp",
      "to":f"whatsapp:+{wa_id}",
      "type":"text",
      "text":{"body": text}
    }
    send_message(payload)
    clear_state(wa_id)
