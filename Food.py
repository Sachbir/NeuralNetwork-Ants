import math
import pygame
from Config import Config
from GameObject import GameObject


class Food(GameObject):

    radius = 4
    collision_box_diameter = 15

    # Stay away from the walls by 5% of height
    # 5% is arbitrary; height because it's always smaller than width
    distance_from_edge = math.floor(Config.screen_size[1] * 0.05)
    minimum_spawn_distance_from_ant = 10

    def __init__(self, screen, color, ant, coordinates=(0, 0)):

        self.ant = ant
        super().__init__(screen, color, coordinates)
        self.spawn(color, coordinates)
        self.collision_box = pygame.Rect(0, 0, 0, 0)

    def spawn(self, color, coordinates=None):

        super().spawn(color, coordinates)

        self.collision_box = pygame.Rect(self.x - Food.collision_box_diameter / 2,  # left
                                         self.y - Food.collision_box_diameter / 2,  # top
                                         Food.collision_box_diameter,  # width
                                         Food.collision_box_diameter)  # height

        width, height = Config.screen_size
        while True:
            avoid_box = pygame.Rect(self.ant.x - Food.minimum_spawn_distance_from_ant,  # left
                                    self.ant.y - Food.minimum_spawn_distance_from_ant,  # top
                                    2 * Food.minimum_spawn_distance_from_ant,   # width
                                    2 * Food.minimum_spawn_distance_from_ant)   # height
            in_avoid_box = avoid_box.collidepoint(self.x, self.y)

            out_of_bounds = ((self.x > width - Food.distance_from_edge or
                              self.x < Food.distance_from_edge or
                              self.y > height - Food.distance_from_edge or
                              self.y < Food.distance_from_edge))
            if not in_avoid_box and not out_of_bounds:
                break

            self.x = (self.x + 100) % width
            self.y = (self.y + 200) % height

    def collides_with(self, point):
        return self.collision_box.collidepoint(point)
