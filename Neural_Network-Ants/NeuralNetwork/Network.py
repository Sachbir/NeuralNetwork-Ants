from NeuralNetwork.NeuronLayer import NeuronLayer
from Config import Config


class Network:

    def __init__(self):

        self.layers = [NeuronLayer(Config.network_config[i], Config.network_config[i + 1])
                       for i in range(len(Config.network_config) - 1)]

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
