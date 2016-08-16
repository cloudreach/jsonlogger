import sys
import json

import pytest
from freezegun import freeze_time

import jsonlogger


@pytest.mark.parametrize('level', [
    'fatal',
    'error',
    'warning',
    'warn',
    'info',
    'debug',
    'trace'
])
def test_levels(mocker, level):
    mocker.patch('jsonlogger.log')
    getattr(jsonlogger, level)('this is a test')
    jsonlogger.log.assert_called_with(level, 'this is a test')
    mocker.resetall()


@freeze_time('2016-01-01 00:00:00')
@pytest.mark.parametrize('args,kwargs,expected_output', (
    (('this is a test with a line',),
     {},
     {'loglevel': 'debug',
      'line': 'this is a test with a line',
      'timestamp': '2016-01-01T00:00:00'}),

    (('this is a test with a line', 100, 'test', [3.0]),
     {},
     {'loglevel': 'debug',
      'line': 'this is a test with a line 100 test [3.0]',
      'timestamp': '2016-01-01T00:00:00'}),

    (({'line': 'this is a test with a dict'},),
     {},
     {'loglevel': 'debug',
      'line': 'this is a test with a dict',
      'timestamp': '2016-01-01T00:00:00'}),

    ([],
     {'line': 'this is a test with kwargs'},
     {'loglevel': 'debug',
      'line': 'this is a test with kwargs',
      'timestamp': '2016-01-01T00:00:00'}),

    (('this is a test with a line + kwargs',),
     {'trace': 123},
     {'loglevel': 'debug',
      'line': 'this is a test with a line + kwargs',
      'trace': 123,
      'timestamp': '2016-01-01T00:00:00'}),

    (('this is a test with a line + dict', {'trace': 123}),
     {},
     {'loglevel': 'debug',
      'line': 'this is a test with a line + dict',
      'trace': 123,
      'timestamp': '2016-01-01T00:00:00'}),

    (('this is a test with a line + dict + kwargs', {'trace': 123}),
     {'error': {'message': 'something bad'}},
     {'loglevel': 'debug',
      'line': 'this is a test with a line + dict + kwargs',
      'trace': 123,
      'timestamp': '2016-01-01T00:00:00',
      'error': {
        'message': 'something bad'
      }}),
))
def test_log(mocker, args, kwargs, expected_output):
    mocker.patch('sys.stdout.write')
    jsonlogger.log('debug', *args, **kwargs)
    assert json.loads(sys.stdout.write.call_args[0][0]) == expected_output
    mocker.resetall()


@freeze_time('2016-01-01 00:00:00')
@pytest.mark.parametrize('args,kwargs,expected_output', (
    (('this is a test',),
     {'exception': Exception('something went wrong')},
     {'loglevel': 'debug',
      'line': 'this is a test',
      'exception': "Exception('something went wrong',)",
      'timestamp': '2016-01-01T00:00:00'}),
    (('this is a test',),
     {'set': set([1, 2, 3])},
     {'loglevel': 'debug',
      'line': 'this is a test',
      'set': '{1, 2, 3}',
      'timestamp': '2016-01-01T00:00:00'}),
))
def test_log_encoder(mocker, args, kwargs, expected_output):
    mocker.patch('sys.stdout.write')
    jsonlogger.log('debug', *args, **kwargs)
    assert json.loads(sys.stdout.write.call_args[0][0]) == expected_output
    mocker.resetall()


def test_unsupported_level():
    with pytest.raises(AssertionError):
        jsonlogger.log('glorp', 'this is a test')


@freeze_time('2016-01-01 00:00:00')
def test_function_trace(mocker):
    mocker.patch('sys.stdout.write')

    @jsonlogger.traceme
    def tracetest(*args, **kwargs):
        return True

    tracetest(1, '2', [3.0], keyword=True, x={})

    assert json.loads(sys.stdout.write.call_args[0][0]) == {
        'call': 'tracetest(1, 2, [3.0], keyword=True, x={})',
        'loglevel': 'trace',
        'timestamp': '2016-01-01T00:00:00'
    }
