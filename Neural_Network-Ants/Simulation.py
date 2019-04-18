import math
import pygame
from pygame import freetype
import sys
from Config import Config
from Entities.Food import Food
from WorldLayer import WorldLayer

import json


class Simulation:

    pygame.init()
    screen = pygame.display.set_mode(Config.screen_size)
    pygame.display.set_caption("Neural Network - Ants")
    icon = pygame.image.load("icon.jpg")
    pygame.display.set_icon(icon)

    pygame.font.init()
    pygame.freetype.init()
    system_font = pygame.freetype.get_default_font()
    text = pygame.freetype.SysFont(system_font, 20)

    log_file = "DataFiles/ant_log.txt"
    best_ant_file = "DataFiles/best_ant_brain.txt"
    last_gen_file = "DataFiles/last_gen_gene_pool.txt"

    def __init__(self):

        self.clock = pygame.time.Clock()
        # noinspection PyUnusedLocal
        self.world_layers = [WorldLayer()
                             for i in range(Config.num_of_ants)]
        self.ants_alive = len(self.world_layers)

        self.best_score = 0
        self.generation_counter = 0

        # with open(Simulation.best_ant_file, "r") as best_ant_file:
        #     self.generation_counter = int(best_ant_file.readline())
        #     best_and_score = best_ant_file.readline()
        #     brain_text = best_ant_file.readline()
        #     brain = json.loads(brain_text)
        #     ant = self.world_layers[0].ant
        #     ant.network.set_network_values(brain, False)

        Simulation.write_to_file("", "w")

    def run(self):

        Simulation.write_to_file("---BEGIN---\n\n")
        while True:

            start_next_cycle = False

            if self.ants_alive == 0:
                start_next_cycle = True
                self.generation_counter += 1
            self.ants_alive = len(self.world_layers)

            start_next_cycle = self.process_events(start_next_cycle)

            if start_next_cycle:
                Simulation.write_to_file("Gen " + str(self.generation_counter))
                self.evolve_ants()
                Food.need_next_location = True
                Food.food_positions = []
            if start_next_cycle or Config.should_wipe_screen:
                Simulation.screen.fill((225, 225, 225))  # Off-white
                Simulation.text.render_to(pygame.display.get_surface(),
                                          (11, 12),     # Offset looks better visually, even if mathematically imperfect
                                          "Gen " + str(self.generation_counter + 1) +
                                          " | Best Score of Last Round: " + str(self.best_score))
            # Updates in here!
            for layer in self.world_layers:
                self.ants_alive -= not layer.update(start_next_cycle)   # Layer returns if any is alive
                                                                        # Remove dead ants from count

            '''Reset Functionality'''
            if Config.render_state != 0:
                pygame.display.flip()
            self.clock.tick(Config.sim_speed_multiplier * 60)  # 60 ticks/second

    def process_events(self, start_next_cycle):

        for event in pygame.event.get():
            if (event.type == pygame.QUIT or
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_q)):  # End simulation
                Simulation.write_to_file("\n----END----\n")
                sys.exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # Restart cycle
                # TODO: Broken; need to fix this
                for layer in self.world_layers:
                    layer.__init__()
                self.generation_counter = 1
                start_next_cycle = True
                Simulation.write_to_file()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:  # Print food location
                WorldLayer.should_print_food_coordinates = not WorldLayer.should_print_food_coordinates
            if event.type == pygame.KEYDOWN and event.key == pygame.K_n:  # Start next cycle
                self.generation_counter += 1
                start_next_cycle = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:  # Show path
                Config.should_wipe_screen = not Config.should_wipe_screen
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:  # Toggle between rendering states
                self.render_mode()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:  # Load best ant
                with open(Simulation.best_ant_file, "r") as best_ant_file:
                    self.generation_counter = int(best_ant_file.readline())
                    best_ant_score = best_ant_file.readline()
                    brain_text = best_ant_file.readline()
                    brain = json.loads(brain_text)
                    ant = self.world_layers[0].ant
                    ant.network.set_network_values(brain, False)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:  # Save generation
                with open(Simulation.last_gen_file, "w") as last_gen_file:
                    last_gen_file.write(str(self.generation_counter))
                    for layer in self.world_layers:
                        ant_brain = layer.ant.network.get_network_values()
                        last_gen_file.write("\n" + str(ant_brain))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_l:  # Load best ant
                with open(Simulation.last_gen_file, "r") as last_gen_file:
                    self.generation_counter = int(last_gen_file.readline())

                    i = 0
                    ant_brain_text = last_gen_file.readline()

                    while ant_brain_text and i < Config.num_of_ants:
                        ant_brain = json.loads(ant_brain_text)
                        self.world_layers[i].ant.set_network_values(ant_brain)

                        ant_brain_text = last_gen_file.readline()
                        i += 1

        return start_next_cycle

    def render_mode(self):

        Config.render_state = (Config.render_state - 1) % 3

        if Config.render_state == 2:                            # Render all
            for world_layer in self.world_layers:
                world_layer.set_render(True)
        elif Config.render_state == 1:                          # Disable render for all but first
            self.world_layers[0].set_render(True)
            for i in range(1, len(self.world_layers)):
                self.world_layers[i].set_render(False)
        else:                                                   # Disable render for first as well
            for world_layer in self.world_layers:
                world_layer.set_render(False)

    def evolve_ants(self):

        # Get all ants
        ants = []
        for i in range(len(self.world_layers)):
            ants.insert(i, self.world_layers[i].ant)

        # Sort ants by their score
        sorted_ants = sorted(ants, key=(lambda this_ant: this_ant.get_score()), reverse=True)
        self.best_score = sorted_ants[0].food_eaten
        Simulation.write_to_file("\tBest ant scored " + str(self.best_score) + "\n")

        # If this generation contains the best ant ever, save it to a file
        with open(Simulation.best_ant_file, "r") as best_ant_file:
            gen_count = best_ant_file.readline()                # First line
            most_food_ever_eaten = best_ant_file.readline()     # Second line
            most_food_ever_eaten = int(most_food_ever_eaten)    # To int

        best_ant_in_gen = sorted_ants[0]
        if best_ant_in_gen.food_eaten > most_food_ever_eaten:
            with open(Simulation.best_ant_file, "w") as best_ant_file:
                best_ant_file.write(str(self.generation_counter) + "\n" +
                                    str(best_ant_in_gen.food_eaten) + "\n" +
                                    str(best_ant_in_gen.network.get_network_values()))

        Simulation.write_to_file()
        self.create_next_generation(sorted_ants)

    def create_next_generation(self, sorted_ants):

        ten_percent = math.floor(Config.num_of_ants * .1)

        # Copy the top 10%'s' brains perfectly
        for i in range(ten_percent):
            smart_ant_brain = sorted_ants[i].network.get_network_values()
            new_ant = self.world_layers[i].ant
            new_ant.set_network_values(smart_ant_brain, False)
            if sorted_ants[i].get_score() < -3.3:
                sys.exit(-2)

        # Pass on the top 9%'s brains, with some variance
        for i in range(ten_percent - 1):  # Don't copy the last ant, otherwise you hit 110% (Due to cloning)
            smart_ant_brain = sorted_ants[i].network.get_network_values()
            for j in range(ten_percent):
                if 10 * (i + 1) + j == Config.num_of_ants:
                    break
                ant_num = 10 * (i + 1) + j
                new_ant = self.world_layers[ant_num].ant
                new_ant.set_network_values(smart_ant_brain, True)

    @staticmethod
    def write_to_file(message="", mode="a"):

        with open(Simulation.log_file, mode) as log_file:
            log_file.write(message)
