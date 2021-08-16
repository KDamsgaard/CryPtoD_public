"""
Project CryPtoD,
Copyright PogD april 2021,
Primary author: Kristian K. Damsgaard
"""

import logging
import sys
from datetime import date


class TestingLogger:
    def __init__(self):
        self._log = None
        # INITIALIZE
        self._initialize_log()

    def _initialize_log(self):
        """
        Sets the logger with various outputs and levels
        """
        log = logging.getLogger()
        log.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        fh_debug = logging.FileHandler(filename=f"logs/{date.today()}_testing_log.txt")
        fh_debug.setLevel(logging.DEBUG)
        fh_debug.setFormatter(formatter)

        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(logging.DEBUG)
        sh.setFormatter(formatter)

        log.addHandler(fh_debug)
        log.addHandler(sh)

        self._log = logging.getLogger(self.__class__.__name__)
        self._log.info(f"Testing log initialized")
