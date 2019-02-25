import pygame
from WorldLayer import WorldLayer
import math


def main():
    pygame.init()

    screen = pygame.display.set_mode((900, 900))
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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:    # Initiate next cycle
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


def selective_breeding_time(world_layers):

    # Step 1: Rank all ants

    ants = []
    for i in range(len(world_layers)):
        ants.insert(i, world_layers[i].ant)

    sorted_ants = sorted(ants, key=(lambda ant: ant.totalScore), reverse=True)

    # for ant in sorted_ants:
    #     print("Ant - Score", ant.totalScore)
    #     print(ant.network.get_network_values())
    #     print()

    # Step 2: Produce a new generation of ants based on the best predecessors

    # for i in range(10):
    #     for j in range(10):
    #         world_layers[i+j].ant.network.generation += 1
    #         world_layers[i+j].ant.network.set_network_values(
    #             sorted_ants[i].network.get_network_values()
    #         )
    for i in range(50):
        world_layers[i].ant.network.generation += 1
        world_layers[i].ant.network.set_network_values(
            sorted_ants[i].network.get_network_values()
        )
        world_layers[2*i].ant.network.generation += 1
        world_layers[2*i].ant.network.set_network_values(
            sorted_ants[i].network.get_network_values()
        )


main()

# Selective breeding
# 1A. Generate ants
# 2. Run cycle
# 3. On cycle end, rank all ants
# 1B. Generate ants based on previous "winners"
