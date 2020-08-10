import pygame

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
    
    def update(self):

        if self.c_state == 0:
            
            c = 0
            for char in self.lobby['selected_characters']:
                if self.lobby['selected_characters'][char] != None:
                    c += 1
            
            if c >= 2:
                self.lobby['start_countdown'] -= (1/60)
            else:
                self.lobby['start_countdown'] = 5 # Reset timer (65)
            
            if self.lobby['start_countdown'] < 0:
                self.c_state = 1
                c = 0
        
        elif self.c_state == 1:
            
            # Initialization of stuff here
            if self.game_information == None:
                pass