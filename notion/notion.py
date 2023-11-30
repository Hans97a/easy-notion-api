from exceptions import InvalidData, APIErrorCore
from database import Database
from user import User
from page import Page

import requests
import json


class Notion(Database, User, Page):
    """
    Need API Key, Database id for easy-notion
    """

    def create_page_in_db(self, data={}) -> dict:
        """
        ## create new page in db
        returns dict
        e.g.

        -- success
        {
            is_created: True,
            page_id: str
        }

        -- fail
        {
            is_created: False,
            detail: str
        }

        ### Notice
        db column type rollup, created_by, created_time, last_edited_by, last_edited_time
        can not be included via api.
        https://developers.notion.com/reference/post-page

        ### data format

        - title, rich_text, number, selecet, status
          key: value
          warning : status value must be predefined in notion app

        - multi_select, people
          key: [value1, value2 ...]   (value must be user's nickname if people)

        - date
          key: [value1, value2]
          (The second value(value2) means the end date. If None, only the start date is registered.)
          value format -> "YYYY-MM-DD" or "YYYY-MM-DD hh:mm:ss"

        """

        request_body = {
            "parent": {"database_id": self.database_id},
            "properties": self._transform_data(data),
        }
        res = requests.post(
            self.page_base_url, headers=self._header, data=json.dumps(request_body)
        )
        is_created = res.status_code == 200
        if is_created:
            return {
                "is_created": True,
                "page_id": res.json()["id"],
            }
        else:
            return {
                "is_created": False,
                "detail": res.json()["message"],
            }

    def update_page(self, page_id: str, data: dict) -> bool:
        """
        ## update page with given data

        ### Notice
          db column type rollup, created_by, created_time, last_edited_by, last_edited_time
          can not be included via api.
          https://developers.notion.com/reference/post-page

        ### data format

        - title, rich_text, number, selecet, status
          key: value
          warning : status value must be predefined in notion app

        - multi_select, people
          key: [value1, value2 ...]   (value must be user's nickname if people)

        - date
          key: [value1, value2]
          (The second value(value2) means the end date. If None, only the start date is registered.)
          value format -> "YYYY-MM-DD" or "YYYY-MM-DD hh:mm:ss"
        """
        data = self._transform_data(data)

        res = requests.patch(
            self.page_base_url + page_id,
            headers=self._header,
            data=json.dumps({"properties": data}),
        )
        if res.status_code == 200:
            return True
        else:
            raise APIErrorCore(res.json()["message"])

    def _transform_data(self, data={}) -> dict:
        """
        transform data for notion db api
        """
        properties = self.get_db_properties()
        data_keys = data.keys()
        column_types = []
        try:
            for key in data_keys:
                column_types.append(properties[key]["type"])
        except:
            raise InvalidData("No corresponding column for database")

        data_form = {}
        for col_type, data_key in zip(column_types, data_keys):
            value = data[data_key]

            if col_type in ["title", "rich_text"]:
                if not isinstance(value, str):
                    raise InvalidData(f"The Key {data_key} must be string")
                data_form[data_key] = {col_type: [{"text": {"content": value}}]}

            elif col_type == "number":
                if not isinstance(value, int):
                    raise InvalidData(f"The Key {data_key} must be int")
                data_form[data_key] = {col_type: value}

            elif col_type in ["select", "status"]:
                data_form[data_key] = {col_type: {"name": value}}

            elif col_type == "multi_select":
                multi_select_form = [{"name": val} for val in value]
                data_form[data_key] = {col_type: multi_select_form}

            elif col_type in ["url", "email", "phone_number"]:
                data_form[data_key] = {col_type: value}

            elif col_type == "people":
                users = [
                    {"object": "user", "id": self.get_user_by_nickname(nickname)["id"]}
                    for nickname in value
                ]
                data_form[data_key] = {col_type: users}

            elif col_type == "checkbox":
                if not isinstance(value, bool):
                    raise InvalidData(f"The Key {data_key} must be boolean")
                data_form[data_key] = {col_type: value}
            elif col_type == "date":
                data_form[data_key] = {col_type: {"start": value[0], "end": value[1]}}

        return data_form
