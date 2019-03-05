import math
import pygame
import random
from Config import Config
from GameObject import GameObject


class Food(GameObject):

    food_positions = []

    radius = 4

    # Stay away from the walls by 5% of height
    #   5% is arbitrary; height because it's typically smaller than width
    distance_from_edge = math.floor(Config.screen_size[1] * 0.05)
    minimum_spawn_distance_from_ant = 200

    need_next_location = True

    screen_width, screen_height = width, height = Config.screen_size

    def __init__(self, color, ant, coordinates=(0, 0)):

        # Save input values
        self.ant = ant

        Food.set_food_path()    # Set first food location
        # Food detects ant
        #   This way we don't need to update the collision box every time the ant moves
        self.collision_box = pygame.Rect(0, 0, 0, 0)

        super().__init__(color, coordinates)
        self.spawn(color, coordinates)

    def update(self, *args):
        super().update()
        # pygame.draw.rect(self.screen, self.color, self.collision_box)     # for debugging

    def spawn(self, color, coordinates=None, other=None):    # Other because of some ant stupidity

        Food.set_food_path()

        # Spawn food
        #   The 'where' depends on how much food the ant has already eaten
        super().spawn(color, Food.food_positions[self.ant.score], other)

        self.collision_box = pygame.Rect(self.x - 2 * Food.radius,  # left
                                         self.y - 2 * Food.radius,  # top
                                         4 * Food.radius,  # width
                                         4 * Food.radius)  # height

    def collides_with(self, point):
        return self.collision_box.collidepoint(point)

    @staticmethod
    def set_food_path():

        if Food.need_next_location:
            x = 100 + 700 * random.randrange(1)
            y = 100 + 700 * random.randrange(1)
            while len(Food.food_positions) > 0:
                # For the first food, just add it
                if (x, y) != Food.food_positions[-1]:
                    # For the rest, continue if the food is different from the previous location
                    # Spawning food at the same location may or may not be too CPU intensive
                    break
                # Else calculate a new random location
                # 700 is arbitrary
                x = 100 + 700 * random.randrange(1)
                y = 100 + 700 * random.randrange(1)
            Food.food_positions.append((x, y))
            Food.need_next_location = False
