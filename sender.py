import requests

def send_hola_mundo(to_whatsapp_id: str, api_url: str, headers: dict):
    payload = {
        "messaging_product": "whatsapp",
        "to": f"whatsapp:+{to_whatsapp_id}",
        "type": "text",
        "text": {"body": "¡Hola Mundo!"}
    }
    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()
