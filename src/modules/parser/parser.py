from core.models.enums.failure_type import FailureType
from core.models.enums.token_class import TokenClass
from core.models.error import Error
from core.models.token import Token
from modules.parser.auxiliary.parser_definitions import ParserDefinitions
from modules.parser.auxiliary.token_sugest_getter import TokenSuggestionGetter
from modules.parser.enums.action_type_num_enum import ActionType
from modules.parser.enums.non_terminals_enum import NonTerminal
from modules.parser.enums.run_option_enum import RunOption
from modules.parser.models.action import Action
from modules.parser.models.grammar_reference import GrammarReference
from modules.parser.models.state import State
from modules.scanner.scanner_runner import ScannerRunner


class Parser:
    __currentToken: Token | None = None
    __lastToken: Token | None = None
    __isReduced = False
    __isError = False
    __lastLine = list[TokenClass]
    __currentLine = None

    def __init__(self, path: str):
        self.__scanner = ScannerRunner(path)
        __parserDefinitions = ParserDefinitions()
        self.__parseTable = __parserDefinitions.parsingTable
        self.__grammarList = __parserDefinitions.grammarList
        self.__stack = [0]

    def run(self, runOption: RunOption):
        self.__runOption = runOption
        self.__slr1()

    def __panicMode(self, token):
        try:
            token = self.__getToken()
            self.__isError = True
            if token == None:
                raise self.__errorHandler(token)
            print("Obtendo próximo token...")
        except Exception as e:
            print(e)
            raise e

    def __tokenInference(self, token):
        suggestedToken, grammarRef = self.__findSuggestedToken(token)
        if suggestedToken is not None:
            print(
                f"\033[32mToken sugerido:\033[0m {suggestedToken.tokenClass}, da gramática: {grammarRef}"
            )
            self.__currentToken = suggestedToken
            self.__isError = True
            return
        print(
            f"\033[31mNenhuma sugestão encontrada para o token: {token.tokenClass}\033[0m"
        )
        self.__panicMode(token)

    def __findSuggestedToken(self, token: Token):
        token_suggestion_getter = TokenSuggestionGetter()
        self.__lastLine.remove(self.__currentToken.tokenClass)
        return token_suggestion_getter.getSuggestion(
            token=token, grammarLine=self.__lastLine, grammarList=self.__grammarList
        )

    def __errorHandler(self, token: Token):
        error: Error = Error(
            failure=FailureType.ParserFailure,
            message=f"Nenhuma transição encontrada - Token: {token.tokenClass.value} ",
            line=token.line,
            col=token.column,
        )
        print(error)

        if self.__runOption == RunOption.panic:
            self.__panicMode(token)
        else:
            self.__tokenInference(self.__lastToken)

    def __goTo(self, terminal: NonTerminal):
        states: list[State] = self.__parseTable[self.__stack[-1]]

        for state in states:
            if state.terminal == terminal:
                action = state.action
                break
        if action.index == None:
            self.__errorHandler(self.__currentToken)
            return
        self.__stack.append(action.index)

    def __reduce(self, action: Action):
        grammarRule: GrammarReference = next(
            (line for line in self.__grammarList if line.rule == action.index), None
        )
        print(grammarRule)
        [self.__stack.pop() for _ in range(grammarRule.quantity)]
        self.__goTo(grammarRule.nonTerminal)
        return

    def __shift(self, action: Action):
        self.__stack.append(action.index)

        return

    def __slr1(self):
        token = None
        contadorTEMP = -1
        while True:
            contadorTEMP += 1
            token = self.__getToken()

            states: list[State] = self.__parseTable[self.__stack[-1]]
            action: Action = next(
                (
                    state.action
                    for state in states
                    if state.token.tokenClass == token.tokenClass
                ),
                None,
            )

            if action.actionType == ActionType.SHIFT:
                self.__shift(action)
                continue
            elif action.actionType == ActionType.REDUCE:
                self.__reduce(action=action)
                self.__isReduced = True
            elif action.actionType == ActionType.ACCEPT:
                print("ACEITO: P' → P")
                print("Parser successfully completed!")
                return True
            else:
                try:
                    self.__errorHandler(token)
                except Exception as e:
                    print("\033[31mParser process failed!\033[0m")
                    return False

    def __getToken(self):
        if self.__isError:
            self.__isError = False
            return self.__currentToken
        if self.__isReduced:
            self.__isReduced = False
            return self.__currentToken
        else:
            self.__lastToken = self.__currentToken
            self.__currentToken: Token = self.__scanner.getToken()
            self.__updateTokenSequence()
            return self.__currentToken

    def __updateTokenSequence(self):
        if self.__currentToken.line == self.__currentLine:
            self.__lastLine.append(self.__currentToken.tokenClass)
        else:
            self.__currentLine = self.__currentToken.line
            self.__lastLine = [self.__currentToken.tokenClass]
