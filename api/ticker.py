import yfinance as yf

msft = yf.Ticker("ETH-USD")

df = msft.history(period='2d', interval='15m').sort_index(ascending=False).reset_index()

df['t'] = df['Datetime'].apply(lambda x: int(x.value / 10**6))
c_vals = list(df['Close'])
o_vals = list(df['Open'])
l_vals = list(df['Low'])
h_vals = list(df['High'])
t_vals = list(df['t'])
print(c_vals[0])


# For searching for symbols
url = 'https://finance.yahoo.com/_finance_doubledown/api/resource/searchassist;searchTerm=eth-usd?device=console&returnMeta=true'