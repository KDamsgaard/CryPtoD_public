"""
Project CryPtoD,
Copyright PogD april 2021,
Primary author: Kristian K. Damsgaard
"""

import json
import logging
import requests


class PublicKrakenServices:
    def __init__(self):
        self._log = logging.getLogger(self.__class__.__name__)

    @staticmethod
    def fetch_trades(pair: str, since: float = None):
        query = "https://api.kraken.com/0/public/Trades"

        params = {}
        if since:
            params['since'] = since
        params['pair'] = pair

        res = requests.post(url=query, data=params)
        if not res.status_code == 200:
            logging.warning(f"KrakenHandler.fetch_trades() >>> Endpoint unreachable (code: {res.status_code})")

        else:
            data = json.loads(res.content)
            if data['error']:
                logging.error(f"KrakenHandler.fetch_trades() >>> Unable to fetch trades (message: {data['error']})")
            else:
                data = data['result']
                return data

        return False

    @staticmethod
    def fetch_asset_pairs():
        query = "https://api.kraken.com/0/public/AssetPairs"
        try:
            res = requests.get(url=query)
            if not res.status_code == 200:
                logging.warning(f"KrakenHandler.fetch_asset_pairs() >>> Endpoint unreachable (code: {res.status_code})")
            else:
                data = json.loads(res.content)
                if data['error']:
                    logging.error(f"KrakenHandler.fetch_asset_pairs() >>> Unable to fetch asset pairs (message: "
                                  f"{data['error']})")
                else:
                    data = data['result']
                    return data
            return False

        except Exception as e:
            logging.error(f"KrakenHandler.fetch_asset_pairs() >>> {query}, {e}")
            return False

    def fetch_pair_information(self, pair_name):
        query = "https://api.kraken.com/0/public/AssetPairs?pair=" + pair_name
        try:
            res = requests.get(url=query)
            if not res.status_code == 200:
                self._log.warning(f"Endpoint unreachable (code: {res.status_code})")
            else:
                data = json.loads(res.content)
                if data['error']:
                    logging.error(f"Unable to fetch asset pairs (message: {data['error']})")
                else:
                    data = data['result'][pair_name]
                    return data
            return False

        except Exception as e:
            self._log.error(f"{query}, {e}")
            return False

    @staticmethod
    def fetch_orderbook_for_pair(pair_name):
        query = f"https://api.kraken.com/0/public/Depth?pair={pair_name}"

        try:
            res = requests.post(url=query)
            if not res.status_code == 200:
                logging.warning(f"KrakenHandler.fetch_orderbook() >>> Endpoint unreachable (code: {res.status_code})")
            else:
                data = json.loads(res.content)
                if data['error']:
                    logging.error(f"KrakenHandler.fetch_orderbook() >>> Unable to fetch orderbook (message: "
                                  f"{data['error']})")
                else:
                    data = data['result']
                    return data
            return False

        except Exception as e:
            logging.error(f"KrakenHandler.fetch_orderbook() >>> {query}, {e}")
            return False

    def get_orderbook(self, pair_name):
        #return _KrakenOrderbook(self.fetch_orderbook(pair_name)[pair_name])
        return self.fetch_orderbook_for_pair(pair_name)[pair_name]


class _KrakenOrderbook:
    def __init__(self, orderbook):
        self.orderbook = orderbook

    def lowest_ask(self):
        return self.orderbook['asks'][0]

    def highest_ask(self):
        return self.orderbook['asks'][-1]

    def lowest_bid(self):
        return self.orderbook['bids'][-1]

    def highest_bid(self):
        return self.orderbook['bids'][0]
