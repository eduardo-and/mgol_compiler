from io import TextIOWrapper

from core.models.token import Token
from core.models.error import Error
from core.models.enums.token_class import TokenClass
from modules.scanner.domain.usecases.language_pattern import LanguagePattern
from modules.scanner.models.state import StateUnity

class Scanner:
    charToIgnore = [32, 10, 9]
    currentLine: int = 0
    currentColumn: int = 0
    languageDict = [range(48, 59),range(97 - 123),range(65,91),44,59,58,33,63,39,34,95,32, 10, 9,40,41,123,125,43,45,47,42,62,60,61,92]
    
    errosByState = {
        TokenClass.ID: "Erro2 - Identificador Invalido",
        TokenClass.LIT: "Erro3 - Literal Invalido",
        TokenClass.NUM: "Erro4 - Numero Invalido",
        TokenClass.COMMENT: "Erro5 - Comentario Invalido"
    }
    
    symbolsList = [
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
        previousTokenClass = None
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
                    self.currentColumn = self.currentColumn - 1 if len(line)== self.currentColumn else self.currentColumn
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
                if tmpNextState == None or char == 10:
                    if currentState.resultingClass == TokenClass.ERROR or not self.__isOnLanguageDict(char):
                        lexeme += chr(char)
                        if currentState.id == 12:
                            previousTokenClass = TokenClass.LIT
                        elif currentState.id == 14:
                            previousTokenClass = TokenClass.COMMENT
                        else:
                            previousTokenClass = currentState.resultingClass
                        return self.__returnToken(lexeme, TokenClass.ERROR, token, previousTokenClass)
                    return self.__returnToken(lexeme, currentState.resultingClass, token)
                else: 
                    lexeme += chr(char)
                    if char == 0:
                        lexeme += "EOF"
                        return self.__returnToken(lexeme, tmpNextState.resultingClass, token)
                    currentState = tmpNextState
        
        raise Exception("Falha no Scanner: Token indefinido")
    
    def restart(self)->None:
        self.currentLine = 0
        self.currentColumn = 0
        return 
    
    def __returnToken(self, lexeme: str, resultingClass: TokenClass, token: Token, previousState: StateUnity = None)->Token:
            token.tokenClass = resultingClass
            token.lexeme = lexeme
            token = self.__setType(token)
            token = self.__reservedWordVerify(token)
            token = self.__iDTreatment(token)
            error = self.__verifyError(token, previousState)
            return token, error
        
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
        
    def __iDTreatment(self, token: Token):
        if token.tokenClass == TokenClass.ID:
            if "-" in token.lexeme:
                token.tokenClass = TokenClass.ERROR
                token.type = self.errosByState[TokenClass.ID]   
            if self.__findTokenByLexeme(token.lexeme) == None:
                self.symbolsList.append(token)
        return token
    
    def __verifyError(self, token: Token, previousTokenClass: StateUnity = None):
        errorMessage = None
        if token.tokenClass == TokenClass.ERROR:            
            if previousTokenClass and self.errosByState.get(previousTokenClass):
                errorMessage = self.errosByState[previousTokenClass]
            else:
                errorMessage = "Erro1 - Caractere Invalido"
            self.currentColumn += 1
        return Error(message=errorMessage, line=token.line, col=token.col) if errorMessage != None else None
    
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

    def __isOnLanguageDict(self, char: int):
        for dict in self.languageDict:
            if isinstance(dict, range):
                if char in dict:
                    return True
            if dict == char:
                return True
                
    def __findTokenByLexeme(self, lexeme: str):
        return next((token for token in self.symbolsList if token.lexeme  == lexeme), None)

    
