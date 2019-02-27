import numpy
import random
from Config import Config as c


class Neuron:

    def __init__(self, input_count):

        self.bias = random.uniform(-1, 1)               # Pre-fill bias with random value
        self.weights = [random.uniform(-1, 1)
                        for i in range(input_count)]    # Pre-fill weights with random values

    # Accepts an array of weights and a bias value
    def set_weights(self, weights, bias):

        self.bias = bias
        self.weights = weights

    # Given an array of inputs, return an output
    def get_output(self, inputs):

        result = self.bias
        for i in range(0, len(inputs)):
            result += inputs[i] * self.weights[i]
        return self.modified_sigmoid(result)

    def modified_sigmoid(self, x):
        return 2 / (1 + numpy.exp(-x)) - 1

    def print_neuron_weights(self):
        print(self.weights)

    def get_neuron_values(self):

        values = []
        for weight in self.weights:
            values.append(weight)
        values.append(self.bias)

        return values

    def set_neuron_values(self, values):

        rounding = 15

        for i in range(len(self.weights)):
            self.weights[i] = round(values[i], rounding) + random.uniform(-c.variance_range, c.variance_range)
        self.bias = round(values[len(values) - 1], rounding) + random.uniform(-c.variance_range, c.variance_range)


