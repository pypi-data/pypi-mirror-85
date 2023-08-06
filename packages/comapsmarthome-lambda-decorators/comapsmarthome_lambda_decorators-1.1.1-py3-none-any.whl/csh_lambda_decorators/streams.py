import base64
import functools
import logging
import os
from simplejson import loads

from csh_lambda_decorators.stream_event_parsers import noop_event_parser


def process_sns_event(_func=None, *, event_parser=noop_event_parser):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(event, _context):
            logging.debug('Received event : {}'.format(event))
            for record in event['Records']:
                event = loads(record['Sns']['Message'])
                event_parser(func, event)

        return wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)


def process_kinesis_event(_func=None, *, event_parser=noop_event_parser):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(event, _context):
            logging.debug('Received event : {}'.format(event))

            for record in event['Records']:
                event = loads(base64.b64decode(record['kinesis']['data']).decode('UTF-8'))
                try:
                    event_parser(func, event)
                except Exception as e:
                    logging.getLogger().error("An unknown error occurred when trying to process kinesis event")
                    logging.getLogger().exception(e)
                    if os.environ.get('SILENT_FAILURE', 'false').lower() != 'true':
                        raise e

        return wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)


def process_sqs_event(_func=None, *, event_parser=noop_event_parser):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(event, _context):
            for record in event['Records']:
                command = loads(record['body'])
                event_parser(func, command)

        return wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)
