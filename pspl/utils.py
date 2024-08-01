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

"""Internal utility helper functions and classes."""

from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING
from pspl.parser.errors import TypeCheckError
from pspl import lexer

if TYPE_CHECKING:
    from rply.token import SourcePosition

__all__ = (
    'MISSING',
    'maybe_eval',
)


class _Missing:
    """The type for utils.MISSING.

    See documentation of MISSING sentinel.
    """
    def __bool__(self) -> bool:
        return False

    def __eq__(self, __o: object) -> bool:
        return False


MISSING: Any = _Missing()
"""A type safe sentinel used where None may be ambiguous."""


def maybe_eval(val: Any) -> Any:
    if hasattr(val, 'eval'):
        return val.eval()
    return val


def validate_type(
        value: Any,
        tp: str,
        mod_name: Optional[str] = None,
        param_name: Optional[str] = None,
        source_pos: Optional[SourcePosition] = None,
) -> None:
    expected = lexer.BUILTIN_TYPES[tp]

    if not isinstance(value, expected):
        raise TypeCheckError(
            lexer.STD_TYPES_MAP[type(value)],
            tp,
            source_pos=source_pos,
            mod_name=mod_name,
            param_name=param_name
        )
