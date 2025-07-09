import requests
import config

def send_message(payload):
    """Envía cualquier payload al API de WhatsApp y retorna la respuesta."""
    resp = requests.post(
        config.WH_API_URL,
        json=payload,
        headers=config.HEADERS
    )
    return resp
