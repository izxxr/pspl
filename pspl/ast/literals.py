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

from ast import literal_eval
from pspl.ast.base import Node

__all__ = (
    'String',
    'Integer',
    'Boolean',
)


class String(Node):
    """Represents a string literal.

    Attributes
    ----------
    value: :class:`str`
        The underlying string literal.
    """
    def __init__(self, value: str) -> None:
        self.value = value

    def eval(self) -> str:
        return literal_eval(self.value)


class Integer(Node):
    """Represents an integer literal.

    Attributes
    ----------
    value: :class:`str`
        The underlying integer literal.
    """
    def __init__(self, value: str) -> None:
        self.value = value

    def eval(self) -> int:
        return int(self.value)


class Boolean(Node):
    """Represents a boolean literal.

    Attributes
    ----------
    value: :class:`bool`
        The underlying boolean literal.
    """
    def __init__(self, value: bool) -> None:
        self.value = value

    def __pspl_bool__(self) -> bool:
        return self.value

    def __pspl_output__(self) -> str:
        return str(self.value).upper()

    def eval(self) -> bool:
        return self.value
