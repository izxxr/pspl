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
    'UnknownType',
    'TypeCheckError',
    'SyntaxError',
    'ParamsError',
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


class TypeCheckError(PSPLParserError):
    """Error indicating 

    Attributes
    ----------
    given: :class:`str`
        The given (invalid) type.
    expected: :class:`str`
        The expected (valid) type.
    mod_name: Optional[:class:`str`]
        If error originated from a module, its name.
    param_name: Optional[:class:`str`]
        If error originated from a module, parameter name that caused the error.
    """
    def __init__(
            self,
            given: str,
            expected: str,
            source_pos: Optional[SourcePosition],
            mod_name: Optional[str] = None,
            param_name: Optional[str] = None,
    ) -> None:

        self.given = given
        self.expected = expected

        if mod_name is None:
            msg = f'Expected type {expected}; received {given} instead'
        else:
            # assume param_name always present if mod_name present
            msg = f'In parameter {param_name} in {mod_name}, expected type {expected}; received {given} instead'

        super().__init__(source_pos, msg)


class IdentifierAlreadyDefined(PSPLParserError):
    """Error indicating that an identifier has already been defined as a constant.

    Attributes
    ----------
    ident: :class:`str`
        The identifier attempted to be redefined.
    """
    def __init__(self, source_pos: Optional[SourcePosition], ident: str) -> None:
        self.ident = ident
        super().__init__(source_pos, "Identifier %r has already been defined as constant" % ident)


class SyntaxError(PSPLParserError):
    """Error indicating a syntax error."""


class ParamsError(PSPLParserError):
    """Error indicating invalid parameters passed to module.

    Attributes
    ----------
    mod_name: :class:`str`
        The name of module that raised the error.
    given: :class:`int`
        Number of arguments given.
    required:
        Number of arguments required.
    """

    def __init__(self, mod_name: str, given: int, required: int, source_pos: Optional[SourcePosition]) -> None:
        self.mod_name = mod_name
        self.given = given
        self.required = required

        super().__init__(source_pos, f"Module {mod_name} takes {required} parameters; {given} given.")
