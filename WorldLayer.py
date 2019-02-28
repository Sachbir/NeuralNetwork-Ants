import random
from Ant import Ant
from Food import Food


class WorldLayer:

    seconds_to_live = 40
    best_score_in_cycle = 0

    should_print_food_coordinates = False

    def __init__(self, screen):

        self.screen = screen

        self.color = (255, 125, 125)
        self.ant = Ant(self, screen, self.color, (150, 150))
        self.food = Food(screen, self.color, self.ant, (600, 300))

    def update(self, start_next_cycle=False):

        if start_next_cycle:
            self.color = (255, 125, 125)
            self.ant.spawn(self.color, (150, 150))
            self.food.spawn(self.color, (600, 300))
            self.ant.time_since_eaten = 0
            WorldLayer.best_score_in_cycle = 0

            self.ant.is_alive = False
            return False

        if self.ant.collides_with((self.food.x, self.food.y)):   # On consumption of food
            self.modify_color()
            self.ant.color = self.color
            self.food.spawn(self.color, None)
            self.ant.score += 1
            self.ant.time_since_eaten = 0
            if WorldLayer.best_score_in_cycle < self.ant.score:
                WorldLayer.best_score_in_cycle = self.ant.score
                if WorldLayer.should_print_food_coordinates:
                    print(" F:", self.food.x, self.food.y, end='')
        self.food.update()

        return not self.ant.update(self.food)

    def modify_color(self):

        if self.color[1] < 0:
            self.color = (self.color[0], 0, 0)
            return

        self.color = (self.color[0], self.color[1] - 50, self.color[2] - 50)

    def restart_ant(self):
        self.color = (random.randrange(225), random.randrange(225), random.randrange(225))
        self.ant = Ant(self, self.screen, self.color, (200, 400))
