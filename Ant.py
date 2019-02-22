from GameObject import GameObject
import math
import random


class Ant(GameObject):

    # Coordinate system constructed as follows:
        # positive x is rightwards (normal)
        # positive y is downwards (inverted)
        # positive rotation is counterclockwise (inverted)

    color = (0, 0, 204)
    radius = 6
    speed = 5

    def __init__(self, screen):
        super().__init__(screen)
        self.direction = random.randrange(628) / 100
        self.direction = 1      # Makes the math easier if this is not a multiple of Pi

    def update(self, food, turn_amount):

        self.turn(turn_amount)
        self.move()
        super().update()

    def move(self):
        self.x += self.__class__.speed * math.cos(self.direction)
        self.y += self.__class__.speed * math.sin(self.direction)

    def turn(self, modification):
        self.direction += modification
        self.direction %= (math.pi * 2)
