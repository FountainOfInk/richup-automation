import websocket
import time


class Game:
    room_id: str
    turn_number: int

    def __init__(self) -> None:
        pass

class playerBot:
    conn: websocket.WebSocketApp
    name: str
    appearance: str
    uid: str
    # every N turns it will our turn, what is N?        
    my_turn_every: int
    game: Game

    def __init__(self, conn, room_id, name, appearance) -> None:
        self.conn = conn
        self.name = name
        self.appearance = appearance


        self.game = Game()
        self.game.room_id = room_id

        join_game(conn, room_id, name, appearance)


    
        
def join_game(conn: websocket.WebSocketApp, room_id: str, name: str, appearance: str = "#FFC73F") -> Game:
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


def roll_dice():
    pass
def terminate(conn: websocket.WebSocket):
    conn.close()
