import mysql.connector
import configparser
from datetime import datetime
from bs4 import BeautifulSoup
from Newspaper import Newspaper
from Article import Article
import requests


class DB_Wrapper:

    config = configparser.RawConfigParser()
    configFilePath = r'config/sql_credentials.txt'
    config.read(configFilePath)

    reichsanzeiger_db = mysql.connector.connect(
        host='localhost',
        user=config.get("credentials", "username"),
        password=config.get("credentials", "password"),
        database="reichsanzeiger"
    )
    print('Status DB:', reichsanzeiger_db)

    cursor = reichsanzeiger_db.cursor(buffered=True)

    def create_newspaper(self, date: datetime.date = None, film_id: str = None):
        """
        The create_newspaper function creates a new newspaper object with the following attributes:
            - date (datetime.date)
            - film_id (str)

        :param self: Used to Refer to the object of the class that is calling this method.
        :param date:datetime.date=None: Used to Set the date of the newspaper.
        :param film_id:str=None: Used to Pass the film_id to the function.
        :return: A newspaper object.
        """

        # NEWspaper = Newspaper(film_id=film_id, date=date)
        return NEWspaper

    def add_articles2newspaper(self, newspaper: Newspaper, element: Article):
        """
        The add_articles2newspaper function adds a list of articles to the newspaper.

        :param self: Used to Access the class attributes.
        :param newspaper:Newspaper: Used to Specify the newspaper that the article will be added to.
        :param element:Article: Used to Pass the article object to the function.
        :return: A list of articles.
        """
        newspaper.add_article(article=element)

    def get_date_for_page(url: str, debug=False):
        """
        The get_date_for_page function accepts a URL as an argument and returns the date of the article at that URL.

        :param url:str: Used to Pass the url of the page that is being scraped.
        :param debug=False: Used to Print out the content of the page.
        :return: A datetime.

        :doc-author: Trelent
        """

        r = requests.get(url, allow_redirects=True)
        if debug:
            print(r.content)
        data = r.content
        Soup = BeautifulSoup(r.text, 'lxml')

        candidate_tag = Soup.find_all("h2")[0].text.strip()
        candidate = candidate_tag.split(',')[-1].split('GMT')[0][:-10]
        dt = datetime.strptime(candidate, ' %d %b %Y').date()
        print(f'As Datetime object: {dt}')
        return dt

    def fetch_for_date(self, date: datetime.date):
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()

        return True


DB_Wrapper.get_date_for_page(
    "https://digi.bib.uni-mannheim.de/periodika/reichsanzeiger/ocr/film/tesseract-4.0.0-20181201/001-7920/0005.hocr")
