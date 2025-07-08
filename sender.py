import requests

def send_quick_replies(to_whatsapp_id: str, api_url: str, headers: dict):
    """Envía un menú de 2 botones: 'Hola Mundo' y 'Adiós Mundo'"""
    payload = {
        "messaging_product": "whatsapp",
        "to": f"whatsapp:+{to_whatsapp_id}",
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": { "text": "Elige una opción:" },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": { "id": "opt_hola", "title": "👋 Hola Mundo" }
                    },
                    {
                        "type": "reply",
                        "reply": { "id": "opt_adios", "title": "👋 Adiós Mundo" }
                    }
                ]
            }
        }
    }
    resp = requests.post(api_url, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()


def send_hola_mundo(to_whatsapp_id: str, api_url: str, headers: dict):
    payload = {
        "messaging_product": "whatsapp",
        "to": f"whatsapp:+{to_whatsapp_id}",
        "type": "text",
        "text": {"body": "¡Hola Mundo!"}
    }
    resp = requests.post(api_url, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()

def send_adios_mundo(to_whatsapp_id: str, api_url: str, headers: dict):
    payload = {
        "messaging_product": "whatsapp",
        "to": f"whatsapp:+{to_whatsapp_id}",
        "type": "text",
        "text": {"body": "👋 Adiós Mundo"}
    }
    resp = requests.post(api_url, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()
