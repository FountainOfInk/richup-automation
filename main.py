import websocket
import time
import json
import rel
from isthisreal import playerBot
import isthisreal

# TODO: create a thread to keep the connection alive
#       for both the websocket, and through the HTTP
#       maintanence-info endpoint

headers = {
    'Cookie': "connect.sid=s%3AY7EkQmqEKraz0HrspU-CDAr6PKr1whPd.l2UpbMP6rysUKlT%2Fj69vPudyDVmkVOm4Qt5FDUi%2B2Ak; __ppIdCC=rixgup_io210883588.43.4; _ga_WE0S6HYRRZ=GS1.1.1688358895.1.1.1688359572.60.0.0; _ga=GA1.2.186912632.1688358896; usprivacy=1YYN; _pbjs_userid_consent_data=3524755945110770; sharedid=738d5254-d80f-420e-9d2c-712b4e7e9efa; __gads=ID=44e6ba0e4763a2e1:T=1688358904:RT=1688358904:S=ALNI_MYXKuvyFHsFnSzM20EhHjCtJVEsiA; __gpi=UID=000009a2eac2ac0f:T=1688358904:RT=1688358904:S=ALNI_MYwBviDPxYHE0kVstKk1VeUh8K00A; _cc_id=5f77588038484baba9a1e179d95095e8; panoramaId_expiry=1688963707952; panoramaId=7a1f69805ee2d423cce983723752bd9563ce17f28a657f9523af3d4fdae490b4; panoramaIdType=panoIndiv; cto_bundle=FxcxSF9vcjREOHhMUEdtd0dWaCUyRjFwdTJ5S3kwSVhNQzg1MFVyY1B3UkVJM041ZVk3U2dPUlVqS1RhNmpKVEw4OXkzaVBPOEhQOWY0VXJvdDlSUjQ0ZzROZDlBSk5HTDFMbGdwRWl1YXp0SW5xSzRSSiUyQlhLMW9hVHdMMmREUzVHdyUyQnNQNjZDVmRVWGxHaFEwJTJGdE1SWHZ2YmE0ZyUzRCUzRA; CountryCode=US; userFromEEA=false"
}

bot: playerBot = None

def on_message(ws: websocket.WebSocket, message):
    if message == "2":
        ws.send("3")
        return

    elif "joined-game" in message:
        self_data = json.loads(message[len("42/api/game,"):])[1]["selfPlayer"]
        bot.uid = self_data["id"]

    # might create a struct representing the game 
    # automatically created from a json example
    # and just load data from that
    elif "entered-room" in message:
        print("hello!!!")
        room_data = json.loads(message[len("42/api/game,"):])[1]["room"]
        bot.game.state = room_data["state"]
        bot.game.current_turn = room_data["stats"]["turnsCount"]

        if room_data["state"] == isthisreal.GAME_IN_PROGRESS:
            bot.uid = room_data['selfParticipantId']
            for i,player in enumerate(room_data["players"]):
                print(f"player:{player['name']}, id:{player['id']}")
                print(f"me: {bot.name}, id: {bot.uid}")
                if player["id"] == bot.uid:
                    bot.my_turn = i+1

        if room_data["id"] != bot.game.room_id:
            raise ValueError

    elif "game-started" in message:
        game_data = json.loads(message[len("42/api/game,"):])[1]
        for i,player in enumerate(game_data["participantsOrder"]):
            if player["id"] == bot.uid:
                bot.my_turn = i+1
        bot.game.current_turn = 1
        bot.game.state = isthisreal.GAME_IN_PROGRESS
    

    if bot.game.state == isthisreal.GAME_IN_PROGRESS:
        #print(f"it is the {bot.game.current_turn}th turn, and my turn is every {bot.my_turn} moves")
        # M % N = 0, where M is some multiple of N
        # so if it's the 9th turn and we are the 3rd
        # player in order, it's our turn (for the third time)
        if bot.game.current_turn % bot.my_turn == 0:
            #print("my turn!")
            if "dice-rolled" in message:
                dice_data = json.loads(message[len("42/api/game,"):])[1]["dice"]
                doubles = dice_data[0] == dice_data[1]
                bot.can_roll_dice = doubles

            if bot.can_roll_dice:
                #print("i can roll the dice, rolling")
                bot.roll_dice()
            else:
                #print("i cannot roll the dice, ending my turn")
                bot.can_roll_dice = True
                bot.end_turn()

        if "turn-ended" in message:
            bot.game.current_turn += 1
        


def on_error(ws, error):
    # print(error)
    pass

def on_close(ws, close_status_code, close_msg):
    #print("### closed ###")
    pass

# MAIN() is here!!
def on_open(ws):
    #print("Opened connection")
    global bot
    bot = playerBot(ws, "5q3pk", "amonger")

if __name__ == "__main__":
    # websocket.enableTrace(True, level="trace")
    ws = websocket.WebSocketApp("wss://richup.io/socket.io/?EIO=4&transport=websocket", header=headers,
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()