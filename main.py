from vmSam import load_samcode, SaM
from analisador_lex import tokenize

# x = 18
# if x < 20:
#     return 0
#else:
    # return 1

    # for i in range(5):
    #     print(i)

# ---------------------------- Teste -----------------------------

code = """
int f(int x){
x++;
return x;
}
main(){
int x = 2;
x = f(x);
}

"""

tokens = tokenize(code)

for token in tokens:
    print(token)

# if __name__ == "__main__":
#     instructions = load_samcode("exemplo.sam")
#     vm = SaM(instructions)
#     vm.run()
#     print("Resultado final:", vm.stack)

