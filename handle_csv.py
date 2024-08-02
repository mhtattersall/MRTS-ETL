# import csv module
import csv

# open csv file
with open('mrts_2019_2020.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter =',') # create a csv reader object
    header = next(csv_reader) # skip the header row of the data
    for row in csv_reader: # iterate through the rows
        print(row) # print each row in turn