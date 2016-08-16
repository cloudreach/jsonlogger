'''
A stupid zero-config module for logging JSON objects to stdout & stderr.
For use by containerised applications using a centralised log aggregator.
'''

import os
from json import dumps, JSONEncoder
from datetime import datetime
from sys import stdout

LOG_LEVELS = {
    'trace': 10,
    'debug': 20,
    'info': 30,
    'warning': 40,
    'warn': 40,
    'error': 50,
    'fatal': 60
}

LOG_LEVEL = LOG_LEVELS[os.getenv('LOG_LEVEL', 'trace').lower()]


class LogEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (list, tuple, str, dict,
                            int, float, bool, type(None))):
            return JSONEncoder.default(self, obj)
        return str(format(repr(obj)))


def traceme(fn):
    '''
    use this to decorate functions for quick and dirty logging of calls
    '''
    def traced(*args, **kwargs):
        trace(call='{}({})'.format(
            fn.__name__,
            ', '.join(list(map(str, args)) +
                      list(map(lambda i: '{}={}'.format(*i),
                               sorted(kwargs.items()))))))
        return fn(*args, **kwargs)
    return traced


def log(levelname, *args, **kwargs):
    levelname = levelname.lower()
    assert levelname in LOG_LEVELS.keys(), 'Unsupported log level'

    if LOG_LEVELS[levelname] < LOG_LEVEL:
        return None

    output = {
        'loglevel': levelname,
        'timestamp': datetime.now().isoformat()
    }

    for arg in args:
        if isinstance(arg, dict):
            output = {**output, **arg}
        else:
            if 'line' in output:
                output['line'] += ' ' + str(arg)
            else:
                output['line'] = str(arg)

    output = dumps({**output, **kwargs}, cls=LogEncoder) + "\n"
    stdout.write(output)


def __level_alias(level):
    globals()[level] = lambda *a, **kw: log(level, *a, **kw)

for level in LOG_LEVELS.keys():
    __level_alias(level)
