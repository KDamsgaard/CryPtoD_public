import logging
import os
import sys
from datetime import date


class LogServices:
    def __init__(self):
        self._log = None
        if not self._log:
            self.__initialize_log()

    @staticmethod
    def _folder_check():
        if not os.path.exists("logs"):
            os.makedirs("logs")

    def __initialize_log(self):
        """
        Sets the logger with various outputs and levels.
        This function should follow the Singleton pattern and only be called exactly once.
        """
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log = logging.getLogger()
        log.setLevel(logging.INFO)

        fh_debug = logging.FileHandler(filename=f"logs/{date.today()}_debug_log.txt")
        fh_debug.setLevel(logging.DEBUG)
        fh_debug.setFormatter(formatter)
        log.addHandler(fh_debug)

        fh_error = logging.FileHandler(filename=f"logs/{date.today()}_error_log.txt")
        fh_error.setLevel(logging.WARNING)
        fh_error.setFormatter(formatter)
        log.addHandler(fh_error)

        sh = logging.StreamHandler(stream=sys.stdout)
        sh.setLevel(logging.INFO)
        sh.setFormatter(formatter)
        log.addHandler(sh)

        self._log = logging.getLogger(self.__class__.__name__)
        self._log.info("Log initialized")
