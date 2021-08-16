import sys
import json
import krakenex
import websocket
import traceback
import logging
from typing import Callable
from threading import Thread
from time import sleep
#from services.system_services import SystemServices
from modules.kraken_services.public_kraken_services import PublicKrakenServices

class KrakenWebSocketService:
    """
    Use this it initialize public and private websockets
    """
    URL_WS_API_PUBLIC = 'wss://ws.kraken.com/'
    URL_WS_API_PRIVATE = 'wss://ws-auth.kraken.com/'

    FEED_HEARTBEAT = {'name': 'heartbeat'}
    FEED_PUBLIC_TRADES = {'name': 'trade'}
    FEED_PUBLIC_ORDERBOOK = {'name': 'book', 'depth': 100}
    # TODO: implement solution for this via REST
    # FEED_PRIVATE_BALANCE = {'name': 'balance'} # Account balance not available through WS api
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


    def __init__(self, api_key=None, api_secret=None):
        self._log = logging.getLogger(self.__class__.__name__)
        self._api_key = api_key
        self._api_secret = api_secret
        self._public = None
        self._private = None
        self._rest = None
        self._initialize()

    def _initialize(self):
        self._public = _KrakenWebSocketService(base_url=KrakenWebSocketService.URL_WS_API_PUBLIC,
                                               timeout=10,
                                               trace=False)
        if self._api_key and self._api_secret:
            import binascii
            try:
                self._private = _KrakenWebSocketService(base_url=KrakenWebSocketService.URL_WS_API_PRIVATE,
                                                        private=True,
                                                        timeout=10,
                                                        trace=False,
                                                        api_key=self._api_key,
                                                        api_secret=self._api_secret)
            except binascii.Error:
                self._log.error(f"Erroneous API key given - private websocket is not available!")

        self._rest = PublicKrakenServices()

    @property
    def public(self):
        return self._public

    @property
    def private(self):
        if not self._private:
            self._log.error(f"Private websocket is None, private actions are not available!")

        return self._private

    @property
    def public_rest(self):
        return self._rest

    def __chunks(self, lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    def subscribe_assets(self):
        asset_pairs = self.public_rest.fetch_asset_pairs()
        keys = asset_pairs.keys()
        ws_names = []
        for key in keys:
            if 'wsname' in asset_pairs[key]:
                ws_names.append(asset_pairs[key]['wsname'])

        if ws_names:
            buckets = self.__chunks(ws_names, 100)
            self._log.info(f'Subscribing to {len(ws_names)} assets')
            for bucket in buckets:
                self._public.subscribe_public(KrakenWebSocketService.FEED_PUBLIC_TRADES, bucket)
                self._public.subscribe_public(KrakenWebSocketService.FEED_PUBLIC_ORDERBOOK, bucket)
                sleep(0.1)


class _KrakenWebSocketService(object):
    """P&D Software's Kraken Web Socket API connector"""
    """Based on: Crypto Facilities Ltd Web Socket API Connector"""

    def __init__(self, base_url: str,
                        private: bool = False,
                        timeout: int = 10,
                        trace: bool = False,
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

        self._message_callbacks = []
        self.kraken_rest = krakenex.API()

        if private:
            if api_key and api_secret:
                self.api_key = api_key
                self.api_secret = api_secret
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
                else:
                    self._log.error('Token for private API calls could not be acquired')
        self.__connect()

    def add_message_callback(self, callback):
        self._message_callbacks.append(callback)

    def _process_message_callbacks(self, message):
        """
        Each time a new message is received from the websocket
        Run all callbacks with message as input
        """
        try:
            message = json.loads(message)
        except Exception as e:
            #print(Exception, e)
            traceback.print_exc()
            message = None

        if message:
            #self._log.info(f'Sending message to {len(self._message_callbacks)} callbacks ({message})')
            if self._message_callbacks:
                for callback in self._message_callbacks:
                    try:
                        callback(message)
                    except Exception as e:
                        traceback.print_exc()


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
            self._log.error('Not enabled to do private API calls')

    def add_buy_order(self, pair, price, volume):
        def order_timeout(self):
            import time
            now = time.time()
            passed = time.time() - now
            while(passed < 10):
                passed = time.time() - now
                print(f"Order timeout in {(10-passed)}")
                time.sleep(2)
            self.cancel_orders()

        order = KrakenWebSocketService.REQUEST_PRIVATE_ADD_ORDER_BUY
        order['pair'] = pair
        order['price'] = str(price)
        order['volume'] = str(volume)
        self.ws.send(json.dumps(order))

        import threading
        threading.Thread(target=order_timeout, args=[self]).start()

    def add_sell_order(self, pair, price, volume):
        def order_timeout(self):
            import time
            now = time.time()
            passed = time.time() - now
            while(passed < 10):
                passed = time.time() - now
                print(f"Order timeout in {(10-passed)}")
                time.sleep(2)
            self.cancel_orders()

        order = KrakenWebSocketService.REQUEST_PRIVATE_ADD_ORDER_SELL
        order['pair'] = pair
        order['price'] = str(price)
        order['volume'] = str(volume)
        self.ws.send(json.dumps(order))

        import threading
        threading.Thread(target=order_timeout, args=[self]).start()

    def cancel_orders(self):
        self.ws.send(json.dumps(KrakenWebSocketService.REQUEST_PRIVATE_CANCEL_ORDER_ALL))

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
        #self.wst = Thread(target=self.ws_thread)
        self.wst.daemon = True
        self.wst.start()

        # Wait for connect before continuing
        conn_timeout = self.timeout
        while (not self.ws.sock or not self.ws.sock.connected) and conn_timeout:
            sleep(1)
            conn_timeout -= 1

        if not conn_timeout:
            self._log.info("Couldn't connect to", self.base_url, "! Exiting.")
            sys.exit(1)

    def ws_thread(self):
        self.ws.run_forever(ping_interval=30)

    def __on_open(self):
        self._log.info("Connected to %s", self.base_url)

    def __on_message(self, message):
        """Listen the web socket connection. Block until a message
        arrives. """
        #self._log.info("New message from websocket")
        #self._log.info(message)
        self._process_message_callbacks(message=message)

    def __on_close(self):
        self._log.info('Websocket connection closed')

    def __on_error(self, error):
        self._log.error(f'Websocket error: {error}')

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

    @property
    def rest_api(self):
        return self.kraken_rest

    @property
    def fetch_asset_pairs(self):
        return self.kraken_rest.query_public('AssetPairs')

    @property
    def ws_names(self):
        asset_pairs = self.fetch_asset_pairs
        keys = asset_pairs.keys()
        ws_names = []
        for key in keys:
            if 'wsname' in asset_pairs[key]:
                ws_names.append(asset_pairs[key]['wsname'])
        return ws_names