import json
import requests
import os
import logging

# Carga servicios y bloqueos
def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)

SERVICES     = load_json("data/services.json")
BLOCKED      = load_json("data/blocked_days.json")

WH_API_URL   = ""  # Se define en main.py
HEADERS      = {}

# Envía menú de servicios
def send_services_menu(to_whatsapp_id, api_url, headers):
    buttons = [
        {"type":"reply","reply":{"id":svc["id"],"title":svc["title"]}}
        for svc in SERVICES
    ]
    payload = {
        "messaging_product":"whatsapp",
        "to":f"whatsapp:+{to_whatsapp_id}",
        "type":"interactive",
        "interactive":{
            "type":"button",
            "body":{"text":"¡Bienvenido! Elige un servicio:"},
            "action":{"buttons":buttons}
        }
    }
    resp = requests.post(api_url, json=payload, headers=headers)
    logging.info(f"send_services_menu → status {resp.status_code}, body {resp.text}")
    return resp

# Envía menú de días de lunes a viernes
def send_weekdays_menu(to_whatsapp_id, service_id, api_url, headers):
    weekdays = [
        ("monday","Lunes"),
        ("tuesday","Martes"),
        ("wednesday","Miércoles"),
        ("thursday","Jueves"),
        ("friday","Viernes"),
    ]
    # Filtra los ya bloqueados
    blocked = BLOCKED.get(service_id, [])
    rows = [
        {"id":f"day_{key}","title":name}
        for key,name in weekdays if key not in blocked
    ]
    payload = {
        "messaging_product":"whatsapp",
        "to":f"whatsapp:+{to_whatsapp_id}",
        "type":"interactive",
        "interactive":{
            "type":"list",
            "body":{"text":"Elige el día de la semana:"},
            "action":{
                "button":"Ver días",
                "sections":[{"title":"Semana laboral","rows":rows}]
            }
        }
    }
    return requests.post(api_url,json=payload,headers=headers)

# Bloquea el día seleccionado para un servicio
def block_day(service_id, day_key):
    blocked = BLOCKED.get(service_id, [])
    if day_key not in blocked:
        blocked.append(day_key)
        BLOCKED[service_id] = blocked
        with open("data/blocked_days.json","w",encoding="utf-8") as f:
            json.dump(BLOCKED,f,ensure_ascii=False,indent=2)