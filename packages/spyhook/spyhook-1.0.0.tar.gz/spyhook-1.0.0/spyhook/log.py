#!/usr/bin/env python3

"""spyhook - logging functionality"""

# stdlib
import logging


class RequestLoggerAdapter(logging.LoggerAdapter):
    """Log adapter that prepends log messages with request_id"""

    @classmethod
    def get_logger(cls, request_id):
        """get logger using RequestLoggerAdapter"""
        return cls(logging.getLogger('spyhook'), {'request_id': request_id})

    def process(self, msg, kwargs):
        """process log messages, prepend with request_id"""
        return f'{self.extra["request_id"]}: {msg}', kwargs
