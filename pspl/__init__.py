"""
Pseudocode Styled Programming Language (PSPL)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An experimental programming language based on the CAIE A-level Computer Science (9618)
pseudocode syntax.
"""

__author__ = "Izhar Ahmad"
__version__ = "0.1.0"

from pspl.state import State as _State

__all__ = (
    'execute',
)


def execute(src: str, *, strict: bool = False) -> int:
    """Executes a source code.

    Returns 0 or -1 to indicate successful execution or unsuccessful
    execution respectively.

    Parameters
    ----------
    src: :class:`str`
        The source code to execute.
    strict: :class:`bool`
        Whether to execute with strict mode enabled.
    """
    state = _State(src, strict=strict)
    return state.run()