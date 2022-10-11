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
from pspl import ast

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
    return ast.Output(tokens[1])

@gen.production('stmt : ST_DECLARE IDENT SYM_COLON IDENT')
def prod_stmt_declare(state: RuntimeState, tokens: Any):
    # TODO: type validation here
    return ast.Declare(tokens[1].getstr(), tokens[3].getstr(), state)

@gen.production('stmt : IDENT OP_ASSIGN expr')
@gen.production('stmt : IDENT SYM_EQUAL expr')
def prod_assign(state: RuntimeState, tokens: Any):
    ident = tokens[0].getstr()
    val = tokens[2]
    state.add_def(ident, val)
    return ast.Assignment(ident, val, state)
