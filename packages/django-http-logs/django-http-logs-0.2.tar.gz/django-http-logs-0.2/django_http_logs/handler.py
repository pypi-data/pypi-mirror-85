"""
Author:     LanHao
Date:       2020/11/17
Python:     python3.6

"""
from logging import Handler

from .tasks import add_log


class AsyncHandler(Handler):
    def emit(self, record):
        add_log.apply_async((record.__dict__,))
