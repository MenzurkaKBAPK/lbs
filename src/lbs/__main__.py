from .compiler import Compiler
from .lexer import LexicalAnalyzer
from .parser import Parser
from .virtual_machine import VirtualMachine


if __name__ == '__main__':
    lexer = LexicalAnalyzer()
    parser = Parser(lexer)

    commands = parser.parse()

    compiler = Compiler()
    program = compiler.compile(commands)

    vm = VirtualMachine()
    output = vm.run(program)

    print('\n'.join(output))
