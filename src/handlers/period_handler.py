# handlers/period_handler.py
from utils.whatsapp_client import send_message
from utils.menu_builder import build_times_menu, build_period_menu, build_services_menu
from storage.state_store import set_state, get_state, clear_state
from utils.errors import safe_handler, ValidationError
from utils.validators import require_button_reply



@safe_handler
def handle_period(wa_id, msg):
    # 1) Recuperar estado previo
    st = get_state(wa_id)
    svc_id  = st.get("service")
    day_key = st.get("day")
    if not svc_id or not day_key:
        
        clear_state(wa_id)

        raise ValidationError(
            "Ha ocurrido un error. Volvamos a empezar.",
            resend_menu=build_services_menu,
            menu_args=[]
        )

    # 2) Validar que venga un button_reply
    btn_id = require_button_reply(
        msg,
        resend_menu=build_period_menu,
        menu_args=[]
    )

    # 3) Extraer y validar el periodo
    if btn_id not in ("period_morning", "period_afternoon"):
        raise ValidationError(
            "Opción inválida. Elige 'Mañana' o 'Tarde'.",
            resend_menu=build_period_menu,
            menu_args=[]
        )
    period = btn_id.replace("period_", "")

    # 4) Continuar flujo: mostrar horas
    set_state(wa_id, {"step": "awaiting_time", 
                      "service": svc_id, 
                      "day": day_key, 
                      "period": period})
    payload = build_times_menu(wa_id, svc_id, day_key, period)
    return send_message(payload)
