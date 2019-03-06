import numpy
import random
from Config import Config


class Neuron:

    def __init__(self, input_count):

        # Pre-fill weights with random values, including an extra for the bias
        # noinspection PyUnusedLocal
        self.weights = [random.uniform(-1, 1)
                        for i in range(input_count + 1)]

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

    def set_neuron_values(self, values, should_modify):

        rounding = 15   # Is this still needed?

        for i in range(len(self.weights)):
            random_deviation = 0
            if should_modify:
                # Deviate neuron values within a given range
                random_deviation = random.uniform(-Config.variance_range, Config.variance_range)
            self.weights[i] = round(values[i], rounding) + random_deviation

    @staticmethod
    def modified_sigmoid(x):
        return 2 / (1 + numpy.exp(-x)) - 1
