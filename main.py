from vmSam import load_samcode, SaM
from analisador_lex import tokenize
from parser import parse
import json

code = """
function main() {
  int x;
  x = 5;
  if (x > 0) {
    x = x - 1;
  } else {
    x = 0;
  }
  end_if
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



tokens = tokenize(code)
ast = parse(tokens)
print(json.dumps(ast, indent=2))


# if __name__ == "__main__":
#      instructions = load_samcode("exemplo.sam")
#      vm = SaM(instructions)
#      vm.run()
#      print("Resultado final:", vm.stack)