"""
Project CryPtoD,
Copyright PogD april 2021,
Primary author: Kristian K. Damsgaard
"""
import logging
import os
import json
import sys


class SystemServices:
    def __init__(self):
        self._log = logging.getLogger(self.__class__.__name__)

    def get_analyzer_script_names(self, with_extension: bool = False):
        try:
            file_names = os.listdir("scripts/analyzers")

            for file_name in file_names:
                if not self._extension_is_py(file_name=file_name):
                    file_names.remove(file_name)
                    self._log.warning(f"removed \"{file_name}\" from list of analyzers")

            if not with_extension:
                for i, file_name in enumerate(file_names):
                    file_names[i] = file_name.split(".")[0]

            return file_names
        except FileNotFoundError:
            self._log.error(f"No analyzers found")

    @staticmethod
    def _extension_is_py(file_name):
        split = file_name.split(".")
        if len(split) == 2:
            if file_name.split(".")[1] == "py":
                return True
        return False

    @staticmethod
    def read_database_information():
        with open("program_settings.json", "r") as file:
            settings = json.load(file)['databases']
            return settings

    @staticmethod
    def read_wh_info():
        with open("program_settings.json", "r") as file:
            settings = json.load(file)['wh_info']
            return settings

    @staticmethod
    def fetch_kraken_keys_settings():
        with open("program_settings.json", "r") as file:
            settings = json.load(file)['kraken_api_keys']
            return settings

    @staticmethod
    def fetch_pair_data_fields():
        with open("program_settings.json", "r") as file:
            settings = json.load(file)['pair_data_fields']
            return settings

    @staticmethod
    def get_attributes(calling_object: object, attribute_names: list):
        """
        Returns a list of attributes contained in the object calling this function.

        :param attribute_names: A list of attribute names
        :return: A list of attribute objects
        """
        attributes = []
        for nm in attribute_names:
            attr_name = "_" + nm
            attributes.append(getattr(calling_object, attr_name))
        return attributes

    @staticmethod
    def fetch_generator_names():
        fetched = os.listdir("scripts/generators")
        names = []
        for f in fetched:
            try:
                slices = f.split(".")
                if slices[1] == "py":
                    names.append(slices[0])
            except IndexError:
                pass
        return names

    @staticmethod
    def fetch_analyzer_names():
        fetched = os.listdir("scripts/analyzers")
        names = []
        for f in fetched:
            try:
                slices = f.split(".")
                if slices[1] == "py":
                    names.append(slices[0])
            except IndexError:
                pass
        return names


    @staticmethod
    def fetch_standard_pair_names():
        with open("program_settings.json", "r") as file:
            pairs = json.load(file)['standard_pairs']
            return pairs

    @staticmethod
    def fetch_rl_currency_names():
        with open("program_settings.json", "r") as file:
            names = json.load(file)['rl_currency_names']
            return names

    @staticmethod
    def exit():
        sys.exit()
