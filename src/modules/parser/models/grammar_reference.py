from modules.parser.enums.terminalsEnum import Terminal


class GrammarReference:
    def __init__(self, rule: int, terminal: str, quantity: int):
        self.rule = int(rule)
        self.terminal = Terminal[terminal]
        self.quantity = int(quantity)
