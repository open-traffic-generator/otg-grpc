import os
import datetime
import logging


def get_current_time():
    current_utc = datetime.datetime.utcnow()
    current_utc = str(current_utc).split('.')[0]
    current_utc = current_utc.replace(' ', '-')
    current_utc = current_utc.replace(':', '-')
    return current_utc


def init_logging(logger_name, level=logging.DEBUG, log_stdout=False):
    logger = logging.getLogger(logger_name)
    logfile = logger_name+'-'+str(get_current_time())+'.log'
    logs_dir = os.path.join(os.path.curdir, 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    logfile = os.path.join(logs_dir, logfile)
    log_format = "{'name': '%(name)s',\
        'level': '%(levelname)s',\
        'ctx': '%(pathname)s',\
        'ts':'%(asctime)s',\
        'msg': '%(message)s'}"
    formatter = logging.Formatter(log_format, "%Y-%m-%dT%H:%M:%SZ")
    fileHandler = logging.FileHandler(logfile, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    logger.setLevel(level)
    logger.addHandler(fileHandler)
    if log_stdout:
        logger.addHandler(streamHandler)
    return logger_name


def get_error_details(exception):
    return exception.args[0], exception.args[1]['errors']


def get_time_elapsed(start):
    end = datetime.datetime.now()
    elapsed = end - start
    return elapsed.total_seconds() * 10 ** 9
