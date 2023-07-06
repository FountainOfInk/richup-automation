import websocket
import time

GAME_LOBBY = 0
GAME_IN_PROGRESS = 1
GAME_FINISHED = 2

class Game:
    room_id: str
    current_turn: int
    state: bool

    def __init__(self, room_id) -> None:
        self.room_id = room_id
        self.state = False

class playerBot:
    conn: websocket.WebSocketApp
    name: str
    appearance: str
    uid: str
    # every N turns it will our turn, what is N?        
    my_turn: int
    game: Game

    def __init__(self, conn, room_id, name, appearance = "#FFC73F") -> None:
        self.conn = conn
        self.name = name
        self.appearance = appearance
        self.uid = None


        self.game = Game(room_id)

        self.join_game(conn, room_id, name, appearance)

        
    def join_game(self):
        # returns the SID (of the connection?)
        self.conn.send("40/api/game,")
        time.sleep(0.5)

        # returns a large (>12kb) json message detailing all the info of the game's current state:
        # all the properties and all their prices, if an auction is going on, who's the top bidder,
        # all the chance cards and their effects, etc. etc.
        self.conn.send('42/api/game,["enter-room",{"roomId":"%s"}]' % self.game.room_id)
        time.sleep(0.5)

        # returns a message containing all the information about the player that just joined (you!)
        self.conn.send('42/api/game,["join-game",{"name":"%s","appearance":"%s"}]' % (self.name, self.appearance))
        time.sleep(0.5)


    def roll_dice(self):
        self.conn.send()

    def leave(self):
        self.conn.close()
