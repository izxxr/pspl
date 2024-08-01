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

from typing import Dict, Any, Optional, TYPE_CHECKING
from pspl.parser.errors import IdentifierAlreadyDefined
from pspl import lexer, utils

if TYPE_CHECKING:
    from rply.token import SourcePosition

__all__ = (
    "Scope",
)


class Scope:
    """Represents a scope.

    A scope defines the context in which certain names are defined and accessible.
    """
    __slots__ = (
        'type_defs',
        'defs',
        'constant_defs',
    )

    def __init__(self) -> None:
        self.type_defs: Dict[str, Any] = {}
        self.defs: Dict[str, Any] = {}
        self.constant_defs: Dict[str, Any] = {}

    def add_type_def(self, ident: str, tp: Any) -> None:
        self.type_defs[ident] = tp

    def get_type_def(self, ident: str) -> Any:
        return self.type_defs[ident]

    def remove_type_def(self, ident: str) -> Any:
        return self.type_defs.pop(ident)

    def add_def(
        self,
        ident: str,
        val: Any,
        *,
        constant: bool = False,
        source_pos: Optional[SourcePosition] = None,
        type_check: bool = True,
    ) -> None:
        
        if type_check:
            try:
                tp = self.get_type_def(ident)
            except KeyError:
                # infer type
                tp = lexer.STD_TYPES_MAP[type(val)]
                self.add_type_def(ident, tp)
            else:
                utils.validate_type(val, tp, source_pos=source_pos)

        if ident in self.constant_defs:
            raise IdentifierAlreadyDefined(source_pos, ident)
        if constant:
            self.constant_defs[ident] = val
        else:
            self.defs[ident] = val

    def get_def(self, ident: str) -> Any:
        if ident in self.constant_defs:
            return self.constant_defs[ident]
        return self.defs[ident]

    def remove_def(self, ident: str) -> Any:
        return self.defs.pop(ident)

    def copy(self) -> Scope:
        """Creates a copy of this scope."""
        copy = Scope()
        copy.type_defs = self.type_defs.copy()
        copy.defs = self.defs.copy()
        copy.constant_defs = self.constant_defs.copy()
        return copy
