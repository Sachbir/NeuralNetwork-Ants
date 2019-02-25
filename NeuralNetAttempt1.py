import pygame
from WorldLayer import WorldLayer
import math


def main():
    pygame.init()

    screen = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()

    world_layers = [WorldLayer(screen)
                    for i in range(100)]

    start_next_cycle = False

    done = False
    while not done:
        '''Events'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:    # Reload

                selective_breeding_time(world_layers)
                print("----------")
                print()
                start_next_cycle = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                for layer in world_layers:
                    print(layer.ant.network.get_network_values())


        screen.fill((225, 225, 225))
        for layer in world_layers:
            layer.update(start_next_cycle)
        start_next_cycle = False

        '''Reset Functionality'''
        pygame.display.flip()
        clock.tick(60)


# Simple decision solution
def turn_decision(*args):

    angular_range = math.pi / 32

    if should_turn_right(*args):
        return angular_range    # Clockwise
    return -angular_range       # Counter-clockwise


def should_turn_right(*args):

    ant_direction = args[0]
    ant_x = args[1]
    ant_y = args[2]
    food_x = args[3]
    food_y = args[4]

    # we already have coordinates for the current location
    # get coordinates for a point 1 unit forwards
    delta_x = ant_x + math.cos(ant_direction)  # * 100
    delta_y = ant_y + math.sin(ant_direction)  # * 100
    # solve the line equation, y = mx + b, of the direction of travel
    m = (delta_y - ant_y) / (delta_x - ant_x)
    b = delta_y - m * delta_x

    # Not quite sure of explanation
    facing_right = ((ant_direction - math.pi / 2) % (2 * math.pi)) > math.pi
    food_is_below = (food_y > (m * food_x + b))  # greater = lower

    if ((facing_right and food_is_below) or
            (not facing_right and not food_is_below)):
        return True     # turn right
    return False        # turn left


def selective_breeding_time(world_layers):

    is_there_a_best = False

    best_ant = world_layers[0].ant

    # Step 1: Rank all ants

    ants = []
    for i in range(len(world_layers)):
        ants.insert(i, world_layers[i].ant)

    sorted_ants = sorted(ants, key=get_score, reverse=True)

    for ant in sorted_ants:
        if ant.score > best_ant.score:
            best_ant = ant
            is_there_a_best = True
        # print("Ant - Score", ant.score)
        # print(ant.network.get_network_values())
        # print()

    # Step 2: Produce a new generation of ants based on the best predecessors

    # for layer in world_layers:
    #     layer.ant.network.generation += 1
    #     layer.ant.network.set_network_values(best_ant.network.get_network_values())

    # Bootleg strategy

    if is_there_a_best:
        for i in range(100):
            world_layers[i].ant.network.set_network_values(
                sorted_ants[math.ceil(math.sqrt(i))].network.get_network_values()
            )


def get_score(ant):

    return ant.score


main()

# Selective breeding
# 1A. Generate ants
# 2. Run cycle
# 3. On cycle end, rank all ants
# 1B. Generate ants based on previous "winners"
