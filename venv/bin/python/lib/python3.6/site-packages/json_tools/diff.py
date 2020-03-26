#!/usr/bin/env python
#-*- coding:utf-8 -*-


from __future__ import print_function
import six

from .loader import load


def diff(local, other):
    """ Calculates the difference between two JSON documents.
        All resulting changes are relative to @a local.

        Returns diff formatted in form of extended JSON Patch (see IETF draft).
    """

    def _recursive_diff(l, r, res, path='/'):
        if type(l) != type(r):
            res.append({
                'replace': path,
                'value': r,
                'details': 'type',
                'prev': l
            })
            return

        delim = '/' if path != '/' else ''

        if isinstance(l, dict):
            for k, v in six.iteritems(l):
                new_path = delim.join([path, k])
                if k not in r:
                    res.append({'remove': new_path, 'prev': v})
                else:
                    _recursive_diff(v, r[k], res, new_path)
            for k, v in six.iteritems(r):
                if k in l:
                    continue
                res.append({
                    'add': delim.join([path, k]),
                    'value': v
                })
        elif isinstance(l, list):
            ll = len(l)
            lr = len(r)
            if ll > lr:
                for i, item in enumerate(l[lr:], start=lr):
                    res.append({
                        'remove': delim.join([path, str(i)]),
                        'prev': item,
                        'details': 'array-item'
                    })
            elif lr > ll:
                for i, item in enumerate(r[ll:], start=ll):
                    res.append({
                        'add': delim.join([path, str(i)]),
                        'value': item,
                        'details': 'array-item'
                    })
            minl = min(ll, lr)
            if minl > 0:
                for i, item in enumerate(l[:minl]):
                    _recursive_diff(item, r[i], res, delim.join([path, str(i)]))
        else:  # both items are atomic
            if l != r:
                res.append({
                    'replace': path,
                    'value': r,
                    'prev': l
                })

    result = []
    _recursive_diff(local, other, result)
    return result


def print_reduced(diff, pretty=True):
    """ Prints JSON diff in reduced format (similar to plain diffs).
    """

    for action in diff:
        if 'add' in action:
            print('+', action['add'], action['value'])
        elif 'remove' in action:
            print('-', action['remove'], action['prev'])


if __name__ == '__main__':
    from sys import argv, stderr
    from optparse import OptionParser
    from json_tools.printer import print_json

    parser = OptionParser()
    parser.add_option('-p', '--pretty', dest='pretty', action='store_true',
                      default=False)
    parser.add_option('-j', '--json', dest='json_format', action='store_true',
                      default=False)

    (options, args) = parser.parse_args()

    if len(args) < 2:
        print('Usage:', argv[0], '[options] local_file other_file', file=stderr)
        exit(-1)

    try:
        with open(args[0]) as f:
            local = load(f)
    except IOError:
        print('Local not found', file=stderr)
        exit(-1)
    except KeyError:
        print('Path to file not specified', file=stderr)
        exit(-1)

    try:
        with open(args[1]) as f:
            other = load(f)
    except IOError:
        print('Other not found', file=stderr)
        exit(-1)
    except KeyError:
        print('Path to other file not specified', file=stderr)
        exit(-1)

    res = diff(local, other)
    if not options.json_format:
        print_reduced(res, options.pretty)
    else:
        print_json(res, "/", options.pretty)
