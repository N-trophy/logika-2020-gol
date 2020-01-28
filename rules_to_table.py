#!/usr/bin/env python3

import sys


CLASSES = {
    'r': 'red',
    'g': 'green',
    'b': 'blue',
    'k': 'gray',
}


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write('Usage: rules_to_table.py rules.txt\n')
        sys.exit(1)

    print('<table class="selector_table">')

    with open(sys.argv[1]) as f:
        for line in f:
            out = '<tr>'
            for c in line.strip():
                out += f'<td class="{CLASSES[c]}">{c}</td>'
            out += '</tr>'
            print(out)

    print('</table>')
