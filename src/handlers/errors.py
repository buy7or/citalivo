from functools import wraps
from utils.whatsapp_client import send_message

class ValidationError(Exception):
    """Se lanza cuando el payload del usuario no cumple con la forma esperada."""
    def __init__(self, message, resend_menu=None):
        super().__init__(message)
        self.message = message
        self.resend_menu = resend_menu  # función o payload a reenviar


def safe_handler(func):
    """Envuelve un handler, captura ValidationError y responde al usuario."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        wa_id = args[0]
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            # 1) Aviso de error     
            send_message({
                "messaging_product":"whatsapp",
                "to": f"whatsapp:+{wa_id}",
                "type": "text",
                "text": {"body": f"❗️ {e.message}"}
            })
            # 2) Reenvío de menú si está definido
            if e.resend_menu:
                payload = e.resend_menu(wa_id, *getattr(e, "menu_args", []))
                send_message(payload)
            # No propagamos más la excepción
    return wrapper