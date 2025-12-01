import sys
from parser import parser, validar_modelo # Importa as funções corrigidas

def gerar_dot(modelo, nome_arquivo="processo.dot"):
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
        print(f"✅ Arquivo DOT '{nome_arquivo}' gerado com sucesso!")
        print("   Use um visualizador de DOT (ex: Graphviz, ou um visualizador online) para ver o diagrama.")
    except IOError as e:
        print(f"❌ Erro ao escrever o arquivo DOT: {e}")

# -----------------------------
# LEITURA DO ARQUIVO DSL
# -----------------------------

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python main.py <nome_do_arquivo>.dsl")
        sys.exit(1)
        
    nome_arquivo_dsl = sys.argv[1]

    try:
        with open(nome_arquivo_dsl, "r", encoding="utf-8") as f:
            codigo = f.read()

        print(f"📄 Analisando o arquivo '{nome_arquivo_dsl}'...")
        # Adicione o set_debug=True no yacc.yacc() se precisar depurar a gramática
        modelo = parser.parse(codigo)
        
        print("✅ Análise Sintática concluída.")
        
        validar_modelo(modelo)
        print("✅ Validação Semântica concluída.")

        # Inicia a geração do DOT (interpretação/criação do artefato)
        gerar_dot(modelo)

    except FileNotFoundError:
        print(f"❌ Erro: Arquivo '{nome_arquivo_dsl}' não encontrado.")
    except (SyntaxError, Exception) as e:
        # Captura erros de sintaxe (do parser) e erros semânticos/KeyError
        print(f"❌ Erro no processamento: {e}")