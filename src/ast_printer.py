from expression import Visitor, Expression, Unary, Binary, Literal, Grouping
from token_type import TokenType
from token_individual import Token
class ASTPrinter(Visitor):
    def __init__(self):
        pass
    def print_ast(self, expression: Expression) -> str:
        return expression.accept(self)

if __name__ == "__main__":
    ast = ASTPrinter()
    unary = Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123))
    grouping = Grouping(Literal(45.67))
    binary = Binary(unary, Token(TokenType.STAR, "*", None, 1), grouping)
    print(ast.print_ast(binary))