import os
import datetime
import logging
import re
from logging.handlers import RotatingFileHandler


class CustomFormatter(logging.Formatter):

    def format(self, record: logging.LogRecord) -> str:
        arg_pattern = re.compile(r'%\((\w+)\)')
        arg_names = [x.group(1) for x in arg_pattern.finditer(self._fmt)]
        for field in arg_names:
            if field not in record.__dict__:
                if field == 'payload':
                    record.__dict__[field] = {}
                else:
                    record.__dict__[field] = None

        return super().format(record)


def get_current_time():
    current_utc = datetime.datetime.utcnow()
    current_utc = str(current_utc).split('.')[0]
    current_utc = current_utc.replace(' ', '-')
    current_utc = current_utc.replace(':', '-')
    return current_utc


def init_logging(
        ctx,
        scope,
        logfile,
        level=logging.DEBUG,
        log_stdout=False,
        type=None):
    logger_name = ctx + '_' + scope # noqa
    logger = logging.getLogger(logger_name)
    logs_dir = os.path.join(os.path.curdir, 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    logfile = os.path.join(logs_dir, logfile)
    if ctx in ['profile']:
        log_format = '{"level":"%(levelname)s","ctx":"' + ctx + '","api":"%(api)s","choice":"%(choice)s","scope":"' + scope + '","nanoseconds":"%(nanoseconds)s","ts":"%(asctime)s.%(msecs)03dZ","msg":"%(message)s"}' # noqa
    else:
        if type in ['payload']:
            log_format = '{"level":"%(levelname)s","ctx":"' + ctx + '","scope":"' + scope + '","api":"%(funcName)s","ts":"%(asctime)s.%(msecs)03dZ","msg":"%(message)s","payload":%(payload)s}' # noqa
        else:
            log_format = '{"level":"%(levelname)s","ctx":"' + ctx + '","scope":"' + scope + '","api":"%(funcName)s","ts":"%(asctime)s.%(msecs)03dZ","msg":"%(message)s"}' # noqa
    formatter = CustomFormatter(log_format, "%Y-%m-%dT%H:%M:%S")
    fileHandler = RotatingFileHandler(
        logfile,
        mode='a',
        maxBytes=25*1024*1024,
        backupCount=2,
        encoding=None,
        delay=0
    )
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    logger.setLevel(level)
    logger.addHandler(fileHandler)
    if log_stdout:
        logger.addHandler(streamHandler)
    return logger


def get_error_details(exception):
    return exception.args[0], exception.args[1]['errors']


def get_time_elapsed(start):
    end = datetime.datetime.now()
    elapsed = end - start
    return elapsed.total_seconds() * 10 ** 9
