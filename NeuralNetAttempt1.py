import math
import pygame
from random import shuffle
from GameObject import GameObject
from WorldLayer import WorldLayer


def main():

    simulation_speed = 20

    pygame.init()

    screen = pygame.display.set_mode((900, 900))
    clock = pygame.time.Clock()

    world_layers = [WorldLayer(screen)
                    for i in range(200)]

    start_next_cycle = False
    ants_alive = len(world_layers)

    generation_counter = 0

    print("---BEGIN---\nGen 0 - ", end='')

    should_quit = False
    while True:

        if ants_alive == 0:
            selective_breeding_time(world_layers)
            start_next_cycle = True
            generation_counter += 1
        ants_alive = len(world_layers)

        '''Events'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_quit = True
                print("\n----END----")
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:    # Initiate next cycle
                for layer in world_layers:
                    layer.restart_ant()
                start_next_cycle = True
                generation_counter = 0
                print("\n")
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                GameObject.should_render_object = not GameObject.should_render_object
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                WorldLayer.should_print_food_coordinates = not WorldLayer.should_print_food_coordinates
        if should_quit:
            break
        if start_next_cycle:
            print("Gen", generation_counter, "- ", end='')
        screen.fill((225, 225, 225))
        for layer in world_layers:
            ants_alive -= layer.update(start_next_cycle)
        start_next_cycle = False

        '''Reset Functionality'''
        if GameObject.should_render_object:
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
    sorted_ants = sorted(ants, key=(lambda ant_2: ant_2.score), reverse=True)
    print("\tBest ant scores", sorted_ants[0].score)

    # Step 2: Produce a new generation of ants based on the best predecessors
    if sorted_ants[0].score > 0:
        for i in range(len(world_layers)):
            world_layers[i].ant.network.set_network_values(
                                sorted_ants[0].network.get_network_values(),
                                sorted_ants[0].score
                            )
    else:
        for i in range(len(world_layers)):
            world_layers[i].restart_ant()

    num_good_ants = 0

    for ant in sorted_ants:
        if ant.score > 0 and ant.score == sorted_ants[0].score:
            num_good_ants += 1
    if num_good_ants > 0:
        for i in range(num_good_ants, len(world_layers)):
            for j in range(math.floor(len(world_layers) / num_good_ants)):
                if i + j < len(world_layers):
                    world_layers[i + j].ant.network.set_network_values(
                        sorted_ants[i].network.get_network_values(),
                        sorted_ants[i].score
                    )
    else:
        for i in range(len(world_layers)):
            world_layers[i].restart_ant()


main()

# Selective breeding
# 1A. Generate ants
# 2. Run cycle
# 3. On cycle end, rank all ants
# 1B. Generate ants based on previous "winners"
