import numpy
import random
from Config import Config


class Neuron:

    def __init__(self, input_count):

        self.weights = [random.uniform(-1, 1)
                        for i in range(input_count + 1)]    # Pre-fill weights with random values
                                                            # +1 for the bias value

    # Given an array of inputs, return an output
    def get_output(self, inputs):

        result = self.weights[-1]   # bia value
        for i in range(0, len(inputs)):
            result += inputs[i] * self.weights[i]

        return Neuron.modified_sigmoid(result)

    def get_neuron_values(self):

        values = []
        for weight in self.weights:
            values.append(weight)

        return values

    def set_neuron_values(self, values):

        rounding = 15   # Is this still needed?

        for i in range(len(self.weights)):
            # Get a random value to deviate from inherited weights
            random_deviation = random.uniform(-Config.variance_range, Config.variance_range)
            # Set weight with the deviation
            self.weights[i] = round(values[i], rounding) + random_deviation

    @staticmethod
    def modified_sigmoid(x):
        return 2 / (1 + numpy.exp(-x)) - 1
