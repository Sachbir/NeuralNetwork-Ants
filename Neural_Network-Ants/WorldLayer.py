from Entities.Ant import Ant
from Entities.Food import Food


class WorldLayer:

    best_score_in_cycle = 0

    should_print_food_coordinates = False
    should_randomize_path = True

    initial_setup_complete = False

    initial_color = (255, 125, 125)     # Pink
    color_change_rate = 50

    def __init__(self):

        self.color = WorldLayer.initial_color
        self.ant = Ant(self, self.color)
        self.food = Food(self.color, self.ant)   # WorldLayer.food_location)

        self.previous_ant = self.ant

    def update(self, start_next_cycle=False):

        if start_next_cycle:
            # Reset values
            WorldLayer.best_score_in_cycle = 0

            self.color = WorldLayer.initial_color
            self.ant.spawn(self.color)
            self.food.spawn(self.color)

        if self.ant.is_alive and self.food.collides_with(self.ant.x, self.ant.y):   # If ant eats food
            # Tell ant it did a good job
            #   Must happen before ant/food spawn (Food spawn location depends on ant score
            self.ant.food_eaten += 1
            self.ant.time_since_eaten = 0

            if self.ant.food_eaten > WorldLayer.best_score_in_cycle:
                WorldLayer.best_score_in_cycle = self.ant.food_eaten
                Food.need_next_location = True
                Food.set_food_path()
                if WorldLayer.should_print_food_coordinates:
                    print(" F:", self.food.x, self.food.y)

            self.modify_color()
            self.ant.color = self.color
            self.food.spawn(self.color)     # Spawn new food with updated color

        # Render
        self.food.update()
        # Returns whether and is alive
        return self.ant.update(self.food)

    def modify_color(self):

        if self.color[1] < 50:  # Colors 1 and 2 are identical; choose either
            self.color = (self.color[0], 0, 0)
            return

        self.color = (self.color[0],
                      self.color[1] - WorldLayer.color_change_rate,
                      self.color[2] - WorldLayer.color_change_rate)

    def set_render(self, value):

        self.ant.should_render = value
        self.food.should_render = value
