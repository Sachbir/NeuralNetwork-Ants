import math
import pygame
import sys
from Config import Config
from Food import Food
from WorldLayer import WorldLayer


class Simulation:

    pygame.init()
    screen = pygame.display.set_mode(Config.screen_size)
    pygame.display.set_caption("Neural Network - Ants")
    icon = pygame.image.load("icon.jpg")
    pygame.display.set_icon(icon)

    log_file = "ant_log.txt"
    best_ant_file = "best_ant_brain.txt"

    def __init__(self):

        self.clock = pygame.time.Clock()
        # noinspection PyUnusedLocal
        self.world_layers = [WorldLayer()
                             for i in range(Config.num_of_ants)]
        self.ants_alive = len(self.world_layers)

        self.best_score = 0
        self.generation_counter = 0

        Simulation.output_text("", "w")

    def run(self):

        Simulation.output_text("---BEGIN---\n")
        while True:

            start_next_cycle = False

            if self.ants_alive == 0:
                start_next_cycle = True
                self.generation_counter += 1
            self.ants_alive = len(self.world_layers)

            start_next_cycle = self.process_events(start_next_cycle)

            if start_next_cycle:
                Simulation.output_text("Gen " + str(self.generation_counter))
                self.evolve_ants()
                Food.need_next_location = True
                Food.food_positions = []
            if start_next_cycle or Config.should_wipe_screen:
                Simulation.screen.fill((225, 225, 225))  # Off-white
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
                Simulation.output_text("\n\n----END----\n")
                sys.exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # Restart cycle
                # TODO: Broken; need to fix this
                for layer in self.world_layers:
                    layer.__init__()
                self.generation_counter = 1
                start_next_cycle = True
                Simulation.output_text()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:  # Print food location
                WorldLayer.should_print_food_coordinates = not WorldLayer.should_print_food_coordinates
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:  # Start next cycle
                self.generation_counter += 1
                start_next_cycle = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:  # Show path
                Config.should_wipe_screen = not Config.should_wipe_screen
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:  # Toggle between rendering states
                self.render_mode()

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
        Simulation.output_text("\tBest ant scored " + str(sorted_ants[0].food_eaten) + "\n")

        # If this generation contains the best ant ever, save it to a file
        with open(Simulation.best_ant_file, "r") as best_ant_file:
            most_food_ever_eaten = int(best_ant_file.readline())

        best_ant_in_gen = sorted_ants[0]
        if best_ant_in_gen.food_eaten > most_food_ever_eaten:
            with open(Simulation.best_ant_file, "w") as best_ant_file:
                best_ant_file.write(str(best_ant_in_gen.food_eaten) + "\n" +
                                    str(best_ant_in_gen.network.get_network_values()))

        Simulation.output_text()
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
    def output_text(message="", mode="a"):

        print(message, end="")
        with open(Simulation.log_file, mode) as log_file:
            log_file.write(message)
