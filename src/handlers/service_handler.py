from sender           import build_services_menu, build_weekdays_menu
from whatsapp_client  import send_message
from state_store      import set_state
from storage.services_repo import get_all_services

def new_user(wa_id):
    payload = build_services_menu(wa_id)
    send_message(payload)
    set_state(wa_id, {"step": "awaiting_service"})

def handle_selection(wa_id, service_id):

    valid_ids = {svc["id"] for svc in get_all_services()}
    if service_id not in valid_ids:
        # Notificar error
        send_message({
            "messaging_product": "whatsapp",
            "to": f"whatsapp:+{wa_id}",
            "type": "text",
            "text": {"body": "Lo siento, esa opción no es válida. Por favor selecciona un servicio de la lista."}
        })
        # Reenviamos menú de servicios y dejamos estado en awaiting_service
        send_message(build_services_menu(wa_id))
        set_state(wa_id, {"step": "awaiting_service"})
        return
    payload = build_weekdays_menu(wa_id, service_id)
    send_message(payload)
    set_state(wa_id, {"step": "awaiting_day", "service": service_id})
