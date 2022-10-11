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

if TYPE_CHECKING:
    from rply.token import SourcePosition

__all__ = (
    'PSPLParserError',
    'IdentifierNotDefined',
)


class PSPLParserError(Exception):
    """Base class for parser related errors.

    This exception class is used for internal error handling.

    Attributes
    ----------
    source_pos: Optional[:class:`rply.token.SourcePosition`]
        The source position of error, if available.
    message: :class:`str`
        The error message.
    """
    def __init__(self, source_pos: Optional[SourcePosition], message: str) -> None:
        self.source_pos = source_pos
        self.message = message
        super().__init__(message)


class IdentifierNotDefined(PSPLParserError):
    """Error indicating that used identifier hasn't been defined.

    Attributes
    ----------
    ident: :class:`str`
        The undefined identifier.
    """
    def __init__(self, source_pos: Optional[SourcePosition], ident: str) -> None:
        self.ident = ident
        super().__init__(source_pos, 'Identifier %r is not defined.' % ident)


class UnknownType(PSPLParserError):
    """Error indicating that type used in DECLARE statement is invalid.

    Attributes
    ----------
    tp: :class:`str`
        The invalid type.
    """
    def __init__(self, source_pos: Optional[SourcePosition], tp: str) -> None:
        self.tp = tp
        super().__init__(source_pos, 'Type %r is invalid' % tp)
