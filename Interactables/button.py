import pygame

class Button:

    def __init__(self, rect, color, font=None, text=("",(255,255,255))):

        self.rect = pygame.Rect(rect)
        self.generate_colors(color)

        self.font = font
        self.text = text
    
    def draw(self, screen):
        color = self.color
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            color = self.color_light
            if pygame.mouse.get_pressed()[0]:
                color = self.color_pressed

        pygame.draw.rect(screen, color, self.rect)

        if self.font:
            button_text = self.font.render(self.text[0],True,self.text[1])
            x = int(self.rect.topleft[0] + (self.rect.width - button_text.get_size()[0])/2)
            y = int(self.rect.topleft[1] + (self.rect.height - button_text.get_size()[1])/2)
            screen.blit(button_text, (x, y))

        
    
    def interact(self):
        '''
        Returns True if button is pressed
        '''
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                return True
        return False
        
    
    def generate_colors(self, rgb):

        self.color = pygame.Color(*rgb)
        
        hue, sat, lum, _ = self.color.hsla

        self.color_light = pygame.Color(0,0,0)
        self.color_light.hsla = (hue, sat, int(0.925*lum), _)

        self.color_pressed = pygame.Color(0,0,0)
        self.color_pressed.hsla = (hue, sat, int(0.75*lum), _)