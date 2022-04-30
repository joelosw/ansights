import mysql.connector
import configparser

config= configparser.RawConfigParser()   
configFilePath = r'config/sql_credentials.txt'
config.read(configFilePath)

reichsanzeiger_db = mysql.connector.connect(
    host='localhost',
    user=config.get("credentials", "username"),
    password=config.get("credentials", "password"),
    database="reichsanzeiger"
)
print(reichsanzeiger_db)

cursor = reichsanzeiger_db.cursor(buffered=True)

cursor.execute("SHOW TABLES;")
tables = cursor.fetchall()
print("Availabke Tables")
for table_name in tables:
    print("-----"+table_name[0]+"-------")
    print('Example Row:')
    
    cursor.execute(f"SHOW COLUMNS FROM {table_name[0]};")
    row_fields = cursor.fetchall()
    print([row[0] for row in row_fields])

    cursor.execute(f"SELECT * FROM {table_name[0]};")
    for i in range(20):
        row = cursor.fetchone()
        #print(row)

cursor.execute(f"SHOW COLUMNS FROM {tables[1][0]};")
row_fields = cursor.fetchall()
print([row[0] for row in row_fields])
cursor.execute('SELECT bildnr, zeitung, ausgabe, jahr FROM titelbl WHERE fid = 1')
for i in range(522):
    row = cursor.fetchone()
    print(row)