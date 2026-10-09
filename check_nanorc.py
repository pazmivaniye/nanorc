#!/usr/bin/env python3
"""Check NanoRC files for consistency"""

__all__ = ['main']

import re
import sys

firstLine = 'syntax "(default|([A-Za-z_0-9-]+)" ".+)"'
secondLine = 'header ".+"'
thirdLine = 'comment ".*"'
fourthLine = 'color white,black ".*"'
charLine = 'color black,white "[^ -~]"'
bodyLine = 'i?color ((bright)?(white|black))?(,(white|black))? (".*"|start=".*'\
    '" end=".*")'
commentLine = 'i?color brightblack ".*"'
lastLine = 'color ,white "\\s+$"'
validName = '[a-z][a-z0-9]*'

def cout(msg: str) -> None:
    print(msg, flush = True)

def cerr(msg: str) -> None:
    print(msg, file = sys.stderr, flush = True)

def main(args: list[str] | None = None) -> int:
    if args is None:
        args = sys.argv[1:]
    if not args:
        return 0
    if args[0] in ['-v', '--verbose']:
        verbose = True
        paths = args[1:]
        cout('Checking %i NanoRC files'%(len(paths)))
    else:
        verbose = False
        paths = args
    failed = False
    for path in paths:
        if verbose:
            cout('Checking "%s"'%(path))
        with open(path) as inFile:
            lines = inFile.read().splitlines()
            numLines = len(lines)
            if numLines < 4:
                failed = True
                cerr('%s:%i: File is too short.'%(path, numLines))
                continue
            m = re.fullmatch(firstLine, lines[0])
            if m and len(m.groups()) == 2:
                if m.groups()[1] is not None:
                    name = m.groups()[1]
                    if not re.match(validName, name):
                        failed = True
                        cerr('%s:%i: Invalid syntax name.'%(path, 1))
                        continue
                    if path != name + '.nanorc':
                        failed = True
                        cerr('%s:%i: Filename and syntax name do not match.'%(
                            path, 1))
                        continue
                elif path != 'default.nanorc':
                    failed = True
                    cerr('%s:%i: File for syntax "default" should be named "def'
                        'ault.nanorc".'%(path, 1))
                    continue
            else:
                failed = True
                cerr('%s:%i: Pattern mismatch.'%(path, 1))
                continue
            headerLen = 1
            for i in range(1, min(4, numLines)):
                if lines[i] == fourthLine:
                    headerLen = i + 1
                    break
            if headerLen < 2:
                failed = True
                cerr('%s:%i: Missing required header lines.'%(path, headerLen))
                continue
            if headerLen == 4:
                if not re.fullmatch(secondLine, lines[1]):
                    failed = True
                    cerr('%s:%i: Pattern mismatch.'%(path, 2))
                    continue
                if not re.fullmatch(thirdLine, lines[2]):
                    failed = True
                    cerr('%s:%i: Pattern mismatch.'%(path, 3))
                    continue
            if headerLen == 3:
                if not re.fullmatch(secondLine, lines[1]) and not re.fullmatch(
                        thirdLine, lines[1]):
                    failed = True
                    cerr('%s:%i: Pattern mismatch.'%(path, 2))
                    continue
            if charLine not in lines:
                failed = True
                cerr('%s:%i: Missing non-ASCII character highlighting rule.'%(
                    path, numLines))
                continue
            charRule = lines.index(charLine)
            for i in range(headerLen, numLines - 1):
                if not lines[i] or lines[i][0] == '#':
                    continue
                if not re.fullmatch(bodyLine, lines[i]):
                    failed = True
                    cerr('%s:%i: Pattern mismatch.'%(path, i + 1))
                    break
                if re.fullmatch(commentLine, lines[i]) and i < charRule:
                    failed = True
                    cerr('%s:%i: Non-ASCII character highlighting rule comes af'
                        'ter first comment highlighting rule.'%(path, i + 1))
                    break
            if failed:
                continue
            if lines[-1] != lastLine:
                failed = True
                cerr('%s:%i: Pattern mismatch.'%(path, numLines))
    return int(failed)

if __name__ == '__main__':
    if sys.platform != 'win32':
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    sys.exit(main())
