import mysql.connector

cnx = None
DB_NAME = "mapper"

cnx = mysql.connector.connect(user='root', password='@Cazaubon2001',
                              host='localhost')
