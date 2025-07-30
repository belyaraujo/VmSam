GRAMATICA = {
    "programa": [["declaracoes", "funcao_principal"]],

    "declaracoes": [["declaracao", "declaracoes"], []],

    "declaracao": [
        ["TYPE_INT", "IDENTIFIER", "SEMICOLON"],
        ["TYPE_DOUBLE", "IDENTIFIER", "SEMICOLON"],
        ["TYPE_STRING", "IDENTIFIER", "SEMICOLON"]
    ],

    "funcao_principal": [["FUNCTION", "IDENTIFIER", "LPAREN", "RPAREN", "LBRACE", "comandos", "RBRACE"]],

    "comandos": [["comando", "comandos"], []],

    "comando": [
        ["RETURN", "expressao", "SEMICOLON"],
        ["atribuicao", "SEMICOLON"],
        ["declaracao"],
        ["if_stmt"],
        ["while_stmt"]
    ],

    
    "if_stmt": [
        ["IF", "LPAREN", "expressao", "RPAREN", "bloco", "else_opt", "END_IF"]
    ],

    "else_opt": [
        ["ELSE", "bloco"],
        []
    ],

    
    "while_stmt": [
        ["WHILE", "LPAREN", "expressao", "RPAREN", "bloco", "END_WHILE"]
    ],

    "bloco": [
        ["LBRACE", "comandos", "RBRACE"]
    ],

    "atribuicao": [["IDENTIFIER", "ASSIGN", "expressao"]],

    "expressao": [["termo", "expressao_op"]],

    "expressao_op": [
        ["PLUS", "termo", "expressao_op"],
        ["MINUS", "termo", "expressao_op"],
        []
    ],

    "termo": [["fator", "termo_op"]],

    "termo_op": [
        ["MULTIPLY", "fator", "termo_op"],
        ["DIVIDE", "fator", "termo_op"],
        []
    ],

    "fator": [
        ["LPAREN", "expressao", "RPAREN"],
        ["INTEGER_LITERAL"],
        ["FLOAT_LITERAL"],
        ["IDENTIFIER"]
    ]
}
