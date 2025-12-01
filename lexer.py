import ply.lex as lex

tokens = (
    'KW_PROCESSO', 'KW_NOME', 'KW_INICIO', 'KW_FIM', 'KW_ATIVIDADES',
    'KW_TIPO', 'KW_SEGUINTE',
    'KW_DONO', 'KW_RESPONSAVEL', 'KW_TEMPO', 'KW_CUSTO',
    'ID_VARIAVEL', 'LIT_STRING', 'NUMERO',
    'OP_ATRIBUICAO',
    'ABRE_CHAVE', 'FECHA_CHAVE', 'VIRGULA',
    'PONTO_VIRGULA', 'SETA'
)

reserved = {
    'processo': 'KW_PROCESSO',
    'nome': 'KW_NOME',
    'inicio': 'KW_INICIO',
    'fim': 'KW_FIM',
    'atividades': 'KW_ATIVIDADES',
    'tipo': 'KW_TIPO',
    'seguinte': 'KW_SEGUINTE',
    'dono': 'KW_DONO',
    'responsavel': 'KW_RESPONSAVEL',
    'tempo': 'KW_TEMPO',
    'custo': 'KW_CUSTO',
}

t_OP_ATRIBUICAO = r'='
t_ABRE_CHAVE = r'{'
t_FECHA_CHAVE = r'}'
t_VIRGULA = r','
t_PONTO_VIRGULA = r';'
t_SETA = r'->'

def t_LIT_STRING(t):
    r'\"[^\"]*\"'
    # Remove as aspas
    t.value = t.value[1:-1]
    return t

def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID_VARIAVEL(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    # Checa por palavras reservadas
    t.type = reserved.get(t.value, 'ID_VARIAVEL')
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    # Não levanta exceção, apenas imprime (o parser fará o controle de erro principal)
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()