import os
import json


class FileServices:
    def __init__(self, pair_name, filename, content):
        self._filename = self.cache_result(pair_name, filename, content)

    @staticmethod
    def _write_file(directory, filename, content):
        if not os.path.exists(directory):
            os.makedirs(directory)
        f = open(f'{directory}/{filename}', 'w+')
        f.write(content)
        f.close()

    def cache_result(self, pair_name, filename, content):
        directory = f'results/{pair_name}'
        filename = f'{filename}.json'
        self._write_file(directory, filename, json.dumps(content))
        return f'{directory}/{filename}'

    @property
    def filename(self):
        return self._filename
