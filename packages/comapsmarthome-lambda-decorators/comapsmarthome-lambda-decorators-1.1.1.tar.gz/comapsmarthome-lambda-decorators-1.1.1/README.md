Provides helpful decorators for aws lambda handler functions.

**@enable_logging**:
Init logger with the level taken from _LOG_LEVEL_ environment variable.
 ```python
 @enable_logging
 def handle_event(event):
    logging.info('This will be logged, because the default level is INFO')
 ```

**@process_sns_event**:
Transforms the function into an sns event processor, meaning the function will be passed the extracted event payload.
 ```python
 @process_sns_event
 def handle_event(event):
    print(event['serial_number']) # event is the payload extracted from the original aws event
 ```

**@process_sqs_event**:
Transforms the function into an sqs command processor, meaning the function will be passed the extracted command payload.
 ```python
 @process_sqs_event
 def handle_event(command):
    print(command['serial_number']) # command is the payload extracted from the original aws event
 ```

**@process_kinesis_event**:
Transforms the function into a kinesis event processor, meaning the function will be passed the extracted event payload.
 ```python
 @process_kinesis_event
 def handle_event(event):
    print(event['serial_number']) # event is the payload extracted from the original aws event
 ```