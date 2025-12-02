# Projeto de Compilador - Linguagens Formais e Compiladores

Este projeto implementa um **compilador para uma linguagem de domínio específico (DSL)** voltada para a modelagem de processos de negócio. O compilador realiza análise léxica, sintática e semântica de arquivos `.dsl`, validando a estrutura do processo e gerando automaticamente **diagramas de fluxo** em formato PNG através do Graphviz.

A DSL permite definir processos com atividades sequenciais e condicionais, facilitando a documentação e visualização de workflows empresariais de forma clara e estruturada.

### Funcionalidades Principais

- **Análise Léxica e Sintática**: Parser robusto baseado em PLY (Python Lex-Yacc)
- **Validação Semântica**: Verifica a consistência do modelo (referências, cardinalidade, etc.)
- **Geração de Diagramas**: Converte automaticamente o processo em gráficos visuais (DOT → PNG)
- **Suporte a Gateways**: Modelagem de fluxos condicionais com múltiplas saídas
- **Tratamento de Erros**: Mensagens claras sobre problemas sintáticos e semânticos

---

## Sintaxe da DSL

### Estrutura Geral de um Arquivo `.dsl`

```
processo {
    nome = "Nome do Processo";
    dono = "Responsável pelo Processo";
    inicio = nome_atividade_inicial;
    
    atividades {
        nome_atividade {
            nome = "Descrição da Atividade";
            tipo = "tarefa" | "gateway";
            responsavel = "Responsável pela Atividade";
            tempo = valor_numerico;
            custo = valor_numerico;
            seguinte = { fluxos };
        }
        
        // mais atividades...
    }
    
    fim = "Mensagem de Finalização";
}
```

### Propriedades do Processo

- `nome` (obrigatório): Nome descritivo do processo
- `dono` (obrigatório): Departamento ou pessoa responsável pelo processo
- `inicio` (obrigatório): ID da atividade inicial (deve existir no bloco `atividades`)
- `fim` (obrigatório): Mensagem exibida ao final do processo

### Propriedades das Atividades

- `nome` (obrigatório): Descrição legível da atividade
- `tipo` (obrigatório): Tipo da atividade
  - `"tarefa"`: Atividade simples (máximo 1 saída)
  - `"gateway"`: Ponto de decisão (mínimo 2 saídas condicionais)
- `responsavel` (obrigatório): Papel ou pessoa responsável pela execução
- `tempo` (opcional): Tempo estimado de execução (em unidades definidas pelo usuário)
- `custo` (opcional): Custo associado à atividade
- `seguinte` (obrigatório): Define o fluxo para as próximas atividades

### Definição de Fluxos (`seguinte`)

#### Fluxo Simples (Tarefa)
```
seguinte = { proxima_atividade };
```

#### Fluxo Condicional (Gateway)
```
seguinte = {
    condicao1 -> atividade1,
    condicao2 -> atividade2,
    condicao3 -> fim
};
```

### Exemplo Completo

```
processo {
    nome = "Processo de Compra";
    dono = "Departamento Financeiro";
    inicio = solicitar_compra;

    atividades {
        solicitar_compra {
            nome = "Solicitar Compra";
            tipo = "tarefa";
            responsavel = "Funcionário";
            tempo = 2;
            custo = 0;
            seguinte = { avaliar_compra };
        }

        avaliar_compra {
            nome = "Avaliar Compra";
            tipo = "gateway";
            responsavel = "Gerente";
            seguinte = {
                aprovado -> aprovar_compra,
                rejeitado -> fim
            };
        }

        aprovar_compra {
            nome = "Aprovar Compra";
            tipo = "tarefa";
            responsavel = "Diretor";
            tempo = 1;
            custo = 500;
            seguinte = { fim };
        }
    }

    fim = "Processo Encerrado";
}
```

---

## Validações Semânticas

O compilador realiza as seguintes verificações durante a análise:

### Exemplos de validações implementadas:

1. Indicar exemplo de código com problema:
    - Problema de Violação de cardinalidade de saída de atividade simples
    - `atividade_1 { tipo="tarefa"; seguinte={ opcao1 -> a2, opcao2 -> a3 } }`  → duas saídas em uma tarefa

2. Explicar porque é considerado um erro e quais as implicações se não tratado:
    - Em notações como BPMN, múltiplos caminhos de saída simultâneos não partem de uma tarefa simples, eles exigem um gateway explícito.
    - Se não tratado, o gerador terá que adivinhar semântica (XOR ou AND).

3. Indicar a possível ação semântica que pode ser feita para resolver ou verificar o problema:
    - Ao reduzir atividade do tipo tarefa, podemos validar que tamanho é <= 1.
    - Se > 1, retorna erro "tarefa com múltiplas saídas; use gateway".
    - Essa verificação é estática, feita no compilador, exatamente como outras regras semânticas de fluxo de controle.

## Requisitos do Sistema

### Dependências Python
Instalação de bibliotecas necessárias:
`pip install -r requirements.txt`

As bibliotecas Python necessárias são:
- `ply` - Python Lex-Yacc para análise léxica e sintática
- `pydot` - Interface Python para Graphviz
- `pillow` - Biblioteca de processamento de imagens

### Graphviz (Requisito Obrigatório)

O Graphviz deve estar instalado no sistema para renderizar os gráficos DOT como imagens.

Windows: 
 - `winget install graphviz`
 - Após a instalação, adicione o diretório bin do Graphviz ao PATH do sistema (geralmente `C:\Program Files\Graphviz\bin`)
 - Para verificar se o Graphviz foi instalado corretamente: `dot -V`

## Como Usar

Execute o compilador passando o arquivo `.dsl` como argumento:

`python main.py exemplo.dsl`

## Arquitetura do Compilador

### Estrutura de Arquivos

- `lexer.py`: Analisador léxico (tokenização)
- `parser.py`: Analisador sintático (gramática) e validações semânticas
- `main.py`: Orquestrador principal + gerador de código (DOT/PNG)
- `exemplo.dsl`: Arquivo de exemplo com sintaxe da DSL
- `requirements.txt`: Dependências Python do projeto

### Pipeline de Compilação

```
Arquivo .dsl
    ↓
[Lexer] → Tokens
    ↓
[Parser] → AST (Abstract Syntax Tree)
    ↓
[Validador Semântico] → Modelo Validado
    ↓
[Gerador de Código] → Arquivo DOT
    ↓
[Graphviz] → Imagem PNG
```

---

## ⚙️ Tecnologias Utilizadas

- **Python 3.x**: Linguagem base do projeto
- **PLY (Python Lex-Yacc)**: Framework para construção de lexers e parsers
- **Graphviz**: Renderização de grafos DOT em imagens
- **pydot**: Interface Python para o Graphviz
- **Pillow**: Processamento de imagens auxiliar
