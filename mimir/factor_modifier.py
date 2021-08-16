"""
Project CryPtoD,
Copyright PogD June 2021,
Primary author: Kristian K. Damsgaard
"""

import logging
import random


class FactorModifier:
    def __init__(self, old_factors, increments):
        self._log = logging.getLogger(self.__class__.__name__)
        self._old_factors = old_factors
        self._increments = increments
        self._new_factors = None

        # INITIALIZE
        random.seed()
        self._generate_new_factors()

    def _generate_new_factors(self):
        key = self._pick_key()
        increment = self._pick_increment()
        new_value = self._modify_value(key=key, increment=increment)
        if new_value:
            new_factors = self._old_factors
            new_factors[key]['value'] = round(new_value, 2)
            self._new_factors = new_factors
        else:
            self._generate_new_factors()

    def _pick_key(self):
        keys = list(self._old_factors.keys())
        max_index = len(keys) - 1
        random_index = random.randint(0, max_index)
        return keys[random_index]

    def _pick_increment(self):
        index_max = len(self._increments) - 1
        index = random.randint(0, index_max)
        return self._increments[index]

    def _modify_value(self, key, increment):
        value = self._old_factors[key]['value']
        increment = increment
        new_value = self._add_subtract(value=value, increment=increment)
        if self._test_constraints(key=key, value=new_value):
            return new_value
        else:
            return None

    @staticmethod
    def _add_subtract(value, increment):
        rand = random.random()
        if rand > 0.5:
            return value + increment
        else:
            return value - increment

    def _test_constraints(self, key, value):
        for constraint in self._old_factors[key]['constraints']:
            operator = constraint['operator']
            target = constraint['target']
            if isinstance(target, str):
                target = self._old_factors[target]['value']
            if not eval(f"{value} {operator} {target}"):
                return False
        return True

    @property
    def new_factors(self):
        return self._new_factors
