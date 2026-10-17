import sys

from .errors import error


class LexicalAnalyzer:

    NUM, ID, IF, ELSE, WHILE, DO, LBRA, RBRA, LPAR, RPAR, PLUS, MINUS,\
        LESS, ASSIGN, SEMICOLON, EOF, EQUAL, MORE, MULT, DIV, POW = range(21)

    SYMBOLS = {'{': LBRA, '}': RBRA, '=': ASSIGN, ';': SEMICOLON, '(': LPAR, ')': RPAR,
               '+': PLUS, '-': MINUS, '<': LESS, '>': MORE, '*': MULT, '/': DIV}

    WORDS = {'if': IF, 'else': ELSE, 'do': DO, 'while': WHILE}

    def __init__(self, stream=None):
        self.stream = stream if stream is not None else sys.stdin
        self.ch = ' '
        self.value = None
        self.sym = None

    def get_ch(self):
        self.ch = self.stream.read(1)

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
                if self.sym == LexicalAnalyzer.ASSIGN \
                        and self.ch in LexicalAnalyzer.SYMBOLS \
                        and LexicalAnalyzer.SYMBOLS[self.ch] == LexicalAnalyzer.ASSIGN:
                    self.sym = LexicalAnalyzer.EQUAL
                    self.get_ch()
                if self.sym == LexicalAnalyzer.MULT \
                        and self.ch in LexicalAnalyzer.SYMBOLS \
                        and LexicalAnalyzer.SYMBOLS[self.ch] == LexicalAnalyzer.MULT:
                    self.sym = LexicalAnalyzer.POW
                    self.get_ch()
            elif self.ch.isascii() and self.ch.isdigit():
                int_val = 0
                while self.ch.isascii() and self.ch.isdigit():
                    int_val = int_val * 10 + int(self.ch)
                    self.get_ch()
                self.value = int_val
                self.sym = LexicalAnalyzer.NUM
            elif self.ch.isascii() and self.ch.isalpha():
                ident = ''
                while self.ch.isascii() and self.ch.isalpha():
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
