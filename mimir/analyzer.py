"""
Project CryPtoD,
Copyright PogD June 2021,
Primary author: Kristian K. Damsgaard
"""

import copy
import logging
import random
import time

from factor_modifier import FactorModifier
from modules.handlers.script_handler import ScriptHandler
from reconstructor import Reconstructor


class Analyzer:
    def __init__(self, db_services, pair_name, analyzer_name):
        self._log = logging.getLogger(self.__class__.__name__)
        self._db_services = db_services
        self._pair_name = pair_name
        self._analyzer_name = analyzer_name
        self._iteration_length = None
        self._exploration_percent = None
        self._minimum_trades = None
        self._increments = None
        self._result_set = None

        self.epoch = 0

        # INITIALIZE
        self._initialize()
        self._run()

    def _initialize(self):
        random.seed()
        self._fetch_settings()
        # self._log.info(self._settings_string())
        self._log.debug(f"{self._pair_name} - Analyzer initialized")

    def _fetch_settings(self):
        fetched = self._db_services.fetch_settings()
        self._iteration_length = fetched['iteration_length']
        self._exploration_percent = fetched['exploration_percent']
        self._minimum_trades = fetched['minimum_trades']
        self._increments = fetched['increments']

    def _run(self):
        while True:
            self._fetch_settings()
            success = self._epoch()
            if not success:
                # self._log.info(f"{self._pair_name} - Not enough trades to perform analysis")
                time.sleep(120)

    def _epoch(self):
        self.epoch += 1
        trades = self._db_services.fetch_trades(pair_name=self._pair_name)
        if len(trades) >= self._minimum_trades:
            exploring = self._is_exploring()
            baseline = self._get_baseline(exploring=exploring)
            iteration_result = None
            for i in range(0, self._iteration_length):
                result_set = self._iteration(baseline=baseline, trades=trades)
                if iteration_result:
                    if result_set['scores']['original'] >= iteration_result['scores']['original']:
                        iteration_result = copy.deepcopy(result_set)
                else:
                    iteration_result = result_set
            self._store_result(result_set=iteration_result)
        else:
            return False
        return True

    def _iteration(self, baseline, trades):
        factors = baseline['factors']
        modifier = FactorModifier(old_factors=factors, increments=self._increments)
        new_factors = modifier.new_factors
        reconstructor = Reconstructor(db_services=self._db_services,
                                      trades=trades,
                                      pair_name=self._pair_name,
                                      analyzer_name=self._analyzer_name,
                                      factors=new_factors)
        return reconstructor.result_set

    def _is_exploring(self):
        percentile = random.random() * 100  # Random percentile
        if percentile < self._exploration_percent:
            return True
        else:
            return False

    def _get_baseline(self, exploring):
        if exploring:
            baseline = self._get_script_baseline_factors()
        else:
            baseline = self._get_best_result_set()
            if not baseline:
                baseline = self._get_script_baseline_factors()
        return baseline

    def _get_script_baseline_factors(self):
        handler = ScriptHandler(self)
        script = handler.load_script(script_type='analyzer',
                                     script_name=self._analyzer_name)
        return {'time': time.time(),
                'scores': {'original': -123456, 'degenerated': -123456},
                'factors': script['factors']}

    def _get_best_result_set(self):
        return self._db_services.fetch_analyzer_best_result(pair_name=self._pair_name,
                                                            script_name=self._analyzer_name)

    def _store_result(self, result_set):
        if result_set['scores']['original'] != -123456:
            old_best = self._db_services.fetch_analyzer_best_result(pair_name=self._pair_name,
                                                                    script_name=self._analyzer_name)
            if self._new_is_better_than_old(new_result=result_set, old_result=old_best):
                self._db_services.set_pair_name_best(pair_name=self._pair_name,
                                                     script_name=self._analyzer_name,
                                                     result_set=result_set)
                self._log.info(f"{self._pair_name} - New analyzer best: {self._result_string(result_set=result_set)}")

            ultimate_best = self._db_services.fetch_ultimate_best(pair_name=self._pair_name)
            if self._new_is_better_than_old(new_result=result_set, old_result=ultimate_best):
                result_set['analyzer'] = self._analyzer_name
                self._db_services.set_ultimate_best(pair_name=self._pair_name,
                                                    result_set=result_set)
                self._log.info(f"{self._pair_name} - New ultimate best: {self._result_string(result_set=result_set)}")

    @staticmethod
    def _new_is_better_than_old(new_result, old_result):
        if old_result:
            if old_result['scores']['degenerated'] >= new_result['scores']['original']:
                return False
        return True

    def _settings_string(self):
        return f"{self._pair_name} - " \
               f"analyzer: \"{self._analyzer_name}\", " \
               f"iteration length: {self._iteration_length}, " \
               f"exploration %: {self._exploration_percent}, " \
               f"minimum trades: {self._minimum_trades}, " \
               f"increments: {self._increments}"

    @staticmethod
    def _result_string(result_set):
        result_string = ""
        if "analyzer" in result_set.keys():
            result_string += f"\"{result_set['analyzer']}\" set to "
        factors = ""
        for key in result_set['factors'].keys():
            if factors != "":
                factors += ", "
            value = result_set['factors'][key]['value']
            factors += f"{key}: {value}"
        result_string += f"{factors} "
        result_string += f"(Score is {round(result_set['scores']['original'], 4)})"
        return result_string
