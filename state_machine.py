
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
            if parent.detection: 
                parent.current_state = STATE["confirming"]
        case 1:
            parent.current_state = STATE["detected"]
        case 2:
            parent.current_state = STATE["resetting"]
            
