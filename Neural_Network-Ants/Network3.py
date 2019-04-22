from NeuralNetwork.NeuronLayer import NeuronLayer
from Config import Config
from random import uniform
import numpy

import sys


class Network:

    def __init__(self):

        self.layers = [NeuronLayer(Config.network_config[i], Config.network_config[i + 1])
                       for i in range(len(Config.network_config) - 1)]

        self.network = []

        for i in range(len(Config.network_config) - 1):     # Number of layers is 1 less than the length of the config array
            layer = []
            for j in range(Config.network_config[i + 1]):       # each config value gives the number of neurons in the previous
                neuron = []
                for k in range(0, Config.network_config[i] + 1):    # for each neuron that's inputting (plus a bias)
                    neuron.append(get_random_weight())                  # assign a weight
                layer.append(neuron)
            self.network.append(layer)

        # print(self.network)
        # sys.exit(10)

        ##### INCOMPLETE

    def get_output(self, inputs):


        current_array = inputs

        # with Pool(2) as p:
        #     for i in range(len(self.layers)):
        #         current_array = p.map(Network.parallelize, self.layers, current_array)

        for i in range(len(self.layers)):
            current_array = self.layers[i].get_outputs(current_array)

        return current_array[0]

    def get_network_values(self):

        values = []

        for layer in self.layers:
            values.append(layer.get_layer_values())

        return values

    def set_network_values(self, values, should_modify=True):

        for i in range(len(self.layers)):
            self.layers[i].set_layer_values(values[i], should_modify)

def get_random_weight():

    return uniform(-1, 1)
