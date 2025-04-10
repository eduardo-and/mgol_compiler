import argparse

from prettytable import PrettyTable

from core.models.token import Token
from core.models.error import Error
from core.models.enums.token_class import TokenClass
from modules.scanner_runner import ScannerRunner


def main():
    parser = argparse.ArgumentParser(description="MGOL Compiler, especifique o caminho do código fonte")
    parser.add_argument("-p","--path", type=str, help="Path do arquivo com o código fonte")
    
    args = parser.parse_args()
    scanRunner = ScannerRunner(args.path)

    try:
        while True:
            print("MENU:")
            print("1 - Escanear todo o arquivo")
            print("2 - Escanear linha por linha")
            print("3 - Imprimir tabela de símbolos")
            print("q - Finalizar execução")

            _option = input("Digite a opção desejada: ")

            match _option:
                case "1":
                    table = PrettyTable()
                    table.field_names = ['Classe', 'Lexema', 'Tipo', 'Linha', 'Coluna']
                    tokensList = scanRunner.runAll()
                    for item in tokensList:
                        if type(item) == Token:
                            table.add_row([item.tokenClass.value,
                                            item.lexeme,
                                            item.type,
                                            item.line,
                                            item.col])
                        elif type(item) == Error:
                            table.add_row([item.message,
                                            '-',
                                            '-',
                                            item.line,
                                            item.col])
                    print(table)
                
                case "2":
                    _key = input("Pressione Enter para prosseguir, digite q e Enter para interromper")
                    while True:
                        token, error = scanRunner.runSingle()
                        if token.tokenClass == TokenClass.EOF or _key == "q":
                            break
                        if error:
                            print(token)
                            _key = input(error)
                        else:
                            _key = input(token)

                case "3":
                    table = PrettyTable()
                    table.field_names = ['Classe', 'Lexema', 'Tipo']
                    for symbol in scanRunner.scanner.symbolsList:
                        table.add_row([symbol.tokenClass.value,
                                        symbol.lexeme,
                                        symbol.type])
                    print(table)

                case "q":
                    print("Finalizando execução...")
                    break

                case _:
                    print("Opção não reconhecida!")
    finally:
        scanRunner.end()
    return 


if __name__ == "__main__":
    main()