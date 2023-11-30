# easy-notion
Use __easy-notion__ for handy Notion API!<br/>
Unofficial Python 3 client for Notion API

# English
## Installation
```
pip install easy-notion
```

## Before Start
To use Notion API, you must get api key from [notion integrations page](https://www.notion.so/my-integrations).<br/>
And then, create new database in your notion workspace.<br/>
Click the database's setting and click 'copy link to view'<br/>
Get database id from copied link before '?v='

`https://www.notion.so/__here_is_database_id__?v=uuid&pvs=4`


## Usage
### Start
```
from notion import Notion

client = Notion("your_api_key", "database_id")
```

### Create new page in your db
```
data = {
    "school": "maycan_school", # school column type in notion is title
    "message": "example message" # message column type in notion is rich_text
    "students": ["Hans", "Woody"] # students column type in notion is people
}
client.create_page_in_db(data)
```

create_page_in_db method returns dictionary like
```
{
    is_created: bool,
    page_id: str, # if is_created is False, then page_id is not given and 'detail' key returned with error message
}
```

- data format

    - title, rich_text, number, selecet, status
        - key: value
        - Be careful! status value must be predefined in notion app.

    - multi_select, people
        - key: [value1, value2 ...]   (value must be user's nickname if people)

    - date
        - key: [value1, value2]
        - The second value(value2) means the end date. If None, only the start date is registered.
        - value format -> "YYYY-MM-DD" or "YYYY-MM-DD hh:mm:ss"

### Update page
```
data = {
    "message": "i want to go home"
}
client.update_page("page_id", data)
```

update_page method returns True (when success), else raise Error with message from Notion

### Retrieve page properties
```
client.get_page_properties("page_id") # returns dictionary
```


## Features
- [X] Create page in Database
- [X] Update page
- [X] Retrieve page properties
- [ ] Query Database

