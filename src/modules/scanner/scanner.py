from io import TextIOWrapper

from core.models.token import Token
from core.models.enums.token_class import TokenClass
from modules.scanner.domain.usecases.language_pattern import LanguagePattern
from modules.scanner.models.state import StateUnity

class Scanner:
    charToIgnore = [32, 10, 9]
    currentLine: int = 0
    currentColumn: int = 0
    
    reservedSymbolsList = [
        Token(tokenClass=TokenClass.inicio, type="inicio", lexeme="inicio"),
        Token(tokenClass=TokenClass.varinicio, type="varinicio", lexeme="varinicio"),
        Token(tokenClass=TokenClass.varfim, type="varfim", lexeme="varfim"),
        Token(tokenClass=TokenClass.escreva, type="escreva", lexeme="escreva"),
        Token(tokenClass=TokenClass.leia, type="leia", lexeme="leia"),
        Token(tokenClass=TokenClass.se, type="se", lexeme="se"),
        Token(tokenClass=TokenClass.entao, type="entao", lexeme="entao"),
        Token(tokenClass=TokenClass.fimse, type="fimse", lexeme="fimse"),
        Token(tokenClass=TokenClass.facaate, type="faca-ate", lexeme="faca-ate"),
        Token(tokenClass=TokenClass.fimfaca, type="fimfaca", lexeme="fimfaca"),
        Token(tokenClass=TokenClass.fim, type="fim", lexeme="fim"),
        Token(tokenClass=TokenClass.inteiro, type="inteiro", lexeme="inteiro"),
        Token(tokenClass=TokenClass.literal, type="literal", lexeme="literal"),
        Token(tokenClass=TokenClass.real, type="real", lexeme="real"),
    ]
    
    def __init__(self, file: TextIOWrapper):
        self.file = file
        self.initialState = LanguagePattern()

    def scan(self)->Token:
        currentState = self.initialState
        token = None
        lexeme = ""
        isStart = True
        
        self.file.seek(0)
        
        for lineIndex, line in enumerate(self.file):
            if isStart:
                if lineIndex < self.currentLine:
                    continue
            else:
                self.currentColumn = 0
                self.currentLine = lineIndex
        
            for columnIndex, char in enumerate(line):
                if isStart:
                    if columnIndex < self.currentColumn:
                        continue
                isStart = False
                self.currentColumn = columnIndex
                
                char = ord(char)
                if char in self.charToIgnore and lexeme == "":
                    continue
                
                if token == None:
                    token = self.__initToken(self.currentColumn, self.currentLine)
                
                tmpNextState = self.__nextState(char, currentState)
                if tmpNextState == None:
                    if token.tokenClass == TokenClass.ERROR:
                        if lexeme == "":
                            lexeme += chr(char)
                    return self.__returnToken(lexeme, currentState, token)
                else: 
                    lexeme += chr(char)
                    if char == 0:
                        lexeme += "EOF"
                        return self.__returnToken(lexeme, tmpNextState, token)
                    currentState = tmpNextState
        
        raise Exception("Falha no Scanner: Token indefinido")
    
    def restart(self)->None:
        self.currentLine = 0
        self.currentColumn = 0
        return 
    
    def __returnToken(self, lexeme: str, currentState: StateUnity, token: Token):
            token.tokenClass = currentState.resultingClass
            token.lexeme = lexeme
            token = self.__setType(token)
            token = self.__reservedWordVerify(token)
            token = self.__verifyError(token)
            return token
        
    def __nextState(self, char, currentState):
        _nextState = currentState.doTransition(char)
        if _nextState:
            return _nextState
        return None
    
    def __initToken(self, column, line):
        return Token(
            tokenClass=TokenClass.ERROR,
            line=line,
            col=column
        )
        
    def __verifyError(self, token: Token):
        if token.tokenClass == TokenClass.ERROR:            
            token.type = "Erro1 - Caractere Inválido"
            self.currentColumn += 1
        return token
    
    def __setType(self, token: Token):
        if token.tokenClass == TokenClass.NUM:
            if token.lexeme.find(".") != -1:
                token.type = "real"
            else:
                token.type = "inteiro"
        elif token.tokenClass == TokenClass.LIT:
            token.type = "literal" 
        return token
    
    def __reservedWordVerify(self, token: Token):
        if token.tokenClass == TokenClass.ID:
            reservedToken = self.__findTokenByLexeme(token.lexeme)
            if reservedToken:
                col = token.col
                line = token.line 
                token = reservedToken
                token.col = col
                token.line = line
        return token

    def __findTokenByLexeme(self, lexeme: str):
        return next((token for token in self.reservedSymbolsList if getattr(token, 'lexeme', None) == lexeme), None)

    
