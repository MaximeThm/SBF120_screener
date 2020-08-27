from pandas_datareader import data as pdr
import yfinance as yf
import pandas as pd
import datetime

yf.pdr_override()
df = pd.read_csv("SBF120.csv")
stocklist = df['TICKER'].tolist()

end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=365)

final = []
price = []
name = []
rating = []
n = 0

for stock in stocklist:
    n += 1
    print("\npulling {} with index {}".format(stock, n))
    df = pdr.get_data_yahoo(stock, start=start_date, end=end_date)

    df['Percent Change'] = df['Adj Close'].pct_change()
    stock_return = df['Percent Change'].sum() * 100
    RS_Rating = round((stock_return / 2) * 10, 2)

    try:
        sma = [50, 150, 200]
        for x in sma:
            df["SMA_" + str(x)] = round(df.iloc[:, 4].rolling(window=x).mean(), 2)

        currentClose = df["Adj Close"][-1]
        moving_average_50 = df["SMA_50"][-1]
        moving_average_150 = df["SMA_150"][-1]
        moving_average_200 = df["SMA_200"][-1]
        low_of_52week = min(df["Adj Close"][-260:])
        high_of_52week = max(df["Adj Close"][-260:])
        moving_average_200_20 = df["SMA_200"][-20]

        # Condition 1: Current Price > 150 SMA and > 200 SMA
        if currentClose > moving_average_150 > moving_average_200:
            condition_1 = True
        else:
            condition_1 = False
        # Condition 2: 150 SMA > 200 SMA
        if moving_average_150 > moving_average_200:
            condition_2 = True
        else:
            condition_2 = False
        # Condition 3: 200 SMA trending up for at least 1 month
        if moving_average_200 > moving_average_200_20:
            condition_3 = True
        else:
            condition_3 = False
        # Condition 4: 50 SMA> 150 SMA and 50 SMA> 200 SMA
        if moving_average_50 > moving_average_150 > moving_average_200:
            condition_4 = True
        else:
            condition_4 = False
        # Condition 5: Current Price > 50 SMA
        if currentClose > moving_average_50:
            condition_5 = True
        else:
            condition_5 = False
        # Condition 6: Current Price is at least 30% above 52 week low
        if currentClose >= (1.3 * low_of_52week):
            condition_6 = True
        else:
            condition_6 = False
        # Condition 7: Current Price is within 25% of 52 week high
        if currentClose >= (.75 * high_of_52week):
            condition_7 = True
        else:
            condition_7 = False

        if condition_1 and condition_2 and condition_3 and condition_4 and condition_5 and condition_6 and condition_7:
            final.append(stock)
            price.append(df['Adj Close'].iloc[-1])
            rating.append(RS_Rating)

    except Exception as e:
        print(e)
        print("No data on " + stock)

df = pd.read_csv("SBF120.csv")
for stocks in final:
    df1 = df.loc[df['TICKER'].isin([stocks])]
    name.append(df1['NAME'].tolist())

df = pd.DataFrame(columns=['Date', 'Name', 'Price', 'Rating'])
df['Name'] = name
df['Date'] = end_date - datetime.timedelta(days=1)
df['Price'] = price
df['Rating'] = rating
df.sort_values('Rating', inplace=True, ascending=False)
df.reset_index(drop=True, inplace=True)

print(df)
