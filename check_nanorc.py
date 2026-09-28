#!/usr/bin/env python3

import re
import sys

pattern0 = '^syntax "(default|[A-Za-z_0-9-]+" ".+)"$'
pattern1 = '^color ,white "\\\\s\\+\\$"$'

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
            num = 0
            for line in inFile:
                num += 1
                line = line.rstrip('\n')
                if num == 1 and not re.match(pattern0, line):
                    failed = True
                    cerr('%s:%i'%(path, num))
                lastLine = line
            if not re.match(pattern1, lastLine):
                failed = True
                cerr('%s:%i'%(path, num))
    return int(failed)

if __name__ == '__main__':
    if sys.platform != 'win32':
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    sys.exit(main())
