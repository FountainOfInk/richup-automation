import websocket
import time
import json
import rel
from isthisreal import join_game, playerBot

# TODO: create a thread to keep the connection alive
#       for both the websocket, and through the HTTP
#       maintanence-info endpoint

headers = {
    'Cookie': "connect.sid=s%3AY7EkQmqEKraz0HrspU-CDAr6PKr1whPd.l2UpbMP6rysUKlT%2Fj69vPudyDVmkVOm4Qt5FDUi%2B2Ak; __ppIdCC=rixgup_io210883588.43.4; _ga_WE0S6HYRRZ=GS1.1.1688358895.1.1.1688359572.60.0.0; _ga=GA1.2.186912632.1688358896; usprivacy=1YYN; _pbjs_userid_consent_data=3524755945110770; sharedid=738d5254-d80f-420e-9d2c-712b4e7e9efa; __gads=ID=44e6ba0e4763a2e1:T=1688358904:RT=1688358904:S=ALNI_MYXKuvyFHsFnSzM20EhHjCtJVEsiA; __gpi=UID=000009a2eac2ac0f:T=1688358904:RT=1688358904:S=ALNI_MYwBviDPxYHE0kVstKk1VeUh8K00A; _cc_id=5f77588038484baba9a1e179d95095e8; panoramaId_expiry=1688963707952; panoramaId=7a1f69805ee2d423cce983723752bd9563ce17f28a657f9523af3d4fdae490b4; panoramaIdType=panoIndiv; cto_bundle=FxcxSF9vcjREOHhMUEdtd0dWaCUyRjFwdTJ5S3kwSVhNQzg1MFVyY1B3UkVJM041ZVk3U2dPUlVqS1RhNmpKVEw4OXkzaVBPOEhQOWY0VXJvdDlSUjQ0ZzROZDlBSk5HTDFMbGdwRWl1YXp0SW5xSzRSSiUyQlhLMW9hVHdMMmREUzVHdyUyQnNQNjZDVmRVWGxHaFEwJTJGdE1SWHZ2YmE0ZyUzRCUzRA; CountryCode=US; userFromEEA=false"
}

bot: playerBot

def on_message(ws: websocket.WebSocket, message):
    if message == "2":
        ws.send("3")
    elif "entered-room" in message:
        room_data = json.loads(message[len("42/api/game,"):])[1]["room"]
        bot.game.turn_number = room_data["stats"]["turnsCount"]
        if room_data["id"] != bot.game.room_id:
            raise ValueError
        for participant in room_data["participants"]:
            if participant["name"] == bot.name:
                bot.uid = participant["id"]
    


def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")
    join_game(ws, "juxdq", "jej")

if __name__ == "__main__":
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://richup.io/socket.io/?EIO=4&transport=websocket", header=headers,
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()