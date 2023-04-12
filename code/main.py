from LexicalAnalyzer import LexicalAnalyzer
from Parser import Parser
from VirtualMachine import VirtualMachine
from Compiler import Compiler

lexer = LexicalAnalyzer()
parser = Parser(lexer)

commands = parser.parse()

compiler = Compiler()
program = compiler.compile(commands)

vm = VirtualMachine()
vm.run(program)
