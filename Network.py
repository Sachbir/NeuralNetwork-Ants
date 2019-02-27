from NeuronLayer import NeuronLayer


class Network:

    def __init__(self, neurons_in_each_layer):

        self.generation = 1

        self.layers = [NeuronLayer(neurons_in_each_layer[i], neurons_in_each_layer[i + 1])
                       for i in range(len(neurons_in_each_layer) - 1)]

    def get_output(self, inputs):

        current_array = inputs

        for i in range(len(self.layers)):
            current_array = self.layers[i].get_outputs(current_array)

        return current_array[0]

    def print_network(self):

        for i in range(len(self.layers)):
            print("layer", i, ":")
            self.layers[i].print_layer()

    def get_network_values(self):

        values = []

        for layer in self.layers:
            values.append(layer.get_layer_values())

        return values

    def set_network_values(self, values):

        for i in range(len(self.layers)):
            self.layers[i].set_layer_values(values[i])
        self.generation += 1
