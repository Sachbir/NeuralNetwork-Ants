import pygame
import random


class GameObject:

    radius = 0

    def __init__(self, screen, color):
        self.screen = screen
        self.x = 0
        self.y = 0
        self.collision_box = pygame.Rect(0, 0, 0, 0)
        self.spawn()
        self.color = color

    def update(self, *arg):
        pygame.draw.circle(self.screen,
                           self.color,
                           (round(self.x), round(self.y)),
                           self.__class__.radius)
        self.collision_box = pygame.Rect(self.x - self.__class__.radius / 2,  # Top left x
                                         self.y - self.__class__.radius / 2,  # Top left y
                                         self.__class__.radius, self.__class__.radius)  # Dimensions

    def spawn(self):

        width, height = pygame.display.get_surface().get_size()

        self.x = random.randrange(width)
        self.y = random.randrange(height)

    def collide(self, pos):
        return self.collision_box.collidepoint(pos)
