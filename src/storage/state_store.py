"""Almacena en memoria el estado de cada usuario (puede cambiarse por Redis fácilmente)."""

_user_states = {}

def get_state(wa_id):
    return _user_states.get(wa_id)

def set_state(wa_id, state):
    _user_states[wa_id] = state

def clear_state(wa_id):
    _user_states.pop(wa_id, None)
