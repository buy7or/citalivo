from utils.menu_builder           import build_services_menu, build_weekdays_menu
from utils.whatsapp_client  import send_message
from state_store      import set_state
from storage.services_repo import get_all_services
from utils.validators import require_button_reply
from utils.errors import safe_handler, ValidationError

def new_user(wa_id):
    payload = build_services_menu(wa_id)
    send_message(payload)
    set_state(wa_id, {"step": "awaiting_service"})

@safe_handler
def handle_selection(wa_id, msg):
    
    svc_id = require_button_reply(
        msg,
        resend_menu=build_services_menu
    )  
    
    valid_ids = {svc["id"] for svc in get_all_services()}
    
    if svc_id not in valid_ids:
        raise ValidationError(
            "Servicio no válido. Elige uno de la lista.",
            resend_menu=build_services_menu
        )

    # 2) lógica normal
    set_state(wa_id, {"step":"awaiting_day","service":svc_id})
    return send_message(build_weekdays_menu(wa_id, svc_id))
