import logging
import sys


class Logger(logging.Logger):
    def __init__(self, logging_level):
        super().__init__('MyLogger')
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.addHandler(handler)
        if logging_level == 'INFO':
            self.setLevel(logging.INFO)
        elif logging_level == 'DEBUG':
            self.setLevel(logging.DEBUG)
        else:
            self.setLevel(logging.ERROR)
