import numbers as nu
import numpy as np
import re

class Container:
    def __init__(self):
        self._items = []

    def size(self):
        return len(self._items)

    def isEmpty(self):
        return not self._items

    def push(self, item):
        self._items.append(item)

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
        if not isinstance(element, nu.Number):
            raise TypeError("The element must be a number")
        result = self.func(element)
        if debug is True:
            print("Function: " + self.func.__name__
            + "({:f}) = {:f}".format(element , result ))
        return result

class Operator:
    def __init__(self, operator, strenght):
        self.operator = operator
        self.strength = strenght

    def execute(self, element_1, element_2, debug = True):
        if not all(isinstance(i, nu.Number) for i in [element_1, element_2]):
            raise TypeError("The element must be a number")
        result = self.operator(element_1, element_2)
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

    def calculate_rpn(self):
        stack = Stack()
        while not self.output_queue.isEmpty():
            element = self.output_queue.pop()
            if isinstance(element, nu.Number):
                stack.push(element)
            if isinstance(element, Function):
                element_2 = stack.pop()
                stack.push(element.execute(element_2))
            if isinstance(element, Operator):
                element_2 = stack.pop()
                element_3 = stack.pop()
                stack.push(element.execute(element_3, element_2))
        return stack.pop()

    def calculate_to_rpn(self, input_queue):
            stack = Stack()
            for element in input_queue:
                if isinstance(element, nu.Number):
                    self.output_queue.push(element) 
                if isinstance(element, Function):
                    stack.push(element)
                if element == "(":
                    stack.push(element)
                if element == ")":
                    while (stack.peek() != "("):
                        self.output_queue.push(stack.pop())
                    stack.pop()
                if isinstance(element, Operator):
                    while (not stack.isEmpty() and (
                    (isinstance(stack.peek(), Operator) and
                    stack.peek().strength >= element.strength) or 
                    isinstance(stack.peek(), Function))):
                        self.output_queue.push(stack.pop())
                    stack.push(element)
            while not stack.isEmpty():
                self.output_queue.push(stack.pop())

    def filter(self, txt):
        return self.functions[txt] if (
            txt in self.functions.keys()
            ) else self.operators[txt] if (
                txt in self.operators.keys()
                ) else txt if txt in ["(", ")"] else float(txt)

    def text_parse(self, txt):
        matches = re.findall(
            '-?\d+\.\d+|-?\d+|\(|\)|ADD|SUBTRACT|DIVIDE|MULTIPLY|EXP|LOG|SIN|COS|SQRT', txt.upper()
            )
        print(matches)
        return [self.filter(i) for i in matches]
    
    def calculate_expression(self, txt):
        self.calculate_to_rpn(self.text_parse(txt))
        return self.calculate_rpn()

def main():
    """main method"""
    calc = Calculator()
    test = "((15 DIVIDE (7 SUBTRACT (1 ADD 1))) MULTIPLY 3) SUBTRACT (2 ADD (1 ADD 1))"
    test2 = "15 ADD 700 ADD 7"
    var2 = calc.calculate_expression(test)
    print(var2)

if __name__ == '__main__':
    main()