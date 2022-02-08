import yfinance as yf

msft = yf.Ticker("ETH-USD")

print(msft.history(period='1d', interval='15m').to_json())

# For searching for symbols
url = 'https://finance.yahoo.com/_finance_doubledown/api/resource/searchassist;searchTerm=eth-usd?device=console&returnMeta=true'