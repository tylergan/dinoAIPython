import pygame
import os
import random


class Cactus:
    IMGS = [pygame.transform.scale(pygame.image.load(os.path.join("imgs", "cactusSmall.png")), (30, 40)),
            pygame.transform.scale(pygame.image.load(os.path.join("imgs", "cactusSmallMany.png")), (50, 50)),
            pygame.transform.scale(pygame.image.load(os.path.join("imgs", "cactusBig.png")), (30, 50))]

    def __init__(self, vel, BG_Width):
        self.state = random.randint(0, len(self.IMGS) - 1)
        self.img = self.IMGS[self.state]
        self.vel = vel
        self.x = BG_Width
        self.y = 225 if self.state != 2 else 215

        # for ANN input
        self.passed = False

    def update_offset(self, offset):
        '''Updates the offset so that it is placed in other x-coordinates away from other objects.'''
        self.x += offset * 50

    def move(self):
        '''Moves the cactus across the screen.'''
        self.x -= self.vel

    def draw(self, win):
        '''Draws the cactus image onto the screen.'''
        win.blit(self.img, (self.x, self.y))

    def collide(self, dino):
        '''Determines whether the Dino collided with the cactus using masking.'''
        dino_mask = dino.get_mask()
        cactus_mask = pygame.mask.from_surface(self.img)
        offset = (self.x - dino.X, self.y - round(dino.y))

        collide = dino_mask.overlap(cactus_mask, offset)

        return True if collide else False
