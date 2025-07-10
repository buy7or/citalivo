

def require_button_reply(msg):
    interactive = msg.get("interactive", {})
    btn = interactive.get("button_reply")
    if not btn:
        from handlers.errors import ValidationError
        raise ValidationError(
            "Por favor selecciona usando los botones.",
            resend_menu=None  # luego inyectaremos el menú adecuado
        )
    return btn["id"]

def require_list_reply(msg):
    interactive = msg.get("interactive", {})
    lst = interactive.get("list_reply")
    if not lst:
        from handlers.errors import ValidationError
        raise ValidationError(
            "Por favor elige una opción de la lista.",
            resend_menu=None
        )
    return lst["id"]