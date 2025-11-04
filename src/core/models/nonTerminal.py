
from modules.parser.enums.non_terminals_enum import NonTerminal


class NonTerminalToken:
    def __init__(self,
                 nonTerminal: NonTerminal,
                 attributes: dict = {},
                 ):
        self.nonTerminal = nonTerminal
        self.attributes = attributes

    def __str__(self):
        return f"não terminal: {self.nonTerminal.value}, atributos: {self.attributes}"