# What's this?

A stupid python module to log messages to stdout.

# Why?

This is meant to be used by containerized applications which have centralized log aggregation of stdout.

It is assumed that the log aggregator will attach things like the hostname, container name, etc.

This module is a bit cleaner than hacking Python's logging module to spit out JSON, or using `print(json.dumps({})`` all the time.

# How do I use it?

It supports `trace`, `debug`, `info`, `warn`, `error`, and `fatal` as levels. You can supply it with positional and keyword arguments and it will munge them into a JSON object:

```python
import jsonlogger as log

log.trace('application started')

log.debug('Something went wrong', filename=__file__)

log.info('This is a dict full of stuff', {'x': 1, 'y': 0})

log.warn("It's about to go critical", {'error': 123}, time_of_death=120000)

log.error(error_message='Oh no!')

log.fatal('the error code was', 500)
```

Will produce the output:

```json
{"timestamp": "2016-08-08T16:21:43.177680", "loglevel": "trace", "line": "application started"}
{"filename": "test.py", "timestamp": "2016-08-08T16:21:43.177777", "loglevel": "debug", "line": "Something went wrong"}
{"x": 1, "y": 0, "timestamp": "2016-08-08T16:21:43.177811", "loglevel": "info", "line": "This is a dict full of stuff"}
{"error": 123, "timestamp": "2016-08-08T16:21:43.177922", "time_of_death": 120000, "loglevel": "warn", "line": "It's about to go critical"}
{"timestamp": "2016-08-08T16:21:43.177982", "error_message": "Oh no!", "loglevel": "error"}
{"timestamp": "2016-08-08T16:21:43.178012", "loglevel": "fatal", "line": "the error code was 500"}
```

There is also a decorator for quickly logging out function calls and their arguments:

```python
import jsonlogger as log

@log.traceme
def somefunc(N):
  return N
```

Will produce:

```json
{"loglevel": "trace", "timestamp": "2016-08-08T16:25:23.402809", "call": "somefunc(1)"}
{"loglevel": "trace", "timestamp": "2016-08-08T16:25:23.402889", "call": "somefunc(100)"}
```

# Environment Variables

- `LOG_LEVEL` to suppress anything beneath the the level specified. Default: `trace`

# Run the tests

```
py.test -v
```
