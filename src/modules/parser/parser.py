from core.models.enums.token_class import TokenClass
from core.models.token import Token
from modules.parser.auxiliary.parser_definitions import ParserDefinitions
from modules.parser.enums.action_type_num import ActionType
from modules.parser.enums.non_terminals_enum import NonTerminal
from modules.parser.models.action import Action
from modules.parser.models.grammar_reference import GrammarReference
from modules.parser.models.state import State
from modules.scanner.scanner_runner import ScannerRunner


class Parser:
    __lastToken = None
    __isReduced = False

    def __init__(self, path: str):
        self.__scanner = ScannerRunner(path)
        __parserDefinitions = ParserDefinitions()
        self.__parseTable = __parserDefinitions.parsingTable
        self.__grammarList = __parserDefinitions.grammarList
        self.__stack = [0]

    def run(self):
        self.__slr1()

    def __errorHandler(self, token):
        return token

    def __goTo(self, terminal: NonTerminal):
        states: list[State] = self.__parseTable[self.__stack[-1]]

        for state in states:
            if state.terminal == terminal:
                action = state.action
                break
        if action.index == None:
            raise self.__errorHandler(token=self.__lastToken)
        self.__stack.append(action.index)
        print(f"GoTo {terminal.value} : {action.index}\n {self.__stack}")

    def __reduce(self, action: Action):
        grammarRule: GrammarReference = next(
            (line for line in self.__grammarList if line.rule == action.index), None
        )
        print(f"Drop {grammarRule.quantity} elements")
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
                print(f"Token: {token.tokenClass.value} Shift: {action.index} \n {self.__stack}")
                continue
            elif action.actionType == ActionType.REDUCE:
                print(f"Token: {token.tokenClass.value} Reduce: {action.index} \n {self.__stack}")
                self.__reduce(action=action)
                self.__isReduced = True
            elif action.actionType == ActionType.ACCEPT:
                return True
            else:
                return self.__errorHandler(token if token != None else self.__lastToken)

    def __getToken(self):
        if self.__isReduced:
            self.__isReduced = False
            return self.__lastToken
        else:
            self.__lastToken = self.__scanner.getToken()
            if self.__lastToken == TokenClass.ERROR:
                return None
            return self.__lastToken
