"""
Abstract Syntax Tree (AST) node definitions for the Tombo language.
Every possible construct in Tombo has a corresponding AST node.
"""
from typing import Any, List, Optional


class ASTNode:
    """Base class for all AST nodes."""
    def __init__(self, line: int = 1, column: int = 1):
        self.line = line
        self.column = column


class Program(ASTNode):
    """Root node representing the entire program."""
    def __init__(self, statements: List[ASTNode] = None, **kwargs):
        super().__init__(**kwargs)
        self.statements = statements or []


# ============================================================================
# LITERALS & IDENTIFIERS
# ============================================================================


class NumberLiteral(ASTNode):
    """Numeric literal (int or float)."""
    def __init__(self, value: float, **kwargs):
        super().__init__(**kwargs)
        self.value = value


class StringLiteral(ASTNode):
    """String literal."""
    def __init__(self, value: str, **kwargs):
        super().__init__(**kwargs)
        self.value = value


class BooleanLiteral(ASTNode):
    """Boolean literal (true or false)."""
    def __init__(self, value: bool, **kwargs):
        super().__init__(**kwargs)
        self.value = value


class Identifier(ASTNode):
    """Variable or function name."""
    def __init__(self, name: str, **kwargs):
        super().__init__(**kwargs)
        self.name = name


class ListLiteral(ASTNode):
    """List literal: [1, 2, 3]."""
    def __init__(self, elements: List[ASTNode] = None, **kwargs):
        super().__init__(**kwargs)
        self.elements = elements or []


class DictLiteral(ASTNode):
    """Dictionary literal: {"key": "value"}."""
    def __init__(self, pairs: List[tuple] = None, **kwargs):
        super().__init__(**kwargs)
        self.pairs = pairs or []


class SetLiteral(ASTNode):
    """Set literal: {1, 2, 3}."""
    def __init__(self, elements: List[ASTNode] = None, **kwargs):
        super().__init__(**kwargs)
        self.elements = elements or []


# ============================================================================
# VARIABLES & ASSIGNMENTS
# ============================================================================


class VariableDecl(ASTNode):
    """Variable declaration: let x = 5 (immutable)."""
    def __init__(self, name: str, value: ASTNode, mutable: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.value = value
        self.mutable = mutable


class ChangeStatement(ASTNode):
    """Variable assignment: change x to 10 (mutable)."""
    def __init__(self, target: ASTNode, value: ASTNode, **kwargs):
        super().__init__(**kwargs)
        self.target = target
        self.value = value


class CompoundAssignment(ASTNode):
    """Compound assignment: x += 5, x -= 2, etc."""
    def __init__(self, target: ASTNode, operator: str, value: ASTNode, **kwargs):
        super().__init__(**kwargs)
        self.target = target
        self.operator = operator
        self.value = value


# ============================================================================
# FUNCTIONS
# ============================================================================


class FunctionDef(ASTNode):
    """Function definition: def foo(x, y) <block> end."""
    def __init__(self, name: str, params: List[str], body: List[ASTNode], docstring: str = None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.params = params
        self.body = body
        self.docstring = docstring


class ShorthandFunctionDef(ASTNode):
    """Shorthand function: defi double(x) => x * 2."""
    def __init__(self, name: str, params: List[str], body: ASTNode, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.params = params
        self.body = body


class FunctionCall(ASTNode):
    """Function call: foo(1, 2, 3)."""
    def __init__(self, callee: ASTNode, args: List[ASTNode] = None, **kwargs):
        super().__init__(**kwargs)
        self.callee = callee
        self.args = args or []


class LambdaExpr(ASTNode):
    """Lambda expression: => x * 2 (used in map, filter, etc)."""
    def __init__(self, params: List[str], body: ASTNode, **kwargs):
        super().__init__(**kwargs)
        self.params = params
        self.body = body


class ReturnStatement(ASTNode):
    """Return statement: return value."""
    def __init__(self, value: ASTNode = None, **kwargs):
        super().__init__(**kwargs)
        self.value = value


# ============================================================================
# CONTROL FLOW
# ============================================================================


class IfStatement(ASTNode):
    """If statement with optional elif and else blocks."""
    def __init__(self, condition: ASTNode, then_block: List[ASTNode], elif_blocks: List[tuple] = None, else_block: List[ASTNode] = None, **kwargs):
        super().__init__(**kwargs)
        self.condition = condition
        self.then_block = then_block
        self.elif_blocks = elif_blocks or []
        self.else_block = else_block


class WhileLoop(ASTNode):
    """While loop: while condition <block> end."""
    def __init__(self, condition: ASTNode, body: List[ASTNode], **kwargs):
        super().__init__(**kwargs)
        self.condition = condition
        self.body = body


class ForLoop(ASTNode):
    """For loop: for item in iterable <block> end."""
    def __init__(self, variable: str, iterable: ASTNode, body: List[ASTNode], **kwargs):
        super().__init__(**kwargs)
        self.variable = variable
        self.iterable = iterable
        self.body = body


class BreakStatement(ASTNode):
    """Break statement: break."""
    pass


class ContinueStatement(ASTNode):
    """Continue statement: continue."""
    pass


class MatchExpr(ASTNode):
    """Pattern matching: match value when pattern: expr end."""
    def __init__(self, value: ASTNode, cases: List[tuple] = None, default: ASTNode = None, **kwargs):
        super().__init__(**kwargs)
        self.value = value
        self.cases = cases or []
        self.default = default


# ============================================================================
# OPERATORS & EXPRESSIONS
# ============================================================================


class BinaryOp(ASTNode):
    """Binary operation: a + b, x * y, etc."""
    def __init__(self, left: ASTNode, operator: str, right: ASTNode, **kwargs):
        super().__init__(**kwargs)
        self.left = left
        self.operator = operator
        self.right = right


class UnaryOp(ASTNode):
    """Unary operation: -x, not y, ~z."""
    def __init__(self, operator: str, operand: ASTNode, **kwargs):
        super().__init__(**kwargs)
        self.operator = operator
        self.operand = operand


class LogicalOp(ASTNode):
    """Logical operation: a and b, x or y."""
    def __init__(self, left: ASTNode, operator: str, right: ASTNode, **kwargs):
        super().__init__(**kwargs)
        self.left = left
        self.operator = operator
        self.right = right


class IndexExpr(ASTNode):
    """Index/subscript access: list[0], dict["key"]."""
    def __init__(self, object: ASTNode, index: ASTNode, **kwargs):
        super().__init__(**kwargs)
        self.object = object
        self.index = index


class SliceExpr(ASTNode):
    """Slice expression: list[1:5], string[2:8]."""
    def __init__(self, object: ASTNode, start: ASTNode = None, stop: ASTNode = None, step: ASTNode = None, **kwargs):
        super().__init__(**kwargs)
        self.object = object
        self.start = start
        self.stop = stop
        self.step = step


class MemberAccess(ASTNode):
    """Member/attribute access: obj.property."""
    def __init__(self, object: ASTNode, property: str, **kwargs):
        super().__init__(**kwargs)
        self.object = object
        self.property = property


class TernaryExpr(ASTNode):
    """Ternary conditional: if condition then value1 else value2."""
    def __init__(self, condition: ASTNode, true_value: ASTNode, false_value: ASTNode, **kwargs):
        super().__init__(**kwargs)
        self.condition = condition
        self.true_value = true_value
        self.false_value = false_value


# ============================================================================
# CLASSES & OBJECTS
# ============================================================================


class ClassDef(ASTNode):
    """Class definition: class Name <body> end."""
    def __init__(self, name: str, parent: str = None, methods: List[FunctionDef] = None, body: List[ASTNode] = None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.parent = parent
        self.methods = methods or []
        self.body = body or []


class MethodCall(ASTNode):
    """Method call: obj.method(args)."""
    def __init__(self, object: ASTNode, method: str, args: List[ASTNode] = None, **kwargs):
        super().__init__(**kwargs)
        self.object = object
        self.method = method
        self.args = args or []


class SelfRef(ASTNode):
    """Reference to self: self."""
    pass


class InitMethod(ASTNode):
    """Constructor method: def init(params) <body> end."""
    def __init__(self, params: List[str], body: List[ASTNode], **kwargs):
        super().__init__(**kwargs)
        self.params = params
        self.body = body


# ============================================================================
# ERROR HANDLING
# ============================================================================


class TryExcept(ASTNode):
    """Try-catch-finally block."""
    def __init__(self, try_block: List[ASTNode], catch_blocks: List[tuple] = None, finally_block: List[ASTNode] = None, **kwargs):
        super().__init__(**kwargs)
        self.try_block = try_block
        self.catch_blocks = catch_blocks or []
        self.finally_block = finally_block


class RaiseStatement(ASTNode):
    """Raise exception: raise error_value."""
    def __init__(self, value: ASTNode, **kwargs):
        super().__init__(**kwargs)
        self.value = value


# ============================================================================
# IMPORTS & MODULES
# ============================================================================


class ImportStatement(ASTNode):
    """Import statement: import module or import module as alias."""
    def __init__(self, module: str, alias: str = None, **kwargs):
        super().__init__(**kwargs)
        self.module = module
        self.alias = alias


class FromImportStatement(ASTNode):
    """From-import statement: from module import name."""
    def __init__(self, module: str, names: List[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.module = module
        self.names = names or []


class UseStatement(ASTNode):
    """Use statement: use module."""
    def __init__(self, module: str, **kwargs):
        super().__init__(**kwargs)
        self.module = module


# ============================================================================
# ASYNC/CONCURRENT
# ============================================================================


class AsyncFunctionDef(ASTNode):
    """Async function definition: async def foo() <block> end."""
    def __init__(self, name: str, params: List[str], body: List[ASTNode], **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.params = params
        self.body = body


class AwaitExpr(ASTNode):
    """Await expression: await async_function()."""
    def __init__(self, value: ASTNode, **kwargs):
        super().__init__(**kwargs)
        self.value = value


# ============================================================================
# COMPREHENSIONS
# ============================================================================


class ListComprehension(ASTNode):
    """List comprehension: [x * 2 for x in list]."""
    def __init__(self, expr: ASTNode, variable: str, iterable: ASTNode, condition: ASTNode = None, **kwargs):
        super().__init__(**kwargs)
        self.expr = expr
        self.variable = variable
        self.iterable = iterable
        self.condition = condition


class DictComprehension(ASTNode):
    """Dict comprehension: {x: x*2 for x in list}."""
    def __init__(self, key: ASTNode, value: ASTNode, variable: str, iterable: ASTNode, condition: ASTNode = None, **kwargs):
        super().__init__(**kwargs)
        self.key = key
        self.value = value
        self.variable = variable
        self.iterable = iterable
        self.condition = condition


class SetComprehension(ASTNode):
    """Set comprehension: {x * 2 for x in list}."""
    def __init__(self, expr: ASTNode, variable: str, iterable: ASTNode, condition: ASTNode = None, **kwargs):
        super().__init__(**kwargs)
        self.expr = expr
        self.variable = variable
        self.iterable = iterable
        self.condition = condition


# ============================================================================
# MISCELLANEOUS
# ============================================================================


class PassStatement(ASTNode):
    """Pass statement: does nothing."""
    pass


class AssertStatement(ASTNode):
    """Assert statement: assert condition, message."""
    def __init__(self, condition: ASTNode, message: str = None, **kwargs):
        super().__init__(**kwargs)
        self.condition = condition
        self.message = message


class PrintStatement(ASTNode):
    """Print statement (for debugging)."""
    def __init__(self, value: ASTNode, **kwargs):
        super().__init__(**kwargs)
        self.value = value


class CommentNode(ASTNode):
    """Comments (preserved in AST for documentation)."""
    def __init__(self, text: str, **kwargs):
        super().__init__(**kwargs)
        self.text = text


# ============================================================================
# AST VISITOR PATTERN
# ============================================================================


class ASTVisitor:
    """Base class for AST traversal and transformation."""

    def visit(self, node: ASTNode) -> Any:
        """Dispatch to appropriate visit_* method."""
        method_name = f"visit_{node.__class__.__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node: ASTNode) -> Any:
        """Called if no specific visitor exists."""
        raise NotImplementedError(
            f"No visit method for {node.__class__.__name__}"
        )
