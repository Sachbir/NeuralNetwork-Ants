import math
import pygame
import random
from Config import Config
from GameObject import GameObject


class Food(GameObject):

    food_positions = []

    radius = 4

    # Stay away from the walls by some percent of height
    #   height because it's typically smaller than width
    distance_from_edge = math.floor(Config.screen_size[1] * 0.10)
    minimum_spawn_distance_from_ant = 200

    need_next_location = True

    screen_width, screen_height = width, height = Config.screen_size

    def __init__(self, color, ant, coordinates=(0, 0)):

        # Save input values
        self.ant = ant

        Food.set_food_path()    # Set first food location
        # Food detects ant
        #   This way we don't need to update the collision box every time the ant moves
        self.collision_box = pygame.Rect(0, 0, 0, 0)

        super().__init__(color, coordinates)
        self.spawn(color, coordinates)

    def update(self, *args):
        super().update()
        # pygame.draw.rect(self.screen, self.color, self.collision_box)     # for debugging

    def spawn(self, color, coordinates=None, other=None):    # Other because of some ant stupidity

        Food.set_food_path()

        # Spawn food
        #   The 'where' depends on how much food the ant has already eaten
        super().spawn(color, Food.food_positions[self.ant.score], other)

        self.collision_box = pygame.Rect(self.x - 2 * Food.radius,  # left
                                         self.y - 2 * Food.radius,  # top
                                         4 * Food.radius,  # width
                                         4 * Food.radius)  # height

    def collides_with(self, x, y):
        return self.collision_box.collidepoint(x, y)

    @staticmethod
    def set_food_path():

        if Food.need_next_location:
            x, y = Food._get_random_screen_corner()
            # Run until food is in a new position
            #   Skip this step if the list is empty
            while len(Food.food_positions) > 0:
                # If the new position is different from the previous, move on
                if (x, y) != Food.food_positions[-1]:
                    break
                # Otherwise, generate a new set of coordinates and try again
                x, y = Food._get_random_screen_corner()
            Food.food_positions.append((x, y))
            print("Added new food position")

        Food.need_next_location = False

    @staticmethod
    def _get_random_screen_corner():

        # Pick a corner on the screen, spaced from the screen borders
        #   The X coordinate will either be the left border or the right
        #       eg. Left side is x = 5
        #           Adding the width, say 100, puts us x = 105, too far
        #           Instead, add the width and subtract the spacing twice (95)
        #   Repeat for Y
        return (Food.distance_from_edge +
                random.randrange(2) * (Config.screen_size[i] - 2 * Food.distance_from_edge)
                for i in range(2)   # For width (0) and height (1)
               )
