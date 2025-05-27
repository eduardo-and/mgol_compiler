import argparse

from modules.parser.enums.run_option_enum import RunOption
from modules.parser.parser import Parser


def main():
    parser = argparse.ArgumentParser(
        description="MGOL Compiler, especifique o caminho do código fonte"
    )
    parser.add_argument(
        "-p", "--path", type=str, help="Path do arquivo com o código fonte"
    )

    args = parser.parse_args()
    parser = Parser(args.path)
    while True:
        print("Modo de Execução:")
        print("1 - Panic Mode")
        print("2 - Token Inference (Heuristic Error Recovery)")

        _option = input("Digite a opção desejada: ")
        if _option == "1":
            parser.run(RunOption.panic)
            return
        if _option == "2":
            parser.run(RunOption.TokenInference)
            return
        else:
            print("Opção inválida!\n")

    return

if __name__ == "__main__":
    main()