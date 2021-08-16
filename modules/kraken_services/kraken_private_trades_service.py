import logging

class KrakenPrivateTradesService:
    def __init__(self):
        self._log = logging.getLogger(self.__class__.__name__)
        self._trades = {}

    def update(self, message):
        if type(message) == list:
            if 'ownTrades' in message[1]:
                self._log.debug(f'Found {message[1]} with {len(message[0])} entries')
                self._update_trades(message)

    def _update_trades(self, trades):
        trades = trades[0]
        for trade in trades:
            # Trade starts with a trade id
            # we don't need this so get the data behind the id
            _id = list(trade.keys())
            trade = trade[_id[0]]
            if trade['pair'] not in self._trades.keys():
                self._trades[trade['pair']] = []
            trade['txid'] = _id
            self._trades[trade['pair']].append(trade)
        self._log.debug(f'Trades: {self._trades}')

    def trades(self, ws_name=None):
        if ws_name:
            if ws_name in self._trades.keys():
                return self._trades[ws_name]
            else:
                return None
        else:
            return self._trades