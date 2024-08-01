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
from pspl.parser import generator
from pspl import ast, lexer

if TYPE_CHECKING:
    from pspl.state import RuntimeState

__all__ = ()

gen = generator.get()

@gen.production('header_param_list : header_param')
@gen.production('header_param_list : header_param OP_SEP header_param_list')
def prod_header_param_list(state: RuntimeState, tokens: Any):
    return ast.HeaderParamList(tokens)

@gen.production('header_param : typedef')
def prod_header_param(state: RuntimeState, tokens: Any):
    typedef = tokens[0]
    return ast.HeaderParam(typedef)

@gen.production('stmt : ST_PROCEDURE IDENT stmt_list ST_ENDPROCEDURE')
@gen.production('stmt : ST_PROCEDURE IDENT SYM_LPAREN header_param_list SYM_RPAREN stmt_list ST_ENDPROCEDURE')
def prod_procedure(state: RuntimeState, tokens: Any):
    block = tokens[2]
    params = []

    if not isinstance(block, ast.Block):
        # params list given
        block = tokens[5]
        params = tokens[3].params

    return ast.Procedure(name=tokens[1].getstr(), block=block, params=params, state=state)

@gen.production('call_param_list : call_param')
@gen.production('call_param_list : call_param OP_SEP call_param_list')
def prod_call_param_list(state: RuntimeState, tokens: Any):
    return ast.CallParamList(tokens)

@gen.production('call_param : expr')
def prod_call_param(state: RuntimeState, tokens: Any):
    return ast.CallParam(value=tokens[0])

@gen.production('stmt : ST_CALL IDENT')
@gen.production('stmt : ST_CALL IDENT SYM_LPAREN call_param_list SYM_RPAREN')
def prod_call(state: RuntimeState, tokens: Any):
    if len(tokens) > 2:
        # params passed
        params = tokens[3].values
    else:
        params = []

    return ast.Call(target=tokens[1].getstr(), params=params, state=state, source_pos=tokens[0].getsourcepos())
