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
from rply.token import Token
from pspl.parser.errors import PSPLParserError
from pspl.parser import generator
from pspl import ast

if TYPE_CHECKING:
    from pspl.state import RuntimeState

__all__ = ()

gen = generator.get()

@gen.production('program : stmt_list')
def prod_program(state: RuntimeState, tokens: Any):
    return ast.Block(tokens)

@gen.error
def generator_error_handler(state: RuntimeState, token: Token):
    tp = token.gettokentype()
    inner = token.getstr()
    pos = token.getsourcepos()
    
    if tp == '$end':
        msg = 'Unexpected end of program'
    else:
        msg = f'Unexpected token {inner} ({tp})'

    raise PSPLParserError(source_pos=pos, message=msg)
