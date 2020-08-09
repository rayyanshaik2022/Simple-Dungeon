import json
import random
import time

import pygame
import pygame.gfxdraw

from Dynamic.crawler import Crawler
from Dynamic.spritesheet import spritesheet
from Interactables.button import Button
from Interactables.text_box import TextBox
from network import Network
from settings import *


class Client:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.fonts = {}
        self.keys_pressed = []
        self.mode_ticks = {'menu':0, 'connecting':0, 'lobby':0}

    def setup(self):
        
        self.fonts['Iceland-Regular'] = '.\Fonts\Iceland-Regular.ttf'
        self.fonts['Nasalization-Regular'] = '.\Fonts\-Nasalization-Regular.ttf'
        self.fonts['Rubber-Biscuit'] = '.\Fonts\-rubber-biscuit.ttf'
        self.fonts['Yoster'] = '.\Fonts\yoster-island.ttf'

        self.state = "Menu"

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000 # Controls update speed (FPS per second)
            self.events()
            self.update()
            self.draw()

    def close(self):
        pygame.quit()
        quit()

    def update(self):
        pygame.display.set_caption(f"Virus | {self.clock.get_fps()}")
        pass

    def draw(self):
        
        if self.state == "Menu":
            self.menu_screen()
        elif self.state == "Connecting-Server":
            self.connecting_screen()
        elif self.state == "Game-Lobby":
            self.lobby_screen()

    def events(self):
        # catch all events here
        self.keys_pressed = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    try:
                        self.keys_pressed.append('del')
                    except:
                        pass
                else:
                    self.keys_pressed.append(event.unicode)
    
    def menu_screen(self):

        if self.mode_ticks['menu'] == 0:
            rint = random.randint
            self.menu_interactables = {'buttons' : {}, 'fonts' : {}, 'crawlers' : [], 'text-boxes' : {}}

            self.menu_interactables['fonts']['title'] = pygame.font.Font(self.fonts['Rubber-Biscuit'], 140)
            self.menu_interactables['fonts']['button-regular'] = pygame.font.Font(self.fonts['Nasalization-Regular'], 70)
            self.menu_interactables['fonts']['text-box-a'] = pygame.font.Font(self.fonts['Nasalization-Regular'], 45)


            self.menu_interactables['buttons']['start'] = Button(
                                                            (500,450,200,100), (49, 82, 135),
                                                            self.menu_interactables['fonts']['button-regular'],
                                                            ("Play", (211, 216, 224))
                                                                )

            self.menu_interactables['text-boxes']['name'] = TextBox(
                (400, 350, 400, 75), (240,240,240), 10,
                (self.menu_interactables['fonts']['text-box-a'], (15,15,15))
            )
            self.menu_interactables['text-boxes']['name'].outline_color = (59, 66, 79)
            self.menu_interactables['text-boxes']['name'].outline_weight = 5

            for i in range(30):
                self.menu_interactables['crawlers'].append(Crawler(rint(5,15), 25, rint(10,65)))

            # Try to see if previous name is saved
            try:
                with open("preferences.txt","r") as file:
                    for line in file:
                        self.menu_interactables['text-boxes']['name'].text = line
                        break
            except:
                pass
        # Background
        self.screen.fill(COLORS['background'])

        # Update crawlers
        for crawler in self.menu_interactables['crawlers']:
            crawler.update(self.mode_ticks['menu'])
            crawler.draw(self.screen)

        # Title text
        title_text = self.menu_interactables['fonts']['title'].render("Virus", True, (240, 242, 245))
        self.screen.blit(title_text, (int( 0.5*WIDTH - 0.5*title_text.get_size()[0]),50))

        # Draw text boxes
        for key in self.menu_interactables['text-boxes']:
            text_box = self.menu_interactables['text-boxes'][key]
            text_box.draw(self.screen)
            text_box.interact(self.keys_pressed)

        # Draw buttons
        for key in self.menu_interactables['buttons']:
            button = self.menu_interactables['buttons'][key]
            button.draw(self.screen)

            if button.interact() and self.mode_ticks['menu'] > 25:
                if key == "start":
                    self.state = "Connecting-Server"
                    with open("preferences.txt","w") as text_file:
                        text_file.write(self.menu_interactables['text-boxes']['name'].text)
                        self.name = self.menu_interactables['text-boxes']['name'].text
                    del self.menu_interactables


        pygame.display.flip()
        self.mode_ticks['menu'] += 1
    
    def connecting_screen(self):

        if self.mode_ticks['connecting'] == 0:
            self.conn_interactables = {
            'buttons' : {}, 
            'fonts' : {
                'conn' : pygame.font.Font(self.fonts['Nasalization-Regular'], 100),
                'conn2' : pygame.font.Font(self.fonts['Nasalization-Regular'], 70),
                'button-regular' : pygame.font.Font(self.fonts['Nasalization-Regular'], 60)
                }}
            
            self.conn_interactables['buttons']['menu'] = Button(
                (int(WIDTH/2 - 210),500,420,120), (49, 82, 135),self.conn_interactables['fonts']['button-regular'],("Main Menu", (211, 216, 224))
                )

            self.net = Network()

        if self.mode_ticks['connecting'] >= 100:
            if self.net.made_connection == None:
                print(self.net.connect(), " to ", self.net.addr)

            if self.net.made_connection:
                self.net.push({"name" : self.name})
                self.state = "Game-Lobby"
                del self.conn_interactables
            else:
                self.screen.fill(COLORS['background'])
                # Connection text
                conn_text = self.conn_interactables['fonts']['conn2'].render("Failed to connect to a server", True, (240, 242, 245))
                self.screen.blit(conn_text, (int( 0.5*WIDTH - 0.5*conn_text.get_size()[0]),250))

                self.conn_interactables['buttons']['menu'].draw(self.screen)

                if self.conn_interactables['buttons']['menu'].interact():
                    self.mode_ticks['menu'] = 0
                    self.mode_ticks['connecting'] = 0
                    self.state = "Menu"
                    del self.net
                    return

        else:
            self.screen.fill(COLORS['background'])

            # Connection text
            conn_text = self.conn_interactables['fonts']['conn'].render("Connecting...", True, (240, 242, 245))
            self.screen.blit(conn_text, (int( 0.5*WIDTH - 0.5*conn_text.get_size()[0]),300))

        pygame.display.flip()
        self.mode_ticks['connecting'] += 1
    
    def lobby_screen(self):

        if self.mode_ticks['lobby'] == 0:

            self.lobby_interactables = {
                'fonts' : {
                    'title' : pygame.font.Font(self.fonts['Nasalization-Regular'], 100),
                    'names' : pygame.font.Font(self.fonts['Nasalization-Regular'], 40)
                },
                'images' : {
                    'Spirit-Boxer' : [],
                    'Samurai-Merchant' : []
                },
                'boxes' : [
                ],
                'counters' : {
                    'img-tick' : 0
                }
            }

            # Set name boxes
            box1 = pygame.Rect(0,0,300,70)
            box1.center = (int(WIDTH/2), 600)
            box2 = box1.copy(); box2.centerx -= box2.width + 50
            box3 = box1.copy(); box3.centerx += box3.width + 50
            box4 = box1.copy(); box4.centery += 120
            box5 = box4.copy(); box5.centerx -= box5.width + 50
            box6 = box4.copy(); box6.centerx += box6.width + 50
            self.lobby_interactables['boxes'] = [box2,box1,box3,box5,box4,box6]

            # Get Spirit Boxer images
            spirit_boxer_images = []
            for i in range(4):
                spirit_boxer_images.append((i*14 + i*2,0,14,19))
            self.lobby_interactables['images']['Spirit-Boxer']=spritesheet('./Assets/Spirit-Boxer-Idle.png').images_at(spirit_boxer_images, (0,0,0))

            # Get Samurai Images
            samurai_images = []
            for i in range(4):
                samurai_images.append((i*38 + i*2,0,38,26))
            self.lobby_interactables['images']['Samurai-Merchant']=spritesheet('./Assets/Samurai-Merchant-Idle.png').images_at(samurai_images, (255,255,255,255))
        
        if self.net.request("state") != 0: # 0 is the state for lobby
            self.screen.fill(COLORS['background'])
            wait_text = self.lobby_interactables['fonts']['title'].render("Session in progress...",True,(240, 242, 245))
            self.screen.blit(wait_text, (int( 0.5*WIDTH - 0.5*wait_text.get_size()[0]),300))
        else:
            self.screen.fill(COLORS['background'])
            all_players = self.net.request("player_names")
            
            
            # Draw cards and names of connected players (in order)
            for i, box in enumerate(self.lobby_interactables['boxes']):
                pygame.draw.rect(self.screen, (27, 29, 33), box)
                if i < len(all_players):
                    name_text = self.lobby_interactables['fonts']['names'].render(all_players[i][1],True,(240, 242, 245))
                    x = int(box.topleft[0] + (box.width - name_text.get_size()[0])/2)
                    y = int(box.topleft[1] + (box.height - name_text.get_size()[1])/2)
                    self.screen.blit(name_text, (x,y))
            
            if self.mode_ticks['lobby'] % 30 == 0:
                self.lobby_interactables['counters']['img-tick'] += 1
            
            samurai_img = self.lobby_interactables['images']['Samurai-Merchant'][self.lobby_interactables['counters']['img-tick']%4]
            samurai_img = pygame.transform.scale(samurai_img, (samurai_img.get_width()*8, samurai_img.get_height()*8))
            self.screen.blit(samurai_img, (0,0))

            spirit_img = self.lobby_interactables['images']['Spirit-Boxer'][self.lobby_interactables['counters']['img-tick']%4]
            spirit_img = pygame.transform.scale(spirit_img, (spirit_img.get_width()*8, spirit_img.get_height()*8))
            self.screen.blit(spirit_img, (400,50))
    
        pygame.display.flip()
        self.mode_ticks['lobby'] += 1

# create the game object
g = Client()
g.setup()
g.run()
