import websocket
import time
import rel
from isthisreal import join_game

# TODO: create a thread to keep the connection alive
#       for both the websocket, and through the HTTP
#       maintanence-info endpoint

def on_message(ws: websocket.WebSocket, message):
    if message == "2":
        ws.send("3")

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")
    join_game(ws, "ahr8d", "west has risen", "#FFFFFF")

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://richup.io/socket.io/?EIO=4&transport=websocket",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()