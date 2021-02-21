import numbers as nu
import numpy as np

class Container:
    def __init__(self):
        self._items = []

    def size(self):
        return len(self._items)

    def isEmpty(self):
        return not self._items

    def pop(self):
        raise NotImplementedError
    
    def peek(self):
        raise NotImplementedError

class Queue(Container):
    def __init__(self):
        super().__init__()

    def peek(self):
        assert not self.isEmpty()
        return self._items[0]

    def pop(self):
        assert not self.isEmpty()
        return self._items.pop(0)

class Stack(Container):
    def __init__(self):
        super().__init__()

    def peek(self):
        assert not self.isEmpty()
        return self._items[-1]

    def pop(self):
        assert not self.isEmpty()
        return self._items.pop(-1)

class Function:
    def __init__(self, func):
        self.func = func

    def execute(self, element, debug = True):
        # Check type
        if not isinstance(element, nu.Number):
            raise TypeError ("The element must be a number")
        result = self.func(element)

        # Report
        if debug is True:
            print("Function: " + self.func.__name__
            + "({:f}) = {:f}".format(element , result ))
        return result

class Operator:
    def __init__(self, operator, strenght):
        self.operator = operator
        self.strength = strenght

    def execute(self, element_1, element_2, debug = True):
        # Check type
        if not all(isinstance(i, nu.Number) for i in [element_1, element_2]):
            raise TypeError
        result = self.operator(element_1, element_2)

        # Report
        if debug is True:
            print("Operator: " + self.operator.__name__
            + "({:f}, {:f}) = {:f}".format(element_1, element_2, result))
        return result

class Calculator:
    def __init__(self):
        self.functions = {
            "EXP" : Function(np.exp),
            "LOG" : Function(np.log),
            "SIN" : Function(np.sin),
            "COS" : Function(np.cos),
            "SQRT" : Function(np.sqrt)
        }
        self.operators = {
            "ADD" : Operator(np.add, 0),
            "MULTIPLY" : Operator(np.multiply, 1),
            "DIVIDE" : Operator(np.divide, 1),
            "SUBTRACT" : Operator(np.subtract, 0)
        }
        self.output_queue = Queue()

