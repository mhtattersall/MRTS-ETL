import mysql.connector

cnx = mysql.connector.connect(user='root',
    password='Sharks16',
    host='127.0.0.1',
    database='mrts',
    auth_plugin='mysql_native_password')

cursor = cnx.cursor()

query_2 = ("""
            CREATE TABLE data (
            NAICS VARCHAR(30) NULL,
            Kind VARCHAR(150) NULL, 
            Jan2019 INT, Feb2019 INT, Mar2019 INT, Apr2019 INT, May2019 INT, Jun2019 INT,
            Jul2019 INT, Aug2019 INT, Sep2019 INT, Oct2019 INT, Nov2019 INT, Dec2019 INT,
            Jan2020 INT, Feb2020 INT, Mar2020 INT, Apr2020 INT, May2020 INT, Jun2020 INT,
            Jul2020 INT, Aug2020 INT, Sep2020 INT, Oct2020 INT, Nov2020 INT, Dec2020 INT);
""")         

cursor.execute(query_2)

cursor.close()
cnx.close()

