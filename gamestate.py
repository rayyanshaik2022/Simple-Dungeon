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
            }
        }