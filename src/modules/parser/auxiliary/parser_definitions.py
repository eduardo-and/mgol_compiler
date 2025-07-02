import copy
import csv
from pathlib import Path
from typing import Callable

from core.models.token import Token
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
        
        def popStack(qty: int, stack: list[Token]):
            for _ in range(qty):
                if stack:
                    stack.pop()
            return stack
        
        def f5 (stack:list[Token],writer,symbolList):
            [writer("\n") for i in range(3)]
            return stack, symbolList
        
        #! F7 e F8 Não precisam realizar nada, ao menos até o momento
        def f6 (stack:list[Token],writer,symbolList):
            try:
                type = next(i for i in stack if(i.tokenClass == TokenClass.INT or 
                                                i.tokenClass == TokenClass.REAL or
                                                i.tokenClass == TokenClass.LIT or
                                                i.tokenClass == TokenClass.REAL or 
                                                i.tokenClass == TokenClass.LIT)) 
                tmpSymList = copy.deepcopy(symbolList)
                finalLexeme = ""
                for token in stack:
                    if(token.tokenClass == TokenClass.ID):
                        try:
                            index = next(i for i,listToken in enumerate(tmpSymList) if listToken.lexeme == token.lexeme)
                            finalLexeme+=f'{symbolList[index].lexeme}, '
                            tmpSymList[index].tokenClass= None
                            symbolList[index].type = type.attributes["type"]             
                        except:
                            break
                finalLexeme= finalLexeme[:-2] ## Remove the last comma and space
                finalLexeme+= ";\n"
                writer(finalLexeme,1)
                if(stack[0].tokenClass == TokenClass.inicio):
                    popStack(len(stack), stack)
                else:
                    popStack(3, stack)
            except Exception as e:
                raise Exception("Erro ao tentar atribuir o tipo ao ID")
            return stack, symbolList
        
        
        def f9_10_11 (stack:list[Token],writer,symbolList):
            if(stack[-1].tokenClass == TokenClass.INT):
                stack[-1].attributes["type"] = "int"
            if(stack[-1].tokenClass == TokenClass.REAL):
                stack[-1].attributes["type"] = "float"
            if(stack[-1].tokenClass == TokenClass.LIT):
                stack[-1].attributes["type"] = "char"
            
            writer(stack[-1].attributes["type"] + " ",1)
            return stack, symbolList
            
        def f13 (stack:list[Token],writer,symbolList):
            idLexeme = stack[-2].lexeme
            token = next(token for token in symbolList if token.lexeme == idLexeme )
            if(token.lexeme != None):
                if(token.type == "int"):
                    writer(f'scanf("%s", {token.lexeme});\n',1)
                if(token.type == "float"):
                    writer(f'scanf("%l", {token.lexeme});\n',1)
                if(token.type == "char"):
                    writer(f'scanf("%d", {token.lexeme});\n',1)
            return stack, symbolList
        
        def f1 (stack:list[Token],writer,symbolList):()
        def f1 (stack:list[Token],writer,symbolList):()
        def f1 (stack:list[Token],writer,symbolList):()
        def f1 (stack:list[Token],writer,symbolList):()
        def f1 (stack:list[Token],writer,symbolList):()
        def f1 (stack:list[Token],writer,symbolList):()
        def f1 (stack:list[Token],writer,symbolList):()
        def f1 (stack:list[Token],writer,symbolList):()
         
        self.grammarList = [
            GrammarReference(2,  NonTerminal.P, [TokenClass.inicio, NonTerminal.V, NonTerminal.A],),
            GrammarReference(3, NonTerminal.V, [TokenClass.varinicio, NonTerminal.LV]),
            GrammarReference(4, NonTerminal.LV, [NonTerminal.D, NonTerminal.LV]),
            GrammarReference(5, NonTerminal.LV, [TokenClass.varfim, TokenClass.PT_V],f5),
            GrammarReference(6, NonTerminal.D, [NonTerminal.L, NonTerminal.TIPO, TokenClass.PT_V],f6),
            GrammarReference(7, NonTerminal.L, [TokenClass.ID, TokenClass.VIR, NonTerminal.L]),
            GrammarReference(8, NonTerminal.L, [TokenClass.ID]),
            GrammarReference(9, NonTerminal.TIPO, [TokenClass.INT],f9_10_11),
            GrammarReference(10, NonTerminal.TIPO, [TokenClass.REAL],f9_10_11),
            GrammarReference(11, NonTerminal.TIPO, [TokenClass.LIT],f9_10_11),
            GrammarReference(12, NonTerminal.A, [NonTerminal.ES, NonTerminal.A]),
            GrammarReference(13, NonTerminal.ES, [TokenClass.leia, TokenClass.ID, TokenClass.PT_V],f13),
            GrammarReference(14, NonTerminal.ES, [TokenClass.escreva, NonTerminal.ARG, TokenClass.PT_V]),
            GrammarReference(15, NonTerminal.ARG, [TokenClass.literal]),
            GrammarReference(16, NonTerminal.ARG, [TokenClass.NUM]),
            GrammarReference(17, NonTerminal.ARG, [TokenClass.ID]),
            GrammarReference(18, NonTerminal.A, [NonTerminal.CMD, NonTerminal.A]),
            GrammarReference(19, NonTerminal.CMD, [TokenClass.ID, TokenClass.RCB, NonTerminal.LD, TokenClass.PT_V]),
            GrammarReference(20, NonTerminal.LD, [NonTerminal.OPRD, TokenClass.OPM, NonTerminal.OPRD]),
            GrammarReference(21, NonTerminal.LD, [NonTerminal.OPRD]),
            GrammarReference(22, NonTerminal.OPRD, [TokenClass.ID]),
            GrammarReference(23, NonTerminal.OPRD, [TokenClass.NUM]),
            GrammarReference(24, NonTerminal.A, [NonTerminal.COND, NonTerminal.A]),
            GrammarReference(25, NonTerminal.COND, [NonTerminal.CAB, NonTerminal.CP]),
            GrammarReference(26, NonTerminal.CAB, [TokenClass.se, TokenClass.AB_P, NonTerminal.EXP_R, TokenClass.FC_P, TokenClass.entao]),
            GrammarReference(27, NonTerminal.EXP_R, [NonTerminal.OPRD, TokenClass.OPR, NonTerminal.OPRD]),
            GrammarReference(28, NonTerminal.CP, [NonTerminal.ES, NonTerminal.CP]),
            GrammarReference(29, NonTerminal.CP, [NonTerminal.CMD, NonTerminal.CP]),
            GrammarReference(30, NonTerminal.CP, [NonTerminal.COND, NonTerminal.CP]),
            GrammarReference(31, NonTerminal.CP, [TokenClass.fimse]),
            GrammarReference(32, NonTerminal.A, [NonTerminal.R, NonTerminal.A]),
            GrammarReference(33, NonTerminal.R, [TokenClass.facaate, TokenClass.AB_P, NonTerminal.EXP_R, TokenClass.FC_P, NonTerminal.CP_R]),
            GrammarReference(34, NonTerminal.CP_R, [NonTerminal.ES, NonTerminal.CP_R]),
            GrammarReference(35, NonTerminal.CP_R, [NonTerminal.CMD, NonTerminal.CP_R]),
            GrammarReference(36, NonTerminal.CP_R, [NonTerminal.COND, NonTerminal.CP_R]),
            GrammarReference(37, NonTerminal.CP_R, [TokenClass.fimse]),
            GrammarReference(38, NonTerminal.A, [TokenClass.fim]),
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
