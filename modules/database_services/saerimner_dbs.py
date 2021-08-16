"""
Project CryPtoD,
Copyright PogD april 2021,
Primary author: Kristian K. Damsgaard
"""
import logging
import time

import pymongo.errors

from modules.database_services.db_services import DBServices


class SaerimnerDBS(DBServices):
    def __init__(self):
        super().__init__()
        self._log = logging.getLogger(self.__class__.__name__)

    def _create_database(self):
        """
        Sets up a new database, if none exists.
        :return: Operation success (bool)
        """
        db = self._primary
        db.settings.insert_one({'_id': 'database_settings',
                                'note': 'clean_delay is given in minutes and retention in hours',
                                'clean_delay': 1,
                                'retention': 24})
        self._insert_all_pairs()
        self.insert_user(username='admin', password='password', permissions=0)
        self._log.warning(f"New admin user created with standard password - this should be changed!")
        self._log.info(f"Database \"{db.name}\" set up.")
        return True

    def _insert_all_pairs(self):
        assets = self._public_kraken_services.fetch_asset_pairs()
        for key in assets.keys():
            pair_name = key
            pair_data = assets[key]
            self._insert_pair(pair_name=pair_name, pair_data=pair_data)
            self._log.debug(f"Inserted {pair_name} into {self._primary}")

    def _insert_pair(self, pair_name, pair_data):
        try:
            db = self._primary
            if not self.pair_collection_exists(pair_name=pair_name):
                collection = db[pair_name]

                info = {'_id': 'info',
                        'pair_name': pair_name,
                        'alt_name': pair_data['altname'],
                        'ws_name': pair_data['wsname']
                        }
                trades = {'_id': 'trades', 'list': []}

                collection.insert_one(info)
                collection.insert_one(trades)
                # self._log.info(f"Inserted collection \"{pair_name}\" into database \"{self.db_name}\"")
        except KeyError as e:
            self._log.error(f"Key error: {e} - {pair_name}: {pair_data}")

    def pair_collection_exists(self, pair_name):
        db = self._primary
        return pair_name in db.list_collection_names()

    def push_trade(self, ws_name, entry):
        pair_name = self.fetch_pair_name_by_ws_name(ws_name=ws_name)
        if not pair_name:
            print(f"{ws_name} >>> {pair_name}")
        try:
            self._primary[pair_name].update_one({'_id': 'trades'}, {'$push': {'list': entry}})
            self._clean_up_pair_data(pair_name=pair_name)
        except pymongo.errors.WriteError as e:
            self._log.error(f"While writing to trades.{entry} >>> {e}")

    def _clean_up_pair_data(self, pair_name):
        db = self._primary
        setting = self.database_settings['retention']
        retention = self._hours_to_seconds(hours=setting)
        timestamp = time.time() - retention
        result = db[pair_name].update_one({'_id': 'trades'}, {'$pull': {'list': {'time': {'$lt': timestamp}}}})
        if result.modified_count:
            self._log.info(f"Cleaned up {pair_name}")

    def fetch_pair_name_by_ws_name(self, ws_name):
        db = self._primary
        for collection in db.list_collection_names():
            if collection not in self._not_pairs:
                info = db[collection].find_one({'_id': 'info'})
                if info['ws_name'] == ws_name:
                    return info['pair_name']
        return False

    def fetch_pair_info(self, pair_name):
        db = self._primary
        return db[pair_name].find_one({'_id': 'info'})

    def fetch_system_settings(self):
        db = self._primary
        return db.settings.find_one({'_id': 'system_settings'})

    def fetch_pair_trades(self, pair_name):
        db = self._primary
        return db[pair_name].find_one({'_id': 'trades'})

    @staticmethod
    def _hours_to_seconds(hours):
        """
        Converts a number of hours into corresponding number of seconds (hours * 60 minutes/hour * 60 seconds/minute)
        """
        return hours * 60 * 60
