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

from typing import Any, Callable, Dict, List, Tuple

__all__ = (
    'TOKENS',
    'IGNORED_TOKENS',
    'BUILTIN_TYPES',
    'STD_TYPES_MAP',
    'INPUT_TYPE_CASTS',
)

TOKENS: Dict[str, str] = {
    # Literals
    'LT_STRING': r'(".+")|(\'.+\')|(\'\')|("")',
    'LT_FLOAT': r'[+-]?([0-9]+([.][0-9]*)|[.][0-9]+)',
    'LT_INTEGER': r'\d+',
    'LT_BOOLEAN_TRUE': r'TRUE',
    'LT_BOOLEAN_FALSE': r'FALSE',

    # Operators
    'OP_ASSIGN': r'<-',
    'OP_SEP': r',',
    'OP_PLUS': r'\+',
    'OP_MINUS': r'-',
    'OP_DIV': r'/',
    'OP_MUL': r'\*',
    'OP_GTEQ': r'>=',
    'OP_LTEQ': r'<=',
    'OP_NEQ': r'<>',
    'OP_GT': r'>',
    'OP_LT': r'<',
    'OP_EQ': r'=',

    # Symbols
    'SYM_COLON': r':',
    'SYM_LPAREN': r'\(',
    'SYM_RPAREN': r'\)',

    # Statements
    'ST_OUTPUT': r'OUTPUT',
    'ST_DECLARE': r'DECLARE',
    'ST_CONSTANT': r'CONSTANT',
    'ST_INPUT': r'INPUT',
    'ST_THEN': r'THEN',
    'ST_IF': r'IF',
    'ST_ENDIF': r'ENDIF',
    'ST_ELSE': r'ELSE',
    'ST_FOR': r'FOR',
    'ST_ENDFOR': r'ENDFOR',
    'ST_TO': r'TO',
    'ST_STEP': r'STEP',
    'ST_WHILE': r'WHILE',
    'ST_DO': r'DO',
    'ST_ENDWHILE': r'ENDWHILE',
    'ST_REPEAT': r'REPEAT',
    'ST_UNTIL': r'UNTIL',
    'ST_PROCEDURE': r'PROCEDURE',
    'ST_ENDPROCEDURE': r'ENDPROCEDURE',
    'ST_CALL': r'CALL',

    # Identifier
    'IDENT': r'[a-zA-Z_][a-zA-Z\d_]*',
}

IGNORED_TOKENS: Tuple[str, ...] = (r'\t', r'\s+')

PRECEDENCE: Tuple[Tuple[str, List[str]], ...] = (
    ('left', ['OP_PLUS', 'OP_MINUS']),
    ('left', ['OP_MUL', 'OP_DIV']),
    ('left', ['OP_EQ', 'OP_NEQ']),
    ('left', ['OP_GT', 'OP_LT']),
    ('left', ['OP_GTEQ', 'OP_LTEQ']),
)

BUILTIN_TYPES: Dict[str, type] = {
    'STRING': str,
    'INTEGER': int,
    'FLOAT': float,
    'BOOLEAN': bool,
}

STD_TYPES_MAP: Dict[type, str] = {
    std_tp: pspl_tp
    for pspl_tp, std_tp in BUILTIN_TYPES.items()
}

def _bool_type_cast(v: str) -> bool:
    v = v.lower()
    if v in ('true', '1'):
        return True
    if v in ('false', '0'):
        return False
    raise ValueError('invalid input')

INPUT_TYPE_CASTS: Dict[str, Callable[[str], Any]] = {
    'STRING': str,
    'INTEGER': int,
    'FLOAT': float,
    'BOOLEAN': _bool_type_cast,
}
