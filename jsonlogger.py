'''
A stupid zero-config module for logging JSON objects to stdout & stderr.
For use by containerised applications using a centralised log aggregator.
'''

import json
from sys import stdout

LOG_LEVELS = ['trace', 'debug', 'info', 'warning', 'warn', 'error', 'fatal']


def traceme(fn):
    '''
    use this to decorate functions for quick and dirty logging of calls
    '''
    def traced(*args, **kwargs):
        trace(traced_call='{}({})'.format(
            fn.__name__,
            ', '.join(list(map(str, args)) +
                      list(map(lambda i: '{}={}'.format(*i),
                               sorted(kwargs.items()))))))
        return fn(*args, **kwargs)
    return traced


def log(levelname, *args, **kwargs):
    levelname = levelname.lower()
    assert levelname in LOG_LEVELS, 'Unsupported log level'

    output = {'loglevel': levelname}

    for arg in args:
        if isinstance(arg, dict):
            output = {**output, **arg}
        else:
            if 'line' in output:
                output['line'] += ' ' + str(arg)
            else:
                output['line'] = str(arg)

    output = json.dumps({**output, **kwargs}) + "\n"
    stdout.write(output)


def __level_alias(level):
    globals()[level] = lambda *a, **kw: log(level, *a, **kw)

for level in LOG_LEVELS:
    __level_alias(level)
