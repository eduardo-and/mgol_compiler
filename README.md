# 🧩 MGOL Compiler

Um **transpilador acadêmico** desenvolvido como parte de um projeto universitário, com o objetivo de converter programas escritos na linguagem fictícia **MGOL** em **código C**.

## 📘 Sobre o Projeto

Este projeto foi desenvolvido para a disciplina de **Compiladores**, com foco em compreender as etapas fundamentais do processo de compilação — desde a **análise léxica e sintática** até a **geração de código**.

A linguagem **MGOL** é uma linguagem didática, inspirada em linguagens estruturadas como **Pascal** e **C**, e utilizada em atividades acadêmicas para o ensino dos conceitos de compiladores.

## ⚙️ Funcionalidades

- Análise léxica dos tokens da linguagem MGOL  
- Análise sintática baseada em uma gramática LL(1)  
- Geração de código equivalente em **C**  
- Tratamento de erros léxicos e sintáticos com feedback ao usuário  
- Interface simples via linha de comando  

## 🧠 Estrutura do Projeto

```
mgol_compiler/
│
├── src/                  # Código-fonte principal
│   ├── lexer/            # Analisador léxico
│   ├── parser/           # Analisador sintático
│   ├── generator/        # Gerador de código C
│   └── main.py           # Ponto de entrada do compilador
│
├── examples/             # Exemplos de programas MGOL
├── output/               # Código C gerado
└── README.md
```

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8+
- (Opcional) GCC ou outro compilador C, caso queira compilar o código gerado

### Passos
1. Clone o repositório:
   ```bash
   git clone https://github.com/eduardo-and/mgol_compiler.git
   cd mgol_compiler
   ```

2. Execute o compilador passando o arquivo MGOL como argumento:
   ```bash
   python src/main.py examples/exemplo.mgol
   ```

3. O código C gerado será salvo em `output/`.

4. (Opcional) Compile o código gerado:
   ```bash
   gcc output/exemplo.c -o exemplo
   ./exemplo
   ```

## 🧩 Exemplo

### Código MGOL:
```mgol
inicio
   inteiro a, b
   leia(a)
   leia(b)
   escreva(a + b)
fimalgoritmo
```

### Código C gerado:
```c
#include <stdio.h>

int main() {
    int a, b;
    scanf("%d", &a);
    scanf("%d", &b);
    printf("%d", a + b);
    return 0;
}
```

## 🧑‍💻 Autor
**Eduardo de Andrade Tristão**  
[LinkedIn](https://linkedin.com/in/eduardo-and) • [GitHub](https://github.com/eduardo-and)

**Lara Portilho**<br>
• [GitHub](https://github.com/lara-portilho)

## 🏛️ Licença
Este projeto foi desenvolvido para fins educacionais e é disponibilizado sob a licença **MIT**.

---

> 💡 *Projeto acadêmico voltado ao estudo de compiladores e transpilação de linguagens.*
