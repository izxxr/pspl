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

"""Helpers for manipulating internal :class:`rply.ParserGenerator` instance."""

from __future__ import annotations

from pspl import lexer
from rply import ParserGenerator

__all__ = (
    "get",
    "reset",
)

_gen: ParserGenerator | None = None


def get() -> ParserGenerator:
    """Returns the :class:`rply.ParserGenerator` object.

    This function caches the generator instance on first call and
    returns the cached value on subsequent calls.
    """
    global _gen
    if _gen:
        return _gen

    _gen = ParserGenerator(lexer.TOKENS, precedence=lexer.PRECEDENCE)
    return _gen


def reset() -> None:
    """Resets the generator cache.

    After calling this method, :func:`get_generator` constructs a new
    generator instance rather than returning a cached one.
    """
    global _gen
    _gen = None
