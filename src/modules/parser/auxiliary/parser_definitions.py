import csv
from pathlib import Path

from modules.parser.enums.actionTypeEnum import ActionType
from modules.parser.models.action import Action
from modules.parser.models.grammar_reference import GrammarReference
from modules.parser.models.state import State


class ParserDefinitions:
    parsingTablePath = "/assets/parse_table.csv"
    grammarListPath = "/assets/grammar_table.csv"

    def __init__(self):
        self.parsingTable = self.__loadParsingTable()
        self.grammarList = self.__loadGrammarTable()

    def __loadGrammarTable(self):
        baseDir = Path(__file__).resolve().parent.parent.parent.parent.parent
        newPath = f"{baseDir}{self.grammarListPath}"
        finalList = []
        with open(newPath, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            table = {rows[0]: rows[1:] for rows in reader}

        for key, value in table.items():
            finalList.append(
                GrammarReference(quantity=value[1], rule=key, terminal=value[0])
            )
        return finalList

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
        elif act[0] == "ACC":
            return ActionType.ACCEPT, None
        return ActionType.ERROR, None
