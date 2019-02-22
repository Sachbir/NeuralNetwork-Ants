from Ant import Ant
from Food import Food

class WorldLayer:

    def __init__(self, screen):

        self.screen = screen
        self.ant = Ant(screen)
        self.food = Food(screen)

    def update(self, restart_world):

        if restart_world:
            self.restart()
            return

        if self.ant.collide((self.food.x, self.food.y)):   # On consumption of food
            self.food.spawn()
        self.food.update()
        self.ant.update(self.food)

    def restart(self):

        self.ant = Ant(self.screen)
        self.food = Food(self.screen)
