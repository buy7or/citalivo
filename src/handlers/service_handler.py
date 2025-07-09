from sender           import build_services_menu, build_weekdays_menu
from whatsapp_client  import send_message
from state_store      import set_state

def new_user(wa_id):
    payload = build_services_menu(wa_id)
    send_message(payload)
    set_state(wa_id, {"step": "awaiting_service"})

def handle_selection(wa_id, service_id):
    payload = build_weekdays_menu(wa_id, service_id)
    send_message(payload)
    set_state(wa_id, {"step": "awaiting_day", "service": service_id})
