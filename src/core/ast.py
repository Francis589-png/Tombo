"""
Minimal AST node classes for Tombo core.
"""

class ASTNode:
    pass

class Module(ASTNode):
    def __init__(self, body):
        self.body = body
    def __repr__(self):
        return f"Module(body={self.body!r})"

class Let(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __repr__(self):
        return f"Let({self.name}, {self.value!r})"

class Change(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __repr__(self):
        return f"Change({self.name}, {self.value!r})"

class If(ASTNode):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body
    def __repr__(self):
        return f"If({self.cond!r}, {self.body!r})"

class Defi(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body
    def __repr__(self):
        return f"Defi({self.name}, {self.params}, {self.body!r})"

class FunctionDef(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body
    def __repr__(self):
        return f"FunctionDef({self.name}, {self.params}, {self.body!r})"

class Call(ASTNode):
    def __init__(self, callee, args):
        self.callee = callee
        self.args = args
    def __repr__(self):
        return f"Call({self.callee!r}, {self.args!r})"

class ListLiteral(ASTNode):
    def __init__(self, elements):
        self.elements = elements
    def __repr__(self):
        return f"List({self.elements!r})"

class Return(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Return({self.value!r})"

class Use(ASTNode):
    def __init__(self, domain_name):
        self.domain_name = domain_name
    def __repr__(self):
        return f"Use({self.domain_name!r})"

# Expressions
class Number(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Number({self.value})"

class String(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"String({self.value!r})"

class Ident(ASTNode):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"Ident({self.name})"

class Binary(ASTNode):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Binary({self.op!r}, {self.left!r}, {self.right!r})"