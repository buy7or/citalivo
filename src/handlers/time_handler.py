# handlers/time_handler.py
from utils.whatsapp_client import send_message
from utils.menu_builder import build_times_menu, build_confirmation_message, build_services_menu
from storage.timeblock_repo import add_block_slot, is_slot_available
from storage.state_store import clear_state, get_state
from utils.errors import safe_handler, ValidationError
from utils.validators import require_list_reply


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

    if not is_slot_available(day_key, slot):
        send_message({
            "messaging_product": "whatsapp",
            "to": f"whatsapp:+{wa_id.split('@')[0]}",
            "type": "text",
            "text": {
                "body": "Lo siento, esa hora ya ha sido reservada. Por favor elige otra."
            }
        })
        return
    
    # 3. Reserva el slot y confirma
    phone = wa_id.split("@")[0]
    add_block_slot(day_key, slot, phone)
    payload = build_confirmation_message(wa_id, svc_id, day_key, slot)
    send_message(payload)

    # 4. Cerramos el flujo
    clear_state(wa_id)
