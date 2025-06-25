class Instruction:
    def __init__(self, opcode, arg=None):
        self.opcode = opcode.upper()
        self.arg = arg

class SaM:
    def __init__(self, instructions):
        self.instructions = instructions
        self.stack = []
        self.memory = [0] * 1024
        self.heap = {}
        self.pc = 0
        self.fbr = 0
        self.sp = 0
        self.running = True

    def push(self, val):
        self.stack.append(val)
        self.sp += 1

    def pop(self):
        self.sp -= 1
        return self.stack.pop()

    def run(self):
        while self.running and self.pc < len(self.instructions):
            instr = self.instructions[self.pc]
            self.execute(instr)
            self.pc += 1

    def execute(self, instr):
        op = instr.opcode
        arg = instr.arg

        if op == "PUSH":
            self.push(arg)
        elif op == "POP":
            self.pop()
        elif op == "ADD":
            self.push(self.pop() + self.pop())
        elif op == "SUB":
            a, b = self.pop(), self.pop()
            self.push(b - a)
        elif op == "TIMES":
            self.push(self.pop() * self.pop())
        elif op == "DIV":
            a, b = self.pop(), self.pop()
            self.push(b // a)
        elif op == "MOD":
            a, b = self.pop(), self.pop()
            self.push(b % a)
        elif op == "LSHIFT":
            self.push(self.pop() << arg)
        elif op == "RSHIFT":
            self.push(self.pop() >> arg)
        elif op == "NOT":
            self.push(0 if self.pop() != 0 else 1)
        elif op == "OR":
            a, b = self.pop(), self.pop()
            self.push(1 if a or b else 0)
        elif op == "AND":
            a, b = self.pop(), self.pop()
            self.push(1 if a and b else 0)

        # Operações lógicas e bitwise
        elif op == "XOR":
            a, b = self.pop(), self.pop()
            self.push(1 if (b != 0) ^ (a != 0) else 0)
        elif op == "NAND":
            a, b = self.pop(), self.pop()
            self.push(0 if (b != 0 and a != 0) else 1)
        elif op == "BITNOT":
            self.push(~int(self.pop()) & 0xFFFFFFFF)
        elif op == "BITAND":
            a, b = int(self.pop()), int(self.pop())
            self.push(b & a)
        elif op == "BITOR":
            a, b = int(self.pop()), int(self.pop())
            self.push(b | a)
        elif op == "BITXOR":
            a, b = int(self.pop()), int(self.pop())
            self.push(b ^ a)
        elif op == "BITNAND":
            a, b = int(self.pop()), int(self.pop())
            self.push(~(b & a) & 0xFFFFFFFF)


        elif op == "GREATER":
            a, b = self.pop(), self.pop()
            self.push(1 if b > a else 0)
        elif op == "LESS":
            a, b = self.pop(), self.pop()
            self.push(1 if b < a else 0)

        elif op == "EQUAL":
            a, b = self.pop(), self.pop()
            self.push(1 if a == b else 0)

        # Comparações especiais
        elif op == "ISNIL":
            self.push(1 if self.pop() == 0 else 0)
        elif op == "ISPOS":
            self.push(1 if self.stack[-1] > 0 else 0)
        elif op == "ISNEG":
            self.push(1 if self.stack[-1] < 0 else 0)

        elif op == "CMP":
            a, b = self.pop(), self.pop()
            self.push(-1 if b < a else (1 if b > a else 0))

        # Operações com ponto flutuante
        elif op == "ADDF":
            self.push(float(self.pop()) + float(self.pop()))
        elif op == "SUBF":
            a, b = self.pop(), self.pop()
            self.push(float(b) - float(a))
        elif op == "TIMESF":
            self.push(float(self.pop()) * float(self.pop()))
        elif op == "DIVF":
            a, b = self.pop(), self.pop()
            self.push(float(b) / float(a))
        elif op == "CMPF":
            a, b = self.pop(), self.pop()
            self.push(-1 if b < a else (1 if b > a else 0))
        elif op == "ITOF":
            self.push(float(self.pop()))
        elif op == "FTOI":
            self.push(int(float(self.pop())))

        # Instruções PUSHIMM variantes
        elif op == "PUSHIMM":
            self.push(arg)
        elif op == "PUSHIMMF":
            self.push(float(arg))
        elif op == "PUSHIMMCH":
            self.push(ord(arg))
        elif op == "PUSHIMMSTR":
            self.heap[self.heap_ptr] = arg
            self.push(self.heap_ptr)
            self.heap_ptr += len(arg) + 1
        elif op == "PUSHIMMPA":
            self.push(arg)
        elif op == "MALLOC":
            size = self.pop()
            self.heap[self.heap_ptr] = [0] * (size + 1)
            self.heap[self.heap_ptr][0] = size
            self.push(self.heap_ptr)
            self.heap_ptr += size + 1

        # Controle de fluxo
        elif op == "JUMP":
            self.pc = arg - 1
        elif op == "JUMPC":
            if self.pop() != 0:
                self.pc = arg - 1
        elif op == "JUMPIND":
            self.pc = self.pop() - 1
        elif op == "JSR":
            self.push(self.pc + 1)
            self.pc = arg - 1
        elif op == "JSRIND":
            addr = self.pop()
            self.push(self.pc + 1)
            self.pc = addr - 1
        elif op == "SKIP":
            offset = self.pop()
            self.pc += offset

        # I/O
        elif op == "READ":
            self.push(int(input("READ (int): ")))
        elif op == "READF":
            self.push(float(input("READF (float): ")))
        elif op == "WRITE":
            print("WRITE:", self.pop())
        elif op == "WRITEF":
            print("WRITEF:", float(self.pop()))

        # Registradores e pilha
        elif op == "PUSHSP":
            self.push(self.sp)
        elif op == "POPSP":
            self.sp = self.pop()
        elif op == "PUSHFBR":
            self.push(self.fbr)
        elif op == "POPFBR":
            self.fbr = self.pop()
        elif op == "LINK":
            self.push(self.fbr)
            self.fbr = self.sp - 1
        elif op == "ADDSP":
            for _ in range(arg):
                self.push(0)
        elif op == "PUSHOFF":
            self.push(self.stack[self.fbr + arg])
        elif op == "STOREOFF":
            self.stack[self.fbr + arg] = self.pop()
        elif op == "DUP":
            self.push(self.stack[-1])
        elif op == "SWAP":
            self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]
        elif op == "PUSHIND":
            addr = self.pop()
            self.push(self.stack[addr])
        elif op == "STOREIND":
            val = self.pop()
            addr = self.pop()
            self.stack[addr] = val
        elif op == "HALT" or op == "STOP":
            self.running = False
        else:
            raise Exception(f"Instrução inválida: {op}")

def load_samcode(filename):
    instructions = []
    with open(filename) as file:
        for line in file:
            parts = line.strip().split(maxsplit=1)
            if not parts or parts[0].startswith("#"):
                continue

            opcode = parts[0].upper()
            arg = None

            if len(parts) > 1:
                raw_arg = parts[1].strip()
                if raw_arg.startswith('"') and raw_arg.endswith('"'):
                    arg = raw_arg.strip('"')
                elif raw_arg.startswith("'") and raw_arg.endswith("'"):
                    arg = ord(raw_arg.strip("'"))
                else:
                    try:
                        if '.' in raw_arg:
                            arg = float(raw_arg)
                        else:
                            arg = int(raw_arg)
                    except ValueError:
                        arg = raw_arg

            instructions.append(Instruction(opcode, arg))
    return instructions

if __name__ == "__main__":
    instructions = load_samcode("exemplo.sam")
    vm = SaM(instructions)
    vm.run()
    print("Resultado final:", vm.stack)
