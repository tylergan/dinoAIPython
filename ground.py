import pygame
import os


class Ground:
    IMG = pygame.image.load(os.path.join("imgs", "ground.png"))
    WIDTH = IMG.get_width()

    def __init__(self, vel):
        # positioning of images
        self.y = 250
        self.x1 = 0
        self.x2 = self.WIDTH

        self.vel = vel

    def move(self):
        '''Move function which makes the ground move (simply cycles through two imaegs)'''
        self.x1 -= self.vel
        self.x2 -= self.vel

        # recycling of two images everytime one exits the left-side of the screen
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        elif self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        '''Draw function for the two cycling images.'''
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
