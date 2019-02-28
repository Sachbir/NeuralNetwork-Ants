import math
import pygame
import sys
from random import shuffle
from Config import Config
from WorldLayer import WorldLayer


def main():

    pygame.init()
    screen = pygame.display.set_mode(Config.screen_size)
    clock = pygame.time.Clock()

    world_layers = [WorldLayer(screen)
                    for i in range(Config.num_of_ants)]
    ants_alive = len(world_layers)

    generation_counter = 0
    print("\n---BEGIN---\n")

    should_wipe_screen = True

    while True:

        start_next_cycle = False

        if ants_alive == 0:
            start_next_cycle = True
            generation_counter += 1
        ants_alive = len(world_layers)

        '''Events'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("\n\n----END----")
                sys.exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Restart cycle
                for layer in world_layers:
                    layer.restart_ant()
                generation_counter = 1
                start_next_cycle = True
                print()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                # Display toggle
                Config.should_render = not Config.should_render
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                # Start next cycle
                generation_counter += 1
                start_next_cycle = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                # Wipe screen toggle
                should_wipe_screen = not should_wipe_screen

        if start_next_cycle:
            print("Gen", generation_counter, end='')
            selective_breeding_time(world_layers)
        if start_next_cycle or should_wipe_screen:
            screen.fill((225, 225, 225))
        for layer in world_layers:
            ants_alive -= layer.update(start_next_cycle)

        '''Reset Functionality'''
        if Config.should_render:
            pygame.display.flip()
        clock.tick(Config.sim_speed_multiplier * 60)


def ant_scoring(ant):

    dist_ant_to_food = ant.distance_to(ant.parent.food)
    score = ant.score * math.sqrt(2 * 900**2) + (dist_ant_to_food / 25)

    return score


def selective_breeding_time(world_layers):

    # Step 1: Rank all ants

    ants = []
    for i in range(len(world_layers)):
        ants.insert(i, world_layers[i].ant)
    shuffle(ants)   # This should mean ants of the same score are sorted differently each time

    # Ants with good history are boosted
    # Ants who recently did well are prioritized
    sorted_ants = sorted(ants, key=ant_scoring, reverse=True)
    print("\tBest ant scored", sorted_ants[0].score)

    # Step 2: Produce a new generation of ants based on the best predecessors
    if ant_scoring(sorted_ants[0]) > 0:
        for i in range(len(world_layers)):
            world_layers[i].ant.network.set_network_values(sorted_ants[0].network.get_network_values())
    else:
        for i in range(len(world_layers)):
            world_layers[i].restart_ant()

    num_good_ants = 0

    for ant in sorted_ants:
        if ant.score > 0 and ant.score == sorted_ants[0].score:
            num_good_ants += 1
    if num_good_ants == 0:
        for i in range(len(world_layers)):
            world_layers[i].restart_ant()
        return

    # print(" Copying brain...", end='')
    for i in range(num_good_ants, len(world_layers)):
        successful_ant_brain = sorted_ants[i].network
        for j in range(math.floor(len(world_layers) / num_good_ants)):
            if i + j < len(world_layers):
                new_ant_brain = world_layers[i + j].ant.network
                new_ant_brain.set_network_values(successful_ant_brain.get_network_values())
            # print("Done", end='')
            return



main()

# Selective breeding
# 1A. Generate ants
# 2. Run cycle
# 3. On cycle end, rank all ants
# 1B. Generate ants based on previous "winners"
