import logging

class KrakenPublicTradesService:
    def __init__(self, callback):
        self._log = logging.getLogger(self.__class__.__name__)
        self._callback = callback
        self._trades = []

    def __debug(self, message):
        self._log.info(message)

    def update(self, message):
        if type(message) == list:
            if 'trade' in message[2]:
                self._log.debug(f'Found {len(message[1])} incomming trades')
                if self._callback:
                    self._callback(message)
                else:
                    self.__debug(message)
