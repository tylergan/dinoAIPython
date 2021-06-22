import pygame
import os
import math
from bird import Bird


class Dino:
    DINO_RUN = [pygame.transform.scale(pygame.image.load(os.path.join("imgs", "dinorun.png")), (40, 40)),  # scaling images -> new (w, h)
                pygame.transform.scale(pygame.image.load(os.path.join("imgs", "dinorun1.png")), (40, 40))]

    DINO_DUCK = [pygame.transform.scale(pygame.image.load(os.path.join("imgs", "dinoduck.png")), (50, 30)),
                 pygame.transform.scale(pygame.image.load(os.path.join("imgs", "dinoduck1.png")), (50, 30))]

    DINO_JMP = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "dinoJump.png")), (40, 40))

    X = 40

    def __init__(self):
        # basic game attributes
        self.img = self.DINO_RUN[0]
        self.img_count = 0
        self.y = 225
        self.vel = 0
        self.gravity = 1.2
        self.state = 0
        self.ducking = False

        # inputs for ANN
        self.inputs = [-1 for _ in range(7)]

    def move(self):
        '''The move function for the Dino.'''
        self.y -= self.vel  # position incrementally updated via main loop
        if self.y < 225:
            if self.ducking:  # make the Dino fall down faster if jump + duck
                self.gravity = 4

            self.vel -= self.gravity  # add gravity (positive -> negative) when in the air to provide smooth jump
        else:
            # on the ground, everything standard
            self.state = 0 if not self.ducking else 1
            self.vel = 0
            self.y = 225 if not self.ducking else 235

    def jump(self, big_jump):
        '''Jump function which only works if on the ground.'''
        if self.y == 225:
            self.state = 2

            if big_jump:
                self.gravity = 2
                self.vel = 18
            else:
                self.gravity = 1.5
                self.vel = 13

    def draw(self, win):
        '''Draw function for the dino images.'''
        self.img_count += 0.4
        img_index = int(self.img_count % len(self.DINO_RUN))
        self.img = self.DINO_RUN[img_index] if self.state == 0 else self.DINO_DUCK[img_index] if self.state == 1 else self.DINO_JMP
        win.blit(self.img, (self.X, self.y))

    def get_mask(self):
        '''Returns the mask of the Dino image.'''
        return pygame.mask.from_surface(self.img)

    def update_inputs(self, obstacles, vel):
        '''Update inputs used for ANN.'''
        # setup objects for inputs
        obstacle = obstacles[0] if not obstacles[0].passed else obstacles[1]  # focus on next obstacle if first one passed
        bird = obstacle if isinstance(obstacle, Bird) else None  # only consider if it is the next obstacle

        # assign inputs
        self.inputs[0] = math.sqrt((obstacle.x - self.X)**2 + (obstacle.y - self.y)**2) # distance to next obstacle
        self.inputs[1] = vel  # speed
        self.inputs[2] = [195, 175, 155].index(bird.y) if bird and not bird.passed else -1  # height of bird (only consider when not passed)
        self.inputs[3] = 1 if bird else -1  # object type (bird or cactus)
        self.inputs[4] = obstacle.img.get_width()  # obstacle width
        self.inputs[5] = obstacle.img.get_height()  # obstacle height
        self.inputs[6] = self.y  # player height

    def decide(self, output):
        '''The Dino decides based off what decision is made from the ANN.'''
        decision = output.index(max(output))

        if decision == 0 and max(output) > 0.5:
            self.jump(True)
        elif decision == 1:
            self.ducking = True if max(output) > 0.5 else False
