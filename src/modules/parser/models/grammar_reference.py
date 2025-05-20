from modules.parser.enums.non_terminals_enum import NonTerminal


class GrammarReference:
    def __init__(self, rule: int, terminal: str, quantity: int):
        self.rule = int(rule)
        self.nonTerminal = NonTerminal[terminal]
        self.quantity = int(quantity)
