from flask import abort
import config

def handle_verification(args):
    """Devuelve hub.challenge si el token es correcto, si no 403."""
    if args.get("hub.verify_token") == config.VERIFY_TOKEN:
        return args.get("hub.challenge"), 200
    abort(403)
