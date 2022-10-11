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

from typing import Any
from pspl.ast.base import Node
from pspl import utils

__all__ = (
    'ArithmeticExpression',
    'Add',
    'Subtract',
    'Div',
    'Mul',
)


class ArithmeticExpression(Node):
    """Base class for arithmetic operators."""
    def __init__(self, left: Any, right: Any) -> None:
        self.left = left
        self.right = right


class Add(ArithmeticExpression):
    """Represents an addition expression."""
    def eval(self) -> Any:
        return utils.maybe_eval(self.left) + utils.maybe_eval(self.right)


class Subtract(ArithmeticExpression):
    """Represents a subtraction expression."""
    def eval(self) -> Any:
        return utils.maybe_eval(self.left) - utils.maybe_eval(self.right)


class Div(ArithmeticExpression):
    """Represents a division expression."""
    def eval(self) -> Any:
        return utils.maybe_eval(self.left) / utils.maybe_eval(self.right)


class Mul(ArithmeticExpression):
    """Represents a multiplication expression."""
    def eval(self) -> Any:
        return utils.maybe_eval(self.left) * utils.maybe_eval(self.right)
