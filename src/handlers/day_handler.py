from sender           import build_confirmation_message
from whatsapp_client  import send_message
from storage.block_repo import add_block
from state_store      import clear_state

def handle_day(wa_id, service_id, day_key):
    add_block(service_id, day_key)
    payload = build_confirmation_message(wa_id, service_id, day_key)
    send_message(payload)
    clear_state(wa_id)
