import copy
import os
from core.models.enums.failure_type import FailureType
from core.models.enums.token_class import TokenClass
from core.models.error import Error
from core.models.token import Token
from modules.parser.auxiliary.parser_definitions import ParserDefinitions
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
    __errorToken: Token | None = None
    __isReduced = False
    __isError = False
    __panic = False
    __semanticStack = []
    __symbolList = [Token]
    __finalCodePath = "output/program.c"
    __finalFile = None
    __isNewLine = True

    def __init__(self, path: str):
        self.__scanner = ScannerRunner(path)
        self.__symbolList = self.__scanner.getSymbolsList()
        __parserDefinitions = ParserDefinitions()
        self.__parseTable = __parserDefinitions.parsingTable
        self.__grammarList = __parserDefinitions.grammarList
        self.__stack = [0]
        self.__initGeneratedFile()

    def __closeGeneratedFile(self):
        if self.__finalFile:
            self.__finalFile.write("\nreturn 0;\n\n}\n")
            self.__finalFile.close()
            print(f"Arquivo gerado com sucesso em: {self.__finalCodePath}")
        else:
            print("Erro ao fechar o arquivo gerado.")
    
    def __initGeneratedFile(self):
        if os.path.exists(self.__finalCodePath):
            os.remove(self.__finalCodePath)
        os.makedirs(os.path.dirname(self.__finalCodePath), exist_ok=True)
        self.__finalFile= open(self.__finalCodePath, 'w', encoding='utf-8')
        self.__finalFile.write("#include <stdio.h>\n\n\n")
        self.__finalFile.write("int main() {\n")
    
    def run(self):
        self.__slr1()

    def __panicMode(self, token):
        try:
            token = self.__getToken()
            self.__isError = True
            if token == None:
                raise self.__errorHandler(token)
            print(f"Próximo token: {token.lexeme}")
        except Exception as e:
            print(e)
            raise e

    def __tokenInference(self, token):
        suggestion = self.__findSuggestedToken(token)
        if suggestion is not None:
            print(
                f"\033[32mToken sugerido:\033[0m {suggestion.tokenClass.value}"
            )
            self.__currentToken = suggestion
            self.__isError = True
            return
        print(
            f"\033[31mNenhuma sugestão de transição encontrada! Ativando modo pânico!\033[0m"
        )
        self.__errorToken = None
        self.__panic = True
        self.__panicMode(token)

    def __findSuggestedToken(self, token):
        for suggestedToken in TokenClass:
            foundRule = self.__attemptInsertion(suggestedToken)
            token = Token(tokenClass=suggestedToken, column=token.column+1, line=token.line)
            if foundRule != None: return token
        return None

    def __attemptInsertion(self, tokenClass):
        simulatedStack = self.__stack[:]
        states: list[State] = self.__parseTable[simulatedStack[-1]][:]
        action: Action = next(
                (
                    state.action
                    for state in states
                    if state.token != None and state.token.tokenClass == tokenClass
                ),
                None,
            )
        
        if action != None and action.actionType == ActionType.REDUCE:
            rule: GrammarReference = [r for r in self.__grammarList if r.rule == action.index][0]
            return rule
        return None

    def __errorHandler(self, token: Token):
        lastMessage = self.__lastToken.lexeme if self.__lastToken.lexeme != '' else self.__lastToken.tokenClass.value
        currentMessage = token.lexeme if token.lexeme != '' else token.tokenClass.value
        error: Error = Error(
            failure=FailureType.ParserFailure,
            message=f"Erro na transição de [{lastMessage}] para [{currentMessage}]",
            line=token.line,
            col=token.column,
        )
        print(error)


        if self.__panic:
            self.__panicMode(token)
        else:
            self.__errorToken = token
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
        
        try:
            self.__semanticStack,self.__scanner.writer= grammarRule.action(
                self.__semanticStack,
                self.__writer,
                self.__symbolList)
        except:
            # Adicionar tratamento de erro e a flag que interrompe a geração do código em C
            return
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
                self.__semanticStack.append(token)
                continue
            elif action.actionType == ActionType.REDUCE:
                self.__reduce(action=action)
                self.__isReduced = True
            elif action.actionType == ActionType.ACCEPT:
                print("ACEITO: P' → P")
                self.__closeGeneratedFile()
                print("Parser successfully completed!")
                return True
            else:
                try:
                    self.__errorHandler(token)
                except Exception as e:
                    print(e)
                    if token.tokenClass == TokenClass.EOF:
                        print("\033[31mParser chegou ao final do arquivo sem encontrar tokens válidos!\033[0m")
                        return False
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
            if self.__errorToken:
                self.__lastToken = self.__currentToken
                self.__currentToken: Token = self.__errorToken
                self.__errorToken = None
                return self.__currentToken
            self.__lastToken = self.__currentToken
            self.__currentToken: Token = self.__scanner.getToken()
            return self.__currentToken

    def __writer(self, text: str,identation: int = 0):
            if(self.__isNewLine):
                [self.__finalFile.write(" ") for _ in range(identation)]
            if("\n" in text):
                self.__isNewLine = True
            else:
                self.__isNewLine = False
            self.__finalFile.write(text)
