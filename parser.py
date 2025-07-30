# parser.py
# Recebe uma lista de tokens gerados pelo lexer e constrói a AST com base em uma gramática LL(1)

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
    while not match('RBRACE') and not match('END_IF') and not match('END_WHILE'):
        cmds.append(parse_comando())
    return cmds


def parse_comando():
    if match('RETURN'):
        advance()
        expr = parse_expressao()
        expect('SEMICOLON')
        return {'type': 'Return', 'expr': expr}

    if match('IF'):
        advance()
        expect('LPAREN')
        cond = parse_expressao()
        expect('RPAREN')
        expect('LBRACE')
        then_block = parse_comandos()
        expect('RBRACE')

        else_block = None
        if match('ELSE'):
            advance()
            expect('LBRACE')
            else_block = parse_comandos()
            expect('RBRACE')

        if match('END_IF'):
            advance()

        return {'type': 'If', 'cond': cond, 'then': then_block, 'else': else_block}

    if match('WHILE'):
        advance()
        expect('LPAREN')
        cond = parse_expressao()
        expect('RPAREN')
        expect('LBRACE')
        body = parse_comandos()
        expect('RBRACE')

        if match('END_WHILE'):
            advance()

        return {'type': 'While', 'cond': cond, 'body': body}

    if match('TYPE_INT') or match('TYPE_DOUBLE') or match('TYPE_STRING'):
        return parse_declaracao()

    if match('IDENTIFIER'):
        # Verifica se é atribuição ou chamada de função
        if (current + 1 < len(tokens)) and tokens[current + 1]['type'] == 'ASSIGN':
            cmd = parse_atribuicao()
            expect('SEMICOLON')
            return cmd
        elif (current + 1 < len(tokens)) and tokens[current + 1]['type'] == 'LPAREN':
            cmd = parse_chamada_funcao()
            expect('SEMICOLON')
            return cmd
        else:
            raise Exception(f"Comando inesperado: {tokens[current]['type']}")

    raise Exception(f"Comando inesperado: {tokens[current]['type'] if current < len(tokens) else 'EOF'}")

def parse_chamada_funcao():
    nome = expect('IDENTIFIER')['value']
    expect('LPAREN')
    args = []
    if not match('RPAREN'):  # Se não for fechamento, tem argumentos
        args.append(parse_expressao())
        while match('COMMA'):
            advance()
            args.append(parse_expressao())
    expect('RPAREN')
    return {'type': 'ChamadaFuncao', 'name': nome, 'args': args}



def parse_atribuicao():
    ident = expect('IDENTIFIER')['value']
    expect('ASSIGN')
    expr = parse_expressao()
    return {'type': 'Atribuicao', 'id': ident, 'expr': expr}

def parse_expressao():
    return parse_relacional()

def parse_relacional():
    left = parse_aditivo()
    while match('GREATER_THAN') or match('LESS_THAN') or match('EQUAL'):
        op = advance()['type']
        right = parse_aditivo()
        left = {'type': 'BinOp', 'op': op, 'left': left, 'right': right}
    return left

def parse_aditivo():
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
