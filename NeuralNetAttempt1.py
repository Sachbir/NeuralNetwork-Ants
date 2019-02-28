import math
import pygame
import sys
from Config import Config
from WorldLayer import WorldLayer


def main():

    pygame.init()
    clock = pygame.time.Clock()

    world_layers = [WorldLayer()
                    for i in range(Config.num_of_ants)]
    ants_alive = len(world_layers)

    generation_counter = 0
    print("\n---BEGIN---\n")

    should_wipe_screen = True

    while True:

        # print("start ", end='')

        start_next_cycle = False

        if ants_alive == 0:
            start_next_cycle = True
            generation_counter += 1
        ants_alive = len(world_layers)

        '''Events'''
        for event in pygame.event.get():
            if (event.type == pygame.QUIT or
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_q)):
                # End simulation
                print("\n\n----END----")
                sys.exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Restart cycle
                WorldLayer.should_randomize_object_locations = True
                for layer in world_layers:
                    layer.__init__()
                generation_counter = 1
                start_next_cycle = True
                print()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                # Render graphics
                Config.should_render = not Config.should_render
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                # Print location of food
                WorldLayer.should_print_food_coordinates = not WorldLayer.should_print_food_coordinates
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                # Start next cycle
                generation_counter += 1
                start_next_cycle = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                # Wipe screen on each tick
                should_wipe_screen = not should_wipe_screen

        if start_next_cycle:
            print("Gen", generation_counter, end='')
            selective_breeding_time(world_layers)
        if start_next_cycle or should_wipe_screen:
            WorldLayer.screen.fill((225, 225, 225))
        WorldLayer.should_randomize_object_locations = True
        for layer in world_layers:
            ants_alive -= layer.update(start_next_cycle)

        '''Reset Functionality'''
        if Config.should_render:
            pygame.display.flip()
        clock.tick(Config.sim_speed_multiplier * 60)

        # print("end")


def ant_ranking(ant):

    if ant.out_of_bounds:
        return 0

    tolerance_in_distance_measure = 25

    dist_ant_to_food = ant.distance_to(ant.parent.food)
    ranking = ant.score * (2 * Config.screen_size[1]) - dist_ant_to_food / tolerance_in_distance_measure

    return ranking


def selective_breeding_time(world_layers):

    ants = []
    for i in range(len(world_layers)):
        ants.insert(i, world_layers[i].ant)

    # Sort ants first by food consumed, then by how close they are to the next food
    sorted_ants = sorted(ants, key=ant_ranking, reverse=True)
    print("\tBest ant scored", sorted_ants[0].score)

    # Find the smartest ants
    num_good_ants = 0
    for ant in sorted_ants:
        if ant_ranking(ant) == ant_ranking(sorted_ants[0]):
            num_good_ants += 1

    # Copy the smartest brains to the next generation (evenly)
    for i in range(num_good_ants, len(world_layers)):
        successful_ant_brain = sorted_ants[i].network
        for j in range(math.floor(len(world_layers) / num_good_ants)):
            if i + j < len(world_layers):
                new_ant_brain = world_layers[i + j].ant.network
                new_ant_brain.set_network_values(successful_ant_brain.get_network_values())
            return



main()

# Selective breeding
# 1A. Generate ants
# 2. Run cycle
# 3. On cycle end, rank all ants
# 1B. Generate ants based on previous "winners"
