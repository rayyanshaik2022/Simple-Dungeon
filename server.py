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


def threaded_client(conn, addr):
    '''
    A threaded function that opens for each connected client.
    It receives input data and sends the current grid state
    '''

    conn.send(pickle.dumps("Connected"))
    print("sent connected")
    id_ = addr[1]
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
            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    del game.lobby['players_connected'][str(id_)]
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

        pass # Do nothing for now

start_new_thread(update_grid, ())
while True:
    conn, addr = s.accept()
    print("Connection from:",addr)
    
    start_new_thread(threaded_client, (conn,addr,))
    game.lobby['players_connected'][str(addr[1])] = {}