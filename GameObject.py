import pygame
import random


class GameObject:

    avoid_radius = 100
    should_render_object = True

    distance_from_edge = 75
    radius = 0

    def __init__(self, screen, color, avoid=None):
        self.screen = screen
        self.x = 0
        self.y = 0
        self.collision_box = pygame.Rect(0, 0, 0, 0)
        if avoid is None:
            self.spawn(color)
        else:
            self.spawn(color, avoid)
        self.color = color

    def update(self, *arg):

        if GameObject.should_render_object:
            pygame.draw.circle(self.screen,
                               self.color,
                               (round(self.x), round(self.y)),
                               self.__class__.radius)
        self.collision_box = pygame.Rect(self.x - self.__class__.radius / 2,  # Top left x
                                         self.y - self.__class__.radius / 2,  # Top left y
                                         self.__class__.radius, self.__class__.radius)  # Dimensions

    def spawn(self, color, avoid=None):

        self.color = color

        width, height = pygame.display.get_surface().get_size()

        self.x = random.randrange(GameObject.distance_from_edge, width - GameObject.distance_from_edge)
        self.y = random.randrange(GameObject.distance_from_edge, height - GameObject.distance_from_edge)

        if avoid is not None:
            avoid_box = pygame.Rect(avoid.x - GameObject.avoid_radius,  # Top left x
                                    avoid.y - GameObject.avoid_radius,  # Top left y
                                    2*GameObject.avoid_radius, 2*GameObject.avoid_radius)  # Dimensions
            while True:
                self.x = random.randrange(GameObject.distance_from_edge, width - GameObject.distance_from_edge)
                self.y = random.randrange(GameObject.distance_from_edge, height - GameObject.distance_from_edge)
                if not avoid_box.collidepoint(self.x, self.y):
                    break

    def collide(self, pos):
        return self.collision_box.collidepoint(pos)
