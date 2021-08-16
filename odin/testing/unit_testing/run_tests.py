"""
Project CryPtoD,
Copyright PogD april 2021,
Primary author: Kristian K. Damsgaard
"""

from odin.testing.unit_testing.test_db_integrity import TestDBIntegrity


def run_tests():
    TestDBIntegrity()


if __name__ == "__main__":
    run_tests()
