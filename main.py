from vmSam import load_samcode, SaM
from analisador_lex import tokenize
from parser import parse


code = """
int x;
function main() {
  x = 2 + 3 * (4 + 1);
  return x;
}

"""

# tokens = tokenize(code)
# print("---- TOKENS ----")
# for token in tokens:
#     print(token)



# print("\n=== AST ===")
# ast = parse(tokens)
# print(ast)

import json

tokens = tokenize(code)
ast = parse(tokens)

with open("ast.json", "w", encoding="utf-8") as f:
    json.dump(ast, f, indent=2)

print("Arquivo 'ast.json' gerado com sucesso!")


# if __name__ == "__main__":
#      instructions = load_samcode("exemplo.sam")
#      vm = SaM(instructions)
#      vm.run()
#      print("Resultado final:", vm.stack)