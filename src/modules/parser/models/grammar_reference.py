from modules.parser.enums.non_terminals_enum import NonTerminal
from core.models.enums.token_class import TokenClass
from typing import List, Union

class GrammarReference:
    def __init__(self, ruleNum: int, nonTerminal: NonTerminal, reduction: List[Union[TokenClass, NonTerminal]]):
        self.rule = int(ruleNum)
        self.nonTerminal = nonTerminal
        self.quantity = len(reduction)
        self.reduction = reduction
    
    def __str__(self):
        string = self.nonTerminal.value + " → " + " ".join([v.value for v in self.reduction])
        return string
