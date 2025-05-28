
from core.models.enums.failure_type import FailureType
from core.models.enums.token_class import TokenClass


class Error:
    def __init__(self,
                 failure: FailureType,
                 message: str = "",
                 line: int = None,
                 col: int = None):
        self.failure = failure
        self.message = message
        self.line = line+1
        self.col = col+1

    def __str__(self):
        return f"\033[31m{self.failure.value}:\033[0m {self.message}, linha: {self.line}, col: {self.col}"