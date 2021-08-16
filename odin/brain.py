"""
Project CryPtoD,
Copyright PogD april 2021,
Primary author: Kristian K. Damsgaard
"""

import logging
import threading
import time
from datetime import datetime

from modules.kraken_services.kraken_private_orderbook_service import KrakenPrivateOrderbookService
from modules.kraken_services.kraken_private_trades_service import KrakenPrivateTradesService
from modules.kraken_services.kraken_private_wallet_service import KrakenPrivateWalletService
from modules.kraken_services.kraken_public_orderbook_service import KrakenPublicOrderbookService
from modules.kraken_services.kraken_public_trades_service import KrakenPublicTradesService
from modules.kraken_services.kraken_websocket_service import KrakenWebSocketService
from modules.system_services.system_services import SystemServices
from pair_watcher import PairWatcher


class Brain:
    """
    This class handles sending incoming trades from the TradesWebsocket to the correct PairWatcher. The PairWatcher
    objects (their names) are loaded from the database when CryPtoD initializes.
    """

    def __init__(self, db_services):
        self._log = logging.getLogger(self.__class__.__name__)
        self._system_services = SystemServices()
        self._db_services = db_services
        self._started = time.time()
        self._alive_count = 0
        # self._watched_ws_names = None
        self._maximum_watched_pairs = 353  # TODO: Fix ugly hard-code
        self._watched_pairs = None
        self._pairs_in_sell_mode = []
        self._pair_watchers = {}
        self._watchers_in_sell_mode = []
        self._websocket_service = None
        self._public_orderbook = None
        self._private_orderbook = None
        self._private_wallet = None
        self._private_account = None
        self._action_buy = None
        self._action_sell = None

        # INITIALIZE
        self._initialize()

    def _initialize(self):
        """
        Initializes the Brain by adding a watcher for each pair name fetched from the database.
        :return: None
        """
        self._set_analyzer_script_names()
        self._set_watched_pairs()
        self._start_background_services()
        self._load_pair_watchers()
        self._log.info(f"Watched pairs: {self._watched_pairs}")
        self._log.info(f"Initialized at {self.started} UTC")
        self._run_forever()

    def _set_analyzer_script_names(self):
        names = self._system_services.get_analyzer_script_names()
        self._db_services.update_script_names(analyzer_script_names=names)

    def _start_background_services(self):
        self._websocket_service = KrakenWebSocketService(api_key=SystemServices.fetch_kraken_keys_settings()['api_key'],
                                      api_secret=SystemServices.fetch_kraken_keys_settings()['api_secret'])

        self._websocket_service.public.add_message_callback(
            KrakenPublicTradesService(self.receive_public_trades).update
        )
        self._public_orderbook = KrakenPublicOrderbookService(depth=10)
        self._websocket_service.public.add_message_callback(
            self._public_orderbook.update
        )
        self._websocket_service.private.add_message_callback(
            KrakenPrivateTradesService().update
        )
        self._websocket_service.private.add_message_callback(
            KrakenPrivateOrderbookService().update
        )

        # If kraken_rest is None, init_asset and balance will act as psudo wallet
        self._private_wallet = KrakenPrivateWalletService(kraken_rest=None, init_asset='ZEUR', init_balance=100)
        self._action_buy = self._websocket_service.private.add_buy_order
        self._action_sell = self._websocket_service.private.add_sell_order

        self._websocket_service.subscribe_assets()

    def _run_forever(self):
        alive_thread = threading.Thread(target=self._alive_thread)
        alive_thread.start()

    def _alive_thread(self):
        while True:
            old_pairs = self._watched_pairs
            self._set_watched_pairs()

            if old_pairs != self._watched_pairs:
                self._load_pair_watchers()
                self._log.info(f"Now tracking {len(self._watched_pairs)} pairs >>> {self._watched_pairs}")

            self._check_threads()
            # self._print_alive()

            time.sleep(5)

    def _check_threads(self):
        threads = threading.enumerate()
        thread_names = []

        for thread in threads:
            if thread.name in self._pair_watchers:
                if not thread.is_alive():
                    self._log.error(f"Thread {thread.name} is dead!")
                thread_names.append(thread.name)

        for pair_name in self._watched_pairs:
            if pair_name not in thread_names:
                self._log.error(f"Thread {pair_name} was not found!")
                self._unwatch(pair_name=pair_name)
                self._remove_pair_watcher(key=pair_name)
                self._log.error(f"{pair_name} was removed from watched pairs.")

    def _print_alive(self):
        print(".", end="")
        self._alive_count += 1
        if self._alive_count % 10 == 0:
            print("")

    def _load_pair_watchers(self):
        self._check_collections()
        if self._watched_pairs:
            for pair_name in self._watched_pairs:
                if pair_name not in self._pair_watchers.keys():
                    self._pair_watchers[pair_name] = PairWatcher(db_services=self._db_services,
                                                                 pair_name=pair_name,
                                                                 orderbook=self.orderbook,
                                                                 action_buy=self._action_buy,
                                                                 action_sell=self._action_sell,
                                                                 account=self._private_account)
                    self._log.info(f"Added PairWatcher {pair_name}")

        # if self._pair_watchers:
        #     keys_to_remove = []
        #     for key in self._pair_watchers.keys():
        #         if key not in self._watched_pairs:
        #             keys_to_remove.append(key)
        #     for key in keys_to_remove:
        #         self._remove_pair_watcher(key=key)
        #         self._log.info(f"Removed PairWatcher {key}")

    def _remove_from_sell_mode(self):
        for key in self._watchers_in_sell_mode:
            if self._pair_watchers[key]. coins == 0:
                self._remove_pair_watcher(key=key)

    def _check_collections(self):
        for pair_name in self._watched_pairs:
            if not self._db_services.pair_collection_exists(pair_name=pair_name):
                self._db_services.insert_pair(pair_name=pair_name)

    def _unwatch(self, pair_name):
        self._watched_pairs.remove(pair_name)
        self._log.info(f"{pair_name} was removed from watch list")

    def _remove_pair_watcher(self, key):
        if self._pair_watchers[key].coins > 0:
            self._watchers_in_sell_mode.append(key)
            self._log.info(f"Pair watcher {key} was set to sell mode.")
        else:
            del self._pair_watchers[key]
            self._log.info(f"Pair watcher {key} was killed.")

    def _set_watched_pairs(self):
        from pair_selector import PairSelector
        selected = PairSelector(db_services=self._db_services).selected_pair_names
        selected = selected[0:self._maximum_watched_pairs]
        self._watched_pairs = selected
        self._db_services.set_watched_pairs(pair_names=selected)
        # self._watched_pairs = self._db_services.watched_pairs

    def receive_public_trades(self, message):
        """
        Receives data from TradesWebsocket and supplies it to the corresponding PairWatcher.
        :param message: message containing trades
        :return: None
        """
        # TODO: Implement subscribing to only watched pairs
        msg_ws_name = message[3]
        trades = message[1]
        try:
            for key in self._pair_watchers.keys():
                if self._pair_watchers[key].ws_name == msg_ws_name:
                    self._pair_watchers[key].receive_public_trades(trades=trades)
            return True
        except Exception as e:
            self._log.debug(f"Was unable to send trades to PairWatcher (ws_name: {msg_ws_name})")
            self._log.debug(f"{e}")
            return False

    def receive_public_order_book(self, message):
        """
        Receives data from TradesWebsocket and supplies it tot the corresponding PairWatcher.
        :param message: message containing trades
        :return: None
        """
        self._public_orderbook.run(message)

    def orderbook(self, ws_name, asks_or_bids):
        ab = {'asks': self._public_orderbook.asks(ws_name), 'bids': self._public_orderbook.bids(ws_name)}
        return ab[asks_or_bids]

    @property
    def database(self):
        return self._db_services.db

    @property
    def started(self):
        return datetime.utcfromtimestamp(self._started).strftime("%d/%m/%Y %H:%M:%S")

    @property
    def pair_names(self):
        return self._watched_pairs

    @property
    def pair_watchers(self):
        return self._pair_watchers

    def __str__(self):
        utc = datetime.utcfromtimestamp(self._started).strftime("%d/%m/%Y %H:%M:%S")
        watcher_keys = self.pair_watchers.keys()
        return f"Brain -----------------------------------------\n" \
               f"Started (UTC): {utc}\n" \
               f"Pair names: {self._watched_pairs}\n" \
               # f"WS names: {self._watched_ws_names}\n" \
               # f"Watchers: {watcher_keys}"
