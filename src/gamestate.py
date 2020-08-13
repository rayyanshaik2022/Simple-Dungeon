import pygame
import numpy as np
import random
import math
from settings import *

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
            
            if c >= 1: # Number of people required to start game
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
                            'pos' : [5*TILE_SIZE, 12*TILE_SIZE],
                            'speed' : 2,
                            'size' : [16*PLAYER_SCALING, 19*PLAYER_SCALING]
                        },
                        'Samurai-Merchant' : {
                            'id_' : self.lobby['selected_characters']['Samurai-Merchant'],
                            'angle' : 0,
                            'pos' : [5*TILE_SIZE, 12*TILE_SIZE],
                            'speed' : 2,
                            'size' : [38*PLAYER_SCALING, 24*PLAYER_SCALING]
                        }
                    }
                }

            for char in self.game_information['players']:
                character = self.game_information['players'][char]
                # Move character
                f_x = character['pos'][0] + math.cos(character['angle']) * character['speed']
                f_y = character['pos'][1] + math.sin(character['angle']) * character['speed']

                # Check if character is out of bounds
                feet_pos = [int(f_x/TILE_SIZE), int((f_y + character['size'][1]/2)/TILE_SIZE)]
                old_feet_pos = [int(character['pos'][0]/TILE_SIZE), int((character['pos'][1] + character['size'][1]/2)/TILE_SIZE)]
                if (feet_pos[0] >= 0 and feet_pos[0] < len(self.map[0][0])) and (feet_pos[1] >= 0 and feet_pos[1] < len(self.map[0])):
                    
                    block_tiles = [0,3,1,4,10,5,8,9]
                    for i in range(100,400,100):
                        for item in block_tiles:
                            if item not in block_tiles:
                                block_tiles.append(item*i)

                    if self.map[0][feet_pos[1]][feet_pos[0]] in block_tiles:

                        if self.map[0][old_feet_pos[1]][feet_pos[0]] not in block_tiles:
                            character['pos'] = [f_x, character['pos'][1]]
                        elif self.map[0][feet_pos[1]][old_feet_pos[0]] not in block_tiles:
                            character['pos'] = [character['pos'][0], f_y]
                        else:
                            # TODO: FIX CORNER UPDATES
                            character['pos'] = [old_feet_pos[0]*TILE_SIZE, old_feet_pos[1]*TILE_SIZE]
                    else:
                        character['pos'] = [f_x, f_y]
                else:
                    character['pos'] = [f_x, f_y]
        
        if self.lobby['players_connected'] == {} and self.c_state not in [-1,0]:
            self.c_state = -1