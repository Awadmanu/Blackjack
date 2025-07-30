import random

class Node:
    def __init__(self):
        self.value = 0
        self.parents = []
        self.weights = []
        self.bias = random.normalvariate(0,2)


class Layer:
    def __init__(self, n_nodes):
        self.nodes = [Node() for _ in range(n_nodes)]


class MLP:
    def __init__(self, layers):
        self.layers = [Layer(layers[l]) for l in range(len(layers))]
        self.n_layers = len(self.layers)
        for node in self.layers[0].nodes:
            node.bias = 0
        for layer in range(1, self.n_layers):
            for node in self.layers[layer].nodes:
                node.parents = self.layers[layer - 1].nodes
                node.weights = [random.normalvariate(0, 1) for _ in node.parents]
 
    def forward(self, inputs):
        for i, value in enumerate(inputs):
            self.layers[0].nodes[i].value = value
        pass

    def backward(self, targets):
        # Placeholder for backward pass logic
        pass

    def train(self, data, targets):
        # Placeholder for training logic
        pass


my_mlp = MLP([3, 5, 2])  # Example initialization with 3 input nodes, 5 hidden nodes, and 2 output nodes

print(my_mlp.layers)
print("MLP initialized with layers:", [len(layer.nodes) for layer in my_mlp.layers])

