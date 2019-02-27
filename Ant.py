import math
import pygame
from Config import Config as c
from GameObject import GameObject
from Network import Network


class Ant(GameObject):

    # Coordinate system constructed as follows:
        # positive x is rightwards (normal)
        # positive y is downwards (inverted)
        # positive rotation is counterclockwise (inverted)

    radius = 8
    speed = 5

    network_configuration = [5, 10, 1]

    def __init__(self, parent, screen, color, coordinates, network_data=None):

        self.parent = parent

        self.score = 0
        self.time_since_eaten = 0

        super().__init__(screen, color, coordinates)
        # self.direction = random.randrange(628) / 100
        self.direction = 1      # Makes the math easier if this is not a multiple of Pi
        self.network = Network(c.network_configuration)
        if network_data is not None:
            self.network.set_network_values(network_data)

    def spawn(self, color, coordinates=None, avoid=None):

        self.score = 0
        super().spawn(color, coordinates, avoid)

    def update(self, food, is_alive):

        self.time_since_eaten += 1

        super().update()

        width, height = pygame.display.get_surface().get_size()
        out_of_bounds = ((self.x > width or
                          self.x < 0 or
                          self.y > height or
                          self.y < 0))
        # out_of_bounds = False  # False = Override 'Out of Bounds' detection

        lifespan_without_food = c.ant_TTL * 60
        if (self.time_since_eaten >= lifespan_without_food) or out_of_bounds:
            is_alive = False

        if is_alive:
            nn_inputs = self.prepare_inputs(food)
            turn_amount = self.network.get_output(nn_inputs)      # Neural network solution
            # turn_amount = self.turn_decision(food)                  # Hard-coded solution
            self.turn(turn_amount)
            self.move()

        return is_alive

    def move(self):
        self.x += c.ant_move_modifier * Ant.speed * math.cos(self.direction)
        self.y += c.ant_move_modifier * Ant.speed * math.sin(self.direction)

    def turn(self, turn_amount):
        self.direction += c.ant_move_modifier * turn_amount  # add (or subtract) movement amount from current direction
        self.direction %= (math.pi * 2)                      # constraint direction to 2 pi radians

    def prepare_inputs(self, food):

        width, height = pygame.display.get_surface().get_size()

        nn_inputs = [
            self.direction / (math.pi * 2),
            self.x / width,
            self.y / height,
            food.x / width,
            food.y / height,
        ]
        return nn_inputs

    def distance_to(self, food):
        return math.sqrt((self.x - food.x)**2 + (self.y - food.y)**2)

    #<editor-fold desc="Manual solution to finding food">
    def turn_decision(self, food):

        angular_range = math.pi / 32

        if self.should_turn_right(food):
            return angular_range    # Clockwise
        return -angular_range       # Counter-clockwise

    def should_turn_right(self, food):

        a = self.direction
        b = self.x
        c = self.y

        # we already have coordinates for the current location
        # get coordinates for a point 1 unit forwards
        delta_x = self.x + math.cos(self.direction)  # * 100
        delta_y = self.y + math.sin(self.direction)  # * 100
        # solve the line equation, y = mx + b, of the direction of travel
        m = (delta_y - self.y) / (delta_x - self.x)
        b = delta_y - m * delta_x

        # Not quite sure of explanation
        facing_right = ((self.direction - math.pi / 2) % (2 * math.pi)) > math.pi
        food_is_below = (food.y > (m * food.x + b))  # greater = lower

        if ((facing_right and food_is_below) or
                (not facing_right and not food_is_below)):
            return True     # turn right
        return False        # turn left
    #</editor-fold>
