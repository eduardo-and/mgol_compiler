
from core.models.enums.token_class import TokenClass


class Token:
    def __init__(self,
                 tokenClass: TokenClass,
                 lexeme: str = "",
                 type: str = None,
                 line: int = None,
                 column: int = None):
        self.tokenClass = tokenClass
        self.lexeme = lexeme
        self.type = type
        self.line = line
        self.column = column
        self.attributes= {}

    def __str__(self):
        return f"classe: {self.tokenClass.value}, lexema: {self.lexeme}, tipo: {self.type}, linha: {self.line}, col: {self.column}"