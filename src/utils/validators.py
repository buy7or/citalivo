

def require_button_reply(msg,resend_menu=None, menu_args=None):
    interactive = msg.get("interactive", {})
    btn = interactive.get("button_reply")
    if not btn:
        from utils.errors import ValidationError
        raise ValidationError(
            "Por favor selecciona usando los botones.",
            resend_menu=resend_menu,
            menu_args=menu_args or []
        )
    return btn["id"]

def require_list_reply(msg, resend_menu=None, menu_args=None):
    interactive = msg.get("interactive", {})
    lst = interactive.get("list_reply")
    if not lst:
        from utils.errors import ValidationError
        raise ValidationError(
            "Por favor elige una opción de la lista.",
            resend_menu=resend_menu,
            menu_args=menu_args or []
        )
    return lst["id"]