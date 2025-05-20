from core.models.enums.token_class import TokenClass


class StateUnity:
    
    def __init__(self, id: int, resultingClass: TokenClass):
        self.id = id
        self.transitions = []
        self.resultingClass = resultingClass
    
    def __str__(self):
        return f"id: {self.id} \nresultingClass: {self.resultingClass}\ntransitions: {self.transitions}"

    def doTransition(self, char): 
        for transition in self.transitions:
            pattern, nextState = transition
            for pattern in pattern:
                if isinstance(pattern, range):
                    if char in pattern:
                        return nextState
                if pattern == char:
                    return nextState
        return None
