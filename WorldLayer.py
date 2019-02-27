import math
import random
from Ant import Ant
from Config import Config as c
from Food import Food


class WorldLayer:

    seconds_to_live = 40
    top_score = 0

    should_print_food_coordinates = False

    def __init__(self, screen):

        self.screen = screen

        self.color = (255, 200, 200)
        self.ant = Ant(self, screen, self.color, (150, 150))
        self.food = Food(screen, self.color, (600, 300), self.ant)

    def update(self, start_next_cycle=False):

        alive = 0
        dead = 1

        ant_is_alive = True

        if start_next_cycle:
            self.color = (255, 200, 200)
            self.ant.spawn(self.color, (150, 150))
            self.food.spawn(self.color, (600, 300), self.ant)
            self.ant.time_since_eaten = 0
            WorldLayer.top_score = 0
            return alive

        if self.ant.collide((self.food.x, self.food.y)):   # On consumption of food
            self.modify_color()
            self.food.spawn(self.color, None, self.ant)
            self.ant.score += 1
            self.ant.time_since_eaten = 0
            if WorldLayer.top_score < self.ant.score:
                WorldLayer.top_score = self.ant.score
                if WorldLayer.should_print_food_coordinates:
                    print(" F:", self.food.x, self.food.y, end='')
        self.food.update()
        ant_is_alive = self.ant.update(self.food, ant_is_alive)

        if ant_is_alive:
            return alive
        return dead

    def set_color(self, color):

        self.color = (255, 200 - 25 * self.ant.score, 200 - 25 * self.ant.score)
        if self.color[1] < 0:
            self.color = (255, 0, 0)

        # variance = math.floor(25 / (self.ant.score + 1) + 1)
        #
        # r = color[0] + random.randrange(-variance, variance)
        # g = color[1] + random.randrange(-variance, variance)
        # b = color[2] + random.randrange(-variance, variance)
        #
        # r = WorldLayer.flatten_values(r)
        # g = WorldLayer.flatten_values(g)
        # b = WorldLayer.flatten_values(b)
        #
        # self.color = (r, g, b)

    def modify_color(self):

        self.color = (255, 200 - 25 * self.ant.score, 200 - 25 * self.ant.score)
        if self.color[1] < 0:
            self.color = (255, 0, 0)


    @staticmethod
    def flatten_values(x):
        if x > 225:
            return 225  # Not too bright
        if x < 25:
            return 25   # Not too dark
        return x

    def restart_ant(self):
        self.color = (random.randrange(225), random.randrange(225), random.randrange(225))
        self.ant = Ant(self, self.screen, self.color, (200, 400))
