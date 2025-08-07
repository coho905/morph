from token_type import TokenType
from token_individual import Token
from main import Morph

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.keywords = {
            "and": TokenType.AND,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "fn": TokenType.FN,
            "for": TokenType.FOR,
            "if": TokenType.IF,
            "null": TokenType.NULL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE
        }

    def isAtEnd(self):
        return self.current >= len(self.source)
    
    def scanTokens(self):
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()
        end_token = Token(TokenType("EOF"), "", None, self.line)
        self.tokens.append(end_token)
        return self.tokens

    def scanToken(self):
        char = self.advance()
        match char:
            case "(":
                self.addToken(TokenType.LEFT_PAREN)
            case ")":
                self.addToken(TokenType.RIGHT_PAREN)
            case "{":
                self.addToken(TokenType.LEFT_BRACE)
            case "}":
                self.addToken(TokenType.RIGHT_BRACE)
            case ",":
                self.addToken(TokenType.COMMA)
            case ".":
                self.addToken(TokenType.DOT)
            case "-":
                if self.match(">"):
                    self.addToken(TokenType.LINE_LESS)
                else:
                    self.addToken(TokenType.MINUS)
            case "+":
                self.addToken(TokenType.PLUS)
            case ";":
                self.addToken(TokenType.SEMICOLON)
            case "*":
                self.addToken(TokenType.STAR)
            case "!":
                if self.match("="):
                    self.addToken(TokenType.BANG_EQUAL)
                else:
                    self.addToken(TokenType.BANG)
            case "=":
                if self.match("="):
                    self.addToken(TokenType.EQUAL_EQUAL)
                else:
                    self.addToken(TokenType.EQUAL)
            case ">":
                if self.match("="):
                    self.addToken(TokenType.GREATER_EQUAL)
                else:
                    self.addToken(TokenType.GREATER)
            case "<":
                if self.match("="):
                    self.addToken(TokenType.LESS_EQUAL)
                elif self.match("-"):
                    self.addToken(TokenType.LINE_GREATER)
                else:
                    self.addToken(TokenType.LESS)
            case "/":
                if self.match("/"):
                    while self.peek() != "\n" and not self.isAtEnd():
                        self.advance()
                else:
                    self.addToken(TokenType.SLASH)
            case " ":
                pass
            case "\n":
                self.line += 1
            case "\r":
                pass
            case "\t":
                pass
            case '"':
                self.string()
            case _:
                if char.isdigit():
                    self.number()
                elif char.isalpha():
                    self.identifier()
                else:
                    Morph.error(self.line, "Unexpected character.")
    
    def advance(self):
        char = self.source[self.current]
        self.current += 1
        return char
    
    def addToken(self, type: TokenType):
        self.tokens.append(Token(type, self.source[self.start:self.current], None, self.line))

    def match(self, expected: str):
        if self.isAtEnd():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True
    
    def peek(self):
        if self.isAtEnd():
            return "\0"
        return self.source[self.current]
    
    def string(self):
        while self.peek() != '"' and not self.isAtEnd():
            if self.peek() == "\n":
                self.line += 1
            self.advance()
        if self.isAtEnd():
            Morph.error(self.line, "Unterminated string.")
        self.advance()
        value = self.source[self.start + 1:self.current - 1]
        self.addToken(TokenType.STRING, value)

    def number(self):
        while self.peek().isdigit():
            self.advance()
        if self.peek() == "." and self.peekNext().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()
        self.addToken(TokenType.NUMBER, float(self.source[self.start:self.current]))

    def identifier(self):
        while self.peek().isalnum() or self.peek() == "_":
            self.advance()
        text = self.source[self.start:self.current]
        if text in self.keywords:
            self.addToken(self.keywords[text])
        else:
            self.addToken(TokenType.IDENTIFIER)

    def peekNext(self):
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]