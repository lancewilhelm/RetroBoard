#https://pypi.org/project/websocket_client/
import websocket

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"BINANCE:ETHUSDT"}')

if __name__ == "__main__":
    websocket.enableTrace(True)
    # ws = websocket.WebSocket()
    # ws.connect("wss://ws.finnhub.io?token=c7vd5g2ad3i9ikp805vg")
    # ws.send('{"type":"subscribe","symbol":"BINANCE:ETHUSDT"}')
    # print(ws.recv())
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=c7vd5g2ad3i9ikp805vg", on_open=on_open)
    ws.run_forever()