from enum import Enum

class ActionType(Enum):
    SHIFT = "S" 
    REDUCE = "R" 
    ERROR = "ERROR" 
    ACCEPT = "ACC" 