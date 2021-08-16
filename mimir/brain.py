"""
Project CryPtoD,
Copyright PogD June 2021,
Primary author: Kristian K. Damsgaard
"""

import logging
import threading
import time

from analyzer import Analyzer
from degenerator import Degenerator
from modules.system_services.system_services import SystemServices


class Brain:
    def __init__(self, db_services):
        self._log = logging.getLogger(self.__class__.__name__)
        self._db_services = db_services
        self._started = time.time()
        self._pair_names = None
        self._analyzer_names = None
        # INITIALIZE AND RUN
        self._initialize()
        self._run()

    def _initialize(self):
        # Set fields
        self._analyzer_names = self._fetch_analyzer_names()
        self._pair_names = self._fetch_pair_names()
        self._log.info(f"Initializing Mimir")

    def _run(self):
        self._start_analyzers()
        self._start_degenerator()

    def _start_analyzers(self):
        for pair_name in self._pair_names:
            for analyzer_name in self._analyzer_names:
                self._log.debug(f"{pair_name} - {analyzer_name} starting...")
                args = (self._db_services,
                        pair_name,
                        analyzer_name)
                analyzer_thread = threading.Thread(target=Analyzer, args=args)
                analyzer_thread.start()

    def _start_degenerator(self):
        Degenerator(db_services=self._db_services,
                    pair_names=self._pair_names,
                    analyzer_names=self._analyzer_names)

    @staticmethod
    def _fetch_analyzer_names():
        return SystemServices().get_analyzer_script_names()

    def _fetch_pair_names(self):
        return self._db_services.fetch_warehouse_pair_names()
