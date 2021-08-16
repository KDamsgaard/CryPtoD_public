import logging
import sys

import bcrypt
from pymongo import MongoClient

from modules.kraken_services.public_kraken_services import PublicKrakenServices
from modules.system_services.system_services import SystemServices


class DBServices:
    def __init__(self):
        self._log = logging.getLogger(self.__class__.__name__)
        self._system_services = SystemServices()
        self._public_kraken_services = PublicKrakenServices()
        self._clients = {}
        self._primary_name = None
        self._primary = None
        self._not_pairs = ['settings', 'users']

        # INITIALIZE
        self._set_clients()
        self._db_check()

    def _set_clients(self):
        db_info = self._system_services.read_database_information()

        for key in db_info.keys():
            setting = db_info[key]
            database_name = setting['name']
            connection = setting['connection']
            port = setting['port']
            self._clients[database_name] = self._initialize_client(connection=connection,
                                                                   port=port)
            if 'primary' in setting:
                self._primary_name = setting['name']
                self._primary = self.db(database_name=self._primary_name)

    @staticmethod
    def _initialize_client(connection, port):
        client = MongoClient(connection, port)
        return {'client': client}

    def client(self, client_name):
        return self._clients[client_name]['client']

    def db(self, database_name):
        return self._clients[database_name]['client'][database_name]

    def insert_user(self, username, password, permissions):
        db = self._primary
        try:
            if db.users.find_one({'user_name': username}):
                self._log.info(f"Insert aborted - User already exists.")
            else:

                schema = {'username': username,
                          'password': bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()),
                          'permissions': permissions}
                db.users.insert_one(schema)
                return True
        except Exception as e:
            self._log.error(f"{e}")
        return False

    def _db_check(self):
        primary = self._primary_name
        client = self.client(client_name=primary)
        database_names = client.list_database_names()
        errors = False
        for key in self._clients.keys():
            if key not in database_names:
                if key == self._primary_name:
                    self._log.warning(f"Database \"{key}\" does not exist, setting up...")
                    self._create_database()
                else:
                    self._log.error(f"Unable to locate necessary database - run \"{key}\" before launching {self._primary_name}")
                    errors = True
        if errors:
            sys.exit()

    def _create_database(self):
        self._log.warning(f"Create_database() called on DBServices superclass.")

    @property
    def system_settings(self):
        return self._primary.settings.find_one({'_id': 'system_settings'})

    @property
    def database_settings(self):
        return self._primary.settings.find_one({'_id': 'database_settings'})

    @property
    def gui_settings(self):
        return self._primary.settings.find_one({'_id': 'gui_settings'})
