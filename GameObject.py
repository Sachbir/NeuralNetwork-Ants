import pygame


class GameObject:

    avoid_radius = 20
    should_render_object = True

    distance_from_edge = 150
    radius = 0

    def __init__(self, screen, color, coordinates, avoid=None):
        self.screen = screen
        self.collision_box = pygame.Rect(0, 0, 0, 0)
        self.x = 0
        self.y = 0
        if avoid is None:
            self.spawn(color, coordinates)
        else:
            self.spawn(color, coordinates, avoid)
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

    def spawn(self, color, coordinates=None, avoid=None):

        self.color = color

        if coordinates is not None:
            self.x, self.y = coordinates
            return

        width, height = pygame.display.get_surface().get_size()
        self.x = (self.x + 100) % width
        self.y = (self.x + 100) % height

        if avoid is None:
            return

        while True:
            avoid_box = pygame.Rect(avoid.x - GameObject.avoid_radius,  # Top left x
                                    avoid.y - GameObject.avoid_radius,  # Top left y
                                    2 * GameObject.avoid_radius, 2 * GameObject.avoid_radius)  # Dimensions
            in_avoid_box = avoid_box.collidepoint(self.x, self.y)

            out_of_bounds = ((self.x > width - GameObject.distance_from_edge or
                              self.x < GameObject.distance_from_edge or
                              self.y > height - GameObject.distance_from_edge or
                              self.y < GameObject.distance_from_edge))
            if not in_avoid_box and not out_of_bounds:
                break

            self.x = (self.x + 100) % width
            self.y = (self.y + 200) % height

    def collide(self, pos):
        return self.collision_box.collidepoint(pos)
