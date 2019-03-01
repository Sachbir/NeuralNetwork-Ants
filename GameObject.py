import pygame
from Config import Config


class GameObject:

    radius = 0

    def __init__(self, screen, color, coordinates):

        self.screen = screen
        self.color = color
        self.x, self.y = coordinates

    def update(self, *args):

        if Config.should_render:
            pygame.draw.circle(self.screen,
                               self.color,
                               (round(self.x), round(self.y)),
                               self.__class__.radius)

    def spawn(self, color, coordinates):

        self.color = color
        self.x, self.y = coordinates
