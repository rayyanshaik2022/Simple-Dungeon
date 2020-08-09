import pygame

class TextBox:

    def __init__(self, rect, color, max_=20, font=(None, (255,255,255))):

        self.rect = pygame.Rect(rect)
        self.color = color

        self.outline_color = color
        self.outline_weight = 1

        self.font = font[0]
        self.font_color = font[1]
        
        self.selected = False
        self.text = ""
        self.max = max_

    def interact(self, keys_pressed):

        if pygame.mouse.get_pressed()[0]:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.selected = True
            else:
                self.selected = False
        
        if self.selected:
            for key in keys_pressed:
                if key == 'del':
                    try:
                        self.text = self.text[:-1]
                    except:
                        pass
                else:
                    self.text += key
        
        while len(self.text) > self.max:
            self.text = self.text[:-1]


    def draw(self, screen):

        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, self.outline_color, self.rect, self.outline_weight)

        if self.font and len(self.text) > 0:
            text = self.font.render(self.text,True,self.font_color)
            x = int(self.rect.topleft[0] + (self.rect.width - text.get_size()[0])/2)
            y = int(self.rect.topleft[1] + (self.rect.height - text.get_size()[1])/2)
            screen.blit(text, (x, y))