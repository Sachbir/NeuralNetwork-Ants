from Config import Config
from numpy import exp as natural_exponent
from random import uniform


class Network:

    def __init__(self):

        self.network = []
        self.set_new_network()

    def set_new_network(self):

        # network config tells the structure of the network
        # each array corresponds to a neuron layer

        num_layers = len(Config.network_config)

        # the first layer is the input layer, so we don't need to modify it
        for i in range(1, num_layers):

            layer = []
            num_neurons = Config.network_config[i]

            for j in range(num_neurons):
                neuron = []
                # add a weight for each of the neuron's input values
                neurons_in_previous_layer = Config.network_config[i - 1]
                for k in range(neurons_in_previous_layer):
                    neuron.append(Network.get_random_weight())
                # add an extra wight for the bias
                neuron.append(Network.get_random_weight())
                # add neuron to layer
                layer.append(neuron)

            self.network.append(layer)

    def get_output(self, inputs):

        # for each layer, feed it inputs and store its outputs
        # then re-feed those outputs as inputs for the next layer

        current_values = inputs
        for layer in self.network:
            # all outputs of this layer
            outputs = []
            for neuron in layer:
                num_weights = len(neuron)
                output = 0
                # each input, multiplied by its respective weight
                for i in range(num_weights - 1):
                    output = current_values[i] * neuron[i]
                # add the bias (last value)
                output += neuron[num_weights - 1]
                output = Network.sigmoid(output)
                outputs.append(output)
            # when all the neurons are done, these values become the input for the next layer
            current_values = outputs

        output_value = current_values[0]

        return output_value

    @staticmethod
    def get_random_weight():

        return uniform(-1, 1)

    @staticmethod
    def sigmoid(x):

        # doubled and lowered by one to offer values from -1 to 1
        return 2 / (1 + natural_exponent(-x)) - 1
