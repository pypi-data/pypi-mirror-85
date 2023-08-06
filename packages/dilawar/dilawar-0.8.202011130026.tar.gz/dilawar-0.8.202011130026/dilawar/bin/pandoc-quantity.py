#!/usr/bin/env python3

"""
A filter for parsing quantities expressed inside \Q or \quantity macro e.g.
\Q{1 m/s}, \quantity{9.8 m per second^2} etc.

Requires:
    - pip3 install pint
    - pip3 install panflute
"""

import re
import sys
import panflute as P
from pint import UnitRegistry
import itertools

U_ = UnitRegistry()

def _print(*args):
    print(*args, file=sys.stderr)

def searchQuantity(text):
    text = text.strip()
    qpat = re.compile(r'(\\Q|\\quantity)\{((?P<val>[.\-e+0-9]+)\s+)?(?P<uexpr>[^}]+)\}',
            re.DOTALL)
    return [x for x in qpat.finditer(text)]

def reformatElem(elem, fmt='md'):
    num, unit = elem.text.split(' ', 2)
    numF = formatEval(num, fmt)
    txt = f'{numF} {unit}'
    new = P.convert_text(txt)[0].content
    return list(new)


def formatEval(val, fmt):
    # TODO: Add a cheap test to check if val can be converted to float.
    val = val.lower()
    val = re.sub(r'(1(\.[0]*)?)e', r'e', val)
    if 'e' not in val:
        return val
    a, b = val.split('e')

    # This block return 1e-20 as e-20 to latex and 10~-20~ to markdown. Prefix
    # is removed to save space.
    if not a:
        if fmt == 'latex':
            return f'10^{b}'
        else:
            return f'10^{b}^'

    if fmt == 'latex':
        return val
    else:
        return f'{a}^{b}^'

def formatQuantity(qexpr, fmt):
    ms = searchQuantity(qexpr)
    res = []
    if not ms:
        res.append((None, qexpr, None, False))
        return res
    for m in ms:
        val, uexpr = m.groupdict().get('val', None), m.groupdict()['uexpr']
        try:
            vval = U_(f'{val} {uexpr}') if val is not None else U_[uexpr]
            res.append((m, vval, val, True))
        except Exception as e:
            P.debug(f'[WARN] Failed to parse {qexpr}. Error: {e}')
            res.append((m, qexpr, None, False))
    return res

def action_quantity(elem, doc):
    w_ = doc.format
    if isinstance(elem, P.RawInline):
        # Here we have simple replacement of whole string.
        for m, f, numval, success in formatQuantity(elem.text, w_):
            if success:
                if w_ == 'latex':
                    # If val (numeric value is None), only have unit.
                    elem.text = f'{f:Lx}' if numval else f'\({f.u:Lx}\)'
                else:
                    elem.text = f'{f:~P}'
                    return reformatElem(elem)
    elif isinstance(elem, P.Math) or isinstance(elem, P.RawBlock):
        # Here we have to replace part of the string. A bit more complicated
        # than before. Use gonna use m.span() to find the locations.
        toreplace = []
        for m, f, numval, success in formatQuantity(elem.text, w_):
            if success:
                toreplace.append((m.span(), f, numval))

        noMatch, new = [], []
        prevI, b = 0, 0
        for (a, b), f, numval in toreplace:
            noMatch.append(elem.text[prevI:a])
            if w_ == 'latex':
                # If val (numeric value is None), only have unit.
                f = f'{f:Lx}' if numval else f'\({f.u:Lx}\)'
            else:
                f = f'{f:~P}'
            new.append(f)
            prevI = b
        # rest of the text
        noMatch.append(elem.text[b:])
        if toreplace:
            newtext = ''.join(itertools.chain(noMatch, new))
            if elem.text != newtext:
                elem.text = newtext

def main(doc=None):
    P.run_filter(action_quantity, doc=doc)

if __name__ == '__main__':
    main()
