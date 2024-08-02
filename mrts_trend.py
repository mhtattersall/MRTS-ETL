import mysql.connector
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

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
total_sales = list(data[0][2:])
sporting_goods_stores = list(data[42][2:])
hobby_toy_game_stores = list(data[43][2:])
book_stores = list(data[44][2:])
months = months[2:]

# create and format a date index
datetime_index = pd.to_datetime(months, format='%b%Y')
datetime_index = datetime_index.to_period('M').to_timestamp()
formatted_dates = datetime_index.strftime('%Y-%m-%d')
df = pd.DataFrame({'months': formatted_dates, 'total_sales': total_sales})
df.set_index('months', inplace=True)
df.index = pd.to_datetime(df.index)

# plot the comparision of 3 categories
plt.plot(months, sporting_goods_stores, color='blue', label='Sporting Goods Stores')
plt.plot(months, hobby_toy_game_stores, color='green', label='Hobby Toy Game Stores')
plt.plot(months, book_stores, color='red', label='Book Stores')
plt.title('MRTS: Comparing 3 Categories', fontsize=18)
formatter = ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x))
plt.gca().yaxis.set_major_formatter(formatter)
plt.xticks(fontsize=8, rotation=45, ha='right')
plt.xlabel('Months', fontsize=14)
plt.ylabel('USD Estimates', fontsize=14)
plt.legend()
plt.show()

# run seasonal decompose method on total_sales data
result = seasonal_decompose(df['total_sales'], model='additive', extrapolate_trend='freq')

# Plot the decomposition
plt.figure(figsize=(10, 6))
plt.subplot(4, 1, 1)
plt.plot(df.index, df['total_sales'], label='Original')
plt.legend()
plt.title('Original Time Series')

plt.subplot(4, 1, 2)
plt.plot(df.index, result.trend, label='Trend')
plt.legend()
plt.title('Trend Component')

plt.subplot(4, 1, 3)
plt.plot(df.index, result.seasonal, label='Seasonal')
plt.legend()
plt.title('Seasonal Component')

plt.subplot(4, 1, 4)
plt.plot(df.index, result.resid, label='Residual')
plt.legend()
plt.title('Residual Component')

plt.tight_layout()
plt.show()

