import mysql.connector
import configparser

config= configparser.RawConfigParser()   
configFilePath = r'config/sql_credentials.txt'
config.read(configFilePath)

reichsanzeiger_db = mysql.connector.connect(
    host='localhost',
    user=config.get("credentials", "username"),
    password=config.get("credentials", "password")
)
print(reichsanzeiger_db)