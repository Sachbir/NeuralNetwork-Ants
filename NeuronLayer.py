from Neuron import Neuron


class NeuronLayer:

    def __init__(self, input_count, neuron_count):

        self.neurons = [Neuron(input_count)
                        for i in range(neuron_count)]   # Populates an array of neurons of specified count

    def get_outputs(self, inputs):

        outputs = [self.neurons[i].get_output(inputs)
                   for i in range(len(self.neurons))]           # Fill outputs with output values of each neuron

        return outputs

    def print_layer(self):

        for neuron in self.neurons:
            neuron.print_neuron_weights()
