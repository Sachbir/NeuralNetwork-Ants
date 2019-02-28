import math
import pygame
from Config import Config
from GameObject import GameObject


class Food(GameObject):

    radius = 4

    # Stay away from the walls by 5% of height
    # 5% is arbitrary; height because it's always smaller than width
    distance_from_edge = math.floor(Config.screen_size[1] * 0.05)
    avoid_radius = 20

    def __init__(self, screen, color, ant, coordinates=(0, 0)):

        self.ant = ant
        super().__init__(screen, color, coordinates)
        self.spawn(color, coordinates)

    def spawn(self, color, coordinates=None):

        super().spawn(color, coordinates)

        width, height = Config.screen_size

        while True:
            avoid_box = pygame.Rect(self.ant.x - Food.avoid_radius,  # Top left x
                                    self.ant.y - Food.avoid_radius,  # Top left y
                                    2 * Food.avoid_radius, 2 * Food.avoid_radius)  # Dimensions
            in_avoid_box = avoid_box.collidepoint(self.x, self.y)

            out_of_bounds = ((self.x > width - Food.distance_from_edge or
                              self.x < Food.distance_from_edge or
                              self.y > height - Food.distance_from_edge or
                              self.y < Food.distance_from_edge))
            if not in_avoid_box and not out_of_bounds:
                break

            self.x = (self.x + 100) % width
            self.y = (self.y + 200) % height
