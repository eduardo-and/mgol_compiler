from io import TextIOWrapper
import copy
from core.models.enums.failure_type import FailureType
from core.models.token import Token
from core.models.error import Error
from core.models.enums.token_class import TokenClass

from modules.scanner.auxiliary.language_pattern import LanguagePattern
from modules.scanner.models.state_unity import StateUnity


class Scanner:
    __charToIgnore = [32, 10, 9]
    __currentLine: int = 0
    __currentColumn: int = 0
    __isFileFinished: bool = False
    __languageDict = [
        range(48, 59),
        range(97 - 123),
        range(65, 91),
        44,
        59,
        58,
        33,
        63,
        39,
        34,
        95,
        32,
        10,
        9,
        40,
        41,
        123,
        125,
        43,
        45,
        47,
        42,
        62,
        60,
        61,
        92,
    ]

    __errosByState = {
        TokenClass.ERROR: "Erro1 - Caractere Invalido",
        TokenClass.ID: "Erro2 - Identificador Invalido",
        TokenClass.LIT: "Erro3 - Literal Invalido",
        TokenClass.NUM: "Erro4 - Numero Invalido",
        TokenClass.COMMENT: "Erro5 - Comentario Invalido",
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
        Token(tokenClass=TokenClass.INT, type="inteiro", lexeme="inteiro"),
        Token(tokenClass=TokenClass.REAL, type="real", lexeme="real"),
        Token(tokenClass=TokenClass.literal, type="literal", lexeme="literal"),
    ]

    def __init__(self, file: TextIOWrapper):
        self.file = file
        self.initialState = LanguagePattern()

    def scan(self) -> Token:
        currentState = self.initialState
        previousTokenClass = None
        token = None
        lexeme = ""
        isStart = True
        
        if self.__isFileFinished:
            raise Exception(Error(
                failure=FailureType.ScannerFailure,
                message="Scanner has reached the end of the file",
                line=self.__currentLine,
                col=self.__currentColumn
            ))
            
        self.file.seek(0)

        for lineIndex, line in enumerate(self.file):
            if isStart:
                if lineIndex < self.__currentLine:
                    continue
            else:
                self.__currentColumn = 0
                self.__currentLine = lineIndex

            for columnIndex, char in enumerate(line):
                if isStart:
                    self.__currentColumn = (
                        self.__currentColumn - 1
                        if len(line) == self.__currentColumn
                        else self.__currentColumn
                    )
                    if columnIndex < self.__currentColumn:
                        continue
                isStart = False
                self.__currentColumn = columnIndex

                char = ord(char)
                if char in self.__charToIgnore and lexeme == "":
                    continue

                if token == None:
                    token = self.__initToken(self.__currentColumn, self.__currentLine)

                tmpNextState = self.__nextState(char, currentState)
                if tmpNextState == None or char == 10:
                    if currentState.resultingClass == TokenClass.ERROR:
                        lexeme += chr(char)
                        if currentState.id == 12:
                            previousTokenClass = TokenClass.LIT
                        elif currentState.id == 14:
                            previousTokenClass = TokenClass.COMMENT
                        elif not self.__isOnLanguageDict(char):
                            previousTokenClass = TokenClass.ERROR
                        else:
                            previousTokenClass = currentState.resultingClass
                        return self.__returnToken(
                            lexeme, TokenClass.ERROR, token, previousTokenClass
                        )
                    if lexeme == "faca":
                        lexeme += chr(char)
                        continue
                    return self.__returnToken(
                        lexeme, currentState.resultingClass, token
                    )
                else:
                    lexeme += chr(char)
                    if char == 0:
                        lexeme += "EOF"
                        return self.__returnToken(
                            lexeme, tmpNextState.resultingClass, token
                        )
                    currentState = tmpNextState

        raise Exception("Falha no Scanner: Token indefinido")

    def restart(self) -> None:
        self.__currentLine = 0
        self.__currentColumn = 0
        return

    def __returnToken(
        self,
        lexeme: str,
        resultingClass: TokenClass,
        token: Token,
        previousTokenClass: TokenClass = None,
    ) -> Token:
        token.tokenClass = resultingClass
        token.lexeme = lexeme
        token = self.__setType(token)
        token = self.__reservedWordVerify(token)
        token = self.__iDTreatment(token)
        error = self.__verifyError(token, previousTokenClass)
        self.__setFileFinished(token)

        # EXTRAIR EM METODO
        if token.tokenClass == TokenClass.literal:
            token.tokenClass = TokenClass.LIT
     
        return token, error

    def __nextState(self, char, currentState):
        _nextState = currentState.doTransition(char)
        if _nextState:
            return _nextState
        return None

    def __initToken(self, column, line):
        return Token(tokenClass=TokenClass.ERROR, line=line, column=column)

    def __setFileFinished(self, token: Token):
        if token.tokenClass == TokenClass.EOF:
            self.__isFileFinished = True
        return token
    def __iDTreatment(self, token: Token):
        if token.tokenClass == TokenClass.ID:
            if self.__findTokenByLexeme(token.lexeme) == None:
                self.symbolsList.append(token)
        return token

    def __verifyError(self, token: Token, previousTokenClass: TokenClass = None):
        errorMessage = None
        if token.tokenClass == TokenClass.ERROR:
            if previousTokenClass and self.__errosByState.get(previousTokenClass):
                errorMessage = self.__errosByState[previousTokenClass]
            else:
                errorMessage = "Erro1 - Caractere Invalido"
            self.__currentColumn += 1
        return (
            Error(failure=FailureType.ScannerFailure, message=errorMessage, line=token.line, col=token.column)
            if errorMessage != None
            else None
        )

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
                col = token.column
                line = token.line
                token = copy.deepcopy(reservedToken)
                token.column = col
                token.line = line
        return token

    def __isOnLanguageDict(self, char: int):
        for dict in self.__languageDict:
            if isinstance(dict, range):
                if char in dict:
                    return True
            if dict == char:
                return True

    def __findTokenByLexeme(self, lexeme: str):
        return next(
            (token for token in self.symbolsList if token.lexeme == lexeme), None
        )
