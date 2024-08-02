import mysql.connector

cnx = mysql.connector.connect(user='root',
    password='Sharks16',
    host='127.0.0.1',
    database='mrts',
    auth_plugin='mysql_native_password')

cursor = cnx.cursor()

query = ("""
        SELECT SUM(
        Jan2019 + Feb2019 + Mar2019 + Apr2019 + May2019 + Jun2019 + 
        Jul2019 + Aug2019 + Sep2019 + Oct2019 + Nov2019 + Dec2019 +
        Jan2020 + Feb2020 + Mar2020 + Apr2020 + May2020 + Jun2020 + 
        Jul2020 + Aug2020 + Sep2020 + Oct2020 + Nov2020 + Dec2020) 
        AS total_sum
        FROM data;
""")

cursor.execute(query)

# print the first cell of all the rows
for row in cursor.fetchall():
    print(row)

cursor.close()
cnx.close()

