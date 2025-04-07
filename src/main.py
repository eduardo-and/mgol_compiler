import argparse

from modules.scanner.domain.usecases.language_pattern import LanguagePattern
from modules.scanner_runner import ScannerRunner


def main():
    parser = argparse.ArgumentParser(description="MGOL Compiler, especifique o caminho do código fonte")
    parser.add_argument("-p","--path", type=str, help="Path do arquivo com o código fonte")
    
    args = parser.parse_args()
    scanRunner = ScannerRunner(args.path)
    scanRunner.runAll()

    return 



if __name__ == "__main__":
    main()