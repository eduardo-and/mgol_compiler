from modules.parser.enums.action_type_num_enum import ActionType


class Action:
    def __init__(self, actionType: ActionType, index: int = None):
        self.actionType = actionType
        self.index = index

    def __str__(self):
        return f"{self.actionType} : {self.index}"