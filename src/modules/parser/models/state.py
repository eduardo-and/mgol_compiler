from core.models.enums.token_class import TokenClass
from core.models.token import Token
from modules.parser.enums.terminalsEnum import Terminal
from modules.parser.models.action import Action


class State:
    def __init__(
        self,
        action: Action,
        lexeme: str = None,
    ):
        self.token = self.__getToken(lexeme)
        self.terminal = self.__getTerminal(lexeme)
        self.action = action

    def __getToken(self, lexeme):
        try:
            return Token(tokenClass=TokenClass[lexeme])
        except:
            return None

    def __getTerminal(self, lexeme):
        try:
            return Terminal[lexeme]
        except:
            return None

    def __str__(self):
        return f"{self.token} : {self.action}"
