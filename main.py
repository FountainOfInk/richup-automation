from websocket import create_connection
import websocket
import time

# TODO: create a thread to keep the connection alive
#       for both the websocket, and through the HTTP
#       maintanence-info endpoint

def init_connection() -> websocket.WebSocket:
    ws = create_connection("wss://richup.io/socket.io/?EIO=4&transport=websocket")
    return ws

def join_game(conn: websocket.WebSocket, room_id: str, name: str, appearance: str = "#FFC73F"):
    # returns the SID (of the connection?)
    conn.send("40/api/game,")
    print(conn.recv())
    check(conn.recv(), 'sid')

    # returns a large (>12kb) json message detailing all the info of the game's current state:
    # all the properties and all their prices, if an auction is going on, who's the top bidder,
    # all the chance cards and their effects, etc. etc.
    print('42/api/game,["enter-room",{"roomId":"{%s}"}]' % room_id)
    conn.send('42/api/game,["enter-room",{"roomId":"{%s}"}]' % room_id)
    check(conn.recv(), '42/api/game,["entered-room",')

    # returns a message containing all the information about the player that just joined (you!)
    conn.send('42/api/game,["join-game",{"name":"%s","appearance":"%s"}]' % (name, appearance))
    check(conn.recv(), '42/api/game,["joined-game",')

    

def terminate(conn: websocket.WebSocket):
    conn.close()

# check if a string contains an expected substring, if it doesn't, print the string and raise an error
def check(string, expected_substring):
    try:
        assert expected_substring in string
    except AssertionError:
        print("Substring not found in string!")
        print("String contents:")
        print(string)
        raise AssertionError

if __name__ == "__main__":
    c = init_connection()
    join_game(c, "q9gvf", "hello")
    # time.sleep(5)
    # terminate(c)