from models.token import Token
from modules.scanner.models.enums.token_class import TokenClass


class Scanner:
    currentLine:int = 0
    currentColumn:int = 0
    symbolList = [
        Token(tokenClass=TokenClass.RESERVED_WORD, lexeme="inicio", type= "inicio"),
        Token(tokenClass=TokenClass.RESERVED_WORD, lexeme="varinicio",type="varinicio"),
        Token(tokenClass=TokenClass.RESERVED_WORD, lexeme="varfim",type="varfim"),
        Token(tokenClass=TokenClass.RESERVED_WORD, lexeme="escreva",type="escreva"),
        Token(tokenClass=TokenClass.RESERVED_WORD, lexeme="leia",type="leia"),
        Token(tokenClass=TokenClass.RESERVED_WORD, lexeme="se",type="se"),
        Token(tokenClass=TokenClass.RESERVED_WORD, lexeme="entao",type="entao"),
        Token(tokenClass=TokenClass.RESERVED_WORD, lexeme="fimse",type="fimse"),
        Token(tokenClass=TokenClass.RESERVED_WORD, lexeme="faca-ate",type="faca-ate"),
        Token(tokenClass=TokenClass.RESERVED_WORD, lexeme="fimfaca",type="fimfaca"),
        Token(tokenClass=TokenClass.RESERVED_WORD, lexeme="fim",type="fim"),
        Token(tokenClass=TokenClass.RESERVED_WORD, lexeme="inteiro",type="inteiro"),
        Token(tokenClass=TokenClass.RESERVED_WORD, lexeme="literal",type="literal"),
        Token(tokenClass=TokenClass.RESERVED_WORD, lexeme="real",type="real"),
        
    ]
    
    def __init__(self,file:str  )->None:
        self.scanner = None
        self.file=file

    def scan(self)->Token:
        return
    
