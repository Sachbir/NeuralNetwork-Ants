import pygame
import random
from Ant import Ant
from Food import Food
from Config import Config


class WorldLayer:

    seconds_to_live = 40
    best_score_in_cycle = 0

    ant_location = (200, 200)
    food_location = (400, 400)

    should_print_food_coordinates = False
    should_randomize_object_locations = False

    screen = pygame.display.set_mode(Config.screen_size)

    def __init__(self):

        if WorldLayer.should_randomize_object_locations:
            print("randomizing")
            WorldLayer.randomize_object_locations()

        self.color = (255, 125, 125)
        self.ant = Ant(self, WorldLayer.screen, self.color, WorldLayer.ant_location)
        self.food = Food(WorldLayer.screen, self.color, self.ant, WorldLayer.food_location)

    def update(self, start_next_cycle=False):

        if start_next_cycle:
            self.color = (255, 125, 125)

            if WorldLayer.should_randomize_object_locations:
                WorldLayer.randomize_object_locations()

            self.ant.spawn(self.color, WorldLayer.ant_location)
            self.food.spawn(self.color, WorldLayer.food_location)
            self.ant.time_since_eaten = 0
            WorldLayer.best_score_in_cycle = 0

        if self.food.collides_with((self.ant.x, self.ant.y)):   # On consumption of food
            self.modify_color()
            self.ant.color = self.color
            self.food.spawn(self.color)
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
    def randomize_object_locations():

        width, height = Config.screen_size
        distance_from_wall = 100

        x = random.randrange(distance_from_wall, width - distance_from_wall)
        y = random.randrange(distance_from_wall, height - distance_from_wall)
        WorldLayer.ant_location = (x, y)
        x = random.randrange(distance_from_wall, width - distance_from_wall)
        y = random.randrange(distance_from_wall, height - distance_from_wall)
        WorldLayer.food_location = (x, y)

        WorldLayer.should_randomize_object_locations = False
