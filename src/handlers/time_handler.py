# handlers/time_handler.py
from utils.whatsapp_client import send_message
from utils.menu_builder import build_times_menu, build_period_menu, build_confirmation_message
from storage.timeblock_repo import add_block_slot
from state_store import clear_state, set_state

def prompt_period(wa_id, service_id, day_key):
    """Pregunta al usuario si prefiere mañana o tarde."""
    payload = build_period_menu(wa_id)
    send_message(payload)
    set_state(wa_id, {"step": "awaiting_period", "service": service_id, "day": day_key})

def prompt_time(wa_id, service_id, day_key, period):
    """Envía el menú de horas filtrado según mañana (<13h) o tarde (>=13h)."""
    payload = build_times_menu(wa_id, service_id, day_key, period)
    send_message(payload)
    set_state(wa_id, {"step": "awaiting_time", "service": service_id, "day": day_key, "period": period})

def handle_time(wa_id, service_id, day_key, slot):
    """Bloquea la hora y envía confirmación."""
    add_block_slot(service_id, day_key, slot)
    payload = build_confirmation_message(wa_id, service_id, day_key, slot)
    send_message(payload)
    clear_state(wa_id)
