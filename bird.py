import pygame
import os
import random


class Bird:
    IMGS = [pygame.transform.scale(pygame.image.load(os.path.join("imgs", "bird.png")), (40, 40)),
            pygame.transform.scale(pygame.image.load(os.path.join("imgs", "bird1.png")), (40, 40))]

    def __init__(self, vel, BG_Width):
        self.state = 0
        self.img = self.IMGS[0]
        self.y = [195, 175, 155][random.randint(0, 2)]
        self.x = BG_Width
        self.vel = vel

        # for ANN input
        self.passed = False

    def move(self):
        '''Moves the bird across the screen.'''
        self.x -= self.vel

    def draw(self, win):
        '''Draws the bird on the screen.'''
        self.state += 0.12
        indx = int(self.state % len(self.IMGS))
        self.img = self.IMGS[indx]

        win.blit(self.img, (self.x, self.y))

    def collide(self, dino):
        '''Determines whether the Dino collided with the bird using masking.'''
        dino_mask = dino.get_mask()
        bird_mask = pygame.mask.from_surface(self.img)
        offset = (self.x - dino.X, self.y - round(dino.y))

        collide = dino_mask.overlap(bird_mask, offset)

        return True if collide else False
