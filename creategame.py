import websocket
import time
import json
import rel
from isthisreal import playerBot
import isthisreal
from utils import log
import requests
import subprocess


headers = {
    'Cookie': "connect.sid=s%3ACuZkgttVDn3fQJXcGC1L81QVvx_xYTir.%2FfR10d1cp%2B0thVzAVp3Nb55WgSCaFSeG8JHAfPusXec; CountryCode=US; userFromEEA=false"
}

bot: playerBot = None
game_code: str = None
start_on_N_players: int = 2
buy_N_properties: int = 5
bought_N_properties: int = 0


def on_message(ws: websocket.WebSocket, message):
    # if not "entered-room" in message:
    log(f"Recieved: {message}", "info")
    if message == "2":
        ws.send("3")
        return
    if "game-error" in message:
        log(message, "error")
        # raise ValueError

    elif "joined-game" in message:
        bot.handle_join_game(message)

    elif "player-joined" in message:
        if bot.game.players == None:
            bot.game.players = 2 # self and the new player
        else:
            bot.game.players += 1
        print(f"Current players: {bot.game.players}")
        if bot.game.players == start_on_N_players:
            bot.start_game()
    # might create a struct representing the game 
    # automatically created from a json example
    # and just load data from that
    elif "entered-room" in message:
        log("entered room")
        room_data = json.loads(message[len("42/api/game,"):])[1]["room"]
        log(f'room state: {room_data["state"]}, gameinprogress: {isthisreal.GAME_IN_PROGRESS}')
        bot.handle_entered_room(message)
        assert bot.game.state == room_data["state"]
        if bot.game.state == isthisreal.GAME_IN_PROGRESS:
            log("REJOINING")
            bot.handle_rejoin(message)



    elif "game-started" in message:
        bot.handle_game_started(message)
    

    if bot.game.state == isthisreal.GAME_IN_PROGRESS:
        if "turn-ended" in message:
            bot.game.current_turn += 1
            log(f"current turn: {bot.game.current_turn}", "success")
            if bot.game.current_turn >= 83:
                print("among us")
        # nth_players_turn = bot.game.current_turn % bot.game.players
        # # M % N = 0, where M is some multiple of N
        # # so if it's the 9th turn and we are the 3rd
        # # player in order, it's our turn (for the third time)
        # assert bot.game.current_turn is not None
        # assert bot.my_turn is not None
        # log(f"Current turn: {bot.game.current_turn}, Nth player's turn: {nth_players_turn}, my turn: {bot.my_turn}")
        # if nth_players_turn == bot.my_turn:
        if "This is not your turn" in message:
            bot.waitingforturn = True
            return
        elif "You have already rolled the dice in this turn" in message:
            global buy_N_properties
            global bought_N_properties
            if buy_N_properties > bought_N_properties:
                bot.purchase_current_property()
                bought_N_properties +=1
            bot.end_turn()
            bot.waitingforturn = False
        else:
            bot.waitingforturn = False

        
        if not bot.waitingforturn:
            bot.roll_dice()

        # log("my turn!", "success")
        # if "dice-rolled" in message:
        #     dice_data = json.loads(message[len("42/api/game,"):])[1]["dice"]
        #     doubles = dice_data[0] == dice_data[1]
        #     bot.can_roll_dice = doubles

        # if not bot.waitingforturn:
        #     log("i can roll the dice, rolling")
        #     bot.roll_dice()
        # else:
        #     log("i cannot roll the dice, ending my turn")
        #     bot.can_roll_dice = True
            
        time.sleep(0.2)
        

def on_error(ws, error):
    raise error
    log(error, "error")
    pass

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")
    print(f"Close status code: {close_status_code}")
    print(f"Close message: {close_msg}")
    pass

# MAIN() is here!!
def on_open(ws):
    log("Opened connection", "success")
    global bot
    bot = playerBot(ws, game_code, "amonger")
    time.sleep(0.2)
    subprocess.Popen(['python3', 'main.py', game_code])


if __name__ == "__main__":
    # websocket.enableTrace(True, level="trace")
    game_code = requests.get("https://richup.io/api/room/new?isPrivate=false").json()["roomId"]
    print(game_code)
    ws = websocket.WebSocketApp("wss://richup.io/socket.io/?EIO=4&transport=websocket", header=headers,
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()