import argparse

from modules.parser.parser import Parser


def main():
    parser = argparse.ArgumentParser(description="MGOL Compiler, especifique o caminho do código fonte")
    parser.add_argument("-p","--path", type=str, help="Path do arquivo com o código fonte")


    while True:
        print("MODO DE ERRO:")
        print("1 - Desespero")
        print("2 - Escanear linha por linha")

        _option = input("Digite a opção desejada: ")
        if _option == "1" or _option == "2": break
        print("Opção inválida!\n")
    
    args = parser.parse_args()
    parser = Parser(args.path, int(_option))
    parser.run()

    return 


if __name__ == "__main__":
    main()