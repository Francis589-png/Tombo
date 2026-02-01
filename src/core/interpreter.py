"""
A minimal interpreter/evaluator for Tombo core AST nodes.
Supports `let`, `change`, `if`, and `defi` (shorthand functions) and simple expressions.
"""
from src.core.ast import Module, Let, Change, If, Defi, Number, String, Ident, Binary, FunctionDef, Call, ListLiteral, Return
from src.core.ast import Use
# Also import the parser AST node classes so the interpreter can accept parser output
from ast.ast_nodes import (
    Program as AstProgram,
    VariableDecl as AstVariableDecl,
    ChangeStatement as AstChangeStatement,
    IfStatement as AstIfStatement,
    ShorthandFunctionDef as AstShorthandFunctionDef,
    FunctionDef as AstFunctionDef,
    NumberLiteral as AstNumberLiteral,
    StringLiteral as AstStringLiteral,
    Identifier as AstIdentifier,
    BinaryOp as AstBinaryOp,
    FunctionCall as AstFunctionCall,
    ListLiteral as AstListLiteral,
    ReturnStatement as AstReturnStatement,
    UseStatement as AstUseStatement,
)

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value


class Environment:
    def __init__(self, parent=None):
        self.store = {}
        self.parent = parent

    def get(self, name):
        if name in self.store:
            return self.store[name]
        if self.parent:
            return self.parent.get(name)
        return None

    def set(self, name, value):
        # set in current scope
        self.store[name] = value

    def assign(self, name, value):
        # assign to nearest scope that has the name; otherwise error
        if name in self.store:
            self.store[name] = value
            return True
        if self.parent:
            return self.parent.assign(name, value)
        return False

    def new_child(self):
        return Environment(parent=self)


class Function:
    def __init__(self, params, body, env: Environment):
        self.params = params
        self.body = body
        self.env = env

    def call(self, args, interp):
        if len(args) != len(self.params):
            raise RuntimeError('Argument count mismatch')
        # create child environment for function execution
        local_env = self.env.new_child()
        for name, val in zip(self.params, args):
            local_env.set(name, val)
        try:
            if isinstance(self.body, list):
                for stmt in self.body:
                    interp.eval_node(stmt, local_env)
                return None
            else:
                return interp.eval_node(self.body, local_env)
        except ReturnException as re:
            return re.value

class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        # register core builtins
        self.global_env.set('print', print)
        self.global_env.set('len', len)
        self.global_env.set('range', lambda *args: list(__import__('builtins').range(*args)))
        
        # Load core libraries
        self._load_stdlib()

    def _load_stdlib(self):
        """Load standard library modules into global environment."""
        try:
            # Load core library
            from src.lib.core import register as core_register
            core_register(self.global_env)
        except ImportError:
            pass  # tolerate missing library
        
        try:
            # Load math library
            from src.lib.math import register as math_register
            math_register(self.global_env)
        except ImportError:
            pass
        
        try:
            # Load string library
            from src.lib.string import register as string_register
            string_register(self.global_env)
        except ImportError:
            pass
        
        try:
            # Load collections library
            from src.lib.collections import register as collections_register
            collections_register(self.global_env)
        except ImportError:
            pass
        
        try:
            # Load I/O library
            from src.lib.io import register as io_register
            io_register(self.global_env)
        except ImportError:
            pass
        
        try:
            # Load time library
            from src.lib.time import register as time_register
            time_register(self.global_env)
        except ImportError:
            pass
        
        # Phase 2 - Utility Libraries
        try:
            from src.lib.regex import register as regex_register
            regex_register(self.global_env)
        except ImportError:
            pass
        
        try:
            from src.lib.json import register as json_register
            json_register(self.global_env)
        except ImportError:
            pass
        
        try:
            from src.lib.xml import register as xml_register
            xml_register(self.global_env)
        except ImportError:
            pass
        
        try:
            from src.lib.crypto import register as crypto_register
            crypto_register(self.global_env)
        except ImportError:
            pass
        
        try:
            from src.lib.os import register as os_register
            os_register(self.global_env)
        except ImportError:
            pass
        
        try:
            from src.lib.sys import register as sys_register
            sys_register(self.global_env)
        except ImportError:
            pass
        
        try:
            from src.lib.iter import register as iter_register
            iter_register(self.global_env)
        except ImportError:
            pass
        
        try:
            from src.lib.functools import register as functools_register
            functools_register(self.global_env)
        except ImportError:
            pass
        
        try:
            from src.lib.types import register as types_register
            types_register(self.global_env)
        except ImportError:
            pass
        
        # Phase 3 - Domain Libraries (auto-load)
        domain_libs = [
            'web', 'database', 'gui', 'ml', 'ai', 'game', 'mobile', 'scientific',
            'blockchain', 'iot', 'quantum', 'cad', 'bio', 'robotics', 'finance',
            'audio', 'video', 'image', 'network', 'concurrency',
            'vision', 'sensors', 'env_sensors', 'bio_sensors'  # Phase 4
        ]
        
        for domain in domain_libs:
            try:
                mod = __import__(f'src.domains.{domain}', fromlist=['register'])
                if hasattr(mod, 'register'):
                    mod.register(self.global_env)
            except ImportError:
                pass  # skip missing domain

    def eval(self, node):
        # Accept either core Module or parser Program AST roots
        if isinstance(node, Module):
            return self.eval_module(node)
        if isinstance(node, AstProgram):
            result = None
            for stmt in node.statements:
                if stmt is None:
                    continue
                result = self.eval_node(stmt, self.global_env)
            return result
        raise RuntimeError('Root must be Module')

    def eval_module(self, module: Module):
        result = None
        for stmt in module.body:
            if stmt is None:
                continue
            result = self.eval_node(stmt, self.global_env)
        return result

    def eval_node(self, node, env: Environment):
        # Handle dict-wrapped expression statements from parser
        if isinstance(node, dict):
            if node.get('type') == 'expr_stmt':
                return self.eval_node(node['expr'], env)

        # -------------------- parser AST (src.ast) handling --------------------
        if isinstance(node, AstVariableDecl):
            val = self.eval_node(node.value, env) if node.value is not None else None
            env.set(node.name, val)
            return val

        if isinstance(node, AstChangeStatement):
            # target is typically an Identifier node
            target = node.target
            if isinstance(target, AstIdentifier):
                name = target.name
            else:
                # fallback: try to evaluate target then error (assign only supports simple identifiers)
                raise RuntimeError('Unsupported assignment target')
            val = self.eval_node(node.value, env)
            ok = env.assign(name, val)
            if not ok:
                raise RuntimeError(f'Undefined variable {name}')
            return val

        if isinstance(node, AstIfStatement):
            cond = self.eval_node(node.condition, env)
            if cond:
                for s in node.then_block:
                    self.eval_node(s, env)
            return None

        if isinstance(node, (AstShorthandFunctionDef, AstFunctionDef)):
            params = node.params
            body = node.body
            fn = Function(params, body, env)
            env.set(node.name, fn)
            return fn

        if isinstance(node, AstUseStatement):
            return None

        if isinstance(node, AstNumberLiteral):
            return node.value

        if isinstance(node, AstStringLiteral):
            v = node.value
            if len(v) >= 2 and ((v[0] == '"' and v[-1] == '"') or (v[0] == "'" and v[-1] == "'")):
                return v[1:-1]
            return v

        if isinstance(node, AstIdentifier):
            val = env.get(node.name)
            if val is not None:
                return val
            raise RuntimeError(f'Undefined identifier {node.name}')

        if isinstance(node, AstFunctionCall):
            callee = node.callee
            if isinstance(callee, AstIdentifier):
                fn = env.get(callee.name)
            else:
                fn = self.eval_node(callee, env)
            if fn is None:
                raise RuntimeError('Call to undefined function')
            args = [self.eval_node(a, env) for a in node.args]
            if isinstance(fn, Function):
                return fn.call(args, self)
            if callable(fn):
                return fn(*args)
            raise RuntimeError('Object is not callable')

        if isinstance(node, AstListLiteral):
            return [self.eval_node(e, env) for e in node.elements]

        if isinstance(node, AstReturnStatement):
            val = self.eval_node(node.value, env) if node.value is not None else None
            raise ReturnException(val)

        if isinstance(node, AstBinaryOp):
            left = self.eval_node(node.left, env)
            right = self.eval_node(node.right, env)
            op = node.operator
            if op == '+': return left + right
            if op == '-': return left - right
            if op == '*': return left * right
            if op == '/': return left / right
            if op == '>': return left > right
            if op == '<': return left < right
            if op == '==': return left == right
            raise RuntimeError(f'Unsupported op {op}')

        # -------------------- core AST (src.core.ast) handling --------------------
        if isinstance(node, Let):
            val = self.eval_node(node.value, env) if node.value is not None else None
            env.set(node.name, val)
            return val
        if isinstance(node, Change):
            val = self.eval_node(node.value, env)
            ok = env.assign(node.name, val)
            if not ok:
                raise RuntimeError(f'Undefined variable {node.name}')
            return val
        if isinstance(node, If):
            cond = self.eval_node(node.cond, env)
            if cond:
                for s in node.body:
                    self.eval_node(s, env)
            return None
        if isinstance(node, Defi):
            fn = Function(node.params, node.body, env)
            env.set(node.name, fn)
            return fn
        if isinstance(node, Use):
            # load domain via DomainManager if available
            from src.core.domain import DomainManager
            dm = DomainManager.get()
            if dm is None:
                # no domain manager registered — no-op
                return None
            domain = dm.load_domain(node.domain_name)
            if domain and hasattr(domain, 'register'):
                domain.register(env)
            return None
        if isinstance(node, FunctionDef):
            fn = Function(node.params, node.body, env)
            env.set(node.name, fn)
            return fn
        if isinstance(node, Number):
            return node.value
        if isinstance(node, String):
            # strip surrounding quotes if present
            v = node.value
            if len(v) >= 2 and ((v[0] == '"' and v[-1] == '"') or (v[0] == "'" and v[-1] == "'")):
                return v[1:-1]
            return v
        if isinstance(node, Ident):
            val = env.get(node.name)
            if val is not None:
                return val
            raise RuntimeError(f'Undefined identifier {node.name}')
        if isinstance(node, Call):
            callee = node.callee
            if isinstance(callee, Ident):
                fn = env.get(callee.name)
            else:
                fn = self.eval_node(callee, env)
            if fn is None:
                raise RuntimeError('Call to undefined function')
            args = [self.eval_node(a, env) for a in node.args]
            if isinstance(fn, Function):
                return fn.call(args, self)
            if callable(fn):
                return fn(*args)
            raise RuntimeError('Object is not callable')
        if isinstance(node, ListLiteral):
            return [self.eval_node(e, env) for e in node.elements]
        if isinstance(node, Return):
            val = self.eval_node(node.value, env) if node.value is not None else None
            raise ReturnException(val)
        if isinstance(node, Binary):
            left = self.eval_node(node.left, env)
            right = self.eval_node(node.right, env)
            op = node.op
            if op == '+': return left + right
            if op == '-': return left - right
            if op == '*': return left * right
            if op == '/': return left / right
            if op == '>': return left > right
            if op == '<': return left < right
            if op == '==': return left == right
            raise RuntimeError(f'Unsupported op {op}')
        # fallback
        return None

if __name__ == '__main__':
    # quick smoke test
    from src.core.lexer import Lexer
    from src.core.parser import Parser
    code = '''
let x = 5
if x > 0
    change x to 10
    defi add(a, b) => a + b
end
'''
    lex = Lexer(code)
    toks = lex.tokenize()
    p = Parser(toks)
    ast = p.parse()
    interp = Interpreter()
    interp.eval(ast)
    print('env:', interp.global_env)
    # call function
    fn = interp.global_env.get('add')
    if fn:
        print('add(2,3)=', fn.call([2,3], interp))
