# What's this?

A stupid python module to log messages to stdout.

# Why?

This is meant to be used by containerised applications which have centralised log aggregation of stdout.

It is assumed that the log aggregator will attach things like the current timestamp, hostname, container name, etc.

This module is a bit cleaner than hacking Python's logging module to spit out JSON, or using print(json.dumps({}) all the time.

# How do I use it?

It supports trace, debug, info, warn, error, and fatal as levels. You can supply it with positional and keyword arguments and it will munge them into a JSON object:

```python
import jsonlogger as log

log.trace('application started')

log.debug('Something went wrong', filename=__file__)

log.info('This is a dict full of stuff', {'x': 1, 'y': 0})

log.warn("It's about to go critical", {'error': 123}, time_of_death=120000)

log.error(error_message='Oh no!')

log.fatal('the error code was', 500)
```

There is also a decorator for quickly logging out function calls and their arguments:

```
import jsonlogger as log

@log.traceme
def somefunc(N):
  return N
```

# Run the tests

```
py.test -v
```
