"""
Project CryPtoD,
Copyright PogD april 2021,
Primary author: Søren B. Ølholm
"""

## KrakenWebsSocketService based on Crypto Facilities Ltd Web Socket API Connector
## FROM https://github.com/CryptoFacilities/WebSocket-v1-Python

import json
import sys
# import krakenex #Required for REST calls
import krakenex
import websocket
from typing import Callable
from time import sleep
from threading import Thread
import logging
import traceback

from modules.database_services.db_services import DBServices
from modules.kraken_services.public_kraken_services import PublicKrakenServices
from modules.system_services.system_services import SystemServices


class PublicOrderbook:
    def __init__(self, depth):
        self._log = logging.getLogger(self.__class__.__name__)
        self._depth = depth
        self._orderbook = {}

    def run(self, book):
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

    def _update(self, ws_name, direction, order):
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
                        self._update(ws_name, 'asks', a_order)

        if 'b' in keys:
            if len(self._orderbook[ws_name]['bids']) >= self._depth:
                del self._orderbook[ws_name]['bids'][0]

            for b_order in orderbook['b']:
                b_order = self._translate(b_order)
                if not self._delete(ws_name, 'bids', b_order):
                    if not self._insert(ws_name, 'bids', b_order):
                        self._update(ws_name, 'bids', b_order)


class PrivateAccountData:
    def __init__(self):
        self._log = logging.getLogger(self.__class__.__name__)
        self._db_services = DBServices()
        self.callback_wallet = None
        self._wallet = None
        self._trades = {}
        self._orderbook = {}

    def set_wallet_callback(self, callback_wallet):
        self.callback_wallet = callback_wallet
        self._update_wallet()

    def _update_wallet(self):
        _wallet = self.callback_wallet()['wallet']
        keys = _wallet.keys()
        for k in keys:
            _wallet[k] = float(_wallet[k])
            # Need to remove any "staking" assets from wallet
            # These are for internal use in kraken, but will appear in the wallet
            if not '.S' in k:
                self._db_services.update_private_wallet(k, float(_wallet[k]))
        self._wallet = _wallet
        self._log.debug(f'New wallet: {self._wallet}')

    def update_trades(self, trades):
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
            self._db_services.update_private_trades(trade['pair'], trade)
            self._remove_from_orderbook(_id)

        self._update_wallet()
        self._log.debug(f'Trades: {self._trades}')

    def update_orderbook(self, orders):
        orders = orders[0]
        for order in orders:
            # Trade starts with a trade id
            # we don't need this so get the data behind the id
            txid = list(order.keys())[0]
            order = order[txid]

            if 'status' in order.keys():
                # Clean up closed orders this goes for both filled and canceled orders
                if 'closed' in order['status'] or 'canceled' in order['status']:
                    self._remove_from_orderbook(txid)
                else:
                    # Make sure it's not a status message
                    if 'descr' in order.keys():
                        if order['descr']['pair'] not in self._orderbook.keys():
                            self._orderbook[order['descr']['pair']] = []
                        order['txid'] = txid
                        self._orderbook[order['descr']['pair']].append(order)
                        self._db_services.insert_private_orderbook(order)


        self._update_wallet()
        self._log.debug(f'Orderbook: {self._orderbook}')

    def _remove_from_orderbook(self, txid):
        self._db_services.remove_private_orderbook(txid)

        for pair_name in self._orderbook.keys():
            for i, order in enumerate(self._orderbook[pair_name]):
                if order['txid'] == txid:
                    self._log.debug(f'Removing closed order {txid}')
                    del self._orderbook[pair_name][i]
                    break


    def reset(self):
        self._orderbook = {}
        self._trades = {}

    def trades(self, ws_name=None):
        if ws_name:
            if ws_name in self._trades.keys():
                return self._trades[ws_name]
            else:
                return None
        else:
            return self._trades

    def orderbook(self, ws_name=None):
        if ws_name:
            if ws_name in self._orderbook.keys():
                return self._orderbook[ws_name]
            else:
                return None
        else:
            return self._orderbook

    def wallet(self, asset_pair=None):
        if asset_pair:
            asset = self._find_wallet_currency(asset_pair)
            if asset:
                amount = self._wallet[asset]
                self._log.debug(f'Wallet> Pair: {asset_pair}/{asset} amount: {amount}')
                return amount
            else:
                return 0
        else:
            return self._wallet

    def _find_wallet_currency(self, asset_pair):
        """
        We need to locate the matching coin from the asset pair name
        by finding the coin that matches part of the asset pair name
        """
        _asset = None
        assets = self._wallet.keys()
        for asset in assets:
            #if asset in asset_pair:
            if asset_pair in asset:
                _asset = asset
                break
        return _asset

class KrakenWebSocketServiceCallbackManager:
    def __init__(self,
                 callback_public_trades: Callable = None,
                 callback_public_orderbook: Callable = None,
                 callback_private_trades: Callable = None,
                 callback_private_orderbook: Callable = None,
                 callback_private_orderstatus: Callable = None,
                 callback_open: Callable = None,
                 callback_close: Callable = None,
                 callback_error: Callable = None):
        """
        :param callback_public_trades(list): callback method for public trades data
        :param callback_public_orderbook(list): callback method for public orderbook data
        :param callback_private_trades(list): callback method for private trades data
        :param callback_private_orderbook(list): callback method for private orderbook data
        :param callback_private_orderstatus(dict): callback method for private orderbook data
        :param callback_open(str): callback method for websocket open message
        :param callback_close(str): callback method for websocket close message
        :param callback_error(str): callback method for websocket error message
        """
        self._log = logging.getLogger(self.__class__.__name__)
        self._public_trades = callback_public_trades
        self._public_orderbook = callback_public_orderbook
        self._private_trades = callback_private_trades
        self._private_orderbook = callback_private_orderbook
        self._private_orderstatus = callback_private_orderstatus
        self._open = callback_open
        self._close = callback_close
        self._error = callback_error

    def __message_type(self, message):
        """
        Figures out what type of data was returned from the websocket and calls the correct type of callback
        :param message: str
        """
        #print(message)
        message = json.loads(message)
        if type(message) == list:
            if 'trade' in message[2]:
                if self._public_trades:
                    self._public_trades(message)
            if 'book' in message[2]:
                if self._public_orderbook:
                    self._public_orderbook(message)
            if 'ownTrades' in message[1]:
                if self._private_trades:
                    self._private_trades(message)
            if 'openOrders' in message[1]:
                if self._private_orderbook:
                    self._private_orderbook(message)

        if type(message) == dict:
            keys = message.keys()
            if 'event' in keys:
                if 'addOrderStatus' in message['event']:
                    if self._private_orderstatus:
                        self._private_orderstatus(message)
                if 'cancelOrderStatus' in message['event']:
                    if self._private_orderstatus:
                        self._private_orderstatus(message)
                if 'cancelAllStatus' in message['event']:
                    if self._private_orderstatus:
                        self._private_orderstatus(message)


    def service_callback_open(self, function, message):
        if self._open:
            self._open(message)
        else:
            self._log.warning('Open> No callback available')
            self._log.debug(f'Open[{function}]> {message}')

    def service_callback_close(self, function, message):
        if self._close:
            self._close(message)
        else:
            self._log.warning('Close> No callback available')
            self._log.warning(f'Close[{function}]> {message}')

    def service_callback_error(self, function, message):
        if self._error:
            self._error(message)
        else:
            self._log.warning('Error> No callback available')
            self._log.error(f'Error[{function}]> {message}')

    def service_callback_message(self, function, message):
        self._log.debug(f'Message> {message}')
        try:
            self.__message_type(message)
        except Exception as e:
            self._log.error(message)
            self.service_callback_error(f'service_callback_message->{function}', traceback.print_exc())


class KrakenWebSocketService(object):
    """P&D Software's Kraken Web Socket API connector"""
    """Based on: Crypto Facilities Ltd Web Socket API Connector"""

    URL_WS_API_PUBLIC = 'wss://ws.kraken.com/'
    URL_WS_API_PRIVATE = 'wss://ws-auth.kraken.com/'

    FEED_HEARTBEAT = {'name': 'heartbeat'}
    FEED_PUBLIC_TRADES = {'name': 'trade'}
    FEED_PUBLIC_ORDERBOOK = {'name': 'book', 'depth': 100}
    # TODO: implement solution for this via REST
    #FEED_PRIVATE_BALANCE = {'name': 'balance'} # Account balance not available through WS api
    FEED_PRIVATE_TRADES = {'name': 'ownTrades', 'token': None}
    FEED_PRIVATE_ORDERBOOK = {'name': 'openOrders', 'token': None}
    REQUEST_PRIVATE_ADD_ORDER_BUY = {"event": "addOrder",
                                      "ordertype": "limit",
                                      "pair": None,
                                      "price": 0,
                                      "token": None,
                                      "type": "buy",
                                      "volume": 0}
    REQUEST_PRIVATE_ADD_ORDER_SELL = {"event": "addOrder",
                                     "ordertype": "limit",
                                     "pair": None,
                                     "price": 0,
                                     "token": None,
                                     "type": "sell",
                                     "volume": 0}
    REQUEST_PRIVATE_CANCEL_ORDER = {"event": "cancelOrder",
                                      "token": None,
                                      "txid": []}
    REQUEST_PRIVATE_CANCEL_ORDER_ALL = {"event": "cancelAll",
                                        "token": None}

    # Special Methods
    def __init__(self, base_url: str,
                        private: bool = False,
                        timeout: int = 10,
                        trace: bool = False,
                        callback_manager: Callable = None,
                        api_key: str = None,
                        api_secret: str = None):

        websocket.enableTrace(trace)
        self._log = logging.getLogger(self.__class__.__name__)
        self.base_url = base_url
        self.api_key = None
        self.api_secret = None
        self.timeout = timeout

        self.ws = None
        #self.kraken_rest = krakenex.API(self.api_key, self.api_secret)
        self.original_challenge = None
        self.signed_challenge = None
        self.challenge_ready = False
        self._token = None
        self._callback_manager = callback_manager

        if private:
            if api_key and api_secret:
                self.api_key = api_key
                self.api_secret = api_secret
            else:
                settings = SystemServices().fetch_kraken_keys_settings()
                self.api_key = settings['api_key']
                self.api_secret = settings['api_secret']
            self.kraken_rest = krakenex.API(self.api_key, self.api_secret)

            if self.api_key and self.api_secret:
                self.__request_token()
                if self._token:
                    # Make token available to all private requests
                    KrakenWebSocketService.REQUEST_PRIVATE_ADD_ORDER_BUY['token'] = self._token
                    KrakenWebSocketService.REQUEST_PRIVATE_ADD_ORDER_SELL['token'] = self._token
                    KrakenWebSocketService.REQUEST_PRIVATE_CANCEL_ORDER['token'] = self._token
                    KrakenWebSocketService.REQUEST_PRIVATE_CANCEL_ORDER_ALL['token'] = self._token
                    KrakenWebSocketService.FEED_PRIVATE_TRADES['token'] = self._token
                    KrakenWebSocketService.FEED_PRIVATE_ORDERBOOK['token'] = self._token
                    #self.__connect()
                else:
                    if self._callback_manager:
                        self._callback_manager.service_callback_error('__init__', 'Token for private API calls could not be acquired')
                    else:
                        self._log.error('Token for private API calls could not be acquired')
        # else:
        #     self.__connect()
        self.__connect()

    # Public feeds
    def subscribe_public(self, feed, ws_names=None):
        """Subscribe to given feed and product ids"""

        if ws_names is None:
            request_message = {
                "event": "subscribe",
                "subscription": feed
            }
        else:
            request_message = {
                "event": "subscribe",
                "subscription": feed,
                "pair": ws_names
            }

        self._log.debug("public subscribe to %s", feed['name'])

        request_json = json.dumps(request_message)
        self.ws.send(request_json)

    def unsubscribe_public(self, feed, ws_names=None):
        """UnSubscribe to given feed and product ids"""
        if ws_names is None:
            request_message = {
                "event": "subscribe",
                "subscription": feed
            }
        else:
            request_message = {
                "event": "subscribe",
                "subscription": feed,
                "pair": ws_names
            }

        self._log.debug("public unsubscribe to %s", feed['name'])
        request_json = json.dumps(request_message)
        self.ws.send(request_json)

    # Private feeds
    def subscribe_private(self, feed):
        """Subscribe to feed"""

        # If auth token exists
        if self.challenge_ready:
            feed['token'] = self._token
            request_message = {"event": "subscribe",
                               'subscription': feed}

            self._log.debug("private subscribe to %s", feed)

            request_json = json.dumps(request_message)
            self.ws.send(request_json)
        else:
            if self._callback_manager:
                self._callback_manager.service_callback_error('subscribe_private', 'Not enabled to do private API calls')
            else:
                self._log.error('Not enabled to do private API calls')

    def unsubscribe_private(self, feed):
        """Unsubscribe to feed"""

        # If auth token exists
        if self.challenge_ready:
            feed['token'] = self._token
            request_message = {"event": "subscribe",
                               'subscription': feed}

            self._log.debug("private unsubscribe to %s", feed)

            request_json = json.dumps(request_message)
            self.ws.send(request_json)
        else:
            if self._callback_manager:
                self._callback_manager.service_callback_error('unsubscribe_private', 'Not enabled to do private API calls')
            else:
                self._log.error('Not enabled to do private API calls')

    def add_buy_order(self, pair, price, volume):
        order = KrakenWebSocketService.REQUEST_PRIVATE_ADD_ORDER_BUY
        order['pair'] = pair
        order['price'] = str(price)
        order['volume'] = str(volume)
        self.ws.send(json.dumps(order))

    def add_sell_order(self, pair, price, volume):
        order = KrakenWebSocketService.REQUEST_PRIVATE_ADD_ORDER_SELL
        order['pair'] = pair
        order['price'] = str(price)
        order['volume'] = str(volume)
        self.ws.send(json.dumps(order))

    def cancel_orders(self):
        self.ws.send(json.dumps(KrakenWebSocketService.REQUEST_PRIVATE_CANCEL_ORDER_ALL))

    def account_balance(self):
        # TODO: look for updates from kraken, to fetch wallet status from websocket
        # This is a special case!
        # For callback manager to accept data, it needs to be json.dumps()
        # because kraken_rest returns as dict or list
        #_balance = json.dumps(self.kraken_rest.query_private('Balance'))
        _balance = self.kraken_rest.query_private('Balance')['result']
        _wallet = {'wallet': _balance}
        self.__on_message(json.dumps(_wallet))
        return _wallet


    """"""""""""""""""""""""""""""" -> CONNECTION AND MESSAGE HANDLING -> """""""""""""""""""""""""""""""""""""""
    def __connect(self):
        """Establish a web socket connection"""
        self.ws = websocket.WebSocketApp(self.base_url,
                                         on_message=self.__on_message,
                                         on_close=self.__on_close,
                                         on_open=self.__on_open,
                                         on_error=self.__on_error,
                                         )

        self.wst = Thread(target=lambda: self.ws.run_forever(ping_interval=30))
        self.wst.daemon = True
        self.wst.start()

        # Wait for connect before continuing
        conn_timeout = self.timeout
        while (not self.ws.sock or not self.ws.sock.connected) and conn_timeout:
            sleep(1)
            conn_timeout -= 1

        if not conn_timeout:
            self._log.debug("Couldn't connect to", self.base_url, "! Exiting.")
            sys.exit(1)

    def __on_open(self):
        self._log.debug("Connected to %s", self.base_url)

        if self._callback_manager:
            self._callback_manager.service_callback_open('__on_open', f'Connected to {self.base_url}')
        else:
            self._log.warning('No callback manager')

    def __on_message(self, message):
        """Listen the web socket connection. Block until a message
        arrives. """

        try:
            #message_json = json.loads(message)
            self._log.debug(message)

            if self._callback_manager:
                self._callback_manager.service_callback_message('__on_message', message)
            else:
                self._log.warning('No callback manager')
        except Exception as e:
            if self._callback_manager:
                self._callback_manager.service_callback_error('__on_message',  traceback.print_exc())
            else:
                self._log.error(e)

    def __on_close(self):
        self._log.info('Connection closed')

        if self._callback_manager:
            self._callback_manager.service_callback_close('__on_close', 'Connection closed')
        else:
            self._log.warning('No callback manager')

    def __on_error(self, error):
        self._log.error(error)

        if self._callback_manager:
            self._callback_manager.service_callback_error('__on_error', error)
        else:
            self._log.warning('No callback manager')

    def __wait_for_challenge_auth(self):
        self.__request_challenge()

    def __request_token(self):
        ## Code provided by kraken
        ## From: https://support.kraken.com/hc/en-us/articles/360034437672
        import time, base64, hashlib, hmac, urllib.request, json

        api_nonce = bytes(str(int(time.time() * 1000)), "utf-8")
        api_request = urllib.request.Request("https://api.kraken.com/0/private/GetWebSocketsToken",
                                             b"nonce=%s" % api_nonce)
        api_request.add_header("API-Key", self.api_key)
        api_request.add_header("API-Sign", base64.b64encode(
            hmac.new(base64.b64decode(self.api_secret),
                     b"/0/private/GetWebSocketsToken" + hashlib.sha256(api_nonce + b"nonce=%s" % api_nonce).digest(),
                     hashlib.sha512).digest()))

        # For some reason calling:
        # json.loads(urllib.request.urlopen(api_request).read())['result']['token']
        # does not work as in the example
        token_obj = json.loads(urllib.request.urlopen(api_request).read())
        #print(token_obj['result'])
        self._token = token_obj['result']['token']
        self.challenge_ready = True
        self._log.debug(f'API token generated: {self._token}')



## TODO: should this be redone to exist fully in here?
def ws_names_from_kraken_api():

    pks = PublicKrakenServices()
    asset_pairs = pks.fetch_asset_pairs()
    keys = asset_pairs.keys()
    ws_names = []
    for key in keys:
        if 'wsname' in asset_pairs[key]:
            ws_names.append(asset_pairs[key]['wsname'])
    return ws_names

def subscribe_trades(kwss_public):
    ws_names = ws_names_from_kraken_api()
    if ws_names:
        kwss_public.subscribe_public(KrakenWebSocketService.FEED_PUBLIC_TRADES, ws_names)
        kwss_public.subscribe_public(KrakenWebSocketService.FEED_PUBLIC_ORDERBOOK, ws_names)