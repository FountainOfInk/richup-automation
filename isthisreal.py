import websocket
import time

def join_game(conn: websocket.WebSocketApp, room_id: str, name: str, appearance: str = "#FFC73F"):
    # returns the SID (of the connection?)
    conn.send("40/api/game,")
    time.sleep(0.5)

    # returns a large (>12kb) json message detailing all the info of the game's current state:
    # all the properties and all their prices, if an auction is going on, who's the top bidder,
    # all the chance cards and their effects, etc. etc.
    conn.send('42/api/game,["enter-room",{"roomId":"%s"}]' % room_id)
    time.sleep(0.5)

    # returns a message containing all the information about the player that just joined (you!)
    conn.send('42/api/game,["join-game",{"name":"%s","appearance":"%s"}]' % (name, appearance))
    time.sleep(0.5)



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