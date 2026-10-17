import unittest

from lbs import LbsError, run_source


class LanguageTests(unittest.TestCase):
    def test_arithmetic_precedence_and_comparisons(self):
        result = run_source(
            '{a=2+3*4;b=(2+3)*4;c=2**3**2;d=7/2;e=c>b;f=a>c;}'
        )

        self.assertEqual(
            result,
            ['a = 14', 'b = 20', 'c = 512', 'd = 3', 'e = 1', 'f = 0'],
        )

    def test_assignment_is_an_expression(self):
        self.assertEqual(run_source('{a=b=3;c=(a=4)+b;}'), ['a = 4', 'b = 3', 'c = 7'])

    def test_if_else(self):
        self.assertEqual(run_source('{a=2;if(a==2)b=7;else b=9;}'), ['a = 2', 'b = 7'])

    def test_while_and_do_while(self):
        result = run_source('{a=1;while(a<4)a=a+1;do b=b+2;while(b<5);}')

        self.assertEqual(result, ['a = 4', 'b = 6'])

    def test_top_level_do_while_consumes_its_semicolon(self):
        self.assertEqual(run_source('do a=a+1;while(a<2);'), ['a = 2'])

    def test_assigned_zero_is_reported(self):
        self.assertEqual(run_source('a=0;'), ['a = 0'])

    def test_unclosed_block_is_a_syntax_error(self):
        with self.assertRaisesRegex(LbsError, '"}" expected'):
            run_source('{a=1;')

    def test_non_ascii_identifier_is_rejected(self):
        with self.assertRaisesRegex(LbsError, 'Unexpected symbol'):
            run_source('я=1;')

    def test_division_by_zero_is_a_language_error(self):
        with self.assertRaisesRegex(LbsError, 'Division by zero'):
            run_source('a=1/0;')


if __name__ == '__main__':
    unittest.main()
