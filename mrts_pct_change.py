import mysql.connector
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

cnx = mysql.connector.connect(user='root',
    password='Sharks16',
    host='127.0.0.1',
    database='mrts',
    auth_plugin='mysql_native_password')

cursor = cnx.cursor()

sql_1 = ("""
    SELECT column_name
    FROM information_schema.columns
    WHERE table_schema = 'mrts' AND table_name = 'data'
    ORDER BY ordinal_position     
""")

cursor.execute(sql_1)

months = []

for row in cursor.fetchall():
    months.append(row)

#convert strings in months to dates
months = [date_str[0].replace(',', '') for date_str in months]

cursor.reset()

sql_2 = ("""
    SELECT * 
    FROM data
""")

cursor.execute(sql_2)

data = []

for row in cursor.fetchall():
    data.append(row)

cursor.close()

cnx.close()

# create lists of category from data download
womens_clothing_stores = list(data[36][2:])
mens_clothing_stores = list(data[35][2:])
months = months[2:]

# create and format a date index
datetime_index = pd.to_datetime(months, format='%b%Y')
datetime_index = datetime_index.to_period('M').to_timestamp()
formatted_dates = datetime_index.strftime('%Y-%m-%d')
df = pd.DataFrame({'months': formatted_dates, 'womens clothing': womens_clothing_stores, 'mens clothing': mens_clothing_stores})
df.set_index('months', inplace=True)
df.index = pd.to_datetime(df.index)

# Calculate percentage changes
percentage_changes = df.pct_change()

# Exclude last 3 values
percentage_changes = percentage_changes.iloc[:-3]

# Compute correlation coefficient
correlation = df['womens clothing'].corr(df['mens clothing'])
per_correlation = percentage_changes['womens clothing'].corr(percentage_changes['mens clothing'])

# Print correlation statistics
print("Correlation coefficient:", correlation)
print("Percentage change correlation coefficient:", per_correlation)

# Calculate total of the two series
total = df['womens clothing'] + df['mens clothing']

# Calculate percentage contribution of each series to the total
percentage_contribution_womens = (df['womens clothing'] / total) * 100
percentage_contribution_mens = (df['mens clothing'] / total) * 100

# Plot the percentage contributions
plt.figure(figsize=(10, 6))
plt.bar(months, percentage_contribution_womens, label='Womens', color='blue', alpha=0.5)
plt.bar(months, percentage_contribution_mens, bottom=percentage_contribution_womens, label='Mens', color='green', alpha=0.5)
formatter = ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x))
plt.gca().yaxis.set_major_formatter(formatter)
plt.xticks(fontsize=8, rotation=45, ha='right')
plt.ylabel('Percentage Contribution (%)')
plt.title('Percentage Contribution of Womens and Mens Clothing Stores to Total')
plt.legend()
plt.show()

# Plot the comparision of 2 categories percentage changes
plt.plot(months[:-3], percentage_changes['womens clothing'], color='blue', label='Womens Clothing Stores')
plt.plot(months[:-3], percentage_changes['mens clothing'], color='green', label='Mens Clothing Stores')
plt.title('MRTS: Comparing Percentage Changes', fontsize=18)
formatter = ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x))
plt.gca().yaxis.set_major_formatter(formatter)
plt.xticks(fontsize=8, rotation=45, ha='right')
plt.xlabel('Months', fontsize=14)
plt.ylabel('Percentage Change', fontsize=14)
plt.legend()
plt.show()

# Plot the comparision of 2 categories
plt.plot(months, womens_clothing_stores, color='blue', label='Womens Clothing Stores')
plt.plot(months, mens_clothing_stores, color='green', label='Mens Clothing Stores')
plt.title('MRTS: Comparing 2 Categories', fontsize=18)
formatter = ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x))
plt.gca().yaxis.set_major_formatter(formatter)
plt.xticks(fontsize=8, rotation=45, ha='right')
plt.xlabel('Months', fontsize=14)
plt.ylabel('USD Estimates', fontsize=14)
plt.legend()
plt.show()