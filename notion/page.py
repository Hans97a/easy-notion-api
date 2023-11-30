from core import NotionAPICore
from exceptions import APICallLimitExceed, PageNotFound, APIErrorCore

import requests


class Page(NotionAPICore):
    """
    Need API Key for User API
    """

    def get_page_properties(self, page_id: str) -> dict:
        res = requests.get(self.page_base_url + page_id, headers=self._header)
        if res.status_code == 429:
            raise APICallLimitExceed()
        elif res.status_code == 200:
            return res.json()["properties"]
        elif res.status_code == 404:
            raise PageNotFound("can not find the page")
        else:
            raise APIErrorCore(res.json()["message"])
