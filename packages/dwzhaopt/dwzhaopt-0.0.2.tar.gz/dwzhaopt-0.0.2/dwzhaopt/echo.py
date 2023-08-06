#!/usr/bin/env python
# Usage: ./build.py group/project

import sys


def echo():
    if len(sys.argv) < 2:
        print 'Usage: {} msg'.format(__file__)
        sys.exit(1)
    msg = sys.argv[1]
    print msg


if __name__ == '__main__':
    echo()
