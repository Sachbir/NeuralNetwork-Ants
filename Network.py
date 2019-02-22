from NeuronLayer import NeuronLayer


class Network:

    def __init__(self, neurons_in_each_layer):

        self.layers = [NeuronLayer(0, 0)] * (len(neurons_in_each_layer) - 1)
        for i in range(len(neurons_in_each_layer) - 1):
            self.layers[i] = NeuronLayer(neurons_in_each_layer[i], neurons_in_each_layer[i + 1])

        # self.layer_count = len(sizes)
        # self.sizes = sizes
        # self.biases = [numpy.random.randn(y, 1) for y in sizes[1:]]
        # self.weights = [numpy.random.randn(y, x) for y, x in zip(sizes[1:], sizes[:-1])]

    def get_output(self, inputs):

        current_array = inputs

        for i in range(len(self.layers)):
            current_array = self.layers[i].get_outputs(current_array)
            #print(current_array)

        return current_array[0]
