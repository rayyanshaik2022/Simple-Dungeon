import pygame
import numpy as np
import random
import math

class GameState:

    def __init__(self):

        self.clock = pygame.time.Clock()
        self.states = ["lobby"]
        self.c_state = 0

        self.lobby = {
            'players_connected' : {},
            'selected_characters' : {
                'Spirit-Boxer' : None,
                'Samurai-Merchant' : None
            },
            'start_countdown' : 65
        }

        self.game_information = None
        self.map = None
    
    def prune_map(self, m):
        layered_map = []
        for layer in m:
            for row in layer:
                if all(i == row[0] and i == -1 for i in row):
                    layer.append(row)
                    layer = layer[1:]

            layered_map.append(layer)
        self.map = layered_map


    def update(self):

        if self.c_state == -1:
            print("RESETTING SERVER")
            self.game_information = None
            self.c_state = 0

        if self.c_state == 0:
            
            c = 0
            for char in self.lobby['selected_characters']:
                if self.lobby['selected_characters'][char] != None:
                    c += 1
            
            if c >= 2: # Number of people required to start game
                self.lobby['start_countdown'] -= (1/60)
            else:
                self.lobby['start_countdown'] = 5 # Reset timer (65)
            
            if self.lobby['start_countdown'] < 0:
                self.c_state = 1
                c = 0
        
        elif self.c_state == 1:
            
            # Initialization of stuff here
            if self.game_information == None:

                # Spawn positions are situational depending on map (set up for map_tutorial)
                self.game_information = {
                    "players" : {
                        'Spirit-Boxer' : {
                            'id_' : self.lobby['selected_characters']['Spirit-Boxer'],
                            'angle' : 0,
                            'pos' : [3*128, 10*128],
                            'speed' : 2
                        },
                        'Samurai-Merchant' : {
                            'id_' : self.lobby['selected_characters']['Samurai-Merchant'],
                            'angle' : 0,
                            'pos' : [3*128, 10*128],
                            'speed' : 2
                        }
                    }
                }

            for char in self.game_information['players']:
                character = self.game_information['players'][char]
                character['pos'][0] += math.cos(character['angle']) * character['speed']
                character['pos'][1] += math.sin(character['angle']) * character['speed']
        
        if self.lobby['players_connected'] == {} and self.c_state not in [-1,0]:
            self.c_state = -1