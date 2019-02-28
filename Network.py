from NeuronLayer import NeuronLayer
from Config import Config


class Network:

    def __init__(self):

        self.layers = [NeuronLayer(Config.network_configuration[i], Config.network_configuration[i + 1])
                       for i in range(len(Config.network_configuration) - 1)]

    def get_output(self, inputs):

        current_array = inputs

        for i in range(len(self.layers)):
            current_array = self.layers[i].get_outputs(current_array)

        return current_array[0]

    def get_network_values(self):

        values = []

        for layer in self.layers:
            values.append(layer.get_layer_values())

        return values

    def set_network_values(self, values):

        for i in range(len(self.layers)):
            self.layers[i].set_layer_values(values[i])
