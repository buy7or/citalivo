# handlers/day_handler.py
from utils.whatsapp_client import send_message
from utils.menu_builder import build_period_menu, build_weekdays_menu, build_services_menu
from storage.state_store import set_state, get_state, clear_state
from utils.errors import safe_handler, ValidationError
from utils.validators import require_list_reply


# TODO comprobar que la elección es un día
# TODO comprobar que el día seleccionado no está bloqueado 

@safe_handler
def handle_day(wa_id, msg):
    
    state = get_state(wa_id)
    svc_id = state.get("service")

    if not svc_id:
        clear_state(wa_id)
        raise ValidationError(
            "Ha ocurrido un error. Volvamos a empezar.",
            resend_menu=build_services_menu,
            menu_args=[None]
        )
    
    raw_id = require_list_reply(
        msg,
        resend_menu=build_weekdays_menu,
        menu_args=[svc_id]
    )

    day_key = raw_id.replace("day_", "")
    
    set_state(wa_id, {"step": "awaiting_period", "service": svc_id, "day": day_key})
    send_message(build_period_menu(wa_id))