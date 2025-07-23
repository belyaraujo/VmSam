tokens = []
current = 0

def parse(tokens_input):
    global tokens, current
    tokens = tokens_input
    current = 0
    return parse_programa()

def match(token_type):
    return current < len(tokens) and tokens[current]['type'] == token_type

def advance():
    global current
    current += 1
    return tokens[current - 1]

def expect(token_type):
    if not match(token_type):
        expected = token_type
        found = tokens[current]['type'] if current < len(tokens) else 'EOF'
        raise Exception(f"Esperado token {expected}, encontrado {found}")
    return advance()

def parse_programa():
    declaracoes = parse_declaracoes()
    main = parse_funcao_principal()
    return {'type': 'Programa', 'declaracoes': declaracoes, 'main': main}

def parse_declaracoes():
    decls = []
    while match('TYPE_INT') or match('TYPE_DOUBLE') or match('TYPE_STRING'):
        decls.append(parse_declaracao())
    return decls

def parse_declaracao():
    tipo = advance()['type']
    ident = expect('IDENTIFIER')['value']
    expect('SEMICOLON')
    return {'type': 'Declaracao', 'tipo': tipo, 'id': ident}

def parse_funcao_principal():
    expect('FUNCTION')
    expect('IDENTIFIER')  # "main"
    expect('LPAREN')
    expect('RPAREN')
    expect('LBRACE')
    comandos = parse_comandos()
    expect('RBRACE')
    return {'type': 'MainFunction', 'comandos': comandos}

def parse_comandos():
    cmds = []
    while not match('RBRACE'):
        cmds.append(parse_comando())
    return cmds

def parse_comando():
    if match('RETURN'):
        advance()
        expr = parse_expressao()
        expect('SEMICOLON')
        return {'type': 'Return', 'expr': expr}
    if match('TYPE_INT') or match('TYPE_DOUBLE') or match('TYPE_STRING'):
        return parse_declaracao()
    cmd = parse_atribuicao()
    expect('SEMICOLON')
    return cmd

def parse_atribuicao():
    ident = expect('IDENTIFIER')['value']
    expect('ASSIGN')
    expr = parse_expressao()
    return {'type': 'Atribuicao', 'id': ident, 'expr': expr}

def parse_expressao():
    left = parse_termo()
    while match('PLUS') or match('MINUS'):
        op = advance()['type']
        right = parse_termo()
        left = {'type': 'BinOp', 'op': op, 'left': left, 'right': right}
    return left

def parse_termo():
    left = parse_fator()
    while match('MULTIPLY') or match('DIVIDE'):
        op = advance()['type']
        right = parse_fator()
        left = {'type': 'BinOp', 'op': op, 'left': left, 'right': right}
    return left

def parse_fator():
    if match('LPAREN'):
        advance()
        expr = parse_expressao()
        expect('RPAREN')
        return expr
    if match('INTEGER_LITERAL') or match('FLOAT_LITERAL'):
        return {'type': 'Literal', 'value': advance()['value']}
    if match('IDENTIFIER'):
        return {'type': 'Var', 'name': advance()['value']}
    raise Exception(f"Fator inesperado: {tokens[current]['type'] if current < len(tokens) else 'EOF'}")
