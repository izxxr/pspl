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

from typing import TYPE_CHECKING, Any
from pspl.parser.errors import UnknownType, SyntaxError as PSPLSyntaxError
from pspl.parser import generator
from pspl import ast, lexer

if TYPE_CHECKING:
    from pspl.state import RuntimeState

__all__ = ()

gen = generator.get()

@gen.production('stmt_list : stmt')
@gen.production('stmt_list : stmt_list stmt')
def prod_stmt_list(state: RuntimeState, tokens: Any):
    return ast.Block(tokens)

@gen.production('stmt : ST_OUTPUT expr')
def prod_stmt_output(state: RuntimeState, tokens: Any):
    value = tokens[1]
    return ast.Output(value)

@gen.production('stmt : ST_DECLARE IDENT SYM_COLON IDENT')
def prod_stmt_declare(state: RuntimeState, tokens: Any):
    ident = tokens[1].getstr()
    tp = tokens[3].getstr()

    if not tp in lexer.BUILTIN_TYPES:
        raise UnknownType(tokens[3].getsourcepos(), tp)

    state.add_type_def(ident, tp)
    return ast.Declare(ident, tp, state)

@gen.production('stmt : ST_INPUT IDENT')
@gen.production('stmt : ST_INPUT expr OP_SEP IDENT')
def prod_stmt_input(state: RuntimeState, tokens: Any):
    maybe_ident = tokens[1]
    if isinstance(maybe_ident, ast.String):
        prompt = maybe_ident.eval()
        ident = tokens[3].getstr()
    else:
        prompt = ''
        ident = maybe_ident.getstr()

    return ast.Input(prompt, ident, state)

@gen.production('stmt : IDENT OP_ASSIGN expr')
@gen.production('assign : IDENT OP_ASSIGN expr')
def prod_assign(state: RuntimeState, tokens: Any):
    ident = tokens[0].getstr()
    val = tokens[2]

    is_update = True
    try:
        state.get_def(ident)
    except KeyError:
        is_update = False

    return ast.Assignment(ident=ident, val=val, state=state, is_update=is_update)


@gen.production('stmt : ST_IF expr ST_THEN stmt_list ST_ENDIF')
@gen.production('stmt : ST_IF expr ST_THEN stmt_list ST_ELSE stmt_list ST_ENDIF')
def prod_if(state: RuntimeState, tokens: Any):
    else_block = None
    if tokens[4].gettokentype() == 'ST_ELSE':
        else_block = tokens[5]
    return ast.If(expr=tokens[1], block=tokens[3], else_block=else_block)


@gen.production('stmt : ST_FOR assign ST_TO expr stmt_list ST_ENDFOR')
@gen.production('stmt : ST_FOR assign ST_TO expr ST_STEP expr stmt_list ST_ENDFOR')
def prod_for(state: RuntimeState, tokens: Any):
    assign = tokens[1]
    step = 1
    block = tokens[4]

    if not isinstance(block, ast.Block):
        # STEP added
        step = tokens[5]
        block = tokens[6]

    return ast.For(
        ident=assign.ident,
        start=assign.val,
        step=step,
        end=tokens[3],
        block=block,
        keep_ident_after=not assign.is_update,
        state=state,
    )


@gen.production('stmt : ST_WHILE expr ST_DO stmt_list ST_ENDWHILE')
def prod_while(state: RuntimeState, tokens: Any):
    return ast.While(
        cond=tokens[1],
        block=tokens[3],
    )
