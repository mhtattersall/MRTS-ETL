import mysql.connector

cnx = mysql.connector.connect(user='root',
    password='Sharks16',
    host='127.0.0.1',
    database='mrts',
    auth_plugin='mysql_native_password')

cursor = cnx.cursor()

query = ("""
    SELECT COUNT(*) AS num_columns
    FROM information_schema.columns
    WHERE table_schema = 'mrts' AND table_name = 'data';
""")

cursor.execute(query)

# print the first cell of all the rows
for row in cursor.fetchall():
    print(row)

cursor.close()
cnx.close()

