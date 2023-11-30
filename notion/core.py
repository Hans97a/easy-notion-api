class NotionAPICore:
    db_base_url = "https://api.notion.com/v1/databases/"
    user_base_url = "https://api.notion.com/v1/users/"
    page_base_url = "https://api.notion.com/v1/pages/"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self._header = {
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
