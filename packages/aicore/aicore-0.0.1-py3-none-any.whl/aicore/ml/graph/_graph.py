class Graph:
    """Graph class used for backward automatic differentiation (backpropagation).


    Can only differentiate w.r.t. scalar values. `backpropagate` function
    should be called on final parameter (after all operations
    were performed).

    Attributes:
        operations (Dict[int, (Operation, Dict[int, (int, bool)])]):
            List of operations which, when backpropagated produce gradients
            for Parameters. Each item is a Tuple containing:
            - Instance of operation
            - Dictionary containing:
                - index of input parameter (so usually it is [0, 1, 2, 3...])
                - Tuple containing:
                    - index of operation which created this input parameter
                    - True/False value whether this node is a leaf

            If node is a leaf it has to be parameter and backpropagation stops
            at this call to `backward` (see `Parameter` class)

        parameters (List[Parameter])
            List of parameters added to this graph.
    """

    def __init__(self):
        self.operations = {}
        self.parameters = []

    def _register_parameter(self, parameter: "Parameter"):
        """Registers parameter inside the graph

        Arguments:
            Instance of Parameter to be registered

        Returns:
            Index of parameter inside the graph which is saved in parameter's instance.

        """
        self.parameters.append(parameter)
        return len(self.parameters) - 1

    def _register_operation(self, operation: "Operation", inputs):
        """Registers operation inside the graph

        Returns:
            Index of operation inside the graph which is saved in parameter's instance.

        """
        last_index = len(list(self.operations.keys()))
        self.operations[last_index] = (operation, inputs)
        return last_index

    @staticmethod
    def _get_gradient(upstream_gradient, output_index):
        """If gradient is a Tuple return element otherwise return upstream_gradient
        as is.

        """
        if isinstance(upstream_gradient, (tuple, list)):
            return upstream_gradient[output_index]
        return upstream_gradient

    def _backpropagate_node(
        self, upstream_gradient, output_index, operation_index, is_leaf
    ) -> None:
        """Backpropagate through single node (Operation or Parameter).

        If Parameter (is_leaf=True) is reached backpropagation will end with
        populating it's gradient.

        If Operation (is_leaf=False) is reached the node will be run through
        graph backpropagation again.

        """
        gradient = Graph._get_gradient(upstream_gradient, output_index)
        if is_leaf:
            self.parameters[operation_index].backward(gradient)
        else:
            # If we went through this operation we should raise an error
            new_operation = self.operations.pop(operation_index, None)
            if new_operation is None:
                raise ValueError(
                    "Trying to backpropagate through non-existent node. Are your paths disjoint?"
                )
            self._backpropagate_graph(new_operation, gradient)

    def _backpropagate_graph(self, operation_and_mapping, upstream_gradient):
        """Backpropagate through graph of operations.

        For any incoming operation it will go over their inputs
        (defined by mapping which points to input nodes) and propagate
        current upstream gradient to them.

        After calculation of gradient it's internal cached is clear by the graph

        """
        operation, mapping = operation_and_mapping
        upstream_gradient = operation.backward(upstream_gradient)
        # Clean cache
        operation.cache = None
        # Multiple outputs
        for output_index, (operation_index, is_leaf) in mapping.items():
            self._backpropagate_node(
                upstream_gradient, output_index, operation_index, is_leaf
            )

    def backward(self, upstream_gradient=1) -> None:
        """Entrypoint for backpropagation through registered nodes.

        `backward` will run through all the nodes contained inside graph in succession,
        starting with the one added as the last one.

        If there are multiple __separable__ paths those will be backpropagated
        as well. If they aren't separable an error will be raised.

        When graph's `backward` is called it will be cleaned from
        all operations (parameters stay inside graph until the graph instance
        is available, usually throughout the whole program).

        """
        while self.operations:
            last_index = list(self.operations.keys())[-1]
            self._backpropagate_graph(
                self.operations.pop(last_index), upstream_gradient
            )


class _GlobalGraph:
    "Class used to hide global state from the main namespace."
    graph = Graph()


def get():
    """Return global graph"""
    return _GlobalGraph.graph
