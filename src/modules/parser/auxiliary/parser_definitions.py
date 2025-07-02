import copy
import csv
from pathlib import Path
from typing import Callable

from core.models.token import Token
from core.models.nonTerminal import NonTerminalToken
from modules.parser.enums.action_type_num_enum import ActionType
from modules.parser.models.action import Action
from modules.parser.models.grammar_reference import GrammarReference
from modules.parser.enums.non_terminals_enum import NonTerminal
from core.models.enums.token_class import TokenClass
from modules.parser.models.state import State


class ParserDefinitions:
    parsingTablePath = "/assets/parse_table.csv"
    
    def __init__(self):
        self.parsingTable = self.__loadParsingTable()
        self.__tabCounter = 2
        self.__temp = []
        self.__loop = ""

        def __verifySymbolList(token, symbolList):
            symbolsLexemes = [t.lexeme for t in symbolList]
            if(token.lexeme not in symbolsLexemes):
                raise Exception("Erro: Variável não declarada")
            return

        def __verifySameType(op1, op2):
            if(op1.attributes["type"] != op2.attributes["type"]):
                raise Exception("Erro: Operandos com tipos incompatíveis")
            return
        
        def __verifyLoop(stack):
            lexemes = []
            for t in stack:
                if isinstance(t, Token):
                    lexemes.append(t.lexeme)
                else:
                    lexemes.append(t.nonTerminal.value)

            print(" ".join(lexemes))
            return TokenClass.facaate.value in lexemes

        def __write(string: str,writer, stack):
            if(__verifyLoop(stack)):
                self.__loop += " " * (self.__tabCounter+2)
                self.__loop += string
            else:
                writer(string,self.__tabCounter)
    

        def f5 (stack:list[Token, NonTerminalToken],writer,symbolList):
            [writer("\n") for _ in range(3)]
            return NonTerminalToken(NonTerminal.LV)
        
        def f6 (stack:list[Token, NonTerminalToken],writer,symbolList):
            tipo = stack[-2].attributes["type"]

            string = f"{self.__temp[-1].lexeme}"
            for token in self.__temp[:-1]:
                string += f", {token.lexeme}"

            for token in self.__temp:
                idxSymbol = [i for i in range(len(symbolList)) if symbolList[i].lexeme == token.lexeme][0]
                symbolList[idxSymbol].type = tipo
            
            writer(f"{string};\n", self.__tabCounter)
            self.__temp = []
            return NonTerminalToken(NonTerminal.D)
        
        def f7 (stack:list[Token, NonTerminalToken],writer,symbolList):
            self.__temp.append(stack[-3])
            return NonTerminalToken(NonTerminal.L)

        def f8 (stack:list[Token, NonTerminalToken],writer,symbolList):
            self.__temp.append(stack[-1])
            return NonTerminalToken(NonTerminal.L)

        def f9 (stack:list[Token, NonTerminalToken],writer,symbolList):
            writer("int ", self.__tabCounter)
            return NonTerminalToken(NonTerminal.TIPO, {"type": "int"})
        
        def f10 (stack:list[Token, NonTerminalToken],writer,symbolList):
            writer("double ", self.__tabCounter)
            return NonTerminalToken(NonTerminal.TIPO, {"type": "float"})
    
        def f11 (stack:list[Token, NonTerminalToken],writer,symbolList):
            writer("literal ", self.__tabCounter)
            return NonTerminalToken(NonTerminal.TIPO, {"type": "lit"})
        
        def f13 (stack:list[Token, NonTerminalToken],writer,symbolList):
            token = stack[-2]
            __verifySymbolList(token, symbolList)

            if(token.type == "int"):
                string = f'scanf("%d", &{token.lexeme});\n'
            if(token.type == "float"):
                string = f'scanf("%lf", &{token.lexeme});\n'
            if(token.type == "lit"):
                string = f'scanf("%s", {token.lexeme});\n'


            __write(string,writer,stack)
            return NonTerminalToken(NonTerminal.ES)
        
        def f14 (stack:list[Token, NonTerminalToken],writer,symbolList):
            arg = stack[-2]
            lexeme = arg.attributes['lexeme']
            type = arg.attributes["type"]

            if(type == "str"):
                string = f'printf({lexeme});\n'
            if(type == "lit"):
                string = f'printf("%s", {lexeme});\n'
            if(type == "int"):
                string = f'printf("%d", {lexeme});\n'
            if(type == "float"):
                string = f'printf("%lf", {lexeme});\n'

            __write(string,writer,stack)

            return NonTerminalToken(NonTerminal.ES)

        def f15 (stack:list[Token, NonTerminalToken],writer,symbolList):
            return NonTerminalToken(NonTerminal.ARG, {"lexeme": stack[-1].lexeme, "type": "str"})
        
        def f16 (stack:list[Token, NonTerminalToken],writer,symbolList):
            type = "float" if "." in stack[-1].lexeme else "int"
            return NonTerminalToken(NonTerminal.ARG, {"lexeme": stack[-1].lexeme, "type": type})

        def f17 (stack:list[Token, NonTerminalToken],writer,symbolList):
            token = stack[-1]
            __verifySymbolList(token, symbolList)
            
            return NonTerminalToken(NonTerminal.ARG, {"lexeme": token.lexeme, "type": token.type})
        
        def f19 (stack:list[Token, NonTerminalToken],writer,symbolList):
            id = stack[-4]
            ld = stack[-2]
            
            if("type" in ld.attributes and id.type != ld.attributes["type"]):
                raise Exception("Erro: Tipos diferentes para atribuição")
            string = f"{id.lexeme} = {ld.attributes['lexeme']};\n"
            __write(string,writer,stack)

            return NonTerminalToken(NonTerminal.CMD)

        def f20 (stack:list[Token, NonTerminalToken],writer,symbolList):
            opr1 = stack[-3]
            opr2 = stack[-1]
            __verifySameType(opr1, opr2)
            if(opr1.attributes['type'] == 'lit'):
                raise Exception('Erro: Operando literal não suportado')

            return NonTerminalToken(NonTerminal.LD, {"lexeme": f"{opr1.attributes['lexeme']} {stack[-2].lexeme} {opr2.attributes['lexeme']}"})

        def f21 (stack:list[Token, NonTerminalToken],writer,symbolList):
            return NonTerminalToken(NonTerminal.LD, stack[-1].attributes)

        def f22 (stack:list[Token, NonTerminalToken],writer,symbolList):
            token = stack[-1]
            __verifySymbolList(token, symbolList)

            return NonTerminalToken(NonTerminal.OPRD, {"lexeme": token.lexeme, "type": token.type})

        def f23 (stack:list[Token, NonTerminalToken],writer,symbolList):
            type = "float" if "." in stack[-1].lexeme else "int"
            return NonTerminalToken(NonTerminal.OPRD, {"lexeme": stack[-1].lexeme, "type": type})

        def f25 (stack:list[Token, NonTerminalToken],writer,symbolList):
            self.__tabCounter -= 2
            string = '}\n'
            __write(string,writer,stack)
            return NonTerminalToken(NonTerminal.COND)

        def f26 (stack:list[Token, NonTerminalToken],writer,symbolList):
            string = f"if({stack[-3].attributes['lexeme']}){{\n"
            __write(string,writer,stack)
            self.__tabCounter += 2
            return NonTerminalToken(NonTerminal.CAB)

        def f27 (stack:list[Token, NonTerminalToken],writer,symbolList):
            opr1 = stack[-3]
            opr2 = stack[-1]
            __verifySameType(opr1, opr2)

            return NonTerminalToken(NonTerminal.EXP_R, {"lexeme": f"{opr1.attributes['lexeme']} {stack[-2].lexeme} {opr2.attributes['lexeme']}"})
        
        def f34 (stack:list[Token, NonTerminalToken],writer,symbolList):
            writer(f"while(!({stack[-4].attributes['lexeme']})){{\n",self.__tabCounter)
            writer(self.__loop)
            writer("}\n",self.__tabCounter)
            self.loop = ""
            return NonTerminalToken(NonTerminal.CP_R)

        self.grammarList = [
            GrammarReference(2, NonTerminal.P, [TokenClass.inicio, NonTerminal.V, NonTerminal.A], lambda *_ : NonTerminalToken(NonTerminal.P)),
            GrammarReference(3, NonTerminal.V, [TokenClass.varinicio, NonTerminal.LV], lambda *_ : NonTerminalToken(NonTerminal.V)),
            GrammarReference(4, NonTerminal.LV, [NonTerminal.D, NonTerminal.LV], lambda *_ : NonTerminalToken(NonTerminal.LV)),
            GrammarReference(5, NonTerminal.LV, [TokenClass.varfim, TokenClass.PT_V],f5),
            GrammarReference(6, NonTerminal.D, [NonTerminal.L, NonTerminal.TIPO, TokenClass.PT_V],f6),
            GrammarReference(7, NonTerminal.L, [TokenClass.ID, TokenClass.VIR, NonTerminal.L], f7),
            GrammarReference(8, NonTerminal.L, [TokenClass.ID], f8),
            GrammarReference(9, NonTerminal.TIPO, [TokenClass.INT],f9),
            GrammarReference(10, NonTerminal.TIPO, [TokenClass.REAL],f10),
            GrammarReference(11, NonTerminal.TIPO, [TokenClass.LIT],f11),
            GrammarReference(12, NonTerminal.A, [NonTerminal.ES, NonTerminal.A], lambda *_ : NonTerminalToken(NonTerminal.A)),
            GrammarReference(13, NonTerminal.ES, [TokenClass.leia, TokenClass.ID, TokenClass.PT_V],f13),
            GrammarReference(14, NonTerminal.ES, [TokenClass.escreva, NonTerminal.ARG, TokenClass.PT_V], f14),
            GrammarReference(15, NonTerminal.ARG, [TokenClass.literal], f15),
            GrammarReference(16, NonTerminal.ARG, [TokenClass.NUM], f16),
            GrammarReference(17, NonTerminal.ARG, [TokenClass.ID], f17),
            GrammarReference(18, NonTerminal.A, [NonTerminal.CMD, NonTerminal.A], lambda *_ : NonTerminalToken(NonTerminal.A)),
            GrammarReference(19, NonTerminal.CMD, [TokenClass.ID, TokenClass.RCB, NonTerminal.LD, TokenClass.PT_V], f19),
            GrammarReference(20, NonTerminal.LD, [NonTerminal.OPRD, TokenClass.OPM, NonTerminal.OPRD], f20),
            GrammarReference(21, NonTerminal.LD, [NonTerminal.OPRD], f21),
            GrammarReference(22, NonTerminal.OPRD, [TokenClass.ID], f22),
            GrammarReference(23, NonTerminal.OPRD, [TokenClass.NUM], f23),
            GrammarReference(24, NonTerminal.A, [NonTerminal.COND, NonTerminal.A], lambda *_ : NonTerminalToken(NonTerminal.A)),
            GrammarReference(25, NonTerminal.COND, [NonTerminal.CAB, NonTerminal.CP], f25),
            GrammarReference(26, NonTerminal.CAB, [TokenClass.se, TokenClass.AB_P, NonTerminal.EXP_R, TokenClass.FC_P, TokenClass.entao], f26),
            GrammarReference(27, NonTerminal.EXP_R, [NonTerminal.OPRD, TokenClass.OPR, NonTerminal.OPRD], f27),
            GrammarReference(28, NonTerminal.CP, [NonTerminal.ES, NonTerminal.CP], lambda *_ : NonTerminalToken(NonTerminal.CP)),
            GrammarReference(29, NonTerminal.CP, [NonTerminal.CMD, NonTerminal.CP], lambda *_ : NonTerminalToken(NonTerminal.CP)),
            GrammarReference(30, NonTerminal.CP, [NonTerminal.COND, NonTerminal.CP], lambda *_ : NonTerminalToken(NonTerminal.CP)),
            GrammarReference(31, NonTerminal.CP, [TokenClass.fimse], lambda *_ : NonTerminalToken(NonTerminal.CP)),
            GrammarReference(32, NonTerminal.A, [NonTerminal.R, NonTerminal.A], lambda *_ : NonTerminalToken(NonTerminal.A)),
            GrammarReference(33, NonTerminal.R, [TokenClass.facaate, TokenClass.AB_P, NonTerminal.EXP_R, TokenClass.FC_P, NonTerminal.CP_R], lambda *_ : NonTerminalToken(NonTerminal.R)),
            GrammarReference(34, NonTerminal.CP_R, [NonTerminal.ES, NonTerminal.CP_R], f34),
            GrammarReference(35, NonTerminal.CP_R, [NonTerminal.CMD, NonTerminal.CP_R], lambda *_ : NonTerminalToken(NonTerminal.CP_R)),
            GrammarReference(36, NonTerminal.CP_R, [NonTerminal.COND, NonTerminal.CP_R], lambda *_ : NonTerminalToken(NonTerminal.CP_R)),
            GrammarReference(37, NonTerminal.CP_R, [TokenClass.fimfaca], lambda *_ : NonTerminalToken(NonTerminal.CP_R)),
            GrammarReference(38, NonTerminal.A, [TokenClass.fim], lambda *_ : NonTerminalToken(NonTerminal.A)),
        ]

    def __loadParsingTable(self):
        baseDir = Path(__file__).resolve().parent.parent.parent.parent.parent
        newPath = f"{baseDir}{self.parsingTablePath}"
        finalDict = {}
        with open(newPath, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            table = {rows[0]: rows[1:] for rows in reader}
        titles = table[""]
        for key, value in table.items():
            if key == "":
                continue
            newValue = []
            for index, _ in enumerate(value):
                act, ind = self.__getActionAndIndex(value[index])
                action = Action(index=ind, actionType=act)

                newValue.append(State(action=action, lexeme=titles[index]))
            finalDict[int(key)] = newValue
        return finalDict

    def __getActionAndIndex(self, act: str):
        if act.isdigit():
            return None, int(act)
        if act == "":
            return ActionType.ERROR, None
        if act[0] == "S":
            return ActionType.SHIFT, int(act.split("S")[1])
        elif act[0] == "R":
            return ActionType.REDUCE, int(act.split("R")[1])
        elif act == "ACC":
            return ActionType.ACCEPT, None
        return ActionType.ERROR, None
