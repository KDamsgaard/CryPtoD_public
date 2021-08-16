from threading import Thread
import logging
import traceback

class KrakenPublicOrderbookService:
    def __init__(self, depth):
        self._log = logging.getLogger(self.__class__.__name__)
        self._depth = depth
        self._orderbook = {}

    def update(self, message):
        if type(message) == list:
            if 'book' in message[2]:
                #self._log.info(f'Found public orderbook')
                self._update(message)

    def _update(self, book):
        if type(book) is list:
            if type(book[1]) is dict:
                # Get ws name
                ws_name = book[3]
                # Get book entries
                orderbook = book[1]
                # Add orderbooks if they do not exist
                self._add_orderbook(ws_name)
                # Create snapshot of books if provided
                self._snapshot_book(ws_name=ws_name, orderbook=orderbook)
                # Manage orderbook entries
                self._manage_book(ws_name=ws_name, orderbook=orderbook)

    def asks(self, ws_name):
        """
        Returns ask direction for ws name
        return: list[dict]
        """
        if ws_name in self._orderbook.keys():
            return sorted(self._orderbook[ws_name]['asks'], key=lambda i: i['price'], reverse=False)
        else:
            return None

    def bids(self, ws_name):
        """
        Returns bid direction for ws name
        return: list[dict]
        """
        if ws_name in self._orderbook.keys():
            return sorted(self._orderbook[ws_name]['bids'], key=lambda i: i['price'], reverse=True)
        else:
            return None

    def _translate(self, order):
        return {
            'price': float(order[0]),
            'volume': float(order[1]),
            'time': float(order[2])
        }

    def _add_orderbook(self, ws_name):
        if ws_name not in self._orderbook.keys():
            self._log.debug(f'Adding {ws_name} to orderbook')
            self._orderbook[ws_name] = {'asks': [], 'bids': []}

    def _find_price_level(self, ws_name, direction, price_level):
        index = None
        if ws_name in self._orderbook.keys():
            for i, order in enumerate(self._orderbook[ws_name][direction]):
                if order['price'] == price_level:
                    index = i
                    break
            return index
        else:
            return None

    def _insert(self, ws_name, direction, order):
        index = None
        for i, page in enumerate(self._orderbook[ws_name][direction]):
            if page['price'] == order['price']:
                index = i
                break
        if not index:
            self._orderbook[ws_name][direction].append(order)
            return True
        else:
            return False

    def _update_book_direction(self, ws_name, direction, order):
        index = None
        for i, page in enumerate(self._orderbook[ws_name][direction]):
            if page['price'] == order['price']:
                index = i
                break
        if index:
            self._orderbook[ws_name][direction][index] = order
            return True
        else:
            return False

    def _delete(self, ws_name, direction, order):
        if order['volume'] == 0.0:
            index = None
            for i, page in enumerate(self._orderbook[ws_name][direction]):
                if page['price'] == order['price']:
                    index = i
                    break
            if index:
                del self._orderbook[ws_name][direction][index]
            return True
        else:
            return False

    def _snapshot_book(self, ws_name, orderbook):
        keys = orderbook.keys()
        if 'as' in keys and 'bs' in keys:
            # if as and bs exist = Is snapshot
            for ask in orderbook['as']:
                self._orderbook[ws_name]['asks'].append(self._translate(ask))

            for bid in orderbook['bs']:
                self._orderbook[ws_name]['bids'].append(self._translate(bid))

            return True
        else:
            return False

    def _manage_book(self, ws_name, orderbook):
        keys = orderbook.keys()

        if 'a' in keys:
            if len(self._orderbook[ws_name]['asks']) >= self._depth:
                del self._orderbook[ws_name]['asks'][0]

            for a_order in orderbook['a']:
                a_order = self._translate(a_order)
                if not self._delete(ws_name, 'asks', a_order):
                    if not self._insert(ws_name, 'asks', a_order):
                        self._update_book_direction(ws_name, 'asks', a_order)

        if 'b' in keys:
            if len(self._orderbook[ws_name]['bids']) >= self._depth:
                del self._orderbook[ws_name]['bids'][0]

            for b_order in orderbook['b']:
                b_order = self._translate(b_order)
                if not self._delete(ws_name, 'bids', b_order):
                    if not self._insert(ws_name, 'bids', b_order):
                        self._update_book_direction(ws_name, 'bids', b_order)

    @property
    def orderbook(self):
        return self._orderbook