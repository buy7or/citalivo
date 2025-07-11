# handlers/time_handler.py
from utils.whatsapp_client import send_message
from utils.menu_builder import build_times_menu, build_period_menu, build_confirmation_message, build_services_menu
from storage.timeblock_repo import add_block_slot
from state_store import clear_state, set_state, get_state
from utils.errors import safe_handler, ValidationError
from utils.validators import require_button_reply,require_list_reply


@safe_handler
def handle_period(wa_id, msg):
    """
    Valida que venga button_reply, que el id sea uno de los esperados,
    y lanza prompt_time. Si falla, reenvía build_period_menu.
    """
    # 1) Recuperar estado previo
    st = get_state(wa_id)
    svc_id  = st.get("service")
    day_key = st.get("day")
    if not svc_id or not day_key:
        raise ValidationError(
            "Ha ocurrido un error interno. Reinicia el flujo.",
            resend_menu=build_period_menu,
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



@safe_handler
def handle_time(wa_id, msg):
    """
    1) Valida que venga list_reply; si no, reenvía build_times_menu con service, day y period.
    2) Extrae slot, lo reserva y confirma.
    3) Limpia estado.
    """
    # 1. Recuperar datos del estado
    st = get_state(wa_id)
    svc_id  = st.get("service")
    day_key = st.get("day")
    period  = st.get("period")
    if not all([svc_id, day_key, period]):
        # Si falta algo, reiniciamos todo el flujo de selección de servicio
        raise ValidationError(
            "Ha ocurrido un error interno. Empecemos de nuevo.",
            resend_menu=build_services_menu,  
            menu_args=[]
        )

    # 2. Validar y extraer el ID de la lista
    raw_id = require_list_reply(
        msg,
        resend_menu=build_times_menu,
        menu_args=[svc_id, day_key, period]
    )
    slot = raw_id.replace("time_", "")

    # 3. Reserva el slot y confirma
    add_block_slot(svc_id, day_key, slot)
    payload = build_confirmation_message(wa_id, svc_id, day_key, slot)
    send_message(payload)

    # 4. Cerramos el flujo
    clear_state(wa_id)
