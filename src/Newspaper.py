import abc
from datetime import datetime
import types
from Article import Article
class Newspaper:
    date: datetime.date=None
    film_id: str = None
    articles: list = None
    file_names: list = None

    def __init__(self, date: datetime.date, film_id: str):
        self.date = date
        self.film_id = film_id  
    
    def add_article(self, article: Article):
        if not self.exists_already(article):
            self.articles.append(article)
            print('Article appended successfully')
    
    def get_articles(self):
        return self.articles

    def exists_already(self, article:Article):
        return article in self.articles

    def remove_article(self, article: Article):
        if not self.exists_already(article):
            print('WARNING: Your article does not exist in the newspaper')
        else:
            for element in self.articles:
                if element.__eq__(article):
                    self.articles.remove(element)
            print('Removal succeded')

    





