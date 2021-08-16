"""
Project CryPtoD,
Copyright PogD april 2021,
Primary author: Kristian K. Damsgaard
"""
import copy
import logging
import threading
import time

from modules.handlers.script_handler import ScriptHandler
from modules.handlers.time_handler import TimeHandler
from modules.system_services.system_services import SystemServices
from benchmarking import Benchmarking


class PairWatcher:
    """
    The PairWatcher handles operations on a given coin pair, as well as tracking status of trading.
    """

    def __init__(self, db_services, pair_name, orderbook, action_buy, action_sell, account):
        self._log = logging.getLogger(self.__class__.__name__)
        self._db_services = db_services
        self._db = self._db_services.db
        self._ready_state = False
        self._benchmarking = None
        self._pair_name = pair_name
        self._ws_name = None
        self._purse = None
        self._coins = None
        self._profit = None
        self._system_settings = None
        self._pair_settings = None
        self._purchase_lock = True
        self._incoming_queue = []
        self._trades = []
        self._analyses = []
        self._actions = []
        self._last_clean = 0
        self._clean_up_delay = 1 * 60  # 1 minute
        self._orderbook = orderbook
        self._real_action_buy = action_buy
        self._real_action_sell = action_sell
        self._account = account
        # INITIALIZE
        self._initialize()

    def _initialize(self):
        """
        Initializes the PairWatcher by fetching the relevant data from the database and adding this to local variables,
        then cleaning up the variables and starting an analysis thread.
        :return: None
        """
        self._load_settings()
        self._load_data()
        self._initialize_benchmarking_module()
        self._clean_up()
        self._start_threads()
        self._log.info(f"Initialized {self._pair_name}.")

    def _start_threads(self):
        at = threading.Thread(target=self._analysis_thread, daemon=True)
        at.name = self._pair_name
        self._thread = at
        at.start()

    def _load_settings(self):
        """
        Loads settings from database.
        """
        settings = self._db_services.fetch_pair_settings(self._pair_name)
        # print(settings)
        if settings:
            if self._pair_settings != settings:
                self._log.debug(f'{self._pair_name} settings loaded: {settings}')
                self._pair_settings = settings
        self._set_ready_state()

    def _load_data(self):
        """
        Loads pair data from database and sets the corresponding fields in PairWatcher. To be used when CryPtoD starts
        up.
        :return: Boolean (success)
        """
        self._ws_name = self._db_services.fetch_pair_info(pair_name=self._pair_name)['ws_name']
        wallet = self._db_services.fetch_pair_wallet(pair_name=self._pair_name)
        self._purse = wallet['purse']
        self._coins = wallet['coins']
        self._profit = wallet['profit']
        self._trades = self._db_services.fetch_pair_trades(pair_name=self._pair_name)
        self._analyses = self._db_services.fetch_pair_analyses(pair_name=self._pair_name)
        self._actions = self._db_services.fetch_pair_actions(pair_name=self._pair_name)

    def _initialize_benchmarking_module(self):
        if self._pair_settings['benchmark']:
            self._benchmarking = Benchmarking(pair_name=self._pair_name)

    def receive_public_trades(self, trades):
        """
        Receives trade data from the Brain and adds it to local variable.
        :param trades: Trades to log (list of trade objects)
        :return: None
        """
        for trade in trades:
            trade = self._translate(trade)
            self._incoming_queue.append(trade)
        self._log.debug(f"{self._pair_name} - received {len(trades)} trades")

    @staticmethod
    def _translate(trade):
        return {
            'price': float(trade[0]),
            'volume': float(trade[1]),
            'time': float(trade[2]),
            'direction': trade[3],
            'type': trade[4]
        }

    def _set_ready_state(self):
        try:
            if self._pair_settings['analyzer'] and self._pair_settings['factors']:
                self._ready_state = True
        except KeyError:
            self._ready_state = False
            self._log.info(f"{self._pair_name} is not ready to execute - missing factors?")
            time.sleep(10)
        except TypeError:
            self._log.error(f"{self._pair_name} - Unable to locate settings.")

    def _analysis_thread(self):
        """
        Endless loop (will terminate with main process thread) which alternatively analyses incoming trades or performs
        service functions (such as storing local data in the database, cleaning local data, etc).
        """
        while self._ready_state:
            if self._incoming_queue:
                if self._benchmarking:
                    start = time.time()

                trade = self._incoming_queue[0]
                self._trades.append(trade)
                del self._incoming_queue[0]
                self._analyze()

                if self._benchmarking:
                    elapsed = time.time() - start
                    self._benchmarking.receive_elapsed(elapsed=elapsed)
            else:
                self._save_data()
                self._clean_up()
                self._load_settings()
                time.sleep(1)
        while not self._ready_state:
            self._load_settings()

    def _analyze(self):
        """
        Loads the corresponding analyzer script and executes it, then logs the result in the corresponding variable
        list.
        """
        analyzer_handler = ScriptHandler(self)
        script = analyzer_handler.load_script(script_type='analyzer', script_name=self._pair_settings['analyzer'])
        args = analyzer_handler.load_args(script['arg_fields'])
        function = script['primary_function']

        analysis = analyzer_handler.run_script(function=function, args=args)
        if analysis:
            self._analyses.append(analysis)
            self._log.info(f"{self._pair_name} - finished analysis")
            if analysis['decision']:
                if analysis['decision']['direction']:
                    decision = analysis['decision']
                    if decision['direction'] == 'b':
                        if not self._purchase_lock:
                            self._fake_action_buy()
                        self._log.debug(f"{self._pair_name} made decision: {decision}")
                    elif decision['direction'] == 's':
                        self._unlock()
                        self._fake_action_sell()
                        self._log.debug(f"{self._pair_name} made decision: {decision}")
                try:
                    if self._benchmarking:
                        elapsed = analysis['benchmark']['elapsed']
                        self._benchmarking.receive_elapsed(elapsed=elapsed)
                except KeyError:
                    pass

    def _unlock(self):
        """
        Unlocks the PairWatcher, enabling it to buy coins. Note that decisions to buy can be made before unlocking, but
        not actual trades.
        """
        if self._purchase_lock:
            self._purchase_lock = False
            self._log.info(f"{self._pair_name} is now unlocked and ready to trade")

    def _fake_action_buy(self):
        """
        Estimation of a purchase.
        """
        if self._purse > 0:
            fee_factor = (self._pair_settings['fees']['taker'] / 100)
            asks = self._orderbook(self.ws_name, 'asks')
            if asks:
                for ask in asks:
                    if self._purse > 0:
                        price = ask['price']
                        order_volume = ask['volume']
                        volume = self._purse / price
                        if volume <= order_volume:
                            cost = volume * price
                        else:
                            volume = order_volume
                            cost = volume * price
                        fee = cost * fee_factor
                        total = cost + fee
                        self._purse -= total
                        self._coins += volume
                        action = {'time': time.time(),
                                  'direction': 'b',
                                  'price': price,
                                  'volume': volume,
                                  'cost': cost,
                                  'fee': fee}
                        self._actions.append(action)
                        self._log.info(f"{self._pair_name} - bought {round(volume, 4)} coins at {round(price, 4)} "
                                       f"(fee: {round(fee, 4)})")
                    else:
                        break

    def _fake_action_sell(self):
        """
        Estimation of a sale.
        """
        if self._coins > 0:
            fee_factor = (self._pair_settings['fees']['taker'] / 100)
            bids = self._orderbook(self.ws_name, 'bids')
            if bids:
                for bid in bids:
                    if self._coins > 0:
                        price = bid['price']
                        order_volume = bid['volume']
                        volume = self._coins
                        if order_volume < volume:
                            volume = order_volume
                        cost = volume * price
                        fee = cost * fee_factor
                        self._purse += cost - fee
                        self._coins -= volume
                        action = {'time': time.time(),
                                  'direction': 's',
                                  'price': price,
                                  'volume': volume,
                                  'cost': cost,
                                  'fee': fee}
                        self._actions.append(action)

                        self._calc_profit()

                        self._log.info(f"{self._pair_name} - sold {round(volume, 4)} coins at {round(price, 4)} "
                                       f"(fee: {round(fee, 4)}, profit: {self._profit})")
                    else:
                        break

    def _calc_profit(self):
        """
        Attempts to estimate the total profit of the actions taken by the PairWatcher - this is done simply by adding
        together all purse earned and subtracting all purse spent (including all fees). Any purchase actions taken after
        the last sale are ignored.
        """
        if self._actions:
            actions_copy = copy.copy(self._actions)

            if actions_copy[-1]['direction'] == 'b':
                del actions_copy[-1]

            spent = 0
            earned = 0

            for action in actions_copy:
                if action['direction'] == 's':
                    spent += float(action['cost'])
                if action['direction'] == 'b':
                    earned += float(action['cost'])
            return earned - spent
        else:
            return 0

    def _save_data(self):
        """
        Saves list variables (trades, analyses, actions) to database while ensuring trades are not
        "double-logged".
        """
        self._db_services.update_purse(pair_name=self._pair_name, new_purse=self._purse)
        self._db_services.update_coins(pair_name=self._pair_name, new_coins=self._coins)
        self._db_services.update_profit(pair_name=self._pair_name, new_profit=self._calc_profit())

        list_names = ['trades', 'analyses', 'actions']

        for list_name in list_names:
            self._push_entries(list_name=list_name)

    def _push_entries(self, list_name):
        """
        Helper function for "_save_data".
        """
        last_pushed = self._db_services.fetch_last_pushed(pair_name=self._pair_name, list_name=list_name)
        try:
            ts_last_pushed = last_pushed['time']
        except TypeError:
            ts_last_pushed = 0
        lst = getattr(self, "_" + list_name)
        count = 0
        for entry in lst:
            if entry['time'] > ts_last_pushed:
                count += 1
                self._db_services.push_list_entry(pair_name=self._pair_name, list_name=list_name, entry=entry)
        if count > 0:
            self._log.debug(f"{self._pair_name} - saved {count} {list_name}")

    def _clean_up(self):
        """
        "Cleans" the local collections (list-variables) by removing the outdated data (IE: data older than the tension timeframe
        for trades and all but the newest analysis and action) - this cleaning to not affect the database directly.
        """
        now = time.time()
        if now > self._last_clean + self._clean_up_delay:
            len_trades_before = len(self._trades)
            len_analyses_before = len(self._analyses)
            len_actions_before = len(self._actions)

            retention = self._pair_settings['retention']
            timeframe = retention['value']
            denominator = retention['denominator']
            settings = SystemServices().fetch_pair_data_fields()
            attribute_names = settings['attribute_names']
            attributes = SystemServices.get_attributes(calling_object=self, attribute_names=attribute_names)

            # Clean non-persisted storage
            for lst in attributes:
                while True:
                    if len(lst) > 0:
                        if lst[0]['time'] < now - TimeHandler().to_seconds(value=timeframe, denominator=denominator):
                            del lst[0]
                        else:
                            break
                    else:
                        break

            # Clean persisted storage
            for lst in attribute_names:
                self._db_services.clean_up_pair_data(pair_name=self._pair_name,
                                                     attribute=lst)

            self._last_clean = now

            len_trades_after = len(self._trades)
            len_analyses_after = len(self._analyses)
            len_actions_after = len(self._actions)

            self._log.debug(f"Watcher \"{self._pair_name}\" was cleaned - "
                            f"tr:[{len_trades_before}/{len_trades_after}], "
                            f"an:[{len_analyses_before}/{len_analyses_after}], "
                            f"ac:[{len_actions_before}/{len_actions_after}]")

    @property
    def pair_name(self):
        return self._pair_name

    @property
    def ws_name(self):
        return self._ws_name

    @property
    def thread(self):
        return self._thread

    @property
    def coins(self):
        return self._coins
