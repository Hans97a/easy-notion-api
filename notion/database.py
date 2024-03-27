from .core import NotionAPICore
from .exceptions import APICallLimitExceed, APIKeyNotFound

import requests


class Database(NotionAPICore):
    """
    Need API Key for Database API
    """

    def __init__(self, api_key: str, database_id: str):
        super().__init__(api_key)
        self.database_id = database_id
        self.database_info = self._get_db_info()

    def _get_db_info(self):
        res = requests.get(self.db_base_url + self.database_id, headers=self._header)
        if res.status_code == 429:
            raise APICallLimitExceed()
        elif res.status_code == 404:
            raise APIKeyNotFound(res.json()["message"])
        else:
            return res.json()

    def get_db_properties(self):
        return self.database_info["properties"]
