from enum import Enum

class FailureType(Enum):
    NoTokenFailure= "No Token Failure"
    ParserFailure= "Parser Failure"
    ScannerFailure= "Scanner Failure"