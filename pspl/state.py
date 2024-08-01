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

from typing import TYPE_CHECKING, Optional
from pspl.parser.errors import PSPLParserError
from pspl.parser import generator
from pspl.scopes import Scope
from pspl import lexer

import rply

if TYPE_CHECKING:
    from rply.lexer import Lexer
    from rply.parser import LRParser
    from rply.token import SourcePosition

__all__ = (
    'RuntimeState',
)


class _LocalScopeManager:
    def __init__(self, state: RuntimeState) -> None:
        self._state = state
        self._previous_scope: Optional[Scope] = None
        self._scope: Scope = None  # type: ignore (late binding)

    def __enter__(self) -> Scope:
        self._previous_scope = self._state.local_scope
        scope = self._state.global_scope.copy()
        self._state.local_scope = scope
        return scope

    def __exit__(self, *_) -> None:
        self._state.local_scope = self._previous_scope


class RuntimeState:
    """Internal state for PSPL runtime.

    This class acts as a state for passing important runtime data into
    parser production rules. This class is not meant to be used in normal
    cases and is initialized and used internally.

    Attributes
    ----------
    source: :class:`str`
        The source code or file name.
    file: :class:`bool`
        Whether :attr:`source` is a file name.
    """
    def __init__(
        self,
        *,
        source: str,
        file: bool = False,
    ) -> None:

        self.source = source
        self.file = file
        self.global_scope = Scope()
        self.local_scope: Optional[Scope] = None
        self._current_scope = None

    @property
    def filename(self) -> Optional[str]:
        """Optional[:class:`str`]: The name of file from which the code is being red.

        None is returned if the source is not a file and is the raw source code.
        """
        return self.source if self.file else None

    def get_current_scope(self) -> Scope:
        if self.local_scope:
            return self.local_scope

        return self.global_scope

    def create_local_scope(self) -> _LocalScopeManager:
        """Creates a new local scope.
        
        This is a context manager interface for managing local
        scope. Upon entering, creates a new local scope and preserves
        previous scope state.

        This allows proper restoring of previous local scope upon
        exiting from the created local scope.
        """
        return _LocalScopeManager(self)

    def _get_lexer(self) -> Lexer:
        lg = rply.LexerGenerator()
        for token, pattern in lexer.TOKENS.items():
            lg.add(token, pattern)
        for pattern in lexer.IGNORED_TOKENS:
            lg.ignore(pattern)
        return lg.build()

    def _get_parser(self) -> LRParser:
        gen = generator.get()
        return gen.build()

    def log_error(
        self,
        error_type: str,
        error_message: str,
        source_pos: Optional[SourcePosition] = None,
    ) -> None:
        if source_pos:
            print(f'At line {source_pos.lineno}, column {source_pos.colno}, index {source_pos.idx}:')
        print(f'{error_type}: {error_message}')

    def exec(self) -> None:
        """Start the execution process."""
        src = self.source
        if self.file:
            with open(src, 'r') as f:
                src = f.read()

        lexer = self._get_lexer()
        parser = self._get_parser()
        tokens = lexer.lex(src)

        try:
            parser.parse(tokens, state=self).eval()  # type: ignore
        except (rply.LexingError, PSPLParserError) as err:
            if isinstance(err, rply.LexingError):
                self.log_error(
                    error_type='SyntaxError',
                    error_message='Invalid syntax',
                    source_pos=err.source_pos,
                )
            else:
                self.log_error(
                    error_type=err.__class__.__name__,
                    error_message=err.message,
                    source_pos=err.source_pos,
                )
