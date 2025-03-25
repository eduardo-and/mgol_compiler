from modules.scanner.models.enums.token_class import TokenClass


class Token:
    def __init__(self, tokenClass:TokenClass, lexeme:str, type:str = None, line:int=None,col:int=None):
        self.token_type = tokenClass
        self.lexeme = lexeme
        self.type = type
        self.line = line
        self.col = col
