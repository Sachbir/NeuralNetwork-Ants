from NeuralNetwork.Neuron import Neuron


class NeuronLayer:

    def __init__(self, input_count, neuron_count):

        # noinspection PyUnusedLocal
        self.neurons = [Neuron(input_count)
                        for i in range(neuron_count)]   # Populates an array of neurons of specified count

    def get_outputs(self, inputs):

        return [self.neurons[i].get_output(inputs)
                for i in range(len(self.neurons))]      # Print an array of the output of all neurons in this layer

    def get_layer_values(self):

        values = []

        for neuron in self.neurons:
            values.append(neuron.get_neuron_values())

        return values

    def set_layer_values(self, values, should_modify):

        for i in range(len(self.neurons)):
            self.neurons[i].set_neuron_values(values[i], should_modify)
