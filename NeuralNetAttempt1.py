import math
import pygame
import sys
from Config import Config
from Food import Food
from WorldLayer import WorldLayer


def main():

    pygame.init()
    clock = pygame.time.Clock()

    # noinspection PyUnusedLocal
    world_layers = [WorldLayer()
                    for i in range(Config.num_of_ants)]
    ants_alive = len(world_layers)

    generation_counter = 0

    print("\n---BEGIN---\n")
    while True:

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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:                             # Restart cycle
                for layer in world_layers:
                    layer.__init__()
                generation_counter = 1
                start_next_cycle = True
                print()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:                             # Render graphics
                Config.should_render = not Config.should_render
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:                           # Print food location
                WorldLayer.should_print_food_coordinates = not WorldLayer.should_print_food_coordinates
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:                            # Start next cycle
                generation_counter += 1
                start_next_cycle = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:                                   # Show path
                Config.should_wipe_screen = not Config.should_wipe_screen

        if start_next_cycle:
            print("Gen", generation_counter, end='')
            evolve_ants(world_layers)
            Food.need_next_location = True
            Food.food_positions = []
        if start_next_cycle or Config.should_wipe_screen:
            WorldLayer.screen.fill((225, 225, 225))     # Off-white
        for layer in world_layers:
            ants_alive -= layer.update(start_next_cycle)

        '''Reset Functionality'''
        if Config.should_render:
            pygame.display.flip()
        clock.tick(Config.sim_speed_multiplier * 60)    # 60 ticks/second


# Most successful ants pass their 'genome' to the next generation
def evolve_ants(world_layers):

    # Get all ants
    ants = []
    for i in range(len(world_layers)):
        ants.insert(i, world_layers[i].ant)

    # Sort ants by their ranking
    sorted_ants = sorted(ants, key=ant_ranking, reverse=True)
    print("\tBest ant scored", sorted_ants[0].score)

    # Find the smartest ants
    num_good_ants = 0
    for ant in sorted_ants:
        if ant_ranking(ant) == ant_ranking(sorted_ants[0]):
            num_good_ants += 1

    # Pass on the smartest brains to the next generation of ants
    # Each of the predecessors has (roughly) an equal number of descendents
    for i in range(num_good_ants, len(world_layers)):
        successful_ant_brain = sorted_ants[i].network
        for j in range(math.floor(len(world_layers) / num_good_ants)):
            if i + j < len(world_layers):
                new_ant = world_layers[i + j].ant
                new_ant.network.set_network_values(successful_ant_brain.get_network_values())
            return


# A sorting algorithm to determine which ants are best
# Rankings based on food eaten and distance from next food
def ant_ranking(ant):

    # ?
    # if not ant.in_bounds:
    #     return 0

    food_score_bias = 2 * Config.screen_size[1]
    food_score = food_score_bias * ant.score

    dist_ant_to_food = ant.distance_to(ant.parent.food)
    dist_score = math.floor(dist_ant_to_food / Config.dist_scoring_leniency)

    ranking = food_score + dist_score

    return ranking


main()

# Selective breeding
# 1A. Generate ants
# 2. Run cycle
# 3. On cycle end, rank all ants
# 1B. Generate ants based on previous "winners"
