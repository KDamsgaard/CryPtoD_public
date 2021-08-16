"""
Project CryPtoD,
Copyright PogD april 2021,
Primary author: Kristian K. Damsgaard
"""

import logging
import threading


class BulkWatcher:
    def __init__(self, db_services):
        self._log = logging.getLogger(self.__class__.__name__)
        self._db_services = db_services
        self._incoming_queue = []
        self._processed = {'amount': 0, 'ws_names': []}

        # INITIALIZE
        self._initialize()

    def _initialize(self):
        """
        Initializes the PairWatcher by fetching the relevant data from the database and adding this to local variables,
        then cleaning up the variables and starting an analysis thread.
        :return: None
        """
        self._start_thread()
        self._log.info(f"Initialized Bulk Watcher")

    def _start_thread(self):
        at = threading.Thread(target=self._alive_thread, daemon=True)
        self._thread = at
        at.start()

    def _alive_thread(self):
        while True:
            if self._incoming_queue:
                self._process()
            else:
                self._log_processed()

    def _process(self):
        message = self._incoming_queue[0]
        self._processed['amount'] += 1
        if message['ws_name'] not in self._processed['ws_names']:
            self._processed['ws_names'].append(message['ws_name'])
        trade = message['trade']
        self._db_services.push_trade(ws_name=message['ws_name'], entry=trade)
        del self._incoming_queue[0]

    def receive_public_trades(self, ws_name, trades):
        """
        Receives trade data from the Brain and adds it to local variable.
        :param ws_name: Web socket identifier of the trade to log
        :param trades: Trades to log (list of trade objects)
        :return: None
        """
        for trade in trades:
            trade = self._translate(trade)
            message = {'ws_name': ws_name, 'trade': trade}
            self._incoming_queue.append(message)

    def _log_processed(self):
        if self._processed['amount'] > 0:
            self._log.info(f"Processed {self._processed['amount']} trades for pairs: {self._processed['ws_names']}")
            self._processed = {'amount': 0, 'ws_names': []}

    @staticmethod
    def _translate(trade):
        return {
            'price': float(trade[0]),
            'volume': float(trade[1]),
            'time': float(trade[2]),
            'direction': trade[3],
            'type': trade[4],
            'misc': trade[5]
        }

