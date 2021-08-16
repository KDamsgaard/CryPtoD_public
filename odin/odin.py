"""
Project CryPtoD,
Copyright PogD april 2021,
Primary author: Kristian K. Damsgaard
"""

import json
from brain import Brain
from setup import Setup


def print_welcome():
    with open("program_settings.json") as file:
        settings = json.load(file)
        # print(settings)
        print(f"\nRunning {settings['program']} ({settings['version']})\n")
        # time.sleep(1)


def main():
    print_welcome()
    setup = Setup()
    Brain(db_services=setup.db_services)


if __name__ == "__main__":
    main()

