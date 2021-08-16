"""
Project CryPtoD,
Copyright PogD april 2021,
Primary author: Kristian K. Damsgaard
"""
import copy
import logging
import time

from modules.handlers.script_handler import ScriptHandler


class Reconstructor:
    def __init__(self, db_services, pair_name, analyzer_name, trades, factors):
        self._log = logging.getLogger(self.__class__.__name__)
        self._db_services = db_services
        self._started = time.time()
        self._pair_name = pair_name
        self._analyzer_name = analyzer_name
        self._incoming_queue = trades
        self._pair_settings = {'factors': factors}
        self._purse = 100
        self._coins = 0
        self._trades = []
        self._analyses = []
        self._actions = []
        self._result_set = {}

        # INITIALIZE
        self._initialize()

    def _initialize(self):
        self._run_analysis()
        self._set_results()

    @staticmethod
    def _alive_thread():
        counter = 0
        while True:
            counter += 1
            time.sleep(3)
            print("", end=".")
            if counter % 100 == 0:
                print()

    def _run_analysis(self):
        # Reconstruct
        if self._incoming_queue:
            for trade in self._incoming_queue:
                self._trades.append(trade)
                del self._incoming_queue[0]
                self._reconstruct()

    def _reconstruct(self):
        analyzer_handler = ScriptHandler(self)
        script = analyzer_handler.load_script(script_type='analyzer', script_name=self._analyzer_name)
        args = analyzer_handler.load_args(script['arg_fields'])
        function = script['primary_function']

        analysis = analyzer_handler.run_script(function=function, args=args)

        if analysis:
            self._analyses.append(analysis)
            # if analysis['decision']['direction']:
            try:
                decision = analysis['decision']
                if decision['direction'] == 'b':
                    self._fake_purchase()
                elif decision['direction'] == 's':
                    self._fake_sale()
            except TypeError:
                pass

    def _set_results(self):
        score = self._calc_score()
        self._result_set = {'time': self._started,
                            'analyzer': self._analyzer_name,
                            'scores': {'original': score, 'degenerated': score},
                            'factors': self._pair_settings['factors'],
                            }

    def _fake_purchase(self):
        price = self._get_price()
        _time = self._get_time()
        if price and self._purse > 0:
            fee = 0.26 / 100 * self._purse
            total_coins = (self._purse - fee) / price

            self._coins = total_coins
            self._purse = 0
            self._actions.append({'time': _time,
                                  'direction': 'b',
                                  'price': price,
                                  'purse': self._purse,
                                  'coins': self._coins,
                                  'fee': fee})

    def _fake_sale(self):
        price = self._get_price()
        _time = self._get_time()  # SBP: We need time of trade
        if price and self._coins > 0:
            total_purse = self._coins * price
            fee = total_purse / 100 * 0.26

            self._purse = total_purse - fee
            self._coins = 0
            self._actions.append({'time': _time,
                                  'direction': 's',
                                  'price': price,
                                  'purse': self._purse,
                                  'coins': self._coins,
                                  'fee': fee})

    def _get_price(self):
        return self._trades[-1]['price']

    def _get_time(self):
        return self._trades[-1]['time']

    def _calc_score(self):
        """
        Attempts to estimate the total profit of the actions taken by the PairWatcher - this is done simply by adding
        together all purse earned and subtracting all purse spent (including all fees). Any purchase actions taken after
        the last sale are ignored.
        """
        profit = -123456
        if self._actions:
            actions_copy = copy.copy(self._actions)

            if actions_copy[-1]['direction'] == 'b':
                del actions_copy[-1]

            spent = 0
            earned = 0

            for action in actions_copy:
                if action['direction'] == 'b':
                    spent += float(action['price']) * float(action['coins'])
                if action['direction'] == 's':
                    earned += float(action['purse'])
            profit = earned - spent

        return profit

    def _fetch_trades(self):
        trades = self._db_services.fetch_trades(pair_name=self._pair_name)
        return trades

    @property
    def pair_name(self):
        return self._pair_name

    @property
    def result_set(self):
        return self._result_set
