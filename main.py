import sys
import os
from parser import parser, validar_modelo


def gerar_dot(modelo, nome_arquivo) -> bool:
    """
    Gera um arquivo Graphviz DOT para visualizar o modelo de processo.
    """
    dot = "digraph G {\n"
    dot += '    rankdir=LR;\n'
    dot += '    Start [shape=Mdiamond, label="Início do Processo"];\n'
    dot += '    End [shape=Msquare, label="Fim do Processo"];\n\n'
    
    # 1. Definição dos nós (Atividades)
    for nome, a in modelo['atividades'].items():
        # CORREÇÃO: Usar .get() para propriedades opcionais (tempo, custo),
        # pois gateways ou outras atividades podem não tê-las.
        tempo = a.get('tempo', 'N/A')
        custo = a.get('custo', 'N/A')
        
        label = (
            f'{a["nome"]}\\n'
            f'Responsável: {a["responsavel"]}\\n'
            f'Tipo: {a.get("tipo", "tarefa")}\\n'
            f'Tempo: {tempo} / Custo: {custo}'
        )
        shape = 'box' if a.get('tipo') != 'gateway' else 'diamond'
        dot += f'    {nome} [label="{label}", shape={shape}];\n'

    dot += '\n'
    
    # 2. Fluxo de Início
    dot += f'    Start -> {modelo["inicio"]} [label="Início"];\n\n'

    # 3. Fluxos entre Atividades
    for nome, a in modelo['atividades'].items():
        seguinte = a.get('seguinte', [])
        for cond, dest in seguinte:
            # Se for 'next', usa uma label vazia (para fluxos não condicionais)
            label = '' if cond == 'next' else cond 
            
            destino_dot = 'End' if dest == 'fim' else dest
            dot += f'    {nome} -> {destino_dot} [label="{label}"];\n'

    dot += "}\n"

    try:
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(dot)
        return True
    except IOError as e:
        print(f"Erro ao escrever o arquivo DOT: {e}")
        return False


def dot_para_png(filename: str, output_png: str = "processo.png") -> bool:
    try:
        import pydot
        with open(filename, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        graphs = pydot.graph_from_dot_data(conteudo)
        graph = graphs[0]
        graph.write_png(output_png)
        return True
    
    except ImportError:
        print("pydot não está instalado. Instale-o para converter DOT para PNG.")
        return False
    
    except Exception as e:
        print(f"Erro ao converter DOT para PNG: {e}")
        return False


if __name__ == "__main__":
    
    # Se nenhum parâmetro for passado, pede o nome do arquivo
    if len(sys.argv) == 1:
        nome_arquivo_dsl = input("Digite o nome do arquivo DSL: ")
    
    # Se um parâmetro passado, extrai o nome do arquivo
    elif len(sys.argv) == 2:
        nome_arquivo_dsl = sys.argv[1]
    
    else:
        raise ValueError("Número incorreto de argumentos. Use: python main.py <nome_do_arquivo>.dsl")
    
    # Verifica se o arquivo existe antes de continuar
    if not os.path.exists(nome_arquivo_dsl):
        raise FileNotFoundError(f"Arquivo '{nome_arquivo_dsl}' não encontrado.")

    try:
        nome_base = os.path.splitext(nome_arquivo_dsl)[0]

        # Lê o conteúdo do arquivo DSL
        print(f"\nProcessando o arquivo '{nome_arquivo_dsl}'...")
        with open(nome_arquivo_dsl, "r", encoding="utf-8") as f:
            codigo = f.read()

        modelo = parser.parse(codigo)       
        print("Análise Sintática concluída.")
        
        validar_modelo(modelo)
        print("Validação Semântica concluída.")

        # Inicia a geração do DOT (interpretação/criação do artefato)
        if gerar_dot(modelo, nome_arquivo=f"{nome_base}.dot"):
            print("Arquivo .dot gerado com sucesso.")
        else:
            print("Erro ao gerar o arquivo .dot.")

        # Tenta converter o DOT para PNG
        nome_arquivo_png = nome_arquivo_dsl.replace('.dsl', '.png')
        if dot_para_png(f"{nome_base}.dot", nome_arquivo_png):
            print(f"Arquivo '{nome_arquivo_png}' gerado com sucesso.")
        else:
            print("Não foi possível gerar o arquivo PNG.")
            print("Para visualuizar o diagrama, use um visualizador de arquivos DOT.")

    except (SyntaxError, Exception) as e:
        # Captura erros de sintaxe (do parser) e erros semânticos/KeyError
        print(f"Erro no processamento: {e}")
