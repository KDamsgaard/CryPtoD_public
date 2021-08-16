"""
Project CryPtoD,
Copyright PogD april 2021,
Primary author: Kristian K. Damsgaard
"""
import logging
import time

import pymongo.errors

from modules.handlers.time_handler import TimeHandler
from modules.kraken_services.public_kraken_services import PublicKrakenServices
from modules.database_services.db_services import DBServices


class OdinDBS(DBServices):
    def __init__(self):
        super().__init__()
        self._log = logging.getLogger(self.__class__.__name__)
        self._public_kraken_services = PublicKrakenServices()

    def _create_database(self):
        """
        Sets up a new database, if none exists.
        :return: Operation success (bool)
        """
        db = self._primary
        db.settings.insert_one({'_id': 'system_settings',
                                'watched_pairs': [],
                                'analyzer_script_names': [],
                                'score_margin': 1,
                                'required_currency_components': ['EUR', 'USD']})
        db.settings.insert_one({'_id': 'pair_settings',
                                'retention': {'value': 6, 'denominator': 'h'},
                                'fees': {'maker': 0.16, 'taker': 0.26},
                                'benchmark': False})
        db.settings.insert_one({'_id': 'database_settings',
                                'clean_delay': 1,
                                'retention': {'value': 24, 'denominator': 'h'}})
        db.settings.insert_one({'_id': 'interface_settings',
                                'chart_update_interval': 2000,
                                'chart_display_seconds': 1 * 60 * 60})
        db.create_collection('users')
        db.create_collection('account')
        db.account.insert_one({'_id': 'wallet'})
        db.account.insert_one({'_id': 'orderbook', 'orders': []})
        db.account.insert_one({'_id': 'trades', 'trades': {}})

        self.insert_user(username='admin',
                         password='password',
                         permissions=0)
        self._log.warning(f"New admin user created with standard password - this should be changed!")
        self._log.info(f"Database \"{db.name}\" set up.")
        return True

    def insert_pair(self, pair_name):
        db = self._primary
        pair_data = self._public_kraken_services.fetch_pair_information(pair_name=pair_name)
        if not self.pair_collection_exists(pair_name=pair_name):
            collection = db[pair_name]

            info = {'_id': 'info',
                    'pair_name': pair_name,
                    'alt_name': pair_data['altname'],
                    'ws_name': pair_data['wsname']
                    }
            wallet = {'_id': 'wallet',
                      'purse': 100,
                      'coins': 0,
                      'profit': 0
                      }
            trades = {'_id': 'trades', 'list': []}
            analyses = {'_id': 'analyses', 'list': []}
            actions = {'_id': 'actions', 'list': []}

            collection.insert_one(info)
            collection.insert_one(wallet)
            collection.insert_one(trades)
            collection.insert_one(analyses)
            collection.insert_one(actions)
            self._log.info(f"Inserted collection \"{pair_name}\" into database \"{db.name}\"")

    def pair_collection_exists(self, pair_name):
        db = self._primary
        return pair_name in db.list_collection_names()

    def update_script_names(self, analyzer_script_names):
        self._primary.settings.update({'_id': 'system_settings'},
                                      {'$set': {'analyzer_script_names': analyzer_script_names}})

    def set_watched_pairs(self, pair_names):
        self._primary.settings.update_one({'_id': 'system_settings'}, {'$set': {'watched_pairs': pair_names}})

    def fetch_pair_info(self, pair_name):
        return self._primary[pair_name].find_one({'_id': 'info'})

    def fetch_system_settings(self):
        return self._primary.settings.find_one({'_id': 'system_settings'})

    def fetch_pair_settings(self, pair_name):
        settings = self._primary.settings.find_one({'_id': 'pair_settings'})
        factors = self._fetch_ultimate_factors_for_pair(pair_name=pair_name)
        if factors:
            settings['analyzer'] = factors[0]
            settings['score'] = factors[1]
            settings['factors'] = factors[2]
        return settings

    def _fetch_ultimate_factors_for_pair(self, pair_name):
        try:
            db = self.db(database_name="Mimir")
            fetched = db[pair_name].find_one({'_id': 'ultimate'})['result']
            analyzer = fetched['analyzer']
            scores = fetched['scores']
            factors = fetched['factors']
            return analyzer, scores, factors
        except KeyError as e:
            self._log.error(f"KeyError - {e}")
            return None
        except TypeError as e:
            self._log.error(f"TypeError - {e}")
            return None

    def fetch_ultimates(self):
        db = self.db(database_name="Mimir")
        collection_names = db.list_collection_names()
        result = {}
        for collection_name in collection_names:
            if collection_name not in self._not_pairs:
                ultimate = db[collection_name].find_one({'_id': 'ultimate'})['result']
                result[collection_name] = ultimate
        return result

    def fetch_ultimate_by_pair_name(self, pair_name):
        try:
            db = self.db(database_name="Mimir")
            return db[pair_name].find_one({'_id': 'ultimate'})['result']
        except KeyError as e:
            self._log.error(f"KeyError - {e}")
            return None
        except TypeError as e:
            self._log.error(f"TypeError - {e}")
            return None

    def fetch_pair_wallet(self, pair_name):
        return self._primary[pair_name].find_one({'_id': 'wallet'})

    def fetch_pair_trades(self, pair_name):
        try:
            db = self.db(database_name="Saerimner")
            return db[pair_name].find_one({'_id': 'trades'})['list']
        except KeyError as e:
            self._log.error(f"KeyError - {e}")
            return []
        except TypeError as e:
            self._log.error(f"TypeError - {e}")
            return []

    def fetch_pair_analyses(self, pair_name):
        try:
            return self._primary[pair_name].find_one({'_id': 'analyses'})['list']
        except KeyError as e:
            self._log.error(f"KeyError - {e}")
            return []
        except TypeError as e:
            self._log.error(f"TypeError - {e}")
            return []

    def fetch_pair_actions(self, pair_name):
        try:
            return self._primary[pair_name].find_one({'_id': 'actions'})['list']
        except KeyError as e:
            self._log.error(f"KeyError - {e}")
            return []
        except TypeError as e:
            self._log.error(f"TypeError - {e}")
            return []

    def fetch_last_pushed(self, pair_name, list_name):
        try:
            last_entry = self._primary[pair_name].find_one({'_id': list_name})['list'][-1]
        except IndexError:
            last_entry = []
        return last_entry

    def push_list_entry(self, pair_name, list_name, entry):
        try:
            self._primary[pair_name].update_one({'_id': list_name}, {'$push': {'list': entry}})
        except pymongo.errors.WriteError as e:
            self._log.error(f"While writing to {list_name}.{entry} >>> {e}")

    def clean_up_pair_data(self, pair_name, attribute):
        db = self._primary
        retention = self.database_settings['retention']
        retention_value = retention['value']
        retention_denominator = retention['denominator']
        timeframe = TimeHandler().to_seconds(value=retention_value,
                                             denominator=retention_denominator)
        timestamp = time.time() - timeframe
        result = db[pair_name].update_one({'_id': attribute}, {'$pull': {'list': {'time': {'$lt': timestamp}}}})
        if result.modified_count:
            self._log.info(f"Cleaned up {pair_name}")

    def update_purse(self, pair_name, new_purse):
        self._primary[pair_name].update_one({'_id': 'wallet'}, {'$set': {'purse': new_purse}})

    def update_coins(self, pair_name, new_coins):
        self._primary[pair_name].update_one({'_id': 'wallet'}, {'$set': {'coins': new_coins}})

    def update_profit(self, pair_name, new_profit):
        self._primary[pair_name].update_one({'_id': 'wallet'}, {'$set': {'profit': new_profit}})

    @staticmethod
    def _hours_to_seconds(hours):
        """
        Converts minutes to seconds for use when comparing timeframes with timestamps. Note that unix
        timestamps are created as seconds (IE: divides the timestamp by 1000), hence this function does not return
        milliseconds.

        :param hours: The amount of minutes to convert to seconds
        :return: Parameter "Minutes" in seconds
        """
        return hours * 60 * 60

    @property
    def watched_pairs(self):
        return self._primary.settings.find_one({'_id': 'system_settings'}, {'watched_pairs': 1})['watched_pairs']
