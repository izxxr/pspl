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

from typing import TYPE_CHECKING, List, Any
from pspl.ast.base import Node
from pspl.ast.statements import Statement
from pspl.parser.errors import IdentifierNotDefined, ParamsError
from pspl.utils import maybe_eval

if TYPE_CHECKING:
    from pspl.state import RuntimeState
    from pspl.ast.block import Block
    from pspl.ast.expressions import TypeDef
    from rply.token import SourcePosition

__all__ = (
    'HeaderParam',
    'HeaderParamList',
    'CallParam',
    'CallParamList',
    'Module',
    'Procedure',
    'Call',
)


class HeaderParam(Node):
    """Represents a parameter in a module's header."""

    def __init__(self, typedef: TypeDef) -> None:
        self.name = typedef.name
        self.type = typedef.type
        self.typedef = typedef


class HeaderParamList(Node):
    """Represents the list of parameters in function's headers."""

    def __init__(self, params: List[HeaderParam]) -> None:
        self.params = []

        for p in params:
            if isinstance(p, HeaderParamList):
                self.params.extend(p.params)
            elif isinstance(p, HeaderParam):
                self.params.append(p)


class CallParam(Node):
    """Represents a parameter passed while calling a module."""

    def __init__(self, value: Any) -> None:
        self.value = value


class CallParamList(Node):
    """Represents the list of parameters passed while calling a module."""

    def __init__(self, values: List[CallParam]) -> None:
        self.values = []

        for v in values:
            if isinstance(v, CallParamList):
                self.values.extend(v.values)
            elif isinstance(v, CallParam):
                self.values.append(v)


class Module(Node):
    """Represents a module.

    This is a base class for other module types.
    """


class Procedure(Module):
    """Represents a procedure.

    A procedure is similar to functions but does not return anything.
    """

    def __init__(self, name: str, block: Block, params: List[Any], state: RuntimeState) -> None:
        self.name = name
        self.block = block
        self.state = state
        self.params = params
        self.state.get_current_scope().add_def(name, self)

    def eval(self) -> None:
        return


class Call(Statement):
    """Represents a CALL statement.

    CALL is used to call a procedure.
    """

    def __init__(self, target: str, params: List[Any], state: RuntimeState, source_pos: SourcePosition) -> None:
        self.target = target
        self.state = state
        self.source_pos = source_pos
        self.params = params

    def eval(self) -> None:
        scope = self.state.get_current_scope()
        try:
            procedure = scope.get_def(self.target)
        except KeyError:
            raise IdentifierNotDefined(self.source_pos, self.target)

        params = self.params
        proc_params = procedure.params
        given = len(params)
        required = len(proc_params)

        if given != required:
            raise ParamsError(procedure.name, given, required, self.source_pos)

        with self.state.create_local_scope() as lscope:
            for proc_param, call_param in zip(proc_params, self.params):
                value = maybe_eval(call_param.value)
                name = proc_param.name
                proc_param.typedef.validate(value, mod_name=procedure.name, param_name=name)
                lscope.add_def(name, value)

            procedure.block.eval()
