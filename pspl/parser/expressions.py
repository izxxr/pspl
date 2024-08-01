# MIT License

# Copyright (c) 2022 I. Ahmad

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Type
from pspl.parser import generator
from pspl.parser.errors import UnknownType
from pspl import ast, lexer

if TYPE_CHECKING:
    from pspl.state import RuntimeState

__all__ = ()

gen = generator.get()

ARITHMETIC_EXPRESSION_NODES: Dict[str, Type[ast.ArithmeticExpression]] = {
    'OP_PLUS': ast.Add,
    'OP_MINUS': ast.Subtract,
    'OP_MUL': ast.Mul,
    'OP_DIV': ast.Div,
}

BOOLEAN_EXPRESSION_NODES: Dict[str, Type[ast.BooleanExpression]] = {
    'OP_EQ': ast.Eq,
    'OP_NEQ': ast.NEq,
    'OP_GT': ast.Gt,
    'OP_LT': ast.Lt,
    'OP_GTEQ': ast.GtEq,
    'OP_LTEQ': ast.LtEq,
}

@gen.production('typedef : IDENT SYM_COLON IDENT')
def prod_typedef(state: RuntimeState, tokens: Any):
    ident = tokens[0].getstr()
    tp = tokens[2].getstr()

    if not tp in lexer.BUILTIN_TYPES:
        raise UnknownType(tokens[3].getsourcepos(), tp)

    return ast.TypeDef(ident, tp, tokens[0].getsourcepos())

@gen.production('expr : LT_STRING')
@gen.production('expr : LT_INTEGER')
@gen.production('expr : LT_FLOAT')
@gen.production('expr : LT_BOOLEAN_TRUE')
@gen.production('expr : LT_BOOLEAN_FALSE')
@gen.production('expr : IDENT')
def prod_expr(state: RuntimeState, tokens: Any):
    tok = tokens[0].gettokentype()
    val = tokens[0].getstr()

    if tok == 'LT_STRING':
        return ast.String(val)
    if tok == 'LT_INTEGER':
        return ast.Integer(val)
    if tok == 'LT_FLOAT':
        return ast.Float(val)
    if tok == 'LT_BOOLEAN_TRUE':
        return ast.Boolean(True)
    if tok == 'LT_BOOLEAN_FALSE':
        return ast.Boolean(False)
    if tok == 'IDENT':
        return ast.Ident(name=val, state=state, pos=tokens[0].getsourcepos())

    assert False

@gen.production('expr : SYM_LPAREN expr SYM_RPAREN')
def prod_expr_parens(state: RuntimeState, tokens: Any):
    return tokens[1]

@gen.production('expr : OP_MINUS expr')
@gen.production('expr : OP_PLUS expr')
def prod_expr_sign(state: RuntimeState, tokens: Any):
    operation = tokens[0].gettokentype()
    if operation == 'OP_MINUS':
        return ast.Subtract(0, tokens[1])
    if operation == 'OP_PLUS':
        return ast.Add(0, tokens[1])

@gen.production('expr : expr OP_PLUS expr')
@gen.production('expr : expr OP_MINUS expr')
@gen.production('expr : expr OP_MUL expr')
@gen.production('expr : expr OP_DIV expr')
def prod_expr_am_operations(state: RuntimeState, tokens: Any):
    op = tokens[1].gettokentype()
    left, right = tokens[0], tokens[2]
    return ARITHMETIC_EXPRESSION_NODES[op](left, right)

@gen.production('expr : expr OP_EQ expr')
@gen.production('expr : expr OP_NEQ expr')
@gen.production('expr : expr OP_GT expr')
@gen.production('expr : expr OP_LT expr')
@gen.production('expr : expr OP_GTEQ expr')
@gen.production('expr : expr OP_LTEQ expr')
def prod_expr_bool(state: RuntimeState, tokens: Any):
    op = tokens[1].gettokentype()
    left, right = tokens[0], tokens[2]
    return BOOLEAN_EXPRESSION_NODES[op](left, right)
