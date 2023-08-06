import itertools
import numpy as np

from ._graph import get

# https://numpy.org/doc/stable/user/basics.subclassing.html
class Parameter(np.ndarray):
    """Parameter class to be populated with gradient.

    Attributes:
        gradient (Optional[np.array]):
            Array with gradients with which parameter can be optimized via
            optimizer
        index_in_graph (int):
            Index of parameter in graph's list
        is_leaf (bool):
            Always True, used by graph to easily discern between parameters
            and operations.
    """
    def __new__(cls, input_array):
        # Input array is an already formed ndarray instance
        # We first cast to be our class type
        obj = np.asarray(input_array).view(cls)
        # Gradient is None until populated
        obj.gradient = None
        obj.index_in_graph = get()._register_parameter(obj)
        obj.is_leaf = True
        obj.last_operation_index = None
        # Return newly created object
        return obj

    # Don't sweat over it, just assigning the same attributes as in new
    def __array_finalize__(self, obj):
        """Re-assign data contained in parameter.

        Workaround for `numpy` subclassing.

        """
        if obj is None: 
            return
        self.gradient = getattr(obj, 'gradient', None)
        self.index_in_graph = getattr(obj, 'index_in_graph', None)
        self.is_leaf = getattr(obj, 'is_leaf', True)
        self.last_operation_index = getattr(obj, 'last_operation_index', None)

    def broadcast_fix(self, gradient):
        """Try to fix numpy's broadcasting with gradient.

        `1` dimensions may be broadcasted to other automatically. There is no
        clear way to know about that which could be easily implemented.

        Broadcasting is equal to summing all the values, hence __any__ dimension
        which might be off in gradient is summed by the function below.

        """
        if gradient.flatten().shape == self.flatten().shape:
            return gradient
        flattened_gradient = gradient.flatten()
        flattened_data = self.flatten()
        if len(flattened_gradient.shape) < len(flattened_data.shape):
            raise ValueError("Data has more dimension than gradient, something went very wrong.")

        to_sum = []
        # Gradient cannot be None as the condition is checked above
        for index, (data_shape, gradient_shape) in enumerate(itertools.zip_longest(flattened_data.shape, flattened_gradient.shape)):
            if data_shape is None or gradient_shape > data_shape:
                to_sum.append(index)
            if data_shape > gradient_shape:
                raise ValueError("Data has more elements than it's gradient")
        return np.sum(flattened_gradient, axis=tuple(to_sum)).flatten()


    def backward(self, upstream_gradient) -> None:
        """Take upstream gradient and update param's gradient with it."""
        self.gradient = self.broadcast_fix(upstream_gradient)

    def clear(self) -> None:
        """Clear gradient to save RAM memory."""
        self.gradient = None
