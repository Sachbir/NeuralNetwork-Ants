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

        self.spawn(color, coordinates, None)

    def update(self, *arg):

        # TODO: How does this get updated x and y values?
        if Config.should_render:
            pygame.draw.circle(GameObject.screen,
                               self.color,
                               (round(self.x), round(self.y)),
                               self.__class__.radius)

    # TODO: How do I remove this other parameter when not needed?
    def spawn(self, color, coordinates, other):

        self.color = color
        self.x, self.y = coordinates
        # self.coordinates = coordinates        # can we make this work?
