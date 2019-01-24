import math
import numpy as np
class NeuralNetwork():
    def __init__(self, dims):
        # take inputs dims = list of integers, number of nodes in each layer
        # create self.layers = list of layer weights as np.arrays
        # create self.bias_layers = list of layer weights as np.arrays (vectors)
        # also store self.num_layers
        self.dims = dims
        self.num_layers = len(self.dims)
        self.layers = []
        self.bias_layers = []
        for i in range(self.num_layers - 1):
            self.layers.append(np.zeros((dims[i], dims[i + 1])))
            self.bias_layers.append(np.zeros(dims[i + 1]))
            for x in range(len(self.bias_layers[i])):
                self.bias_layers[i][x] = -1

    def randomize_weights(self, min=-1, max=1):
        # loop through self.layers and self.bias_layers
        # set all values to random.uniform between min and max
        for i in range(self.num_layers - 1):
            self.layers[i] = np.random.rand(len(self.layers[i]), len(self.layers[i][0]))
            self.layers[i] = 2 * self.layers[i] - 1
            self.bias_layers[i] = np.random.rand(1, len(self.bias_layers[i]))
            self.bias_layers[i] = self.bias_layers[i] * 2 - 1

        pass

    def print_layers(self):
        for l, b in zip(self.layers, self.bias_layers):
            print("layer")
            print(l)
            print("bias")
            print(b)
def forward_propagate(NN, x, A, verbose = False):
    A = np.vectorize(A)
    for i in range(NN.num_layers-1):
        x = A(np.dot(x,NN.layers[i])+NN.bias_layers[i])
        if verbose:
            print (x)
    return x
def sigmoid(x,k=1):
    return 1/(1+math.exp(-k*x))
def step(x):
    return 1 if x>0 else 0


def backprop(TS):
    NN = NeuralNetwork([2,2,1])
    for i in range(1000):
        for a,b in TS:





