import pygame
from Config import Config


class GameObject:

    radius = 0  # override in child classes
    screen = None

    def __init__(self, color, coordinates):

        if GameObject.screen is None:
            GameObject.screen = pygame.display.get_surface()

        # Initialize variables
        self.color = None
        self.x = None
        self.y = None

        self.spawn(color, coordinates)

    def update(self, *arg):

        if Config.should_render:
            pygame.draw.circle(GameObject.screen,
                               self.color,
                               (round(self.x), round(self.y)),
                               self.__class__.radius)

    def spawn(self, color, coordinates):

        self.color = color
        self.x, self.y = coordinates
        # self.coordinates = coordinates        # can we make this work?
