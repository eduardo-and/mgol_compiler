from modules.parser.aux.parser_definitions import ParserDefinitions
from modules.scanner.scanner_runner import ScannerRunner


class Parser:
    def __init__(self, path:str):
        self.scanner = ScannerRunner(path)
        parserDefinitions = ParserDefinitions()
        self.parseTable = parserDefinitions.parserTable 

    def run(self):
        tokens = self.scanner.getToken()
        self.slr1()
        
    def errorHandler(self, token):
    def shift(self, token):
    
    def slr1(self):
        
        pass