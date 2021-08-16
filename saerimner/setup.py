"""
Project CryPtoD,
Copyright PogD april 2021,
Primary author: Kristian K. Damsgaard
"""

import logging

from modules.database_services.saerimner_dbs import SaerimnerDBS
from modules.system_services.log_services import LogServices
from modules.system_services.system_services import SystemServices


class Setup:
    """
    Class for controlling setting up and tearing down CryPtoD database, initializing log, etc.
    """
    def __init__(self):
        self._log_services = LogServices()
        self._log = logging.getLogger(self.__class__.__name__)
        self._system_services = SystemServices()
        self._db_services = SaerimnerDBS()

    @property
    def db_services(self):
        return self._db_services
