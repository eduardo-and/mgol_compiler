import argparse

from prettytable import PrettyTable

from modules.scanner_runner import ScannerRunner
from core.models.enums.token_class import TokenClass


def main():
    _table = PrettyTable()
    _table.field_names = ['Classe', 'Lexema', 'Tipo', 'Linha', 'Coluna']
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
                    tokensList = scanRunner.runAll()
                    for token in tokensList:
                        _table.add_row([token.tokenClass.value,
                                        token.lexeme,
                                        token.type,
                                        token.line,
                                        token.col])
                    print(_table)
                
                case "2":
                    _key = input("Pressione Enter para prosseguir, digite q e Enter para interromper")
                    while True:
                        token = scanRunner.runSingle()
                        _key = input(token)
                        if token.tokenClass == TokenClass.EOF or _key == "q":
                            break

                case "3":
                    #aqui
                    print('aa')

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