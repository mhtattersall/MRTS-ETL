import mysql.connector
import csv

cnx = mysql.connector.connect(user='root',
    password='Sharks16',
    host='127.0.0.1',
    database='mrts',
    auth_plugin='mysql_native_password')

cursor = cnx.cursor()

with open('mrts_2019_2020.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter =',')
    header = next(csv_reader) # skip the header row
    for row in csv_reader:
        sql = ("""
        INSERT INTO data (NAICS, Kind, 
        Jan2019, Feb2019, Mar2019, Apr2019, May2019, Jun2019,
        Jul2019, Aug2019, Sep2019, Oct2019, Nov2019, Dec2019,
        Jan2020, Feb2020, Mar2020, Apr2020, May2020, Jun2020,
        Jul2020, Aug2020, Sep2020, Oct2020, Nov2020, Dec2020) 
        VALUES (%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
        """)
        val = (row[0],row[1],
        row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],
        row[14],row[15],row[16],row[17],row[18],row[19],row[20],row[21],row[22],row[23],row[24],row[25])
        cursor.execute(sql,val)
        cnx.commit()


cursor.close()
cnx.close()

