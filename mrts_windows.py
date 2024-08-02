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
new_car_dealers = list(data[11][2:])
used_car_dealers = list(data[12][2:])
months = months[2:]

# create and format a date index
datetime_index = pd.to_datetime(months, format='%b%Y')
datetime_index = datetime_index.to_period('M').to_timestamp()
formatted_dates = datetime_index.strftime('%Y-%m-%d')
df = pd.DataFrame({'months': formatted_dates, 'New Cars': new_car_dealers, 'Used Cars': used_car_dealers})
df.set_index('months', inplace=True)
df.index = pd.to_datetime(df.index)

# set window period size
window_size_1 = 3
window_size_2 = 6

# apply rolling function to data Series with varyign window sizes
rolling_mean_new_3 = df['New Cars'].rolling(window=window_size_1).mean()
rolling_mean_used_3 = df['Used Cars'].rolling(window=window_size_1).mean()
rolling_mean_new_6 = df['New Cars'].rolling(window=window_size_2).mean()
rolling_mean_used_6 = df['Used Cars'].rolling(window=window_size_2).mean()

# Plot the results using matplotlib
plt.figure(figsize=(10, 6))
formatter = ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x))
plt.gca().yaxis.set_major_formatter(formatter)
plt.xticks(fontsize=10, rotation=45, ha='right')
plt.plot(months, df['New Cars'], label='New Cars', color='blue')
plt.plot(months, rolling_mean_new_3, label=f'New Cars Rolling Mean ({window_size_1} periods)', color='green')
plt.plot(months, rolling_mean_new_6, label=f'New Cars Rolling Mean ({window_size_2} periods)', color='purple')
plt.plot(months, df['Used Cars'], label='Used Cars', color='orange')
plt.plot(months, rolling_mean_used_3, label=f'Used Cars Rolling Mean ({window_size_1} periods)', color='red')
plt.plot(months, rolling_mean_used_6, label=f'Used Cars Rolling Mean ({window_size_2} periods)', color='brown')
plt.ylabel('USD Millions')
plt.title('MRTS: Rolling Window Operation for New and Used Car Dealers')
plt.legend(loc='upper left')
plt.grid(True)
plt.show()