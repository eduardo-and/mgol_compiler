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
    parser.run()
    return

if __name__ == "__main__":
    main()