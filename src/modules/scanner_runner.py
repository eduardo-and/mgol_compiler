import os
import shutil

from pathlib import Path

from core.models.token import Token
from core.models.enums.token_class import TokenClass
from modules.scanner.scanner import Scanner


class ScannerRunner:
    def __init__(self, path):   
        baseDir = Path(__file__).resolve().parent.parent.parent
        newPath = f"{baseDir}/.tmp/{path.split('/')[-1]}"
        os.makedirs(".tmp", exist_ok=True)
        shutil.copy(f"{baseDir}/{path}", newPath)
        _sourceCode = open(newPath, "a+", encoding="utf-8")
        _sourceCode.write("\n\x00")
        self.scanner = Scanner(file=_sourceCode)

    def runSingle(self)->Token:
        token,errorMessage = self.scanner.scan()
        print(errorMessage) if errorMessage else None
        if token.tokenClass == TokenClass.EOF:
            self.scanner.restart()

        return token
    
    def runAll(self)->list[Token]:
        tokensList: list[Token] = []

        self.scanner.restart()

        while True:
            token,errorMessage = self.scanner.scan()
            print(errorMessage) if errorMessage else None
            tokensList.append(token)
            if token.tokenClass == TokenClass.EOF:
                break

        self.scanner.restart()

        return tokensList
    
    def end(self):
        shutil.rmtree(".tmp")