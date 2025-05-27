from core.models.enums.token_class import TokenClass
from core.models.token import Token
from modules.parser.models.grammar_reference import GrammarReference


class TokenSuggestionGetter:

    def getSuggestion(
        self, token, grammarList: list, grammarLine: list[TokenClass]
    ) -> tuple | None:
        biggerCorrespondence = 0
        findedRule: GrammarReference = None
        correspondencesLines = []
        for rule in grammarList:
            reduction = rule.reduction
            correspondences = sum(a == b for a, b in zip(reduction, grammarLine))
            if correspondences > biggerCorrespondence:
                if token.tokenClass in reduction:
                    nextTokenIndex = reduction.index(token.tokenClass) + 1
                    if (
                        len(reduction) > nextTokenIndex
                        and type(reduction[nextTokenIndex]) == TokenClass
                    ):
                        correspondencesLines.append((correspondences, reduction))
        if len(correspondencesLines) > 0:
            suggestion = self.__findBestMatch(
                token.tokenClass,
                correspondencesLines,
                tokenIndexOnGrammarLine=grammarLine.index(token.tokenClass),
            )
                
            for grammar in grammarList:
                if grammar.reduction == suggestion[1]:
                    grammarFinded = grammar
                    break
            return (suggestion[0], grammarFinded)

        return None

    def __findBestMatch(
        self,
        token: TokenClass,
        correspondencesFinded: list,
        tokenIndexOnGrammarLine: int,
    ):
        bestMatch = None
        for correspondences, rule in correspondencesFinded:
            tokenIndex = rule.index(token)
            if tokenIndex == tokenIndexOnGrammarLine:
                if bestMatch is None:
                    bestMatch = (correspondences, rule)
                elif correspondences > bestMatch[0]:
                    bestMatch = (correspondences, rule)
        if bestMatch is not None:
            grammarList = bestMatch[1]
            nextTokenIndex = self.__getTokenIndex(token, grammarList) + 1
            return Token(tokenClass=grammarList[nextTokenIndex]), grammarList
        else:
            grammarList = correspondencesFinded[0][1]
            nextTokenIndex = self.__getTokenIndex(token, grammarList) + 1
            return Token(tokenClass=grammarList[nextTokenIndex]), grammarList

    def __getTokenIndex(self, token: TokenClass, grammar: list[TokenClass]):
        return grammar.index(token)
