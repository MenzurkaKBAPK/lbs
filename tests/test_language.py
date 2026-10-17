import io
import sys
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from lbs.compiler import Compiler
from lbs.lexer import LexicalAnalyzer
from lbs.parser import Parser
from lbs.virtual_machine import VirtualMachine


def execute(source):
    with patch.object(sys, "stdin", io.StringIO(source)):
        tree = Parser(LexicalAnalyzer()).parse()
    program = Compiler().compile(tree)
    with redirect_stdout(io.StringIO()):
        return VirtualMachine().run(program)


class LanguageTests(unittest.TestCase):
    def test_arithmetic_and_comparisons(self):
        result = execute("{a=2+3;b=7-4;c=3*4;d=8/2;e=2**3;f=e>c;}")

        self.assertEqual(
            result,
            ["a = 5", "b = 3", "c = 12", "d = 4", "e = 8"],
        )

    def test_if_else(self):
        self.assertEqual(execute("{a=2;if(a==2)b=7;else b=9;}"), ["a = 2", "b = 7"])

    def test_while_and_do_while(self):
        result = execute("{a=1;while(a<4)a=a+1;do b=b+2;while(b<5);}")

        self.assertEqual(result, ["a = 4", "b = 6"])


if __name__ == "__main__":
    unittest.main()
