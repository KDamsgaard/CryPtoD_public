"""
Project CryPtoD,
Copyright PogD June 2021,
Primary author: Kristian K. Damsgaard
"""

import logging


class Benchmarking:
    def __init__(self, pair_name):
        self._log = logging.getLogger(self.__class__.__name__)
        self._pair_name = pair_name
        self._fastest_analysis = None
        self._slowest_analysis = None
        self._amount_analyses_performed = 0
        self._total_time_spend_analysing = 0

    def receive_elapsed(self, elapsed):
        self._amount_analyses_performed += 1
        self._total_time_spend_analysing += elapsed

        if self._is_fastest(elapsed=elapsed):
            self._set_fastest(elapsed)

        if self._is_slowest(elapsed=elapsed):
            self._set_slowest(elapsed)

        self._log_benchmark()

    def _is_fastest(self, elapsed):
        if not self._fastest_analysis:
            return True
        return elapsed < self._fastest_analysis

    def _is_slowest(self, elapsed):
        if not self._slowest_analysis:
            return True
        return elapsed > self._slowest_analysis

    def _set_fastest(self, timestamp):
        self._fastest_analysis = round(timestamp, 6)

    def _set_slowest(self, timestamp):
        self._slowest_analysis = round(timestamp, 6)

    def _log_benchmark(self):
        amount_analyses = self._amount_analyses_performed
        slowest = self._slowest_analysis
        average = self.average
        self._log.info(
            f"{self._pair_name} - Analyses: {amount_analyses}, slowest: {slowest}, average: {average} ")

    @property
    def analyses_performed(self):
        return self._amount_analyses_performed

    @property
    def average(self):
        return round(self._total_time_spend_analysing / self._amount_analyses_performed, 6)

    @property
    def slowest(self):
        return self._slowest_analysis

    @property
    def fastest(self):
        return self._fastest_analysis
