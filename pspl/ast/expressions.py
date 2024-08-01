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

from typing import TYPE_CHECKING, Any, Optional, Union
from pspl.ast.literals import Boolean
from pspl.ast.base import Node
from pspl.parser.errors import IdentifierNotDefined, TypeCheckError
from pspl import utils, lexer

if TYPE_CHECKING:
    from pspl.state import RuntimeState
    from rply.token import SourcePosition

__all__ = (
    'Ident',
    'TypeDef',
    'ArithmeticExpression',
    'Add',
    'Subtract',
    'Div',
    'Mul',
    'BooleanExpression',
    'Eq',
    'NEq',
    'Gt',
    'GtEq',
    'Lt',
    'LtEq',
)


class Ident(Node):
    """Represents an identifier"""
    def __init__(self, name: str, state: RuntimeState, pos: SourcePosition) -> None:
        self.name = name
        self.pos = pos
        self._state = state

    def eval(self) -> Any:
        scope = self._state.get_current_scope()
        try:
            return scope.get_def(self.name)
        except KeyError:
            raise IdentifierNotDefined(self.pos, self.name)


class TypeDef(Node):
    """Type definition expression."""
    def __init__(self, name: str, type: str, source_pos: SourcePosition) -> None:
        self.name = name
        self.type = type
        self.source_pos = source_pos

    def validate(self, value: Any, mod_name: Optional[str] = None, param_name: Optional[str] = None) -> None:
        utils.validate_type(
            value,
            self.type,
            mod_name=mod_name,
            param_name=param_name,
            source_pos=self.source_pos,
        )


class ArithmeticExpression(Node):
    """Base class for arithmetic operators."""
    def __init__(self, left: Any, right: Any) -> None:
        self.left = left
        self.right = right


class Add(ArithmeticExpression):
    """Represents an addition expression."""
    def eval(self) -> Union[int, str]:
        lhs = utils.maybe_eval(self.left)
        rhs = utils.maybe_eval(self.right)
        if isinstance(lhs, str) or isinstance(rhs, str):
            return str(lhs) + str(rhs)
        return lhs + rhs


class Subtract(ArithmeticExpression):
    """Represents a subtraction expression."""
    def eval(self) -> int:
        return utils.maybe_eval(self.left) - utils.maybe_eval(self.right)


class Div(ArithmeticExpression):
    """Represents a division expression."""
    def eval(self) -> int:
        return utils.maybe_eval(self.left) / utils.maybe_eval(self.right)


class Mul(ArithmeticExpression):
    """Represents a multiplication expression."""
    def eval(self) -> int:
        return utils.maybe_eval(self.left) * utils.maybe_eval(self.right)


class BooleanExpression(Node):
    """Base class for various boolean expressions."""
    def __init__(self, left: Any, right: Any) -> None:
        self.left = left
        self.right = right

    def eval(self) -> Boolean:
        ...

    def __pspl_bool__(self) -> bool:
        return self.eval().value

    def __pspl_output__(self) -> str:
        return self.eval().__pspl_output__()


class Eq(BooleanExpression):
    """Represents an equality boolean expression."""
    def eval(self) -> Boolean:
        return Boolean(utils.maybe_eval(self.left) == utils.maybe_eval(self.right))


class NEq(BooleanExpression):
    """Represents an inequality boolean expression."""
    def eval(self) -> Boolean:
        return Boolean(utils.maybe_eval(self.left) != utils.maybe_eval(self.right))


class Gt(BooleanExpression):
    """Represents a greater than boolean expression."""
    def eval(self) -> Boolean:
        return Boolean(utils.maybe_eval(self.left) > utils.maybe_eval(self.right))


class GtEq(BooleanExpression):
    """Represents a greater than or equality boolean expression."""
    def eval(self) -> Boolean:
        return Boolean(utils.maybe_eval(self.left) >= utils.maybe_eval(self.right))


class Lt(BooleanExpression):
    """Represents a less than boolean expression."""
    def eval(self) -> Boolean:
        return Boolean(utils.maybe_eval(self.left) < utils.maybe_eval(self.right))


class LtEq(BooleanExpression):
    """Represents an less than or equality boolean expression."""
    def eval(self) -> Boolean:
        return Boolean(utils.maybe_eval(self.left) <= utils.maybe_eval(self.right))
