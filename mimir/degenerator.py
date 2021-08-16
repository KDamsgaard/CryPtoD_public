"""
Project CryPtoD,
Copyright PogD June 2021,
Primary author: Kristian K. Damsgaard
"""

import logging
import time


class Degenerator:
    def __init__(self, db_services, pair_names, analyzer_names):
        self._log = logging.getLogger(self.__class__.__name__)
        self._db_services = db_services
        self._pair_names = pair_names
        self._analyzer_names = analyzer_names
        self._degeneration_factor = None
        self._degeneration_delay = None

        # INITIALIZE
        self._initialize()
        self._run()

    def _initialize(self):
        settings = self._db_services.fetch_settings()
        self._degeneration_factor = settings['degeneration_factor']
        self._degeneration_delay = settings['degeneration_delay']

    def _run(self):
        while True:
            for pair_name in self._pair_names:
                self._degenerate_ultimate(pair_name=pair_name)
                for analyzer_name in self._analyzer_names:
                    self._degenerate_best(pair_name=pair_name,
                                          analyzer_name=analyzer_name)
            self._log.info(f"Full degeneration complete.")
            time.sleep(self._degeneration_delay)

    def _degenerate_ultimate(self, pair_name):
        ultimate = self._db_services.fetch_ultimate_best(pair_name=pair_name)
        if ultimate:
            degenerated = ultimate['scores']['degenerated']
            ultimate['scores']['degenerated'] = degenerated - self._degeneration_factor
            self._db_services.set_ultimate_best(pair_name=pair_name,
                                                result_set=ultimate)
            # self._log.info(f"Degenerated {pair_name} ultimate "
            #                f"({ultimate['scores']['original']}/{ultimate['scores']['degenerated']}).")

    def _degenerate_best(self, pair_name, analyzer_name):
        best = self._db_services.fetch_analyzer_best_result(pair_name=pair_name,
                                                            script_name=analyzer_name)
        if best:
            degenerated = best['scores']['degenerated']
            best['scores']['degenerated'] = degenerated - self._degeneration_factor
            self._db_services.set_pair_name_best(pair_name=pair_name,
                                                 script_name=analyzer_name,
                                                 result_set=best)
            # self._log.info(f"Degenerated {pair_name} - \"{analyzer_name}\" best.")

    def _has_best(self, pair_name, analyzer_name):
        pass
