import ply.lex
import ply.yacc

tokens = (
    'ID',
    'STRING',
    'COMMA',
    'EQUALS',
    'BOOLEAN',
    'NONE',
    'INTEGER',
    'FLOAT',
    'LPARENS',
    'RPARENS',
    'FORMAT',
    'ASTERISK',
)


def AnnotLexer():
    def t_STRING(t):
        r''''[^']*'|"[^"]*"'''
        t.value=t.value[1:-1]
        return t
    
    def t_BOOLEAN(t):
        r'True|False'
        t.value=(t.value=='True')
        return t

    def t_NONE(t):
        r'None'
        t.value=None
        return t

    def t_FLOAT(t):
        r'-?\d+.\d+'
        t.value=float(t.value)
        return t
    
    def t_INTEGER(t):
        r'-?\d+'
        t.value=int(t.value)
        return t

    t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    t_FORMAT = r'\{.*?\}'
    
    t_COMMA = r','
    t_EQUALS = r'='
    t_LPARENS = r'\('
    t_RPARENS = r'\)'
    t_ASTERISK = r'\*'

    t_ignore = ' \t\r\n'

    # Error handling rule
    def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)
        

    return ply.lex.lex()

def AnnotParser():

    def p_expr(p):
        ''' expr : func_call
                 | format_list'''
        p[0]=p[1]
    
    def p_func_call_arguments(p):
        'func_call : ID LPARENS arguments RPARENS'
        p[0] = (p[1],) + p[3]

    def p_func_call_empty(p):
        'func_call : ID LPARENS RPARENS'
        p[0] = (p[1], [], {})

    def p_arguments_args_kwargs(p):
        'arguments : args COMMA kwargs'
        p[0] = (p[1], p[3])
    
    def p_arguments_args(p):
        'arguments : args'
        p[0] = (p[1], {})
        
    def p_arguments_kwargs(p):
        'arguments : kwargs'
        p[0] = ([], p[1])
        
    def p_args_args(p):
        'args : args COMMA value'
        p[0] = p[1] + [p[3]]

    def p_args_value(p):
        'args : value'
        p[0] = [p[1]]

    def p_kwargs_kwargs(p):
        'kwargs : kwargs COMMA kwargs'
        p[0] = p[1].copy()
        p[0].update(p[3])
        
    def p_kwargs(p):
        'kwargs : ID EQUALS value'
        p[0] = {p[1]: p[3]}

    def p_value(p):
        '''value : STRING
                 | BOOLEAN
                 | NONE
                 | INTEGER
                 | FLOAT'''
        p[0] = p[1]

    def p_format_list_add(p):
        'format_list : format_list COMMA named_format'
        p[0] = p[1].copy()
        p[0].update(p[3])
        
    def p_format_list(p):
        'format_list : named_format'
        p[0] = p[1]

    def p_named_format(p):
        'named_format : ID EQUALS FORMAT'
        p[0] = {p[1]: p[3]}

    def p_all_format(p):
        'named_format : ASTERISK EQUALS FORMAT'
        p[0] = {'*': p[3]}

    # Error rule for syntax errors
    def p_error(p):
        print("Syntax error in input!: {}".format(p))
        
    return ply.yacc.yacc()

_PARSER=None

def parse(s):
    global _PARSER
    if not _PARSER:
        _PARSER=AnnotParser()
    return _PARSER.parse(s, lexer=AnnotLexer())
