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

"""This module contains definitions of language tokens (lexer rules)."""

from __future__ import annotations

from typing import Any, Callable, Dict, Tuple

__all__ = (
    'TOKENS',
    'IGNORED_TOKENS',
    'BUILTIN_TYPES',
    'INPUT_TYPE_CASTS',
)

TOKENS: Dict[str, str] = {
    # Literals
    'LT_STRING': r'(".+")|(\'.+\')|(\'\')|("")',
    'LT_INTEGER': r'\d+',

    # Operators
    'OP_ASSIGN': r'<-',
    'OP_SEPARATOR': r',',

    # Symbols
    'SYM_EQUAL': r'=',
    'SYM_COLON': r':',

    # Statements
    'ST_OUTPUT': r'OUTPUT',
    'ST_DECLARE': r'DECLARE',
    'ST_INPUT': r'INPUT',

    # Identifier
    'IDENT': r'[a-zA-Z_][a-zA-Z\d_]*',
}

IGNORED_TOKENS: Tuple[str, ...] = (r'\t', r'\s+')

BUILTIN_TYPES: Tuple[str, ...] = (
    'STRING',
    'INTEGER',
)

INPUT_TYPE_CASTS: Dict[str, Callable[[str], Any]] = {
    'STRING': str,
    'INTEGER': int,
}
