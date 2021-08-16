import logging

class KrakenPrivateOrderbookService:
    def __init__(self):
        self._log = logging.getLogger(self.__class__.__name__)
        self._orderbook = {}

    def update(self, message):
        if type(message) == list:
            if 'openOrders' in message[1]:
                self._log.info(f'Found {message[1]} with {len(message[0])} entries')
                self._update_orderbook(message)

    def _update_orderbook(self, orders):
        orders = orders[0]
        for order in orders:
            # Trade starts with a trade id
            # First store the txid and then get orderdata from txid
            txid = list(order.keys())[0]
            order = order[txid]

            if 'status' in order.keys():
                # Clean up closed orders this goes for both filled and canceled orders
                if 'closed' in order['status'] or 'canceled' in order['status']:
                    self._remove_from_orderbook(txid)
                else:
                    # Make sure it's not a status message
                    # It will have a descr key if not status message
                    if 'descr' in order.keys():
                        # Check if pair exist in book
                        if order['descr']['pair'] not in self._orderbook.keys():
                            # If not then add it with empty list
                            self._orderbook[order['descr']['pair']] = []
                        # Add the txid to the order
                        order['txid'] = txid
                        # Add the order to list
                        self._orderbook[order['descr']['pair']].append(order)

    def _remove_from_orderbook(self, txid):
        for pair_name in self._orderbook.keys():
            for i, order in enumerate(self._orderbook[pair_name]):
                if order['txid'] == txid:
                    self._log.debug(f'Removing closed order {txid}')
                    del self._orderbook[pair_name][i]
                    break

    @property
    def orderbook(self):
        return self._orderbook