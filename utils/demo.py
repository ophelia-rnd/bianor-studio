from constants.demo import DEMO_ID_PREFIX, DEMO_MODEL_PREFIX

def is_demo_id(val) -> bool:
    return bool(val and str(val).startswith(DEMO_ID_PREFIX))

def is_demo_model(val) -> bool:
    return bool(val and str(val).startswith(DEMO_MODEL_PREFIX))
