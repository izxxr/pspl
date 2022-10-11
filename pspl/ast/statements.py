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
from pspl.ast.base import Node

if TYPE_CHECKING:
    from pspl.state import RuntimeState

__all__ = (
    'Statement',
    'Output',
    'Declare',
    'Assignment',
)


class Statement(Node):
    """Represents a statement.

    This is a base class for other statements.
    """


class Output(Statement):
    """Represents an output statement used for printing a value to stream.

    Attributes
    ----------
    value: :class:`Node`
        The value to print.
    """
    def __init__(self, value: Node) -> None:
        self.value = value

    def eval(self) -> None:
        print(self.value.eval())


class Declare(Statement):
    """Represents a declare statement used for declaring type of an identifier.

    Attributes
    ----------
    ident: :class:`str`
        The identifier string.
    tp: :class:`str`
        The type of identifier.
    """
    def __init__(self, ident: str, tp: str, state: RuntimeState) -> None:
        self.ident = ident
        self.tp = tp
        self._state = state

    def eval(self) -> None:
        self._state.add_type_def(self.ident, self.tp)


class Assignment(Statement):
    """Represents an assignment statement.

    Attributes
    ----------
    ident: :class:`str`
        The identifier string.
    val: :class:`str`
        The value assigned to identifier.
    """
    def __init__(self, ident: str, val: Any, state: RuntimeState) -> None:
        self.ident = ident
        self.val = val
        self._state = state

    def eval(self) -> None:
        pass
