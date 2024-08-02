import mysql.connector

cnx = mysql.connector.connect(user='root',
    password='Sharks16',
    host='127.0.0.1',
    auth_plugin='mysql_native_password')

cursor = cnx.cursor()

query_1 = ("CREATE DATABASE mrts")

cursor.execute(query_1)

cursor.close()
cnx.close() 

