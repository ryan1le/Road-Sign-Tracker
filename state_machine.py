import time
from settings import *

STATE = {
    "idle": 0,
    "confirming": 1,
    "detected": 2,
    "resetting": 3
}

def state_machine(parent):
    match parent.current_state: 
        case 0: 
            if (parent.idle_confirm_trigger >= IDLE_CONFIRM_FILTER_THRESHOLD): 
                parent.confirm_detected_filter.reg_time(time.time())
                parent.current_state = STATE["confirming"]
        case 1:
            if (parent.confirm_detected_trigger >= CONFIRM_DETECTED_FILTER_THRESHOLD):
                if (parent.confirm_detected_filter.is_timeout(time.time(), 0.35)):
                    parent.current_state = STATE["detected"]
            else:
                parent.reset_filter.reg_time(CONFIRM_DETECTED_FILTER_THRESHOLD)
                parent.current_state = STATE["resetting"]
        case 2:
            if (parent.confirm_detected_trigger >= 0.5):
                parent.current_state = STATE["detected"]
            else:
                parent.current_state = STATE["resetting"]
        case 3:
            if (parent.reset_filter.is_timeout(time.time(), 0.25)):
                parent.current_state = STATE['idle']
            else:
                if (parent.idle_confirm_trigger >= IDLE_CONFIRM_FILTER_THRESHOLD):
                    parent.current_state = STATE['confirming']

