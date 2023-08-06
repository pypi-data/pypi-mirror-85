"""Mathematical operations usable with graph and backpropagation.

Each function (lowercase) has it's corresponding class which can handle
backpropagation. This approach allows us to simply use ops like this:

    from coreai.supervised import graph as g

    g.mean(np.array([1, 2, 3, 4, 5]))
    g.get().backward()


"""

import abc

import numpy as np

from ._graph import get
from ._parameter import Parameter


class Operation(abc.ABC):
    """Base class of mathematical operation to be run on Parameter/np.array

    Attributes:
        cache (Optional[np.array])
            Cache attribute one can use to save anything during forward pass
            to reuse in backward
        index_in_graph (int):
            Index of operation in graph's operation dictionary
        is_leaf (bool):
            Always `False`, used by graph to easily discern between parameters
            and operations.
    """

    def __init__(self):
        self.cache = None
        self.index_in_graph = None
        self.is_leaf = False

    def __call__(self, *arguments):
        """Run forward and register operation in graph.

        Additionally operation's inputs will be registered using mapping and
        whether those are leafs (parameters) or operations to be further
        backpropagated.

        """
        mapping = {}
        add_to_graph = False
        for input_index, argument in enumerate(arguments):
            if isinstance(argument, Parameter):
                add_to_graph = True
                is_first_operation = argument.last_operation_index is None
                if is_first_operation:
                    mapping[input_index] = (argument.index_in_graph, True)
                else:
                    mapping[input_index] = (argument.last_operation_index, False)

        if add_to_graph:
            self.index_in_graph = get()._register_operation(self, mapping)
            for argument in arguments:
                if isinstance(argument, Parameter):
                    argument.last_operation_index = self.index_in_graph

        # Pack return value in tuple always
        return self.forward(*arguments)

    @abc.abstractmethod
    def forward(self, *_):
        """Define your forward pass here.

        Use self.cache to cache anything needed during backpropagation.

        """
        pass

    @abc.abstractmethod
    def backward(self, upstream_gradient):
        """Define your backward pass here.

        Use self.cache in order to calculate gradient. There has to be as
        many outputs as there was inputs to forward.

        """
        pass


# Concrete implementations
class _Add(Operation):
    def forward(self, a, b):
        return a + b

    def backward(self, upstream_gradient):
        return upstream_gradient, upstream_gradient


def add(a, b):
    return _Add()(a, b)


class _Mean(Operation):
    def __init__(self, axis: int = None):
        super().__init__()
        self.axis = axis

    def forward(self, inputs):
        mean = np.mean(inputs, axis=self.axis)
        self.cache = np.ones_like(inputs) / inputs.size
        return mean

    def backward(self, upstream_gradient):
        return upstream_gradient * self.cache


def mean(inputs, axis: int = None):
    return _Mean(axis)(inputs)


class _Sigmoid(Operation):
    def forward(self, inputs):
        self.cache = 1 / (np.exp(-inputs) + 1)
        return self.cache

    def backward(self, upstream_gradient):
        return upstream_gradient * self.cache * (1 - self.cache)


def sigmoid(inputs):
    return _Sigmoid()(inputs)


class _Dot(Operation):
    def forward(self, a, b):
        self.cache = {"a": a, "b": b}
        return a @ b

    # Needs automatic reshape in order to work
    def backward(self, upstream_gradient):
        return (
            upstream_gradient @ self.cache["b"].T,
            self.cache["a"].T @ upstream_gradient,
        )


def dot(a, b):
    return _Dot()(a, b)


class _SquaredError(Operation):
    def forward(self, logits, targets):
        self.cache = logits - targets
        return np.sum(self.cache ** 2, axis=1)

    def backward(self, upstream_gradient):
        gradient = 2 * self.cache * upstream_gradient.reshape(-1, 1)
        return gradient, -gradient


def squared_error(a, b):
    return _SquaredError()(a, b)


class _CrossEntropyWithLogits(Operation):
    @staticmethod
    def _softmax(logits):
        exps = np.exp(logits - np.max(logits).reshape(-1, 1))
        return exps / np.sum(exps, axis=1).reshape(-1, 1)

    def forward(self, logits, targets):
        softmax = _CrossEntropyWithLogits._softmax(logits)
        logsoftmax = np.log(softmax)
        self.cache = {"softmax": softmax, "logsoftmax": logsoftmax, "logits": logits}
        return -np.sum(targets * logsoftmax, axis=1)

    def _backward_pass(self, d_output, inputs):
        expanded_output = d_output.reshape(-1, 1)
        return (
            -expanded_output * self.cache["logsoftmax"],
            expanded_output
            * (
                self.cache["softmax"]
                * np.expand_dims(np.sum(self.cache["logits"], axis=1), axis=1)
                - inputs["logits"]
            ),
        )


def cross_entropy_with_logits(logits, targets):
    return _SquaredError()(logits, targets)
