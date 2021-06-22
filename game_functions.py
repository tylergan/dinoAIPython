import pygame
import random
from cactus import Cactus
from bird import Bird


def draw_window(win, dinos, ground, obstacles, score, generation, best_score):
    '''Function that draws and moves the objects of the game.'''
    win.fill((235, 235, 235))

    # display score
    STAT_FONT = pygame.font.SysFont("comicsans", 20)
    text = STAT_FONT.render("Score: {}".format(score), 1, (0, 0, 0))
    win.blit(text, (600 - 10 - text.get_width(), 10))
    text = STAT_FONT.render("Generation: {}".format(generation), 1, (0, 0, 0))
    win.blit(text, (0, 10))
    text = STAT_FONT.render("Best Score: {}".format(best_score), 1, (0, 0, 0))
    win.blit(text, (0, 30))

    # draw objects
    ground.draw(win)

    for obstacle in obstacles:
        obstacle.draw(win)

    for dino in dinos:
        dino.draw(win)

    pygame.display.flip()

    # move images
    ground.move()

    for dino in dinos:
        dino.move()

    for obstacle in obstacles:
        obstacle.move()


def update(vel, ground, obstacles, score):
    '''Function that updates the cactus by either adding or removing them from the game.'''
    # update velocity of possibly outdated objects
    obstacles.sort(key=lambda obj: obj.x)

    for obstacle in obstacles:
        obstacle.vel = vel

    ground.vel = vel

    # removing cactus that needs removing
    to_rem = [obstacle for obstacle in obstacles if obstacle.x < (0 - obstacle.img.get_width())]  # remove obstacles that are off screen

    for obstacle in to_rem:  # actually remove obstacles
        obstacles.remove(obstacle)

    # determing how many obstacles to add
    cactus_count = len([obstacle for obstacle in obstacles if isinstance(obstacle, Cactus)])
    for _ in range(2 - cactus_count):
        obstacles.append(Cactus(vel, ground.WIDTH))

    # check whether to generate a bird
    if random.randrange(0, 200) == 10 and len([obstacle for obstacle in obstacles if (isinstance(obstacle, Bird))]) == 0 and int(score) > 400:
        obstacles.append(Bird(vel, ground.WIDTH))

    # make sure obstacles are not too close together
    i = 0
    while i + 1 < len(obstacles):
        if obstacles[i + 1].x - obstacles[i].x < 250:
            obstacles[i + 1].x += 250 + 50 * (vel - 8)

        i += 1
