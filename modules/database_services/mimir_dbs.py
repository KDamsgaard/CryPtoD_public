"""
Project CryPtoD,
Copyright PogD april 2021,
Primary author: Kristian K. Damsgaard
"""
import logging

from modules.database_services.db_services import DBServices


class MimirDBS(DBServices):
    def __init__(self):
        super().__init__()
        self._log = logging.getLogger(self.__class__.__name__)
        self._ignore = ['settings', 'users']

    def _create_database(self):
        primary = self._primary_name
        db = self.db(database_name=primary)
        db.settings.insert_one({'_id': 'system_settings',
                                'analyzer_name': 'mid_range_activation',
                                'iteration_length': 10,
                                'exploration_percent': 10,
                                'minimum_trades': 3000,
                                'increments': [0.1, 1, 10, 50, 100],
                                'degeneration_factor': 0.1,
                                'degeneration_delay': 6
                                })

        db.create_collection('users')
        self.insert_user(username='admin',
                         password='password',
                         permissions=0)
        self._log.warning(f"New admin user created with standard password - this should be changed!")
        self._log.info(f"Database \"{db.name}\" set up.")
        return True

    def set_pair_name_best(self, pair_name, script_name, result_set):
        self._primary[pair_name].update_one({'_id': script_name}, {'$set': {'best': result_set}}, upsert=True)

    def set_ultimate_best(self, pair_name, result_set):
        self._primary[pair_name].update_one({'_id': 'ultimate'}, {'$set': {'result': result_set}}, upsert=True)

    def push_positive_result(self, pair_name, script_name, result_set):
        self._primary[pair_name].update_one({'_id': script_name}, {'$push': {'positive': result_set}}, upsert=True)

    def fetch_settings(self):
        return self._primary.settings.find_one({'_id': 'system_settings'})

    def fetch_analyzer_best_result(self, pair_name, script_name):
        try:
            return self._primary[pair_name].find_one({'_id': script_name}, {'best': 1})['best']
        except TypeError:
            return None
        except KeyError:
            return None

    def fetch_ultimate_best(self, pair_name):
        try:
            return self._primary[pair_name].find_one({'_id': 'ultimate'})['result']
        except TypeError:
            return None
        except KeyError:
            return None

    def fetch_positive_results(self, pair_name, script_name, dataset_name):
        return self._primary[pair_name].find_one({'_id': script_name}, {dataset_name: {'positive': 1}})

    def fetch_warehouse_pair_names(self):
        db = self.db(database_name="Saerimner")
        collections = db.list_collection_names()
        for entry in self._ignore:
            collections.remove(entry)
        return list(collections)

    def fetch_trades(self, pair_name):
        try:
            db = self.db(database_name="Saerimner")
            return db[pair_name].find_one({'_id': 'trades'}, {'list': 1})['list']
        except TypeError:
            return []
