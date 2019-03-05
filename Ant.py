import math
from Config import Config
from GameObject import GameObject
from Network import Network


class Ant(GameObject):

    # Coordinate system constructed as follows:
        # positive x is rightwards (normal)
        # positive y is downwards (inverted)
        # positive rotation is counterclockwise (inverted)

    radius = 8
    speed = 5

    start_location = (Config.screen_size[0] / 2,
                      Config.screen_size[1] / 2)  # Middle of screen
    lifespan_without_food = Config.ant_TTL * 60     # How many seconds before an ant starves to death

    def __init__(self, parent, color, network_data=None):

        # Store input values
        self.parent = parent

        # Initialize game object
        super().__init__(color, self.start_location)

        # Creating empty ant attributes
        self.is_alive = None
        self.in_bounds = None
        self.score = None
        self.time_since_eaten = None
        self.direction = 1      # Whole numbers (non-multiples of pi) avoids future 'divide by zero' errors
        self.network = Network()

        # Create ant
        self.spawn(color, self.start_location, network_data)

    # Set/Reset an ant's values
    def spawn(self, color, location=None, network_data=None):

        # Set initial values
        self.is_alive = True
        self.in_bounds = True
        self.score = 0
        self.time_since_eaten = 0
        # No need to set direction again; carries over from previous generation, which is random enough

        # Define ant brain
        if network_data is not None:
            self.network.set_network_values(network_data)

        # Respawn ant
        super().spawn(color, Ant.start_location, network_data)

    def update(self, food):

        if self.is_alive:
            # Normal life processes
            self.time_since_eaten += 1

            # Get screen size, and see if ant is inside it
            width, height = Config.screen_size
            self.in_bounds = (0 < self.x < width and
                              0 < self.y < height)

            if not self.in_bounds or (self.time_since_eaten >= Ant.lifespan_without_food):
                # If ant leaves screen, or hasn't eaten for a while, kill it
                self.is_alive = False
                return self.is_alive
            else:
                nn_inputs = self.prepare_nn_inputs(food)
                turn_amount = self.network.get_output(nn_inputs)      # Neural network solution
                # turn_amount = self.turn_decision(food)              # Hard-coded solution
                self.move(turn_amount)
                super().update()
        return self.is_alive

    def move(self, turn_amount):

        # Turn
        self.direction += Config.ant_move_modifier * turn_amount  # modify turn amount (within permitted range)
        self.direction %= (math.pi * 2)  # constraint direction to 2 pi radians
        # Move
        self.x += Config.ant_move_modifier * Ant.speed * math.cos(self.direction)
        self.y += Config.ant_move_modifier * Ant.speed * math.sin(self.direction)

    def prepare_nn_inputs(self, food):

        width, height = Config.screen_size

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

    def set_network_values(self, values):

        self.network.set_network_values(values)
        self.spawn(self.color)

    # <editor-fold desc="Manual solution to finding food">
    def turn_decision(self, food):

        angular_range = math.pi / 32

        if self.should_turn_right(food):
            return angular_range    # Clockwise
        return -angular_range       # Counter-clockwise

    def should_turn_right(self, food):

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
    # </editor-fold>
