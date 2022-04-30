import mysql.connector
import configparser
from datetime import datetime

class DB_Wrapper:
    
    config= configparser.RawConfigParser()   
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

    def create_newspaper(self, date: datetime.date=None, film_id: str = None):
        # NEWspaper = Newspaper(film_id=film_id, date=date)
        return NEWspaper

    def add_articles2newspaper(self, newspaper: Newspaper):
        
        newspaper.add_article(article=element)

    def fetch_for_date(self, date: datetime.date):
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        
        return True