import pygame
import random
from Ant import Ant
from Food import Food
from Config import Config


class WorldLayer:

    seconds_to_live = 40
    best_score_in_cycle = 0

    ant_location = (200, 200)
    food_positions = []

    should_print_food_coordinates = False
    should_randomize_object_locations = True
    should_randomize_path = True

    screen = pygame.display.set_mode(Config.screen_size)

    def __init__(self):

        WorldLayer.randomize_ant_path()

        self.color = (255, 125, 125)
        self.ant = Ant(self, WorldLayer.screen, self.color, WorldLayer.ant_location)
        self.food = Food(WorldLayer.screen, self.color, self.ant, WorldLayer.food_positions[self.ant.score])   # WorldLayer.food_location)

    def update(self, start_next_cycle=False):

        if start_next_cycle:
            WorldLayer.randomize_ant_path()

            self.color = (255, 125, 125)
            self.ant.spawn(self.color, WorldLayer.ant_location)
            self.food.spawn(self.color, WorldLayer.food_positions[self.ant.score])

            WorldLayer.best_score_in_cycle = 0

        if self.food.collides_with((self.ant.x, self.ant.y)):   # On consumption of food
            self.modify_color()
            self.ant.color = self.color
            self.food.spawn(self.color, WorldLayer.food_positions[self.ant.score])
            self.ant.score += 1
            self.ant.time_since_eaten = 0
            if WorldLayer.best_score_in_cycle < self.ant.score:
                WorldLayer.best_score_in_cycle = self.ant.score
                if WorldLayer.should_print_food_coordinates:
                    print(" F:", self.food.x, self.food.y)
        self.food.update()

        return not self.ant.update(self.food)   # TODO: Figure out why this is inverted

    def modify_color(self):

        if self.color[1] < 50:
            self.color = (self.color[0], 0, 0)
            return

        self.color = (self.color[0], self.color[1] - 50, self.color[2] - 50)

    @staticmethod
    def randomize_ant_path():

        if WorldLayer.should_randomize_path:
            for i in range(10):
                x = 100 + 700 * random.randrange(1)
                y = 100 + 700 * random.randrange(1)
                WorldLayer.food_positions[i] = (x, y)
            x = 100 + 700 * random.randrange(1)
            y = 100 + 700 * random.randrange(1)
            WorldLayer.ant_location = (x, y)
            WorldLayer.should_randomize_path = False
