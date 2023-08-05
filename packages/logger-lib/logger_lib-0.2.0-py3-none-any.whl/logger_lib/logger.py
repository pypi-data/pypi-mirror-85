import logging
import json
from json.decoder import JSONDecodeError
from colorlog import ColoredFormatter

LOGFORMAT = ('%(log_color)s %(asctime)s | %(levelname)-4s | '
             '%(name)s | %(message)s')

log_format = ColoredFormatter(LOGFORMAT)


class Logger():
    def __init__(self, name):
        self.name = name
        self.logger = logging.getLogger(name)
        screen_handler = logging.StreamHandler()
        screen_handler.setFormatter(log_format)
        self.logger.addHandler(screen_handler)

    def debug(self, msg, line=__file__, **kwargs):
        self.logger.setLevel(logging.DEBUG)
        kwargs.update({'msg': msg})
        self.logger.debug(json.dumps(kwargs))

    def info(self, msg, **kwargs):
        self.logger.setLevel(logging.INFO)
        kwargs.update({'msg': msg})
        self.logger.info(json.dumps(kwargs))

    def warn(self, msg, **kwargs):
        self.logger.setLevel(logging.WARN)
        kwargs.update({'msg': msg})
        self.logger.warn(json.dumps(kwargs))

    def error(self, msg, **kwargs):
        self.logger.setLevel(logging.ERROR)
        kwargs.update({'msg': msg})
        self.logger.error(json.dumps(kwargs))

    def error_and_throw_exception(self, msg, **kwargs):
        if "response" in kwargs:
            response = kwargs["response"]
            try:
                response_body = response.json()
            except JSONDecodeError:
                response_body = None
            kwargs["status_code"] = response.status_code
            kwargs["response"] = response_body
        self.error(msg, **kwargs)
        raise TestCheckError(msg)

    def success_message(self, msg, **kwargs):
        if "response" in kwargs:
            response = kwargs["response"]
            try:
                response_body = response.json()
            except JSONDecodeError:
                response_body = None
            kwargs["status_code"] = response.status_code
            kwargs["response"] = response_body
        self.info(msg, **kwargs)


class TestCheckError(ValueError):
    def __init__(self, arg):
        self.strerror = arg
        self.args = (arg,)


def getLogger(name=__name__):
    return Logger(name)
