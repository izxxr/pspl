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

from typing import Any, Dict, Optional
from pspl.state import RuntimeState

import threading

__all__ = (
    'PSPLRunner',
)


class PSPLRunner:
    """The PSPL runner.

    This class consumes the source code, prepares it for execution and
    executes it. This class is a high level interface to many pre-execution
    steps such as lexical analysis and parser setup.

    For general information regarding the usage of this class, see the getting
    started page.
    """
    def __init__(self) -> None:
        self._state: Optional[RuntimeState] = None
        self._lock = threading.Lock()

    def _get_state(self, *args: Any, **kwargs: Any) -> RuntimeState:
        return RuntimeState(*args, **kwargs)

    def _setup(self, source: str, file: bool = False) -> RuntimeState:
        self._lock.acquire()
        self._state = self._get_state(source=source, file=file)
        return self._state

    def _cleanup(self) -> None:
        self._state = None
        self._lock.release()

    def run(
        self,
        source: str,
        /,
        *,
        file: bool = False,
        wait: bool = True,
    ) -> None:
        """Runs the code from provided source.

        The first parameter can either be the PSPL source code or
        the file name to execute. If it is a file, ``file`` keyword
        argument must be set to True.

        This method is thread safe as such if this method is called
        when the runner is already acquired in another thread or task,
        it will block until runner finishes previous task. ``wait`` can
        be passed as ``False`` to raise a :exc:`RuntimeError` instead
        of waiting.

        Parameters
        ----------
        source: :class:`str`
            The source file name or code.
        file: :class:`bool`
            Whether the passed parameter is a file name. Defaults to False.
        wait: :class:`bool`
            Whether to wait until previous task is finished. When False, raises
            a :exc:`RuntimeError` if the runner is already acquired. Defaults to
            True.
        """
        if self._lock.locked() and not wait:
            raise RuntimeError('Runner is already acquired')

        try:
            state = self._setup(source=source, file=file)
            state.exec()
        finally:
            self._cleanup()
