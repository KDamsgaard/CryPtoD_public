"""
Project CryPtoD,
Copyright PogD april 2021,
Primary author: Kristian K. Damsgaard
"""

import logging

from odin.services.db_services import DBServices
from odin.services.system_services import SystemServices
from odin.testing.unit_testing.testing_logger import TestingLogger

db_services = DBServices()
db = db_services.db

"""
These tests are not set up to use pytest. Simply run this script from "run_tests".
"""


class TestDBIntegrity:
    def __init__(self):
        # Initialize log
        TestingLogger()
        self._log = logging.getLogger(self.__class__.__name__)
        self._tested_pairs = []
        self._untested_pairs = []
        # Run tests
        self.test_all_trades_are_logged()
        self.test_stored_documents()

    def test_all_trades_are_logged(self):
        self._log.warning(f"Testing that all incoming trades are logged is not implemented!")

    def test_collection_order(self, pair_name, document, list_name, direction):
        count = 0
        errors = []
        try:
            for i, entry in enumerate(document):
                if document[i]['time'] > document[i + 1]['time']:
                    errors.append(f"{pair_name} - time at {i} > time at {i + 1} in {list_name}['{direction}']")
                for j, t in enumerate(document):
                    if i != j:
                        if document[i]['time'] == document[j]['time']:
                            same = True
                            for key in document[i].keys():
                                if document[i][key] != document[j][key]:
                                    same = False
                                if same:
                                    errors.append(f"{pair_name} - seems to have logged the same entry at {i} and {j} "
                                                  f"in {list_name}['{direction}']")
        except IndexError:
            count += 1

        if count > 1:
            errors.append(f"{pair_name} - Encountered {count} number of index errors while testing "
                          f"{list_name}['{direction}'] (expecting 1)")

        if not errors:
            result = [f"{pair_name} - {list_name}['{direction}'] appears in order."]
        else:
            result = errors
        return result

    def test_stored_documents(self):
        fields = SystemServices().fetch_pair_data_fields()
        attribute_names = fields['attribute_names']
        directions = fields['directions']

        tested = []
        untested = []

        for pair_name in db_services.all_pairs:
            for name in attribute_names:
                for direction in directions:
                    lst = db.trade_data.find_one({'_id': pair_name}, {name: 1})[name][direction]
                    if lst:
                        result = self.test_collection_order(pair_name=pair_name,
                                                            document=lst,
                                                            list_name=name,
                                                            direction=direction)
                        if len(result) > 1:
                            for res in result:
                                self._log.error(res)
                        else:
                            tested.append(f"{pair_name}:{name}['{direction}']")
                            self._log.info(result[0])
                    else:
                        untested.append(f"{pair_name}:{name}['{direction}']")
                        # self._log.warning(f"{pair_name}:{list_name}['{direction}'] is empty")
        self._log.info(f"Tested: {tested}")
        if untested:
            self._log.warning(f"Untested: {untested}")
