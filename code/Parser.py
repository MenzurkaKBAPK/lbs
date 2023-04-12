from LexicalAnalyzer import LexicalAnalyzer
from base_functions import error


class Node:
    def __init__(self, kind, value=None, condition=None, body1=None, body2=None):
        self.kind = kind
        self.value = value
        self.condition = condition
        self.body1 = body1
        self.body2 = body2


class Parser:

    VAR, CONST, ADD, SUB, LT, SET, IF, IF_ELSE, WHILE, DO, EMPTY, SEQ, EXPR, PROG, P_EQUAL = range(15)

    def __init__(self, lexer):
        self.lexer = lexer

    def term(self):
        if self.lexer.sym == LexicalAnalyzer.ID:
            n = Node(Parser.VAR, self.lexer.value)
            self.lexer.next_token()
            return n
        elif self.lexer.sym == LexicalAnalyzer.NUM:
            n = Node(Parser.CONST, self.lexer.value)
            self.lexer.next_token()
            return n
        else:
            return self.paren_expr()

    def summa(self):
        n = self.term()
        while self.lexer.sym == LexicalAnalyzer.PLUS or self.lexer.sym == LexicalAnalyzer.MINUS:
            if self.lexer.sym == LexicalAnalyzer.PLUS:
                kind = Parser.ADD
            else:
                kind = Parser.SUB
            self.lexer.next_token()
            n = Node(kind, condition=n, body1=self.term())
        return n

    def test(self):
        n = self.summa()
        if self.lexer.sym == LexicalAnalyzer.LESS:
            self.lexer.next_token()
            n = Node(Parser.LT, condition=n, body1=self.summa())
        elif self.lexer.sym == LexicalAnalyzer.EQUAL:
            self.lexer.next_token()
            n = Node(Parser.P_EQUAL, condition=n, body1=self.summa())
        return n

    def expr(self):
        if self.lexer.sym != LexicalAnalyzer.ID:
            return self.test()
        n = self.test()
        if n.kind == Parser.VAR and self.lexer.sym == LexicalAnalyzer.ASSIGN:
            self.lexer.next_token()
            n = Node(Parser.SET, condition=n, body1=self.expr())
        return n

    def paren_expr(self):
        if self.lexer.sym != LexicalAnalyzer.LPAR:
            error('Parser', '"(" expected')
        self.lexer.next_token()
        n = self.expr()
        if self.lexer.sym != LexicalAnalyzer.RPAR:
            error('Parser', '")" expected')
        self.lexer.next_token()
        return n

    def statement(self):
        if self.lexer.sym == LexicalAnalyzer.IF:
            n = Node(Parser.IF)
            self.lexer.next_token()
            n.condition = self.paren_expr()
            n.body1 = self.statement()
            if self.lexer.sym == LexicalAnalyzer.ELSE:
                n.kind = Parser.IF_ELSE
                self.lexer.next_token()
                n.body2 = self.statement()
        elif self.lexer.sym == LexicalAnalyzer.WHILE:
            n = Node(Parser.WHILE)
            self.lexer.next_token()
            n.condition = self.paren_expr()
            n.body1 = self.statement()
        elif self.lexer.sym == LexicalAnalyzer.DO:
            n = Node(Parser.DO)
            self.lexer.next_token()
            n.condition = self.statement()
            if self.lexer.sym != LexicalAnalyzer.WHILE:
                error('Parser', '"while" expected')
            self.lexer.next_token()
            n.body1 = self.paren_expr()
            if self.lexer.sym != LexicalAnalyzer.SEMICOLON:
                error('Parser', '";" expected')
        elif self.lexer.sym == LexicalAnalyzer.SEMICOLON:
            n = Node(Parser.EMPTY)
            self.lexer.next_token()
        elif self.lexer.sym == LexicalAnalyzer.LBRA:
            n = Node(Parser.EMPTY)
            self.lexer.next_token()
            while self.lexer.sym != LexicalAnalyzer.RBRA:
                n = Node(Parser.SEQ, condition=n, body1=self.statement())
            self.lexer.next_token()
        else:
            n = Node(Parser.EXPR, condition=self.expr())
            if self.lexer.sym != LexicalAnalyzer.SEMICOLON:
                error('Parser', '";" expected')
            self.lexer.next_token()
        return n

    def parse(self):
        self.lexer.next_token()
        node = Node(Parser.PROG, condition=self.statement())
        if self.lexer.sym != LexicalAnalyzer.EOF:
            error('Parser', "Invalid statement syntax")
        return node
