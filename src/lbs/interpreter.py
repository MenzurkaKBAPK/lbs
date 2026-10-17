import io

from .compiler import Compiler
from .lexer import LexicalAnalyzer
from .parser import Parser
from .virtual_machine import VirtualMachine


def run_source(source):
    """Parse, compile, and execute LBS source code."""
    lexer = LexicalAnalyzer(io.StringIO(source))
    tree = Parser(lexer).parse()
    program = Compiler().compile(tree)
    return VirtualMachine().run(program)
