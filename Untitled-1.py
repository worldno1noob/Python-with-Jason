from pandas.core.frame import DataFrame
import requests
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

resolution = 86400
start_time = int(time.time()) - resolution * 730
end_time = int(time.time())
response = requests.get(
    f'https://ftx.com/api/markets/BTC-PERP/candles?resolution={resolution}&start_time={start_time}&end_time={end_time}').json()['result']
data = pd.DataFrame(response)
data['SMA20'] = data['close'].rolling(window=20).mean().shift()
data['SMA50'] = data['close'].rolling(window=50).mean().shift()


def calculate_ema(SMA, days, smoothing=2):
    ema = [SMA]
    for price in SMA:
        ema.append((price * (smoothing / (1 + days))) +
                   ema[-1] * (1 - (smoothing / (1 + days))))
    return ema


def buy_and_sell(data):

    tobuy = []
    tosell = []
    a = 0
    for i in range(len(data)):
        if data['SMA20'][i] > data['SMA50'][i]:
            if a != 1:
                tobuy.append(data['close'][i])
                tosell.append(np.nan)
                a = 1
            else:
                tobuy.append(np.nan)
                tosell.append(np.nan)
        elif data['SMA20'][i] < data['SMA50'][i]:
            if a != -1 and a == 1:
                tobuy.append(np.nan)
                tosell.append(data['close'][i])
                a = -1
            else:
                tobuy.append(np.nan)
                tosell.append(np.nan)
        else:
            tobuy.append(np.nan)
            tosell.append(np.nan)
    return(tobuy, tosell)


buy_and_sell = buy_and_sell(data)
data['Tobuy'] = buy_and_sell[0]
data['Tosell'] = buy_and_sell[1]

calculate_ema = calculate_ema(data['SMA20'], 20)
data['EMA'] = calculate_ema[0]

plt.figure(figsize=(12, 5))
plt.plot(data['close'], label="BTC", alpha=0.4)
plt.plot(data['SMA20'], label="SMA-20", alpha=0.4, color='purple')
plt.plot(data['SMA50'], label="SMA-50", alpha=0.4, color='orange')
plt.plot(data['EMA'], label="EMA", alpha=0.4, color='blue')
plt.scatter(data.index, data['Tobuy'], label='buy', marker=6, color='green')
plt.scatter(data.index, data['Tosell'], label='sell', marker=7, color='red')
plt.title('The close price history BTC')
plt.xlabel('From 20/10/21 - 21/10/20')
plt.ylabel('Close price of BTC in USD')
plt.legend(loc='lower right')
plt.show()
