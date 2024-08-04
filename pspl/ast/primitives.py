# MIT License

# Copyright (c) 2022-2024 I. Ahmad

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

from typing import Generic, TypeVar, TYPE_CHECKING
from pspl.ast.datatype import DataType

if TYPE_CHECKING:
    from pspl.state import State
    from rply.token import SourcePosition

__all__ = (
    'DataType',
    'String',
)


_DT = TypeVar('_DT')


class Primitive(DataType, Generic[_DT]):
    """Base class for primitive data types.

    Subclasses of this class on their own represent a primitive
    data type but their instances represent a literal for that
    data type.
    """

    STD_DATATYPE: type[_DT]

    def __init__(self, value: _DT, state: State, source_pos: SourcePosition) -> None:
        self.value = value
        super().__init__(state=state, source_pos=source_pos)

    def __pspl_output__(self):
        return self.value


class String(Primitive[str]):
    """Represents the string data type or literal."""

    DATATYPE_NAME = 'STRING'
    STD_DATATYPE = str


PRIMITIVE_DATATYPES = {
    'STRING': String,
}
