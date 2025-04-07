from contextvars import Token
import os
from pathlib import Path
import shutil
from core.models.enums.token_class import TokenClass
from modules.scanner.scanner import Scanner


class ScannerRunner:
    _isRunningSingle = False

    def __init__(self, path):   
        base_dir = Path(__file__).resolve().parent.parent.parent  # sobe 1 nível de /src para o root
        newPath= f"{base_dir}/.tmp/{path.split("/")[-1]}"
        os.makedirs(".tmp", exist_ok=True)
        shutil.copy(f"{base_dir}/{path}", newPath)
        _sourceCode = open(newPath, "a+", encoding="utf-8")
        _sourceCode.write("\x00")
        self.scanner = Scanner(file=_sourceCode)

    def runSingle(self)->Token:
        self._isRunningSingle=True
        
        tokensList:list[Token] 
        token = self.scanner.scan()
        tokensList.add(token)
        if(token.tokenClass == TokenClass.EOF):
            self._isRunningSingle=False
        
        return token
    
    def runAll(self)->list[Token]:
        tokensList:list[Token] = []
        if(self._isRunningSingle):
            self.scanner.restart()
        while True:
            token = self.scanner.scan()
            print(token)
            tokensList.append(token)
            if(token.tokenClass == TokenClass.EOF):
                break
        
        return tokensList