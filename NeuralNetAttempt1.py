import pygame
from WorldLayer import WorldLayer
import math


def main():
    pygame.init()

    screen = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()

    world_layers = [WorldLayer(screen)
                    for i in range(10)]

    restart_world = False

    done = False
    while not done:
        '''Events'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #     mouse_pos = pygame.mouse.get_pos()
            #     if food.collide(mouse_pos):
            #         food.spawn()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:    # Reload

                selective_breeding_time(world_layers)
                print("----------")
                print()

                restart_world = True
                time_since_scored = 0
        # if time_since_scored == (3 * 60):   # On time expiry
        #                                     # Seconds * ticks/second
        #     print("Resetting...")
        #     restart_world = True
        #     time_since_scored = 0

        '''Rendering'''
        screen.fill((225, 225, 225))
        for layer in world_layers:
            layer.update(restart_world)
        restart_world = False

        '''Reset Functionality'''
        pygame.display.flip()
        clock.tick(60)


def turn_decision(*args):

    angular_range = math.pi / 32

    # turn_amount -> eventually get from NN
    # turn_amount = 2 * turn_amount - 1
    # turn_amount *= angular_range

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

    # sorted_ants = []
    # sorted_ants.insert(0, world_layers[0].ant)       # add first ant to list by default
    #
    # for i in range(1, len(world_layers)):
    #     ant_is_sorted = False
    #     unsorted_ant = world_layers[i].ant
    #     for sorted_ant in sorted_ants:
    #         if unsorted_ant.score > sorted_ant.score:
    #             sorted_ants.insert(i - 1, unsorted_ant)
    #             ant_is_sorted = True
    #     if not ant_is_sorted:
    #         sorted_ants.append(unsorted_ant)

    ants = []
    for i in range(len(world_layers)):
        ants.insert(i, world_layers[i].ant)

    sorted_ants = sorted(ants, key=get_score, reverse=True)

    for ant in sorted_ants:
        print("Ant - Score", ant.score)
        print(ant.network.print_network())
        print()

    return


def get_score(ant):

    return ant.score


main()
