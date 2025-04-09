
from core.models.enums.token_class import TokenClass


class Error:
    def __init__(self,
                 message: str = "",
                 line: int = None,
                 col: int = None):
        self.message = message
        self.line = line
        self.col = col

    def __str__(self):
        return f"{self.message}, linha: {self.line}, col: {self.col}"