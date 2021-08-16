import logging
import threading
import time


class KrakenPrivateWalletService:
    def __init__(self, kraken_rest=None, init_asset=None, init_balance=None):
        self._log = logging.getLogger(self.__class__.__name__)
        self._kraken_rest = kraken_rest
        self._kraken_wallet = {}
        self._local_wallet = {}

        if init_asset and init_balance:
            # Init wallet with asset balance
            self._local_wallet[init_asset] = init_balance

        threading.Thread(target=self._exec).start()

    def _exec(self):
        if self._kraken_rest:
            self._log.info('Found connection to kraken REST API')
            self._log.info('Initializing wallet update thread')
            while True:
                self._fetch_account_balance()
                time.sleep(5)

    def _fetch_account_balance(self):
        """
        Fetch updated wallet balance from kraken
        If updated balance differs from local wallet
        update local wallet
        """
        # TODO: look for updates from kraken, to fetch wallet status from websocket

        self._log.info('Fetching new wallet data from kraken')
        _balance = self._kraken_rest.query_private('Balance')
        if _balance['error']:
            self._log.error(_balance['error'])
        else:
            if 'result' in _balance.keys():
                self._kraken_wallet = _balance['result']
                if self._local_wallet != self._kraken_wallet:
                    self._log.warning('Kraken wallet & local wallet balance mismatch! Updating local wallet')
                    self._local_wallet = self._kraken_wallet

    def balance(self, asset):
        """
        Get wallet balance for asset
        """
        # If asset does not exist in wallet, add the asset with balance = 0
        if asset not in self._local_wallet.keys():
            self._log.warning(f'Asset: {asset} not found in local wallet')
            self._log.info(f'Adding {asset}=0 to local wallet')
            self._local_wallet[asset] = 0

        return self._local_wallet[asset]

    def withdraw(self, asset, amount):
        self._local_wallet[asset] = float(self._local_wallet[asset]) - amount

    def deposit(self, asset, amount):
        self._local_wallet[asset] = float(self._local_wallet[asset]) + amount
