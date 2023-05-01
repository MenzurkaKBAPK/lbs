from Parser import Parser
from VirtualMachine import VirtualMachine


class Compiler:
    def __init__(self):
        self.program = []
        self.pc = 0

    def gen(self, command):
        self.program.append(command)
        self.pc += 1

    def compile(self, node):
        if node.kind == Parser.VAR:
            self.gen(VirtualMachine.IFETCH)
            self.gen(node.value)
        elif node.kind == Parser.CONST:
            self.gen(VirtualMachine.IPUSH)
            self.gen(node.value)
        elif node.kind == Parser.ADD:
            self.compile(node.condition)
            self.compile(node.body1)
            self.gen(VirtualMachine.IADD)
        elif node.kind == Parser.SUB:
            self.compile(node.condition)
            self.compile(node.body1)
            self.gen(VirtualMachine.ISUB)
        elif node.kind == Parser.MULT:
            self.compile(node.condition)
            self.compile(node.body1)
            self.gen(VirtualMachine.IMULT)
        elif node.kind == Parser.DIV:
            self.compile(node.condition)
            self.compile(node.body1)
            self.gen(VirtualMachine.IDIV)
        elif node.kind == Parser.POW:
            self.compile(node.condition)
            self.compile(node.body1)
            self.gen(VirtualMachine.IPOW)
        elif node.kind == Parser.LT:
            self.compile(node.condition)
            self.compile(node.body1)
            self.gen(VirtualMachine.ILT)
        elif node.kind == Parser.P_EQUAL:
            self.compile(node.condition)
            self.compile(node.body1)
            self.gen(VirtualMachine.IEQUAL)
        elif node.kind == Parser.MT:
            self.compile(node.condition)
            self.compile(node.body1)
            self.gen(VirtualMachine.IMT)
        elif node.kind == Parser.SET:
            self.compile(node.body1)
            self.gen(VirtualMachine.ISTORE)
            self.gen(node.condition.value)
        elif node.kind == Parser.IF:
            self.compile(node.condition)
            self.gen(VirtualMachine.JZ)
            addr = self.pc
            self.gen(0)
            self.compile(node.body1)
            self.program[addr] = self.pc
        elif node.kind == Parser.IF_ELSE:
            self.compile(node.condition)
            self.gen(VirtualMachine.JZ)
            addr1 = self.pc
            self.gen(0)
            self.compile(node.body1)
            self.gen(VirtualMachine.JMP)
            addr2 = self.pc
            self.gen(0)
            self.program[addr1] = self.pc
            self.compile(node.body2)
            self.program[addr2] = self.pc
        elif node.kind == Parser.WHILE:
            addr1 = self.pc
            self.compile(node.condition)
            self.gen(VirtualMachine.JZ)
            addr2 = self.pc
            self.gen(0)
            self.compile(node.body1)
            self.gen(VirtualMachine.JMP)
            self.gen(addr1)
            self.program[addr2] = self.pc
        elif node.kind == Parser.DO:
            addr = self.pc
            self.compile(node.condition)
            self.compile(node.body1)
            self.gen(VirtualMachine.JNZ)
            self.gen(addr)
        elif node.kind == Parser.SEQ:
            self.compile(node.condition)
            self.compile(node.body1)
        elif node.kind == Parser.EXPR:
            self.compile(node.condition)
            self.gen(VirtualMachine.IPOP)
        elif node.kind == Parser.PROG:
            self.compile(node.condition)
            self.gen(VirtualMachine.HALT)
        return self.program
