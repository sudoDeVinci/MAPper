import mysql.connector

cnx = None
DB_NAME = "mapper"

cnx = mysql.connector.connect(user='root', password='root',
                              host='localhost')
