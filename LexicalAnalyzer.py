import sys
from base_functions import error


class LexicalAnalyzer:

    NUM, ID, IF, ELSE, WHILE, DO, LBRA, RBRA, LPAR, RPAR, PLUS, MINUS, LESS, EQUAL, SEMICOLON, EOF = range(16)

    SYMBOLS = {'{': LBRA, '}': RBRA, '=': EQUAL, ';': SEMICOLON,
               '(': LPAR, ')': RPAR, '+': PLUS, '-': MINUS, '<': LESS}

    WORDS = {'if': IF, 'else': ELSE, 'do': DO, 'while': WHILE}

    def __init__(self):
        self.ch = ' '
        self.value = None
        self.sym = None

    def get_ch(self):
        self.ch = sys.stdin.read(1)

    def next_token(self):
        self.value = None
        self.sym = None
        while self.sym is None:
            if len(self.ch) == 0:
                self.sym = LexicalAnalyzer.EOF
            elif self.ch.isspace():
                self.get_ch()
            elif self.ch in LexicalAnalyzer.SYMBOLS:
                self.sym = LexicalAnalyzer.SYMBOLS[self.ch]
                self.get_ch()
            elif self.ch.isdigit():
                int_val = 0
                while self.ch.isdigit():
                    int_val = int_val * 10 + int(self.ch)
                    self.get_ch()
                self.value = int_val
                self.sym = LexicalAnalyzer.NUM
            elif self.ch.isalpha():
                ident = ''
                while self.ch.isalpha():
                    ident += self.ch.lower()
                    self.get_ch()
                if ident in LexicalAnalyzer.WORDS:
                    self.sym = LexicalAnalyzer.WORDS[ident]
                elif len(ident) == 1:
                    self.sym = LexicalAnalyzer.ID
                    self.value = ord(ident) - ord('a')
                else:
                    error('LexicalAnalyzer', 'Unknown identifier: ' + ident)
            else:
                error('LexicalAnalyzer', 'Unexpected symbol: ' + self.ch)
