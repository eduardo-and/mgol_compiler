# MGOL_compiler

## Tutorial

1. Execute o comando abaixo na pasta do programa python

    ```sh
    python3 -m venv .venv
    ```             
2. Execute o comando 

    ⚠️Windows
    ```sh
    cd .venv\Scripts 
    ./activate
    ```
    ⚠️MacOS/Linux
    ```sh
    source .venv/bin/activate
    ```

3. Retorne para a raiz do projeto python e em seguida instale as dependências

    ```sh
    pip install -r dependencies.txt
    ```
4. Em seguida o programa já está pronto para uso

    Abaixo temos um exemplo:
    ```sh
        python ./src/main.py -p ./exampleCode.txt
    ```

5. Para executar o output, use
    ```sh
        gcc output/program.c -o output/program
        ./output/program
    ```