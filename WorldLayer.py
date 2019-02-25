from Ant import Ant
from Food import Food
import random
import math


class WorldLayer:

    seconds_to_live = 20

    def __init__(self, screen):

        self.screen = screen

        self.color = (random.randrange(255), random.randrange(255), random.randrange(255))
        self.ant = Ant(self, screen, self.color, None)
        self.food = Food(screen, self.color, self.ant)

        self.time_since_eaten = 0

    def update(self, start_next_cycle=False):

        alive = 0
        dead = 1

        should_move = True

        if start_next_cycle:
            self.ant.spawn(self.color)
            self.food.spawn(self.color, self.ant)
            self.time_since_eaten = 0
            return alive

        if self.time_since_eaten >= (WorldLayer.seconds_to_live * 60):
            should_move = False

        if self.ant.collide((self.food.x, self.food.y)):   # On consumption of food
            self.food.spawn(self.color, self.ant)
            self.ant.total_score += 1
            self.ant.score += 1
            self.time_since_eaten = 0
            print("!", end='')
        self.food.update()
        self.ant.update(self.food, should_move)

        self.time_since_eaten += 1

        if should_move:
            return alive
        return dead

    def set_color(self, color):

        variance = math.floor(25 / (self.ant.total_score + 1))

        r = color[0] + random.randrange(-variance, variance)
        g = color[1] + random.randrange(-variance, variance)
        b = color[2] + random.randrange(-variance, variance)

        r = WorldLayer.flatten_values(r)
        g = WorldLayer.flatten_values(g)
        b = WorldLayer.flatten_values(b)

        self.color = (r, g, b)

    @staticmethod
    def flatten_values(x):
        if x > 255:
            return 255
        if x < 50:
            return 0
        return x
