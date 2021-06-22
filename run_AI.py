import neat
import os
import pickle5 as pickle
from genome_eval import eval_genomes
import visualize


checkpoint = False
checkpoint_f = ""


def run(config_path):
    '''This function runs the entire program.'''
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    if checkpoint:
        p = neat.Checkpointer.restore_checkpoint(checkpoint_f)
    else:
        p = neat.Population(config)

    # provide statistics on each generation to stdout
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # have a checkpoint for every 20 generations
    # p.add_reporter(neat.Checkpointer(50))

    winner = p.run(eval_genomes)  # set fitness function and run the eval_genome functon.
    print('\nBest genome:\n{!s}'.format(winner))

    pickle.dump(winner, open("best.pkl", "wb"))

    # visualise information about the best Genome
    node_names = {-1: "Distance to Next Obstacle", -2: "Speed", -3: "Height of Bird", -4: "Obstacle Type", -5: "Obstacle Width", -6: "Obstacle Height", -7: "Player Height",
                   0: "Jump", 1: "Duck"}
    visualize.draw_net(config, winner, True, node_names=node_names, filename="best_dino")
    visualize.plot_stats(stats, view=True)
    visualize.plot_species(stats, view=True)



def replay_genome(config_path, genome_path=""):
    '''Loads the previous winning genome and plays it.'''
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    # unpickle winner
    with open(genome_path, "rb") as f:
        genome = pickle.load(f)

    # convert loaded genome into required data structure
    genomes = [(1, genome)]

    # call game with only loaded genome
    eval_genomes(genomes, config)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "AI_config.txt")
    # replay_genome(config_path)
    run(config_path)
