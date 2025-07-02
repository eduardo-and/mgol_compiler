from core.models.token import Token
from modules.parser.enums.non_terminals_enum import NonTerminal
from core.models.enums.token_class import TokenClass
from typing import Callable, List, Union

class GrammarReference:
    def __init__(self, ruleNum: int, nonTerminal: NonTerminal, reduction: List[Union[TokenClass, NonTerminal]], action: Callable[[any, any, any],any]=None):
        self.rule = int(ruleNum)
        self.nonTerminal = nonTerminal
        self.quantity = len(reduction)
        self.reduction = reduction
        self.action = action
    
    def __str__(self):
        string = self.nonTerminal.value + " → " + " ".join([v.value for v in self.reduction])
        return string
