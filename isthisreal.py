import websocket
import time
import json
from utils import log

GAME_LOBBY = 0
GAME_IN_PROGRESS = 1
GAME_FINISHED = 2

class Game:
    room_id: str
    # the index of the current player
    # whose turn it is, where 1 is
    # the first player
    current_turn: int
    players: int
    state: int
    host: str

    def __init__(self, room_id) -> None:
        self.room_id = room_id
        self.state = None
        self.current_turn = None
        self.players = None
        self.host = None

class playerBot:
    conn: websocket.WebSocketApp
    name: str
    appearance: str
    uid: str
    waitingforturn: bool
    # every N turns it will our turn, what is N?        
    my_turn: int
    game: Game

    can_roll_dice: int

    def __init__(self, conn, room_id, name, appearance = "#FFC73F") -> None:
        self.conn = conn
        self.name = name
        self.appearance = appearance
        self.uid = None
        self.can_roll_dice = True
        self.my_turn = None
        self.waitingforturn = False

        self.game = Game(room_id)
        self.enter_room()
            
        
        
    def enter_room(self):
        # returns the SID (of the connection?)
        self.conn.send("40/api/game,")
        time.sleep(0.2)

        # returns a large (>12kb) json message detailing all the info of the game's current state:
        # all the properties and all their prices, if an auction is going on, who's the top bidder,
        # all the chance cards and their effects, etc. etc.
        self.conn.send('42/api/game,["enter-room",{"roomId":"%s"}]' % self.game.room_id)
        time.sleep(0.2)

    def join_game(self):
        # returns a message containing all the information about the player that just joined (you!)
        self.conn.send('42/api/game,["join-game",{"name":"%s","appearance":"%s"}]' % (self.name, self.appearance))
        time.sleep(0.2)

    
    # set my_turn, game.current_turn, and game.state
    def handle_game_started(self, message: str):
        log("Game starting!", "info")
        game_data = json.loads(message[len("42/api/game,"):])[1]
        self.game.players = len(game_data["participantsOrder"])
        for i,player in enumerate(game_data["participantsOrder"]):
            if player["id"] == self.uid:
                self.my_turn = i
        self.game.current_turn = 0
        self.game.state = GAME_IN_PROGRESS

    # set uid
    def handle_join_game(self, message: str):
        self_data = json.loads(message[len("42/api/game,"):])[1]["selfPlayer"]
        self.uid = self_data["id"]
    
    # set game.state, game.current_turn, game.host
    def handle_entered_room(self, message: str):
        room_data = json.loads(message[len("42/api/game,"):])[1]["room"]
        self.game.state = room_data["state"]
        if not self.game.state == GAME_IN_PROGRESS:
            self.join_game()

    # set uid, game.players, and my_turn
    def handle_rejoin(self, message: str):
        data = json.loads(message[len("42/api/game,"):])[1]
        room_data = data["room"]

        self.uid = data['selfParticipantId']

        self.game.players = len(room_data["players"])
        self.game.current_turn = room_data["stats"]["turnsCount"]
        

        for i,player in enumerate(room_data["players"]):
            log(f"player:{player['name']}, id:{player['id']}")
            log(f"me: {self.name}, id: {self.uid}")
            if player["id"] == self.uid:
                self.my_turn = i
                break

    def roll_dice(self):
        self.conn.send('42/api/game,["plz-roll-dices"]')
    
    def end_turn(self):
        self.conn.send('42/api/game,["end-turn"]')
    
    def start_game(self):
        self.conn.send('42/api/game,["start-game"]')
    
    def resign(self):
        self.conn.send('42/api/game,["do-bankrupt"]')
    
    def purchase_current_property(self):
        self.conn.send('42/api/game,["purchase-property"]')

    def leave(self):
        self.conn.close()
