#!/usr/bin/env python
from __future__ import print_function

__version__ = '0.1.0'
__all__ = ['samplitude']

try:
    import matplotlib.pyplot as plt
except ImportError as err:
    print('Warning: matplotlib unavailable, plotting disabled')
    plt = None

import itertools

from ._samplitude import _Samplitude
from ._generators import (sinegenerator, cosinegenerator, tangenerator)
from ._utils import _generator, _set

s8e = _Samplitude()

s8e.generator('sin', sinegenerator, infinite=True)
s8e.generator('cos', cosinegenerator, infinite=True)
s8e.generator('tan', tangenerator, infinite=True)


class _SizedIterator(object):
    def __init__(self, elements, n):
        if not hasattr(elements, '__next__'):
            self._elements = iter(elements)
        else:
            self._elements = elements
        self._n = n
        self._i = 0

    def toJSON(self):
        return list(self)

    def __len__(self):
        return self._n

    def __iter__(self):
        return self

    def __next__(self):
        if self._i == self._n:
            raise StopIteration
        v = next(self._elements)
        self._i += 1
        return v


@s8e.generator('chi2')
def _chi2(df, loc=0, scale=1):
    try:
        import scipy.stats
    except ImportError:
        print('Missing library scipy.stats, `chi2` not supported')
        return

    chi2 = scipy.stats.chi2.rvs
    df, loc, scale = [float(x) for x in [df, loc, scale]]
    while True:
        yield chi2(df=df, loc=loc, scale=scale)


@s8e.generator('pert')
def _pert(low, peak, high, g=4.0):
    # From github.com/tisimst/mcerp (pypi:mcerp)
    try:
        import scipy.stats as ss
    except ImportError:
        print('Missing library scipy.stats, `pert` not supported')
        return

    a, b, c = [float(x) for x in [low, peak, high]]
    assert a <= b <= c, 'PERT "peak" must be greater than "low" and less than "high"'
    assert g >= 0, 'PERT "g" must be non-negative'
    mu = (a + g * b + c) / (g + 2)
    if mu == b:
        a1 = a2 = 3.0
    else:
        a1 = ((mu - a) * (2 * b - a - c)) / ((b - mu) * (c - a))
        a2 = a1 * (c - mu) / (mu - a)

    low = a
    high = c
    beta = ss.beta(a1, a2, loc=a, scale=high - low)
    while True:
        yield beta.rvs()


@s8e.generator('count', infinite=True)
def _count(start=0, step=1):
    return itertools.count(start=start, step=step)


def __listnstrip(gen):
    return list(map(str.strip, gen))


@s8e.generator('csv')
def _csv_generator(fname, col=None, sep=None):
    try:
        import pandas as pd
    except ImportError:
        print('Warning: pandas unavailable, csv disabled')
        return []
    if sep is None:
        df = pd.read_csv(fname)
    else:
        df = pd.read_csv(fname, sep=sep)
    if col is None:
        return df[df.columns[0]]
    if isinstance(col, int):
        return df[df.columns[col]]
    return df[col]


@s8e.generator('stdin')
def _stdin_generator():
    import sys
    return __listnstrip(sys.stdin)


@s8e.generator('words')
def _words_generator():
    import os
    if os.getenv('DICTIONARY') is not None:
        fname = os.getenv('DICTIONARY')
        if os.path.isfile(fname):
            with open(fname, 'r') as fwords:
                return __listnstrip(fwords.readlines())
    files = ('/usr/share/dict/words', '/usr/dict/words')
    for fname in files:
        if os.path.isfile(fname):
            with open(fname, 'r') as fwords:
                return __listnstrip(fwords.readlines())
    import sys
    sys.stderr.write('Warning: words list not found.\n'
                     'Set environment variable DICTIONARY to dict file.\n'
                     'Or simply pipe to samplitude and use `stdin()`.\n')
    return []


@s8e.generator('file')
def _file_generator(fname):
    import os
    if not os.path.isfile(fname):
        raise IOError('No such file {}'.format(fname))
    with open(fname, 'r') as f:
        temp = f.read().splitlines()
    for line in temp:
        yield line


@s8e.filter('fft')
def _fft(gen):
    import numpy as np

    try:
        import scipy.fftpack
    except ImportError:
        print('Missing library scipy.fftpack, `fft` not supported')
        return

    gen = np.array(gen)
    N = len(gen)
    f = scipy.fftpack.fft(gen)
    return list(f[:N // 2])


@s8e.filter('dropna')
def _dropna(gen):
    for x in gen:
        if x != x:
            continue
        yield x


@s8e.filter('pairs')
def _pairwise(gen):
    _sentinel = object()
    prev = _sentinel
    for elt in gen:
        if prev is _sentinel:
            prev = elt
        else:
            yield prev, elt
            prev = _sentinel
    raise StopIteration


@s8e.filter('round')
def _rounder(gen, r=3):
    for x in gen:
        yield round(x, r)


@s8e.filter('int')
def _inter(gen):
    for x in gen:
        yield int(x)


@s8e.filter('zip')
def _(gen1, gen2):
    for x, y in zip(gen1, gen2):
        yield x, y


@s8e.filter('scale')
def _scale(gen, s=1):
    if isinstance(s, (int, float, complex)):
        for x in gen:
            yield x * s
    else:
        for x, y in zip(gen, s):
            yield x * y


@s8e.filter('shift')
def _shift(gen, s=0):
    if isinstance(s, (int, float, complex)):
        for x in gen:
            yield x + s
    else:
        for x, y in zip(gen, s):
            yield x + y


@s8e.filter('sample', limiter=True)
def _sample(dist, n):
    return _SizedIterator(dist, n)


@s8e.filter('head', limiter=True)
def _head(dist, n=5):
    return _SizedIterator(dist, n)


@s8e.filter('swap')
def _swap(gen):
    if isinstance(gen, dict):
        for k in sorted(gen.keys()):
            yield (gen[k], k)
        return
    for elt in gen:
        if isinstance(elt, tuple):
            eltp = list(elt)
            eltp.reverse()
            yield tuple(eltp)
        else:
            elt.reverse()
            yield elt


@s8e.filter('elt_join')
def _elt_join(gen, sep=' '):
    for x in gen:
        yield sep.join(map(str, x))


@s8e.filter('elt_cut')
def _elt_cut(gen, fields=None, delimiter=None, s=False):
    if delimiter is None:
        delimiter = '\t'

    def _cut(elt):
        elt = str(elt)
        if delimiter not in elt:
            return () if s else (elt,)
        tokens = elt.split(delimiter)
        return tokens[fields]

    for x in gen:
        yield _cut(x)


@s8e.filter('gobble')
def _gobble(*args, **kwargs):
    return []


@s8e.filter('len')
def _len(gen):
    try:
        return len(gen)
    except TypeError:
        return len(list(gen))


@s8e.filter('drop')
def _drop(dist, n):
    i = 0
    for elt in dist:
        if i < n:
            i += 1
            continue
        yield elt


@s8e.filter('sort')
def _sort(gen, reverse=False):
    if isinstance(gen, (int, float, complex)):
        return (gen,)
    if isinstance(gen, dict):
        return ((k, gen[k])
                for k in sorted(gen.keys(), reverse=reverse))
    gen = list(gen)
    return tuple(sorted(gen, reverse=reverse))


@s8e.filter('counter')
def _counter(dist):
    from collections import Counter
    return Counter(dist)


@s8e.filter('product')
def _product(A, B, combiner=None):
    if combiner is None or combiner == 'tuple':
        comb = lambda x, y: tuple((x, y))
    elif combiner in ('add', '+'):
        comb = lambda x, y: x + y
    elif combiner in ('minus', 'sub', '-'):
        comb = lambda x, y: x - y
    elif combiner in ('mul', '*'):
        comb = lambda x, y: x * y
    elif combiner in ('div', '/'):
        comb = lambda x, y: x / y
    elif combiner in ('idiv', '//'):
        comb = lambda x, y: x // y
    elif combiner == 'set':
        comb = lambda x, y: _set((x, y))
    elif combiner.startswith('concat'):
        comb = lambda x, y: '{}{}'.format(x, y)

    return tuple(comb(a, b)
                 for a in A for b in B)


@s8e.filter('permutations')
def _permutations(gen, r=None):
    for perm in itertools.permutations(gen, r=r):
        yield perm


@s8e.filter('combinations')
def _combinations(gen, r):
    for comb in itertools.combinations(gen, r=r):
        yield comb


@s8e.filter('hist')
def _hist(vals, bins=None):
    if plt is None:
        return vals
    vals = list(vals)  # consuming generator
    if bins is None:
        try:
            plt.hist(vals, bins='auto')
        except:
            plt.hist(vals)
    else:
        plt.hist(vals, bins=bins)
    plt.show()
    return vals


@s8e.filter('line')
def _line(vals):
    if plt is None:
        return vals
    vals = list(vals)  # consuming generator
    plt.plot(vals)
    plt.show()
    return vals


@s8e.filter('scatter')
def _scatter(vals):
    if plt is None:
        return vals
    if isinstance(vals, dict):
        vals = vals.items()
    x, y = zip(*list(vals))
    plt.scatter(x, y)
    plt.show()
    return vals


@s8e.filter('heat')
def _(vals, res=256, color='viridis'):
    import numpy as np
    if plt is None:
        return vals
    if isinstance(vals, dict):
        vals = vals.items()
    x, y = zip(*list(vals))
    heatmap, _, _ = np.histogram2d(x, y, bins=res)
    plt.imshow(heatmap, cmap=color)
    plt.show()
    return vals


@s8e.filter('cli')
def _cli(vals):
    if isinstance(vals, dict):
        return '\n'.join(['{} {}'.format(k, vals[k]) for k in vals])
    elif isinstance(vals, (int, float, complex)):
        vals = [vals]
    return '\n'.join(map(str, vals))


@s8e.filter('json')
def _json(vals):
    import json
    finite = lambda x : hasattr(vals, 'finite') or not hasattr(vals, 'is_infinite')

    if isinstance(vals, _SizedIterator):
        return json.dumps(vals.toJSON())

    if hasattr(vals, '__next__'):
        if finite(vals):
            return json.dumps(list(vals))
        else:
            return '<infinite generator>'

    return json.dumps(vals)


def __verify_no_jinja_braces(tmpl):
    tmpl = str(tmpl).strip()
    if tmpl.startswith('{{'):
        raise UserWarning('Do not prefix with "{{".')
    if tmpl.endswith('}}'):
        raise UserWarning('Do not postfix with "}}".')
    return tmpl


def _check_for_infinite_generators(template):
    ast = s8e.jenv.parse(template)
    has_infinite_generator = False
    has_limiter = False

    node = ast.body[0].nodes[0]
    #  The AST provide nodes back to front. If an infinite generator
    #  is found before a limiter, the expression will never complete.
    while node is not None:
        if hasattr(node, 'name'):
            if node.name in ast.environment.filters:
                filter = ast.environment.filters[node.name]
            elif node.name in ast.environment.globals:
                filter = ast.environment.globals[node.name]
            else:
                raise ValueError("no filter named '%s'" % node.name)

            if hasattr(filter, 'is_infinite') and filter.is_infinite:
                has_infinite_generator = True
            if hasattr(filter, 'is_limiter') and filter.is_limiter:
                if has_infinite_generator:
                    break
                else:
                    has_limiter = True

        node = node.node if hasattr(node, 'node') else None

    if has_infinite_generator and not has_limiter:
        raise ValueError('the expression has an infinite generator')


def samplitude(tmpl, seed=None, filters=None):
    if tmpl.strip() == '':
        raise ValueError('Empty template')

    tmpl = '{{ %s }}' % __verify_no_jinja_braces(tmpl)

    if seed:
        s8e.set_seed(seed)
    if filters:
        s8e.add_filters(filters)

    _check_for_infinite_generators(tmpl)

    template = s8e.jenv.from_string(tmpl)

    res = template.render()
    if res is None:
        return

    if res.startswith('<samplitude._SizedIterator'):
        tmpl = tmpl[3:-3].split('|')
        return '"{}"'.format(' | '.join(map(str.strip, tmpl)))
    return res


def _exit_with_usage(argv):
    msg = """\
{0} {1}

Usage:    {0} "cmd" [seed]
Example:  {0} "normal(100, 5) | sample(1000) | cli"
          {0} "normal(100, 5) | sample(1000) | cli" 1349
          {0} "normal(100, 5) | sample(1000) | hist | gobble"
          {0} "['win', 'draw', 'loss'] | choice | sample(6) | sort | cli"
""".format('samplitude', __version__)
    exit(msg)


def main():
    from sys import argv
    if not 1 < len(argv) < 4:
        _exit_with_usage(argv)

    template = argv[1]
    seed = None

    if len(argv) == 3:
        try:
            seed = int(argv[2])
        except Exception:
            _exit_with_usage(argv)

    res = samplitude(template, seed=seed)
    if res:
        print(res)


if __name__ == '__main__':
    main()
