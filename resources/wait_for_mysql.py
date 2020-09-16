import os
import mysql.connector
from time import sleep
from dotenv import load_dotenv
load_dotenv(os.getenv('WORKDIR') + '/.env')

while True:
    try:
        conn = mysql.connector.connect(host=os.getenv('MYSQL_HOST'),
                                        user=os.getenv('MYSQL_USER'),
                                        port=os.getenv('MYSQL_PORT'),
                                        password=os.getenv('MYSQL_PSWD'),
                                        use_pure=True)
        cursor = conn.cursor(buffered=True)
        cursor.execute("CREATE DATABASE IF NOT EXISTS " + os.getenv('MYSQL_DATABASE'))
        cursor.execute("USE " + os.getenv('MYSQL_DATABASE'))
        print('MySQL is available now.')
        break
    except Exception as e:
        print(e)
        sleep(3)

