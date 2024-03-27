from .core import NotionAPICore
from .exceptions import APICallLimitExceed, UserNotFound

import requests


class User(NotionAPICore):
    """
    Need API Key for User API
    """

    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.users: dict = self._save_all_users()

    def _save_all_users(self) -> dict:
        res = requests.get(self.user_base_url, headers=self._header)
        users = dict()

        if res.status_code == 429:
            raise APICallLimitExceed()

        if res.status_code == 200:
            for user in res.json()["results"]:
                if user["type"] == "person":
                    users[user["name"]] = {
                        "id": user["id"],
                        "avatar_url": user["avatar_url"],
                        "email": user["person"]["email"],
                    }
        return users

    def get_user_by_nickname(self, nickname: str) -> dict:
        try:
            return self.users[nickname]
        except:
            raise UserNotFound("No corresponding user was found.")
