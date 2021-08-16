
import logging
import pytz

from datetime import datetime
from tzlocal import get_localzone


class TimeHandler:
    """
    Contains various methods for handling timestamps and datetime objects as well as converting days/hours/minutes into
    equivalent seconds.
    """
    def __init__(self):
        self._log = logging.getLogger(self.__class__.__name__)

    def to_seconds(self, value, denominator):
        """
        This method takes a value and denominator and returns the corresponding amount of seconds.
        """
        if value <= 0:
            self._log.error(f"to_seconds() was passed a negative or zero value.")

        if denominator == "d":
            return value * 60 * 60 * 24
        elif denominator == "h":
            return value * 60 * 60
        elif denominator == "m":
            return value * 60
        else:
            self._log.error("to_seconds() was passed an unknown denominator (must be \"d\", \"h\" or \"m\").")

    @staticmethod
    def aware_utc_from_timestamp(timestamp):
        """
        Takes a unix timestamp and returns a timezone aware datetime object for the UTC timezone.
        """
        return datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)

    @staticmethod
    def aware_local_from_timestamp(timestamp):
        """
        Takes a unix timestamp and returns a timezone aware datetime object for the computer-local timezone.
        """
        return datetime.fromtimestamp(timestamp).astimezone(get_localzone())

    @staticmethod
    def local_zone():
        """
        Returns a descriptive string for the local timezone.
        """
        return get_localzone()
