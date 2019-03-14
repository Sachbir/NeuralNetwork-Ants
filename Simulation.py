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
                    # TODO: Broken; need to fix this
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
                self.evolve_ants()
                Food.need_next_location = True
                Food.food_positions = []
            if start_next_cycle or Config.should_wipe_screen:
                Simulation.screen.fill((225, 225, 225))  # Off-white
            for layer in self.world_layers:
                self.ants_alive -= not layer.update(start_next_cycle)   # Layer returns if any is alive
                                                                        # Remove dead ants from count

            '''Reset Functionality'''
            if Config.should_render:
                pygame.display.flip()
            self.clock.tick(Config.sim_speed_multiplier * 60)  # 60 ticks/second

    def evolve_ants(self):

        # Get all ants
        ants = []
        for i in range(len(self.world_layers)):
            ants.insert(i, self.world_layers[i].ant)

        # Sort ants by their ranking
        sorted_ants = sorted(ants, key=(lambda this_ant: this_ant.get_score()), reverse=True)
        # print("\tBest ant scored", sorted_ants[0].food_eaten)

        # Top 10% ants are duplicated as is

        ten_percent = math.floor(Config.num_of_ants * .1)

        print()
        for i in range(ten_percent):
            smart_ant_brain = sorted_ants[i].network.get_network_values()
            new_ant = self.world_layers[i].ant
            new_ant.set_network_values(smart_ant_brain, False)
            print(i, " ", round(sorted_ants[i].get_score(), 3))
            if sorted_ants[i].get_score() < -3.3:
                sys.exit(-2)

        # Top 9 ants get 10 offspring

        for i in range(ten_percent - 1):  # Don't copy the last ant, otherwise you hit 110% (Due to cloning)
            smart_ant_brain = sorted_ants[i].network.get_network_values()
            for j in range(ten_percent):
                if 10 * (i + 1) + j == Config.num_of_ants:
                    break
                ant_num = 10 * (i + 1) + j
                self.world_layers[ant_num].ant.set_network_values(smart_ant_brain, True)

    @staticmethod
    def write_to_file(message, mode="a"):

        with open(Simulation.log_file, mode) as log_file:
            log_file.write(message)
