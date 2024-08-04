# MIT License

# Copyright (c) 2022-2024 I. Ahmad

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

from typing import TYPE_CHECKING
from pspl.parser import generator as parsergen
from pspl import lexer

import rply

if TYPE_CHECKING:
    from rply.lexer import Lexer
    from rply.parser import LRParser
    from rply.token import SourcePosition

__all__ = (
    'State',
)


class State:
    """The PSPL state.

    This class holds stateful data used by the PSPL parser. An instance
    of this class is passed to parser's production rules by RPLY in the
    `state` parameter.
    """

    def __init__(self, src: str, *, strict: bool = False) -> None:
        self.src = src
        self.strict = strict

    def _build_lexer(self) -> Lexer:
        lg = rply.LexerGenerator()

        for token, pattern in lexer.TOKENS.items():
            lg.add(token, pattern)

        for pattern in lexer.IGNORED_TOKENS:
            lg.ignore(pattern)

        return lg.build()

    def _build_parser(self) -> LRParser:
        gen = parsergen.get()
        return gen.build()

    def log_error(self, error_type: str, error_message: str, pos: SourcePosition) -> None:
        print(f'Error at line {pos.lineno}, col {pos.colno}:')
        print(f'{error_type}: {error_message}')

    def run(self) -> int:
        """Execute the source code.

        Returns an exit code indicating the type of exit. Namely,
        if 0 is returned, the code executed successfully. If an
        error occured, -1 is returned.
        """
        lexer = self._build_lexer()
        parser = self._build_parser()
        tokens = lexer.lex(self.src)

        try:
            parser.parse(tokens, state=self).eval()  # type: ignore
        except rply.LexingError as err:
            self.log_error(
                error_type='SyntaxError',
                error_message='Invalid syntax',
                pos=err.source_pos,
            )
            return -1
        else:
            return 0

    @classmethod
    def from_file(cls, filename: str, *, strict: bool = False) -> State:
        """Creates a state instance from source code read from the given filename."""
        with open(filename, 'r') as f:
            src = f.read()

        return cls(src, strict=strict)
