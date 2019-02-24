import random
import numpy


class Neuron:

    def __init__(self, input_count):

        self.weights = [random.uniform(-1, 1)
                        for i in range(input_count)]    # Pre-fill weights with random values
        self.bias = random.uniform(-1, 1)               # Pre-fill bias with random value

    # Accepts an array of weights and a bias value
    def set_weights(self, weights, bias):

        self.weights = weights
        self.bias = bias

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
