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

from pspl.state import State
from pspl import __version__

import click


@click.command()
@click.option('--version', help='Show PSPL version', is_flag=True, default=False)
@click.option('--strict', help='Execute with strict mode enabled', is_flag=True, default=False)
@click.argument('filename', type=str)
def main(version: bool, strict: bool, filename: str):
    """Command line interface for PSPL."""
    if version:
        return print(__version__)

    try:
        state = State.from_file(filename, strict=strict)
    except FileNotFoundError:
        print(f'error: file {filename!r} does not exist')
    else:
        state.run()


if __name__ == '__main__':
    main()
