from Ant import Ant
from Food import Food

class WorldLayer:

    def __init__(self, screen):

        self.screen = screen
        self.ant = Ant(screen)
        self.food = Food(screen)

        self.time_since_eaten = 0

    def update(self, restart_world):

        should_move = True

        if restart_world:
            self.restart()
            self.time_since_eaten = 0
            self.ant.score = 0
            return

        if self.time_since_eaten >= (3 * 60):
            should_move = False

        if self.ant.collide((self.food.x, self.food.y)):   # On consumption of food
            self.food.spawn()
            self.ant.score += 1
            self.time_since_eaten = 0
        self.food.update()
        self.ant.update(self.food, should_move)

        self.time_since_eaten += 1

    def restart(self):

        self.ant = Ant(self.screen)
        self.food = Food(self.screen)
