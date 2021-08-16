"""
Project CryPtoD,
Copyright PogD June 2021,
Primary author: Kristian K. Damsgaard
"""

import logging
import threading
import time

from bulk_watcher import BulkWatcher
#from modules.kraken_services.KrakenAPIService import KrakenWebSocketServiceCallbackManager, KrakenWebSocketService
from modules.kraken_services.kraken_public_orderbook_service import KrakenPublicOrderbookService
from modules.kraken_services.kraken_public_trades_service import KrakenPublicTradesService
from modules.kraken_services.kraken_websocket_service import KrakenWebSocketService
from modules.kraken_services.KrakenAPIService import subscribe_trades


class Brain:
    def __init__(self, db_services):
        self._log = logging.getLogger(self.__class__.__name__)
        self._db_services = db_services
        self._bulk_watcher = None
        self._public_orderbook = None
        # Initialize
        self._initialize()

    def _initialize(self):
        self._start_background_services()
        self._run_forever()

    def _start_background_services(self):
        self._bulk_watcher = BulkWatcher(db_services=self._db_services)

        kwss = KrakenWebSocketService()
        self._public_orderbook = KrakenPublicOrderbookService(depth=10)

        kwss.public.add_message_callback(
            KrakenPublicTradesService(self.receive_public_trades).update
        )
        kwss.public.add_message_callback(
            self._public_orderbook.update
        )

        kwss.public.subscribe_public(KrakenWebSocketService.FEED_PUBLIC_ORDERBOOK)
        kwss.subscribe_assets()

    def _run_forever(self):
        alive_thread = threading.Thread(target=self._alive_thread)
        alive_thread.start()

    def _alive_thread(self):
        while True:
            time.sleep(5)

    def receive_public_trades(self, message):
        """
        Receives data from TradesWebsocket and supplies it to the corresponding PairWatcher.
        :param message: message containing trades
        :return: None
        """
        msg_ws_name = message[3]
        trades = message[1]
        try:
            self._bulk_watcher.receive_public_trades(ws_name=msg_ws_name, trades=trades)
            return True
        except Exception as e:
            self._log.debug(f"unable to send trades to BulkWatcher (ws_name: {msg_ws_name}) >>> {e}")
            return False

    @property
    def watcher(self):
        return self._bulk_watcher
