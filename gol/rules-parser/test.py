#!/usr/bin/env python3

import json
import sys
from rules import rules


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: test.py rules.txt\n')
        sys.exit(1)

    with open(sys.argv[1]) as f:
        print(json.dumps(rules(f.read(), 'rgb').repr(), indent=4))
