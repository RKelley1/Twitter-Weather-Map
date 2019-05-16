import psycopg2
from os import environ


class Config(object):
    AWS_DB_NAME = 'AWS_DB_NAME'
    AWS_DB_USERNAME = 'AWS_DB_USERNAME'
    AWS_DB_PASSWORD = 'AWS_DB_PASSWORD'
    AWS_DB_ENDPOINT = 'AWS_DB_ENDPOINT'
    AWS_DB_PORT = 'AWS_DB_PORT'

    _store = {}

    def __init__(self):
        self._conn = None
        self.configure()

    def __getitem__(self, item):
        return self._store[item]

    def configure(self):
        self.load_var(self.AWS_DB_ENDPOINT)
        self.load_var(self.AWS_DB_NAME)
        self.load_var(self.AWS_DB_PASSWORD)
        self.load_var(self.AWS_DB_USERNAME)

    def load_var(self, var, default=None):
        try:
            self._store.update({var: environ[var]})
        except KeyError:
            raise Exception(f'Unable to find {var}. Perhaps you need to source the config file?')

    def get(self, item):
        return self.__getitem__(item)

    def get_db(self):
        if not self._conn:
            self._conn = psycopg2.connect(
                dbname=config[config.AWS_DB_NAME],
                user=config[config.AWS_DB_USERNAME],
                password=config[config.AWS_DB_PASSWORD],
                host=config[config.AWS_DB_ENDPOINT]
            )

        return self._conn



config = Config()
