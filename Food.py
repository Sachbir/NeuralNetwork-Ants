from GameObject import GameObject


class Food(GameObject):
    radius = 4

    def __init__(self, screen, color, ant, coordinates=(0, 0)):
        super().__init__(screen, color, ant, coordinates)
