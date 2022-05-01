import abc
from datetime import datetime
import types


class Article:
    date: datetime.date = None
    film_id: str = None
    file_name: str = None
    content: str = "Placeholder"

    def __init__(self, date: datetime.date, film_id: str, file_name: str):
        self.date = date
        self.film_id = film_id
        self.file_name = file_name

    def get_content(self):
        return self.content

    def set_content(self, new_content: str):
        self.content = new_content

    def __eq__(self, o: Article):
        return o.film_id == self.film_id and o.file_name == self.file_name
