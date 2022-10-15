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

from typing import TYPE_CHECKING, Any, Optional
from pspl.ast.base import Node
from pspl import utils

if TYPE_CHECKING:
    from pspl.state import RuntimeState
    from pspl.ast.block import Block

__all__ = (
    'Statement',
    'Output',
    'Declare',
    'Assignment',
    'Input',
    'If',
    'For',
)


class Statement(Node):
    """Represents a statement.

    This is a base class for other statements.
    """


class Output(Statement):
    """Represents an output statement used for printing a value to stream.

    Attributes
    ----------
    value:
        The value to print.
    end:
        The end of line.
    """
    def __init__(self, value: Any) -> None:
        self.value = value

    def eval(self) -> None:
        if hasattr(self.value, '__pspl_output__'):
            value = self.value.__pspl_output__()
        else:
            value = utils.maybe_eval(self.value)
        print(value)


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
        pass


class Assignment(Statement):
    """Represents an assignment statement.

    Attributes
    ----------
    ident: :class:`str`
        The identifier string.
    val: :class:`str`
        The value assigned to identifier.
    """
    def __init__(self, ident: str, val: Any, is_update: bool, state: RuntimeState) -> None:
        self.ident = ident
        self.val = val
        self.is_update = is_update
        self._state = state

    def eval(self) -> None:
        pass


class Input(Statement):
    """Represents an input statement used for taking input from user.

    Attributes
    ----------
    prompt: :class:`str`
        The prompt to show.
    ident: :class:`Node`
        The identifier to store the input in.
    """
    def __init__(self, prompt: str, ident: str) -> None:
        self.prompt = prompt
        self.ident = ident

    def eval(self) -> None:
        pass


class If(Statement):
    """Represents an if conditional statement.
    
    Parameters
    ----------
    expr:
        The expression to check for.
    block: :class:`ast.Block`
        The block to execute.
    """
    def __init__(self, expr: Any, block: Block, else_block: Optional[Block] = None) -> None:
        self.expr = expr
        self.block = block
        self.else_block = else_block

    def eval(self) -> Any:
        val = True
        if hasattr(self.expr, '__pspl_bool__'):
            val = self.expr.__pspl_bool__()
        if val:
            self.block.eval()
        else:
            if self.else_block:
                self.else_block.eval()


class For(Statement):
    """Represents an for loop.

    Parameters
    ----------
    start:
        The start point.
    end:
        The end point.
    block: :class:`ast.Block`
        The block to execute.
    """
    def __init__(
        self,
        start: Any,
        end: Any,
        step: Any,
        block: Block,
        ident: str,
        keep_ident_after: bool,
        state: RuntimeState,
    ) -> None:
        self.start = start
        self.end = end
        self.step = step
        self.block = block
        self.ident = ident
        self.keep_ident_after = keep_ident_after
        self._state = state

    def eval(self) -> Any:
        step = utils.maybe_eval(self.step)
        start = utils.maybe_eval(self.start)
        end = utils.maybe_eval(self.end) + step
        ident = self.ident
        for i in range(start, end, step):
            self._state.add_def(self.ident, i)
            self.block.eval()
        if self.keep_ident_after:
            self._state.remove_def(ident)
