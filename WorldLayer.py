from Ant import Ant
from Food import Food
import random


class WorldLayer:

    def __init__(self, screen):

        self.screen = screen

        self.color = (random.randrange(255), random.randrange(255), random.randrange(255))
        self.ant = Ant(screen, self.color, None)
        self.food = Food(screen, self.color)

        self.time_since_eaten = 0

    def update(self, start_next_cycle=False):

        should_move = True

        if start_next_cycle:
            self.ant.spawn()
            self.food.spawn()
            self.time_since_eaten = 0
            self.ant.score = 0
            return

        if self.time_since_eaten >= (10 * 60):
            should_move = False

        if self.ant.collide((self.food.x, self.food.y)):   # On consumption of food
            self.food.spawn()
            self.ant.score += 1
            self.time_since_eaten = 0
            print("Score!")
        self.food.update()
        self.ant.update(self.food, should_move)

        self.time_since_eaten += 1
