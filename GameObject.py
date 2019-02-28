import math
import pygame
from Config import Config


class GameObject:

    radius = 0

    def __init__(self, screen, color, coordinates):

        self.screen = screen
        self.color = color
        self.x, self.y = coordinates

        self.is_alive = True

    def update(self, *arg):

        if Config.should_render or not self.is_alive:
            pygame.draw.circle(self.screen,
                               self.color,
                               (round(self.x), round(self.y)),
                               self.__class__.radius)

    def spawn(self, color, coordinates=None):

        self.color = color

        if coordinates is not None:
            self.x, self.y = coordinates
            return

        width, height = Config.screen_size
        self.x = (self.x + 100) % width
        self.y = (self.x + 100) % height
