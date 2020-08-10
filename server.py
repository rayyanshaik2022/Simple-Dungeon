import pickle
import socket
import sys

from gamestate import GameState

from _thread import *

server = "192.168.0.4"
port = 5555

print(f"Attempting to start server on ({server},{port})")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind(('', port))
except socket.error as e:
    print(str(e))
    print("Server will start on local address")


s.listen(2)
print("Waiting for a connection, Server Started")


game = GameState()

def disconect(id_):

    del game.lobby['players_connected'][str(id_)]

    for character in game.lobby['selected_characters']:
        if game.lobby['selected_characters'][character] == str(id_):
            game.lobby['selected_characters'][character] = None

def threaded_client(conn, addr):
    '''
    A threaded function that opens for each connected client.
    It receives input data and sends the current grid state
    '''

    id_ = addr[1]
    conn.send(pickle.dumps(id_))
    print("sent id")

    # If over 6 players connected
    if len(game.lobby['players_connected']) > 6:
        print("Lost connection")
        disconect(id_)
        print("Removed",id_,"from the lobby")
        conn.close()
        return

    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            reply = {"message" : "reply"}

            if not data:
                print("Disconnected")
                break
            else:
                #print("Received input", data)
                #print("Sending grid state:",reply)
                pass
            
            if data['action'] == 'push':
                for key in data['data']:
                    game.lobby['players_connected'][str(id_)][key] = data['data'][key]
                    print(f"{id_}'s {key} set to {data['data'][key]}")
            elif data['action'] == 'request':
                req = data['data']
                if req == "state":
                    reply = game.c_state
                elif req == "player_names":
                    reply = [[key, game.lobby['players_connected'][key]['name']] for key in game.lobby['players_connected']]
                elif req == "selected_characters":
                    reply = game.lobby["selected_characters"]
                elif req == "lobby_countdown":
                    reply = game.lobby['start_countdown']
            elif data['action'] == 'try':
                for key in data['data']:
                    if key == "selected-character":
                        if game.lobby['selected_characters'][data['data'][key]] == None:
                            for character in game.lobby['selected_characters']:
                                if game.lobby['selected_characters'][character] == str(id_):
                                    game.lobby['selected_characters'][character] = None
                            game.lobby['selected_characters'][data['data'][key]] = str(id_)
                        elif game.lobby['selected_characters'][data['data'][key]] == str(id_):
                            game.lobby['selected_characters'][data['data'][key]] = None
                        else:
                            pass
            
            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    disconect(id_)
    print("Removed",id_,"from the lobby")
    conn.close()

def update_grid():
    '''
    Function that manages the game state.
    Using a clock, it updates 60 times a
    second (60 ticks)
    '''

    UPS = 60 # Updates per second
    while True:
        game.clock.tick(UPS)

        game.update()

start_new_thread(update_grid, ())
while True:
    conn, addr = s.accept()
    print("Connection from:",addr)
    
    start_new_thread(threaded_client, (conn,addr,))
    game.lobby['players_connected'][str(addr[1])] = {}