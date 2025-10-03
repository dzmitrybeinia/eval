# Lesson name: Introdução aos Fundamentos de Programação: Variáveis, Tipos de Dados e Estruturas Lógicas

## Intro

### Bem-vindos ao mundo da programação!

A programação é como um idioma que permite aos computadores realizarem tarefas, resolverem problemas e tomarem decisões. Neste mundo, as **variáveis** guardam informações importantes e as **estruturas lógicas** ajudam os computadores a decidir o que fazer em diferentes situações. Vamos explorar esses conceitos iniciais que são essenciais para criar códigos claros e eficientes! 🖥️

#### **Themes:**
- introdução à programação

## Content slide

### O que são variáveis?

Uma variável é como uma caixa rotulada que guarda informações. Ela permite que os programas armazenem dados que podem ser usados ou alterados posteriormente.

**Exemplo:**
```python
numero_favorito = 7
```
Aqui:
- `numero_favorito` é o nome da variável.
- `7` é o valor armazenado na variável.

Pense em variáveis como ferramentas para organizar dados no código.

#### **Themes:**
- definição de variáveis

## YesNo

**Statement:** Variáveis podem guardar apenas um tipo de informação ao mesmo tempo.

**Answer:** False

**Feedback:**
Variáveis podem armazenar vários tipos de informações simultaneamente. Por exemplo, uma variável pode conter um número, uma string ou uma lista contendo vários dados. O tipo de informação que uma variável pode conter é determinado pelo tipo de dado que é atribuído a ela.


## Content slide

### Compreendendo os Tipos de Dados

Os **tipos de dados** definem o tipo de informação que uma variável pode armazenar. Aqui estão alguns comuns:
- **Inteiros (int):** Números inteiros, como 1, 42 ou -7.
- **Strings (str):** Texto entre aspas, como "Olá" ou "Programação".
- **Booleanos (bool):** Verdadeiro ou Falso.

**Exemplos:**
```python
idade = 13         # Inteiro
nome = "Alex"      # String
é_estudante = True # Booleano
```
Escolher o tipo de dado correto é essencial para evitar erros e realizar operações específicas.

#### **Themes:**
- tipos de dados

## YesNo

**Statement:** É possível atribuir uma string a uma variável de tipo inteiro sem qualquer conversão.

**Answer:** False

**Feedback:**
Nas linguagens de programação, as variáveis são tipadas, o que significa que elas devem ser atribuídas com valores compatíveis com seu tipo. Atribuir uma string a uma variável de tipo inteiro, sem conversão explícita, resultaria em um erro de tipo. Em Python, por exemplo, você precisaria converter a string para um inteiro usando a função 'int()' ou enfrentar um TypeError.


## Content slide

### Como nomear variáveis?

Escolher nomes claros para variáveis ajuda a tornar o código mais compreensível.

**Exemplo:**
```python
altura_em_cm = 170    # Nome claro
x = 170               # Nome pouco claro
```

**Dicas para nomear variáveis:**
- Use letras minúsculas e underscores para facilitar a leitura (ex.: `idade_usuario`).
- Não comece o nome com números (ex.: `2nome`).
- Evite espaços nos nomes (ex.: `idade usuario` é inválido).

#### **Themes:**
- boas práticas para nomes de variáveis

## YesNo

**Statement:** Variáveis em Python podem começar com um número.

**Answer:** False

**Feedback:**
Em Python, o início de um nome de variável não pode ser um número. Os nomes devem começar com uma letra minúscula ou um underscore seguido de uma letra minúscula.


## Content slide

### Estruturas Lógicas Simples

As estruturas lógicas ajudam os programas a tomar decisões com base em condições. A mais comum é o **if**.

**Exemplo:**
```python
idade = 13
if idade >= 18:
    print("Você é adulto.")
else:
    print("Você não é adulto.")
```

**Como funciona:**
- O `if` verifica a condição: `idade >= 18`.
- Se for verdadeira, o programa exibe "Você é adulto.".
- Se for falsa, exibe "Você não é adulto.".

Essas estruturas são fundamentais para criar programas dinâmicos.

#### **Themes:**
- estrutura lógica if

## YesNo

**Statement:** Em uma estrutura lógica if, a instrução print é executada independentemente da condição.

**Answer:** False

**Feedback:**
Não, a instrução print dentro de uma estrutura lógica if é executada apenas se a condição for verdadeira. Caso contrário, o código dentro do bloco 'else' é executado. Isso permite que o programa tome diferentes ações com base em diferentes condições.

