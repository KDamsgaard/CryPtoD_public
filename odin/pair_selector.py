"""
Project CryPtoD,
Copyright PogD April 2021,
Primary author: Kristian K. Damsgaard
"""

import logging


class PairSelector:
    def __init__(self, db_services):
        self._log = logging.getLogger(self.__class__.__name__)
        self._db_services = db_services
        self._required_currency_components = None
        self._score_margin = None
        self._pairs_to_watch = []

        # INITIALIZE
        self._initialize()

    def _initialize(self):
        self._load_settings()

    def _load_settings(self):
        settings = self._db_services.fetch_system_settings()
        self._required_currency_components = settings['required_currency_components']
        self._score_margin = settings['score_margin']

    def positive_ultimates(self):
        pairs_to_watch = []
        ultimates = self._db_services.fetch_ultimates()
        for key in ultimates.keys():
            if ultimates[key]['scores']['original'] > self._score_margin:
                pairs_to_watch.append({'pair_name': key,
                                       'analyzer': ultimates[key]['analyzer'],
                                       'score': ultimates[key]['scores']['original']})
        return sorted(pairs_to_watch, key=self._select_score_from_entry, reverse=True)

    def _score_is_high_enough(self, score):
        if score > self._score_margin:
            return True
        return False

    @staticmethod
    def _select_score_from_entry(entry):
        return entry['score']

    @property
    def selected_pair_names(self):
        pair_names = []
        for entry in self.positive_ultimates():
            pair_names.append(entry['pair_name'])
        return pair_names
