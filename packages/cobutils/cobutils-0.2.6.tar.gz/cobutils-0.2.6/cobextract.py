#!/usr/bin/env python

import sys

from cobutils.extract import main

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)
