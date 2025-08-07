from dataclasses import dataclass
from token_individual import Token
    

class Expression:
    def __init__(self):
        pass
    def accept(self, visitor):
        pass

@dataclass
class Binary(Expression):
    left: Expression
    operator: Token
    right: Expression
    def accept(self, visitor):
        return visitor.visit_binary(self)

@dataclass 
class Unary(Expression):
    operator: Token
    right: Expression
    def accept(self, visitor):
        return visitor.visit_unary(self)

@dataclass
class Grouping(Expression):
    expression: Expression
    def accept(self, visitor):
        return visitor.visit_grouping(self)

@dataclass
class Literal(Expression):
    value: any
    #@override
    def accept(self, visitor):
        return visitor.visit_literal(self)


class Visitor:
    def __init__(self):
        pass
    def paran(self, name: str, *expressions: Expression):
        string = "("
        string += name
        for expr in expressions:
            string += " "
            string += expr.accept(self)
        string +=")"
        return string
        
    '''def visit_literal(self, expression: Literal):
        return "(" + str(type(expression.value).__name__) + " " + str(expression.value) + ")"'''
    def visit_literal(self, expression: Literal):
        if expression.value is None:
            return "null"
        return str(expression.value)
    def visit_grouping(self, expression: Grouping):
        return self.paran('group', expression.expression)
    def visit_unary(self, expression: Unary):
        return self.paran(expression.operator.lexeme, expression.right)
    def visit_binary(self, expression: Binary):
        return self.paran(expression.operator.lexeme, expression.left, expression.right)
