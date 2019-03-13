import math
import pygame
import sys
from Config import Config
from Food import Food
from WorldLayer import WorldLayer


class Simulation:

    pygame.init()
    screen = pygame.display.set_mode(Config.screen_size)

    log_file = "ant_log.txt"

    def __init__(self):

        self.clock = pygame.time.Clock()
        # noinspection PyUnusedLocal
        self.world_layers = [WorldLayer()
                             for i in range(Config.num_of_ants)]
        self.ants_alive = len(self.world_layers)

        self.best_score = 0
        self.generation_counter = 0

        Simulation.write_to_file("", "w")

    def run(self):

        print("\n---BEGIN---\n")
        while True:

            start_next_cycle = False

            if self.ants_alive == 0:
                start_next_cycle = True
                self.generation_counter += 1
            self.ants_alive = len(self.world_layers)

            '''Events'''
            for event in pygame.event.get():
                if (event.type == pygame.QUIT or
                        (event.type == pygame.KEYDOWN and event.key == pygame.K_q)):  # End simulation
                    print("\n\n----END----")
                    sys.exit(0)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # Restart cycle
                    for layer in self.world_layers:
                        layer.__init__()
                    self.generation_counter = 1
                    start_next_cycle = True
                    print()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:  # Render graphics
                    Config.should_render = not Config.should_render
                if event.type == pygame.KEYDOWN and event.key == pygame.K_f:  # Print food location
                    WorldLayer.should_print_food_coordinates = not WorldLayer.should_print_food_coordinates
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:  # Start next cycle
                    self.generation_counter += 1
                    start_next_cycle = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:  # Show path
                    Config.should_wipe_screen = not Config.should_wipe_screen

            if start_next_cycle:
                print("Gen", self.generation_counter, end='')
                self.evolve_ants_2()
                Food.need_next_location = True
                Food.food_positions = []
            if start_next_cycle or Config.should_wipe_screen:
                Simulation.screen.fill((225, 225, 225))  # Off-white
            for layer in self.world_layers:
                self.ants_alive -= layer.update(start_next_cycle)

            '''Reset Functionality'''
            if Config.should_render:
                pygame.display.flip()
            self.clock.tick(Config.sim_speed_multiplier * 60)  # 60 ticks/second

    # Most successful ants pass their 'genome' to the next generation
    def evolve_ants(self):

        # Get all ants
        ants = []
        for i in range(len(self.world_layers)):
            ants.insert(i, self.world_layers[i].ant)

        # Sort ants by their ranking
        sorted_ants = sorted(ants, key=Simulation.ant_ranking, reverse=True)
        print("\tBest ant scored", sorted_ants[0].food_eaten)

        # Find the smartest ants
        num_good_ants = 0
        for ant in sorted_ants:
            if Simulation.ant_ranking(ant) == Simulation.ant_ranking(sorted_ants[0]):
                num_good_ants += 1

        if sorted_ants[0].food_eaten == 0:
            Simulation.write_to_file("Lasted " + str(self.generation_counter) + " gen\tBest score:"
                                     + str(sorted_ants[0].food_eaten) + "\n")
            self.generation_counter = 0
            print("Everyone failed. Let's try again")
            for layer in self.world_layers:
                layer.__init__()
            return

        # TODO: True copying portion doesn't seem to work? Hard to say
        for i in range(num_good_ants):
            new_ant_brain = self.world_layers[i].ant.network
            smart_ant_brain = sorted_ants[i].network
            new_ant_brain.set_network_values(smart_ant_brain.get_network_values(), False)

        children_per_smart_ant = math.floor(len(self.world_layers) / num_good_ants)

        # For each smart ant, skipping past the first few (because they're just clones of the good ones)
        # Jump at increments of the number of children per
        for i in range(num_good_ants, len(self.world_layers), children_per_smart_ant):
            smart_ant_brain = sorted_ants[i].network
            for j in range(children_per_smart_ant):
                if i + j >= len(self.world_layers):
                    # Don't go past the total number of ants present
                    return
                new_ant_brain = self.world_layers[i + j].ant.network
                new_ant_brain.set_network_values(smart_ant_brain.get_network_values())

    # A sorting algorithm to determine which ants are best
    # Rankings based on food eaten and distance from next food
    @staticmethod
    def ant_ranking(ant):

        # ?
        # if not ant.in_bounds:
        #     return 0

        food_score_bias = 2 * Config.screen_size[1]
        food_score = food_score_bias * ant.food_eaten

        # dist_ant_to_food = ant.distance_to(ant.parent.food)
        # dist_score = math.floor(dist_ant_to_food / Config.dist_scoring_leniency)

        ranking = food_score    # + dist_score

        return ranking

        # Most successful ants pass their 'genome' to the next generation

    def evolve_ants_2(self):

        # Get all ants
        ants = []
        for i in range(len(self.world_layers)):
            ants.insert(i, self.world_layers[i].ant)

        # Sort ants by their ranking
        sorted_ants = sorted(ants, key=(lambda this_ant: this_ant.get_score()), reverse=True)
        print("\tBest ant scored", sorted_ants[0].food_eaten)

        # Top 10 ants are duplicated as is

        for i in range(10):
            smart_ant_brain = sorted_ants[i].network.get_network_values()
            self.world_layers[i].ant.set_network_values(smart_ant_brain, False)
            print(i, " ", round(sorted_ants[i].get_score(), 3))

        # Top 9 ants get 10 offspring

        for i in range(9):
            smart_ant_brain = sorted_ants[i].network.get_network_values()
            for j in range(10):
                ant_num = 10 * (i + 1) + j
                self.world_layers[ant_num].ant.set_network_values(smart_ant_brain, True)

    @staticmethod
    def write_to_file(message, mode="a"):

        with open(Simulation.log_file, mode) as log_file:
            log_file.write(message)
