import os
import shutil

from pathlib import Path

from core.models.token import Token
from core.models.error import Error
from core.models.enums.token_class import TokenClass
from modules.scanner.scanner import Scanner


class ScannerRunner:
    def __init__(self, path):   
        baseDir = Path(__file__).resolve().parent.parent.parent.parent
        newPath = f"{baseDir}/.tmp/{path.split('/')[-1]}"
        os.makedirs(".tmp", exist_ok=True)
        shutil.copy(f"{baseDir}/{path}", newPath)
        _sourceCode = open(newPath, "a+", encoding="utf-8")
        _sourceCode.write("\n\x00")
        self.scanner = Scanner(file=_sourceCode)

    def getToken(self)->Token:        
        token, error = self.scanner.scan()
        if token.tokenClass == TokenClass.ERROR:
            print(error)
            print("Obtendo próximo token...")
            return self.getToken()
        if token.tokenClass == TokenClass.COMMENT:
            return self.getToken()

        return token
    
    def runAll(self)->list[Token, Error]:
        tokensList: list[Token, Error] = []

        self.scanner.restart()

        while True:
            token, error = self.scanner.scan()
            if token.tokenClass == TokenClass.COMMENT:
                token, error = self.scanner.scan()
            
            tokensList.append(token)
            if error: tokensList.append(error)
            if token.tokenClass == TokenClass.EOF:
                break

        self.scanner.restart()

        return tokensList
    
    def end(self):
        shutil.rmtree(".tmp")