from websocket import create_connection
import websocket
import time

def init_connection() -> websocket.WebSocket:
    ws = create_connection("wss://richup.io/socket.io/?EIO=4&transport=websocket")
    return ws

def join_game(conn: websocket.WebSocket, room_id: str):
    conn.send("40/api/game,")
    a = conn.recv()
    print(a)
    conn.send('42/api/game,["enter-room",{"roomId":"{%s}"}]' % room_id)

def terminate(conn: websocket.WebSocket):
    conn.close()

if __name__ == "__main__":
    c = init_connection()
    join_game(c, "3f2ag")
    time.sleep(5)
    # terminate(c)