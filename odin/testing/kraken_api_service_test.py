"""
Project CryPtoD,
Copyright PogD april 2021,
Primary author: Søren B. Ølholm
"""

from odin.services.KrakenAPIService import KrakenWebSocketService
from odin.services.KrakenAPIService import KrakenWebSocketServiceCallbackManager
from odin.services.KrakenAPIService import PublicOrderbook
from odin.services.KrakenAPIService import PrivateAccountData
from pprint import pprint
import logging

logging.basicConfig(level=logging.INFO)
_log = logging.getLogger(__name__)

def _cb_trades(_list: list):
    pprint(_list)


def _private_orderstatus(_dict: dict):
    print('Orderstatus')
    pprint(_dict)

api_key = "HdDsCkiXNz6WNhgSBbvu90pPwUIj6XSdRfPEAQuFMTxttVB7yYX3tcpH"  # accessible on your Account page under Settings -> API Keys
api_secret = "3Pvisp9/ff9Er9Qd82KgMx5/I44Ixm5qt6D/s3a+iaj7c1DQyVAKLDswX/0Zy3DXmgcCYSX1/O31ctWOtLN/zA=="  # accessible on your Account page under Settings -> API Keys
timeout = 10
trace = False  # set to True for connection verbose logging

account = PrivateAccountData()
KrakenWebSocketService.FEED_PUBLIC_ORDERBOOK['depth'] = 10
public_orderbook = PublicOrderbook(depth=KrakenWebSocketService.FEED_PUBLIC_ORDERBOOK['depth'])
kwssman = KrakenWebSocketServiceCallbackManager(callback_public_trades=_cb_trades,
                                                callback_public_orderbook=public_orderbook.run,
                                                callback_private_orderstatus=_private_orderstatus,
                                                callback_private_orderbook=account.update_orderbook,
                                                callback_private_trades=account.update_trades)

kwss_private = KrakenWebSocketService(base_url=KrakenWebSocketService.URL_WS_API_PRIVATE,
                                        private=True,
                                        timeout=10,
                                        trace=trace,
                                        callback_manager=kwssman,
                                        api_key="HdDsCkiXNz6WNhgSBbvu90pPwUIj6XSdRfPEAQuFMTxttVB7yYX3tcpH",
                                        api_secret="3Pvisp9/ff9Er9Qd82KgMx5/I44Ixm5qt6D/s3a+iaj7c1DQyVAKLDswX/0Zy3DXmgcCYSX1/O31ctWOtLN/zA==")
account.set_wallet_callback(kwss_private.account_balance)

kwss_public = KrakenWebSocketService(base_url=KrakenWebSocketService.URL_WS_API_PUBLIC,
                                     timeout=10,
                                     trace=trace,
                                     callback_manager=kwssman)


#kwss_public.subscribe_public(KrakenWebSocketService.FEED_PUBLIC_ORDERBOOK, ['XBT/EUR'])

"""
import time
#time.sleep(10)
while True:
    print('Asks', public_orderbook.asks('XBT/EUR'))
    print('Bids', public_orderbook.bids('XBT/EUR'))
    time.sleep(5)
"""

kwss_private.subscribe_private(KrakenWebSocketService.FEED_PRIVATE_ORDERBOOK)
kwss_private.subscribe_private(KrakenWebSocketService.FEED_PRIVATE_TRADES)
#kwss_private.account_balance()

import time
time.sleep(2)
account.reset()

#print('Trades', account.trades())
#print('Book', account.orderbook())
#print('Wallet', account.wallet())

#time.sleep(5)
print('Add order')
kwss_private.add_buy_order('XRP/EUR', 0.1, 20)
#time.sleep(1)
#kwss_private.add_buy_order('XRP/EUR', 0.11, 22)

#print('Trades', account.trades())
#print('Book', account.orderbook())
#print('Wallet', account.wallet())

time.sleep(60)
print('Cancel orders')
kwss_private.cancel_orders()

time.sleep(5)
#print('Trades', account.trades())
#print('Book', account.orderbook())
#print('Wallet', account.wallet())

