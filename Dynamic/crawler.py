import pygame
import random

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from settings import *

class Crawler:

    def __init__(self, length, size, speed):

        self.size = size
        self.speed = speed
        self.direction = None
        self.snake = self.spawn(length)


        self.color = pygame.Color(0,0,0)
        self.color.hsla = (random.randint(1,360), 30, 42, 1)
    
    def update(self, tick):
        if tick % self.speed == 0:
            out = True
            for i in range(len(self.snake)):

                if self.direction[0] != 0:
                    self.snake[i][0] += self.direction[0]
                if self.direction[1] != 0:
                    self.snake[i][1] += self.direction[1]

                # If snake is fully out of bounds, respawn
                if self.snake[i][0] > 0 and self.snake[i][0] < WIDTH and \
                    self.snake[i][1] > 0 and self.snake[i][1] < HEIGHT:
                    out = False
            
            if out:
                self.snake = self.spawn(len(self.snake))
    def draw(self, screen):
        
        for point in self.snake:
            pygame.draw.rect(screen, self.color, (point[0]+1, point[1]+1, self.size-2, self.size-2))

    def spawn(self, length):
        
        r = random.random()
        snake = []
        if r < 0.25:
            snake = [[random.randint(0,WIDTH-self.size), 0]]
            self.direction = [0,self.size]
            for i in range(length):
                snake.insert(0, [ snake[-1][0], snake[-i-1][1]-self.direction[1] ])
        elif r < 0.5:

            snake = [[0, random.randint(0,HEIGHT-self.size)]]
            self.direction = [self.size, 0]
            for i in range(length):
                snake.insert(0, [ snake[-i-1][0]-self.direction[0], snake[-1][1]])
        elif r < 0.75:
            snake = [[random.randint(0,WIDTH-self.size), HEIGHT-self.size]]
            self.direction = [0,-self.size]
            for i in range(length):
                snake.insert(0, [ snake[-1][0], snake[-i-1][1]-self.direction[1] ])
        else:
            snake = [[WIDTH-self.size, random.randint(0,HEIGHT-self.size)]]
            self.direction = [-self.size, 0]
            for i in range(length):
                snake.insert(0, [ snake[-i-1][0]-self.direction[0], snake[-1][1]])
        
        return snake