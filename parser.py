import ply.yacc as yacc
from lexer import tokens 

# -------------------------
# GRAMÁTICA PRINCIPAL
# -------------------------

def p_programa(p):
    "programa : processo"
    p[0] = p[1]

def p_processo(p):
    "processo : KW_PROCESSO ABRE_CHAVE definicoes_processo FECHA_CHAVE"
    p[0] = p[3]

def p_definicoes_processo(p):
    "definicoes_processo : prop_nome prop_dono prop_inicio bloco_atividades prop_fim"
    p[0] = {
        p[1][0]: p[1][1],
        p[2][0]: p[2][1],
        p[3][0]: p[3][1],
        'atividades': p[4],
        p[5][0]: p[5][1]
    }

# -------------------------
# PROPRIEDADES DO PROCESSO E ATIVIDADE (regras únicas para reutilização)
# -------------------------

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

# -------------------------
# BLOCO DE ATIVIDADES
# -------------------------

def p_bloco_atividades(p):
    "bloco_atividades : KW_ATIVIDADES ABRE_CHAVE lista_atividades FECHA_CHAVE"
    p[0] = p[3]

def p_lista_atividades(p):
    """lista_atividades : lista_atividades atividade
                          | empty"""
    if len(p) == 3:
        p[1][p[2]['id']] = p[2]
        p[0] = p[1]
    else:
        p[0] = {}

def p_atividade(p):
    "atividade : ID_VARIAVEL ABRE_CHAVE lista_propriedades_atividade FECHA_CHAVE"
    props_dict = dict(p[3])
    p[0] = {'id': p[1], **props_dict}

# -------------------------
# PROPRIEDADES DA ATIVIDADE
# -------------------------

def p_lista_propriedades_atividade(p):
    """lista_propriedades_atividade : propriedade_atividade lista_propriedades_atividade
                                     | empty"""
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_propriedade_atividade(p):
    """propriedade_atividade : prop_nome 
                             | prop_tipo
                             | prop_responsavel
                             | prop_tempo
                             | prop_custo
                             | prop_seguinte"""
    p[0] = p[1]

# def p_prop_nome_atividade(p): -> REMOVIDA para evitar duplicidade, usando p_prop_nome

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

# -------------------------
# FLUXOS CONDICIONAIS (CORREÇÃO DE KW_FIM como ID)
# -------------------------

# Nova regra para permitir KW_FIM como um destino de fluxo, resolvendo o erro de sintaxe.
def p_flow_target(p):
    """flow_target : ID_VARIAVEL
                   | KW_FIM"""
    # Se for KW_FIM, retorna 'fim'. Se for ID_VARIAVEL, retorna seu valor (o ID).
    p[0] = p[1]

def p_lista_fluxos(p):
    # Usa flow_target para destinos únicos de fluxo ({ destino })
    """lista_fluxos : fluxo_condicional lista_fluxos_continua
                     | flow_target"""
    if len(p) == 2:
        # Caso 1: flow_target sozinho (Fluxo simples: { destino })
        p[0] = [('next', p[1])]
    else:
        # Caso 2: Fluxo condicional (ou lista de condicionais)
        p[0] = [p[1]] + p[2]

def p_fluxo_condicional(p):
    # Usa flow_target para o destino do fluxo (p[3])
    "fluxo_condicional : ID_VARIAVEL SETA flow_target"
    # (condição, destino)
    p[0] = (p[1], p[3])

def p_lista_fluxos_continua(p):
    """lista_fluxos_continua : VIRGULA fluxo_condicional lista_fluxos_continua
                             | empty"""
    if len(p) == 4:
        p[0] = [p[2]] + p[3]
    else:
        p[0] = []

def p_empty(p):
    "empty :"
    pass

# -------------------------
# VALIDAÇÃO SEMÂNTICA
# -------------------------

def validar_modelo(modelo):
    atividades = modelo.get('atividades', {})
    inicio = modelo.get('inicio')
    fim_processo = modelo.get('fim') # Usado para referência no fim

    if not inicio:
        raise Exception("Erro Semântico: Propriedade 'inicio' do processo não definida.")

    if inicio not in atividades:
        raise Exception(f"Erro Semântico: Atividade inicial '{inicio}' não existe.")

    for nome, a in atividades.items():
        seguinte = a.get('seguinte', []) 
        
        if a.get('tipo') == 'gateway' and len(seguinte) < 2:
            raise Exception(f"Erro Semântico: Gateway '{nome}' precisa de pelo menos 2 saídas (condicionais).")
        
        for cond, dest in seguinte:
            if dest != 'fim' and dest not in atividades:
                raise Exception(f"Erro Semântico: O destino '{dest}' da atividade '{nome}' não está definido.")
            # Validação: Se o destino for 'fim', checa se o processo tem a propriedade fim definida (semântica)
            if dest == 'fim' and not fim_processo:
                 print(f"⚠️ Aviso Semântico: Atividade '{nome}' aponta para 'fim', mas a propriedade 'fim' do processo não está definida.")

        if 'nome' not in a or 'responsavel' not in a:
             print(f"⚠️ Aviso Semântico: Atividade '{nome}' faltando propriedades essenciais (nome/responsavel).")


# -------------------------
# ERROS
# -------------------------

def p_error(p):
    if p:
        raise SyntaxError(
            f"Erro de sintaxe no token '{p.value}' ({p.type}) linha {p.lineno}"
        )
    else:
        raise SyntaxError("Erro de sintaxe no fim do arquivo. Certifique-se de que todas as chaves e ponto e vírgulas estão fechados.")

parser = yacc.yacc()