from enum import Enum


class TokenClass(Enum):

    NUM = "num"
    INT = "int"
    REAL = "real"
    LIT = "lit"
    ID = "id"
    COMMENT = "COMMENT"
    EOF = "EOF"
    RESERVED_WORD = "RESERVED_WORD"
    OPR = "opr"
    RCB = "rcb"
    OPM = "opm"
    AB_P = "ab_p"
    FC_P = "fc_p"
    PT_V = "pt_v"
    ERROR = "ERROR"
    VIR = "vir"
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
  


