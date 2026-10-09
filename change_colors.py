#!/usr/bin/env python3
"""Change Nano color scheme from B&W to color"""

__all__ = ['main']

import re
import sys
from pathlib import Path

commentColor = 'blue'
keywordColor = 'brightyellow'
warningColor = 'green'

swaps = {
    'brightblack': commentColor,
    'brightwhite': keywordColor,
    'black,white': 'black,' + warningColor,
    ',white': ',' + warningColor,
}

allPattern = 'i?color (' + '|'.join(n for n in swaps) + ') '

def cerr(msg: str) -> None:
    print(msg, file = sys.stderr, flush = True)

def main(args: list[str] | None = None) -> int:
    if args is None:
        args = sys.argv[1:]
    if args:
        cerr('Error: Script does not take arguments.')
        return 1
    dir = Path(__file__).parent
    for path in dir.glob('*.nanorc'):
        with path.open() as inFile:
            lines = inFile.read().splitlines()
        if not lines:
            cerr('Warning: File "%s" is empty.'%(path))
            continue
        numLines = len(lines)
        for i in range(numLines):
            m = re.match(allPattern, lines[i])
            if not m:
                continue
            color = m.group(1)
            color = swaps[color]
            head = lines[i][0:m.start(1)]
            tail = lines[i][m.end(1):]
            lines[i] = head + color + tail
        with path.open('w') as outFile:
            outFile.write('\n'.join(lines))
    return 0

if __name__ == '__main__':
    sys.exit(main())
