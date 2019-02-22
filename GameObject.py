import pygame
import random


class GameObject:

    color = (0, 0, 0)
    radius = 0

    def __init__(self, screen):
        self.screen = screen
        self.x = 0
        self.y = 0
        self.collision_box = pygame.Rect(0, 0, 0, 0)
        self.spawn()

    def update(self, *arg):
        pygame.draw.circle(self.screen,
                           self.__class__.color,
                           (round(self.x), round(self.y)),
                           self.__class__.radius)
        self.collision_box = pygame.Rect(self.x - self.__class__.radius / 2,  # Top left x
                                         self.y - self.__class__.radius / 2,  # Top left y
                                         self.__class__.radius, self.__class__.radius)  # Dimensions

    def spawn(self):
        self.x = random.randrange(500)
        self.y = random.randrange(500)

    def collide(self, pos):
        return self.collision_box.collidepoint(pos)
