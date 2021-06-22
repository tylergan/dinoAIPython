import pygame
import neat
from visualize import draw_net
import matplotlib.pyplot as plt
from dino import Dino
from ground import Ground
from bird import Bird
from game_functions import (
    draw_window,
    update
)

pygame.font.init()


def eval_genomes(genomes, config):
    '''The main function of the game where the AI algorithm takes place.'''
    # Initialise our AI (brain) which contains the ANN
    dinos = []
    nets = []

    for _, genome in genomes:
        nets.append(neat.nn.FeedForwardNetwork.create(genome, config))
        genome.fitness = 0

        dinos.append(Dino())

    # setup the game
    global generation, best_score, scores
    generation += 1

    score, inc = 0, 0.15
    gen_scores, gen_dinos = [], []

    vel = 8
    ground = Ground(vel)
    obstacles = []
    update(vel, ground, obstacles, score)

    win = pygame.display.set_mode((WIDTH, HEIGHT))

    while len(dinos) > 0:
        # pygame.time.Clock().clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    plt.plot(scores)
                    plt.show()

        # check collision
        for obstacle in obstacles:
            for x, dino in enumerate(dinos):
                if obstacle.collide(dino):
                    genomes[x][1].fitness -= 5
                    gen_scores.append(genomes[x][1].fitness)
                    gen_dinos.append(genomes[x][1])
                    nets.pop(x)
                    dinos.pop(x)

                if obstacle.x < dino.X and not obstacle.passed:
                    obstacle.passed = True
                    genomes[x][1].fitness += 1

        # update game information
        for x, dino in enumerate(dinos):
            dino.update_inputs(obstacles, vel)
            output = nets[x].activate(dino.inputs)
            dino.decide(output)
            genomes[x][1].fitness += 0.005

        if int(score) % 100 == 0 and int(score) != 0:  # checkpoint at every 100
            inc += 0.05
            vel += 1
            score += 1  # make int(score) % 100 == 0 only true once (as inc -> float)

        update(vel, ground, obstacles, score)
        draw_window(win, dinos, ground, obstacles, int(score), generation, best_score)
        score += inc

    # scores to plot fitness across all generations
    scores.append(max(gen_scores))
    gen_dinos.sort(key=lambda x: x.fitness, reverse=True)

    # draws the neural network of the fittest dino of the generation
    if score > best_score:
        best_score = int(score)

        # obtain and draw network of fittest genome so far
        node_names = {-1: "Distance to Next Obstacle", -2: "Speed", -3: "Height of Bird", -4: "Obstacle Type", -5: "Obstacle Width", -6: "Obstacle Height", -7: "Player Height",
                       0: "Jump", 1: "Duck"}
        draw_net(config, gen_dinos[0], True, node_names=node_names, filename="fittest_g_gen")


WIDTH = 600
HEIGHT = 300
generation = 0
best_score = 0
scores = []
