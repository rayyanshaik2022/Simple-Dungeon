import pygame
import numpy as np

pygame.init()

WIDTH = 1200
HEIGHT = 800
FPS = 60

screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()
ss_bits = 8
ideal_size = 32
picker_size = 64
selected_img = 0
c = 0
selected_layer = 1
rotation = 0

a_width = 25
a_height = 25

layer1 = []
layer2 = []
for i in range(a_height):
    a = []
    b = []
    for j in range(a_width):
        a.append(-1)
        b.append(-1)
    layer1.append(a)
    layer2.append(b)
    

class spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as message:
            print ('Unable to load spritesheet image:', filename)
            raise SystemExit
    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA); image.convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates" 
        return [self.image_at(rect, colorkey) for rect in rects]
    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

img_locs = []
for i in range(5):
    for j in range(7):
        img_locs.append((j*ss_bits,i*ss_bits,ss_bits, ss_bits))

rot_0_images = spritesheet('./src/Assets/tile_set_0angle.png').images_at(img_locs, (0,0,0))
rot_90_images = spritesheet('./src/Assets/tile_set_90angle.png').images_at(img_locs, (0,0,0))
rot_180_images = spritesheet('./src/Assets/tile_set_180angle.png').images_at(img_locs, (0,0,0))
rot_270_images = spritesheet('./src/Assets/tile_set_270angle.png').images_at(img_locs, (0,0,0))

running = True
while running:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                selected_layer = 1
            elif event.key == pygame.K_2:
                selected_layer = 2
            elif event.key == pygame.K_s:
                l1 = np.array(layer1)
                l2 = np.array(layer2)

                np.savetxt("maplayer1.txt", l1,fmt='%d')
                np.savetxt("maplayer2.txt", l2,fmt='%d')
                print('saved map')
            elif event.key == pygame.K_r:
                rotation = (rotation+100) % 400
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            m_x, m_y = pygame.mouse.get_pos()

            if m_y >= 600 and m_x >= 800:
                c = -1
                print('erase mode')
            else:
                
                start_pos = (850,50)
                f = 0
                for i in range(7):
                    for j in range(5):         
                        if m_x >= j*picker_size+5*j+start_pos[0] and m_x <= j*picker_size+5*j+start_pos[0]+picker_size:
                            if m_y >= i*picker_size+5*i + start_pos[1] and m_y <= i*picker_size+5*i + start_pos[1] + picker_size:
                                print('you clicked',f)
                                c = f + rotation
                                print(c, "is")
                        f += 1
                
            i_x = m_x // ideal_size
            i_y = m_y // ideal_size

            if i_x < a_width and i_y < a_height:
                if selected_layer == 1:
                    layer1[i_y][i_x] = c
                elif selected_layer == 2:
                    layer2[i_y][i_x] = c


    screen.fill((26, 29, 31))
    pygame.draw.line(screen, (255,255,255), (800,0), (800,HEIGHT))
    pygame.display.set_caption(f"Map Builder | Layer {selected_layer}")
    
    current_images = None
    if rotation < 100:
        current_images = rot_0_images
    elif rotation < 200:
        current_images = rot_90_images
    elif rotation < 300:
        current_images = rot_180_images
    elif rotation < 400:
        current_images = rot_270_images

    c1 = 0
    start_pos = (850,50)
    for i in range(7):
        for j in range(5):
            img = pygame.transform.scale(current_images[c1], [picker_size,picker_size])
            screen.blit(img, (j*picker_size+5*j+start_pos[0], i*picker_size+5*i + start_pos[1]))
            c1 += 1
    
    for i in range(len(layer1)):
        for j in range(len(layer1[0])):
            val = layer1[i][j]
            if val != -1:
                current_images = None
                if val < 100:
                    current_images = rot_0_images
                elif val < 200:
                    current_images = rot_90_images
                    val -= 100
                elif val < 300:
                    current_images = rot_180_images
                    val -= 200
                elif val < 400:
                    current_images = rot_270_images
                    val -= 300
                img = pygame.transform.scale(current_images[val], [ideal_size,ideal_size])
                screen.blit(img, (j*ideal_size, i*ideal_size))
    
    for i in range(len(layer1)):
        for j in range(len(layer1[0])):
            val = layer2[i][j]
            if val != -1:
                current_images = None
                if val < 100:
                    current_images = rot_0_images
                elif val < 200:
                    current_images = rot_90_images
                    val -= 100
                elif val < 300:
                    current_images = rot_180_images
                    val -= 200
                elif val < 400:
                    current_images = rot_270_images
                    val -= 300
                img = pygame.transform.scale(current_images[val], [ideal_size,ideal_size])
                screen.blit(img, (j*ideal_size, i*ideal_size))

    for i in range(len(layer1)):
        continue
        pygame.draw.line(screen, (255,255,255), (0,i*ideal_size), (800,i*ideal_size))
        pygame.draw.line(screen, (255,255,255), (i*ideal_size,0), (i*ideal_size, HEIGHT))

    pygame.display.flip()

pygame.quit()