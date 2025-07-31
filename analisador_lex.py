import re


regex_table = {
    # Estruturas de Decisão e Repetição
    r"^if$": "IF",
    r"^else$": "ELSE",
    r"^end_if$": "END_IF",
    r"^while$": "WHILE",
    r"^end_while$": "END_WHILE",
    r"^for$": "FOR",
    r"^function$": "FUNCTION",
    r"^return$": "RETURN",
    r"^break$": "BREAK",
    r"^continue$": "CONTINUE",

    # Constantes e tipos
    r"^const$": "CONST",
    r"^int$": "TYPE_INT",
    r"^double$": "TYPE_DOUBLE",
    r"^string$": "TYPE_STRING",

    # Booleanos e nulos
    r"^true$": "TRUE",
    r"^false$": "FALSE",
    r"^null$": "NULL",
    r"^undefined$": "UNDEFINED",

    # Operadores
    r"^\+$": "PLUS",
    r"^-$": "MINUS",
    r"^\*$": "MULTIPLY",
    r"^/$": "DIVIDE",
    r"^%$": "MOD",
    r"^===$": "STRICT_EQUAL",
    r"^==$": "EQUAL",
    r"^!=$": "NOT_EQUAL",
    r"^!==$": "STRICT_NOT_EQUAL",
    r"^>$": "GREATER_THAN",
    r"^>=$": "GREATER_EQUAL",
    r"^<$": "LESS_THAN",
    r"^<=$": "LESS_EQUAL",
    r"^=$": "ASSIGN",
    r"^\+\+$": "INCREMENT",
    r"^--$": "DECREMENT",
    r"^&&$": "AND",
    r"^\|\|$": "OR",
    r"^!$": "NOT",

    # Pontuação
    r"^\($": "LPAREN",
    r"^\)$": "RPAREN",
    r"^\{$": "LBRACE",
    r"^\}$": "RBRACE",
    r"^\[$": "LBRACKET",
    r"^\]$": "RBRACKET",
    r"^;$": "SEMICOLON",
    r"^:$": "COLON",
    r"^,$": "COMMA",
    r"^\.$": "DOT",

    # Literais
    r"^\d+$": "INTEGER_LITERAL",
    r"^\d+\.\d+$": "FLOAT_LITERAL",
    r"^\".*\"$": "STRING_LITERAL",
    r"^'.*'$": "STRING_LITERAL",


    r"^[a-zA-Z_][a-zA-Z0-9_]*:$": "LABEL",

    # Identificadores
    r"^[a-zA-Z_$][a-zA-Z0-9_$]*$": "IDENTIFIER"
}

def tokenize(input_code):
    tokens = []
    lines = input_code.splitlines()
    
    for line_num, line in enumerate(lines, 1):
        # Remove comentários
        line = line.split('#')[0].strip()
        if not line:
            continue

        words = re.findall(r'\w+|[^\s\w]', line)
        for word in words:
            matched = False
            for regex, token_type in regex_table.items():
                if re.match(regex, word):
                    tokens.append({
                        'type': token_type,
                        'value': word,
                        'line': line_num
                    })
                    matched = True
                    break
            if not matched:
                raise ValueError(f'Token inválido: "{word}" na linha {line_num}')
    return tokens
