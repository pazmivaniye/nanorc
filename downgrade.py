#!/usr/bin/env python3
"""Downgrade NanoRC syntax to support older versions"""

__all__ = ['main']

import re
import sys
from pathlib import Path

defaultLine = 'color white,black ".*"'
gsPattern = '(un)?set guidestripe'
lightPattern = '(i?color) (bold,)?light'
normalPattern = '(i?color) normal,normal '

def getContents(path: Path) -> list[str]:
    try:
        with path.open() as inFile:
            lines = inFile.read().splitlines()
    except Exception as e:
        raise type(e)('Failed to read from file: %s'%(e))
    if not lines:
        raise ValueError('File "%s" is empty.'%(path))
    return lines

def dumpContents(path: Path, lines: list[str]) -> None:
    try:
        with path.open('w') as outFile:
            for line in lines:
                outFile.write(line)
                outFile.write('\n')
    except Exception as e:
        raise type(e)('Failed to write to file: %s'%(e))

def downgradeMainFile(path: Path) -> None:
    lines = getContents(path)
    numLines = len(lines)
    for i in range(numLines):
        if re.match(gsPattern, lines[i]):
            lines[i] = '#' + lines[i]
    dumpContents(path, lines)

def downgradeSyntaxFile(path: Path) -> None:
    lines = getContents(path)
    if defaultLine not in lines:
        lines.insert(1, defaultLine)
    numLines = len(lines)
    for i in range(numLines):
        m = re.match(lightPattern, lines[i])
        if m:
            lines[i] = m.group(1) + ' bright' + lines[i][m.end():]
            continue
        m = re.match(normalPattern, lines[i])
        if m:
            lines[i] = m.group(1) + ' white,black ' + lines[i][m.end():]
    dumpContents(path, lines)

def cerr(msg: str) -> None:
    print(msg, file = sys.stderr, flush = True)

def main(args: list[str] | None = None) -> int:
    if args is None:
        args = sys.argv[1:]
    if args:
        cerr('ValueError: Script does not take arguments.')
        return 1
    dir = Path(__file__).parent
    path = dir / 'nanorc'
    try:
        downgradeMainFile(path)
    except Exception as e:
        cerr('%s: Failed to downgrade "%s": %s'%(type(e).__name__, path, e))
        return 1
    for path in dir.glob('*.nanorc'):
        try:
            downgradeSyntaxFile(path)
        except Exception as e:
            cerr('%s: Failed to downgrade "%s": %s'%(type(e).__name__, path, e))
            return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
