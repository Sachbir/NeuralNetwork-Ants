import pygame
from WorldLayer import WorldLayer
import math
from random import shuffle


def main():

    simulation_speed = 10

    pygame.init()

    screen = pygame.display.set_mode((700, 700))
    clock = pygame.time.Clock()

    world_layers = [WorldLayer(screen)
                    for i in range(100)]

    start_next_cycle = False
    ants_alive = len(world_layers)

    generation_counter = 0

    print("---BEGIN---\n- ", end='')

    should_quit = False
    while True:

        if ants_alive == 0:
            selective_breeding_time(world_layers)
            start_next_cycle = True
            print("\nGen", generation_counter, "- ", end='')
        ants_alive = len(world_layers)

        '''Events'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_quit = True
                print("\n----END----")
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:    # Initiate next cycle
                selective_breeding_time(world_layers)
                start_next_cycle = True
                print()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                for layer in world_layers:
                    print(layer.ant.network.get_network_values())
        if should_quit:
            break

        screen.fill((225, 225, 225))
        for layer in world_layers:
            ants_alive -= layer.update(start_next_cycle)
        start_next_cycle = False

        '''Reset Functionality'''
        pygame.display.flip()
        clock.tick(simulation_speed * 60)


def selective_breeding_time(world_layers):

    # Step 1: Rank all ants

    ants = []
    for i in range(len(world_layers)):
        ants.insert(i, world_layers[i].ant)
        shuffle(ants)   # This should mean ants of the same score are sorted differently each time

    # Ants with good history are boosted
    # Ants who recently did well are prioritized
    sorted_ants = sorted(ants, key=(lambda ant: ant.total_score), reverse=True)
    sorted_ants = sorted(sorted_ants, key=(lambda ant: ant.score), reverse=True)
    print("\tBest ant:", sorted_ants[0].score, "with a historical score:", sorted_ants[0].total_score, end='')

    # Step 2: Produce a new generation of ants based on the best predecessors
    for i in range(99):
        world_layers[i].ant.network.generation += 1
        world_layers[i].ant.network.set_network_values(
            sorted_ants[math.floor(i / 3)].network.get_network_values(),
            sorted_ants[math.floor(i / 3)].score
        )
        world_layers[i].set_color(sorted_ants[i].parent.color)
    world_layers[99].ant.network.generation += 1
    world_layers[99].ant.network.set_network_values(
        sorted_ants[0].network.get_network_values(),
        sorted_ants[0].score
    )

    shuffle(world_layers)


main()

# Selective breeding
# 1A. Generate ants
# 2. Run cycle
# 3. On cycle end, rank all ants
# 1B. Generate ants based on previous "winners"
