import ply.yacc as yacc
from lexer import tokens 

# Permite que um programa inicie por um processo e contenha apenas 1
def p_programa(p):
    "programa : processo"
    p[0] = p[1]

# Garante que todo programa tenha um abre chaves e fecha chaves
def p_processo(p):
    "processo : KW_PROCESSO ABRE_CHAVE definicoes_processo FECHA_CHAVE"
    p[0] = p[3]


# Estrutura geral de processo usado também na montagem final
def p_definicoes_processo(p):
    "definicoes_processo : prop_nome prop_dono prop_inicio bloco_atividades prop_fim"
    p[0] = {
        p[1][0]: p[1][1],
        p[2][0]: p[2][1],
        p[3][0]: p[3][1],
        'atividades': p[4],
        p[5][0]: p[5][1]
    }

# prop_nome é usada tanto para Processo quanto para Atividade.
def p_prop_nome(p):
    "prop_nome : KW_NOME OP_ATRIBUICAO LIT_STRING PONTO_VIRGULA"
    p[0] = ('nome', p[3])

def p_prop_dono(p):
    "prop_dono : KW_DONO OP_ATRIBUICAO LIT_STRING PONTO_VIRGULA"
    p[0] = ('dono', p[3])

def p_prop_inicio(p):
    "prop_inicio : KW_INICIO OP_ATRIBUICAO ID_VARIAVEL PONTO_VIRGULA"
    p[0] = ('inicio', p[3])

def p_prop_fim(p):
    # Usa o KW_FIM como esperado para a propriedade do processo
    "prop_fim : KW_FIM OP_ATRIBUICAO LIT_STRING PONTO_VIRGULA"
    p[0] = ('fim', p[3])

# Garante que o bloco de atividades tenha um abrir chave e fechar chave e uma lista
def p_bloco_atividades(p):
    "bloco_atividades : KW_ATIVIDADES ABRE_CHAVE lista_atividades FECHA_CHAVE"
    p[0] = p[3]

# Ela pode ter alguma atividade ou ser vazia no processo, pipe
def p_lista_atividades(p):
    """lista_atividades : lista_atividades atividade
                          | empty"""
    # Possui atividade, atualiza o dicionário
    if len(p) == 3:
        p[1][p[2]['id']] = p[2]
        p[0] = p[1]
    # Nenhuma atividade
    else:
        p[0] = {}

# Estrutura atividade
def p_atividade(p):
    "atividade : ID_VARIAVEL ABRE_CHAVE lista_propriedades_atividade FECHA_CHAVE"
    props_dict = dict(p[3])
    p[0] = {'id': p[1], **props_dict}

def p_lista_propriedades_atividade(p):
    """lista_propriedades_atividade : propriedade_atividade lista_propriedades_atividade
                                     | empty"""
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

# Aqui qualquer atividade pode receber alguma dessas propriedades
def p_propriedade_atividade(p):
    """propriedade_atividade : prop_nome 
                             | prop_tipo
                             | prop_responsavel
                             | prop_tempo
                             | prop_custo
                             | prop_seguinte"""
    p[0] = p[1]

def p_prop_tipo(p):
    "prop_tipo : KW_TIPO OP_ATRIBUICAO LIT_STRING PONTO_VIRGULA"
    p[0] = ('tipo', p[3])

def p_prop_responsavel(p):
    "prop_responsavel : KW_RESPONSAVEL OP_ATRIBUICAO LIT_STRING PONTO_VIRGULA"
    p[0] = ('responsavel', p[3])

def p_prop_tempo(p):
    "prop_tempo : KW_TEMPO OP_ATRIBUICAO NUMERO PONTO_VIRGULA"
    p[0] = ('tempo', p[3])

def p_prop_custo(p):
    "prop_custo : KW_CUSTO OP_ATRIBUICAO NUMERO PONTO_VIRGULA"
    p[0] = ('custo', p[3])

def p_prop_seguinte(p):
    "prop_seguinte : KW_SEGUINTE OP_ATRIBUICAO ABRE_CHAVE lista_fluxos FECHA_CHAVE PONTO_VIRGULA"
    p[0] = ('seguinte', p[4])

# Define o fluxo, permitindo ir para uma outra atividade ou o fim.
def p_flow_target(p):
    """flow_target : ID_VARIAVEL
                   | KW_FIM"""
    p[0] = p[1]

# Tratar condições especiais
def p_lista_fluxos(p):
    """lista_fluxos : fluxo_condicional lista_fluxos_continua
                     | flow_target"""
# Caso não seja condicional, apenas retorna destino e tipo
    if len(p) == 2:
        p[0] = [('next', p[1])]
    else:
# Caso Fluxo condicional permite duas tuplas
        p[0] = [p[1]] + p[2]

# Se encontrar uma seta, quer dizer que é um fluxo condicional que depende
# Transforma em tupla, condição e destino
def p_fluxo_condicional(p):
    "fluxo_condicional : ID_VARIAVEL SETA flow_target"
    p[0] = (p[1], p[3])

# Permite trabalhar com com mais de uma tupla
def p_lista_fluxos_continua(p):
    """lista_fluxos_continua : VIRGULA fluxo_condicional lista_fluxos_continua
                             | empty"""
    if len(p) == 4:
        p[0] = [p[2]] + p[3]
    else:
        p[0] = []
        
# Vazio
def p_empty(p):
    "empty :"
    pass

# Análise semântica
def validar_modelo(modelo):
    atividades = modelo.get('atividades', {})
    inicio = modelo.get('inicio')
    fim_processo = modelo.get('fim')

# Valida se contem esses tokens necessários
    if not inicio:
        raise Exception("Erro Semântico: Propriedade 'inicio' do processo não definida.")

    if inicio not in atividades:
        raise Exception(f"Erro Semântico: Atividade inicial '{inicio}' não existe.")

# Percorre as atividades, a = dados da atividade
    for nome, a in atividades.items():
        seguinte = a.get('seguinte', []) 
        
        # Se ela for tarefa comum deve ter máximo uma saída
        if a.get('tipo') == 'tarefa' and len(seguinte) > 1:
            raise Exception(f"Erro Semântico: Tarefa '{nome}' tem múltiplas saídas ({len(seguinte)}); use gateway para fluxos condicionais.")
        
        # Se ela for tarefa condicional precisa ter mínimo 2 saídas
        if a.get('tipo') == 'gateway' and len(seguinte) < 2:
            raise Exception(f"Erro Semântico: Gateway '{nome}' precisa de pelo menos 2 saídas (condicionais).")
        
        # Verifica se o destino (o próximo do anterior) é uma atividade ou fim
        for cond, dest in seguinte:
            if dest != 'fim' and dest not in atividades:
                raise Exception(f"Erro Semântico: O destino '{dest}' da atividade '{nome}' não está definido.")
            if dest == 'fim' and not fim_processo:
                 print(f"Aviso Semântico: Atividade '{nome}' aponta para 'fim', mas a propriedade 'fim' do processo não está definida.")
        # Verifica se tem nome ou responsável (nas atividades)
        if 'nome' not in a or 'responsavel' not in a:
             print(f"Aviso Semântico: Atividade '{nome}' faltando propriedades essenciais (nome/responsavel).")

# Apontamento de erros
def p_error(p):
    if p:
        raise SyntaxError(
            f"Erro de sintaxe no token '{p.value}' ({p.type}) linha {p.lineno}"
        )
    else:
        raise SyntaxError("Erro de sintaxe no fim do arquivo. Certifique-se de que todas as chaves e ponto e vírgulas estão fechados.")

parser = yacc.yacc()