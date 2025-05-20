from enum import Enum


class TokenClass(Enum):

    NUM = "NUM"
    INT = "INT"
    REAL = "REAl"
    LIT = "LIT"
    ID = "ID"
    COMMENT = "COMMENT"
    EOF = "EOF"
    RESERVED_WORD = "RESERVED_WORD"
    OPR = "OPR"
    RCB = "RCB"
    OPM = "OPM"
    AB_P = "AB_P"
    FC_P = "FC_P"
    PT_V = "PT_V"
    ERROR = "ERROR"
    VIR = "VIR"
    inicio = "inicio"
    varinicio = "varinicio"
    varfim = "varfim"
    escreva = "escreva"
    leia = "leia"
    se = "se"
    entao = "entao"
    fimse = "fimse"
    facaate = "faca-ate"
    fimfaca = "fimfaca"
    fim = "fim"   
    literal = "literal"
  


