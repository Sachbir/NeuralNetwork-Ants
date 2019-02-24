from GameObject import GameObject
import math
import random
from Network import Network


class Ant(GameObject):

    # Coordinate system constructed as follows:
        # positive x is rightwards (normal)
        # positive y is downwards (inverted)
        # positive rotation is counterclockwise (inverted)

    color = (0, 0, 204)
    radius = 6
    speed = 5

    score = 0

    network_configuration = [5, 5, 1]

    def __init__(self, screen):
        super().__init__(screen)
        self.direction = random.randrange(628) / 100
        self.direction = 1      # Makes the math easier if this is not a multiple of Pi

        self.network = Network(self.__class__.network_configuration)

    def update(self, food, should_move):

        if should_move:
            nn_inputs = self.prepare_inputs(food)
            turn_amount = self.network.get_output(nn_inputs)
            # print(turn_amount)
            self.turn(turn_amount)
            self.move()
        super().update()

    def spawn(self):
        self.network = Network(self.__class__.network_configuration)
        super().spawn()

    def move(self):
        self.x += self.__class__.speed * math.cos(self.direction)
        self.y += self.__class__.speed * math.sin(self.direction)

    def turn(self, modification):
        self.direction += modification
        self.direction %= (math.pi * 2)

    def prepare_inputs(self, food):
        nn_inputs = [
            self.direction / (math.pi * 2),
            self.x / 500,
            self.y / 500,
            food.x / 500,
            food.y / 500,
        ]
        return nn_inputs
