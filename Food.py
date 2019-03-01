import math
import pygame
from Config import Config
from GameObject import GameObject


class Food(GameObject):

    radius = 4

    # Stay away from the walls by 5% of height
    # 5% is arbitrary; height because it's always smaller than width
    distance_from_edge = math.floor(Config.screen_size[1] * 0.05)
    minimum_spawn_distance_from_ant = 200

    def __init__(self, screen, color, ant, coordinates=(0, 0)):

        self.ant = ant
        super().__init__(screen, color, coordinates)
        self.collision_box = pygame.Rect(0, 0, 0, 0)
        self.spawn(color, coordinates)

    def update(self, *args):
        super().update()
        # pygame.draw.rect(self.screen, self.color, self.collision_box)     # for debugging

    def spawn(self, color, coordinates):

        super().spawn(color, coordinates)

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

        self.collision_box = pygame.Rect(self.x - 2 * Food.radius,  # left
                                         self.y - 2 * Food.radius,  # top
                                         4 * Food.radius,  # width
                                         4 * Food.radius)  # height

    def collides_with(self, point):
        return self.collision_box.collidepoint(point)
