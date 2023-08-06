from jijmodeling.expression.expression import Operator
from jijmodeling.variables.variable import Variable

def equal(left, right):
    return Equal([left, right])

def neq(left, right):
    return NotEqual([left, right])

class Condition(Operator):
    def __and__(self, other):
        return AndOperator([self, other])
    
    def __xor__(self, other):
        return XorOperator([self, other])

    def __or__(self, other):
        return OrOperator([self, other])

class Equal(Condition):
    def operation(self, objects: list) -> bool:
        return objects[0] == objects[1]

class NotEqual(Condition):
    def operation(self, objects: list) -> bool:
        return objects[0] != objects[1]

class LessThan(Condition):
    def operation(self, objects: list) -> bool:
        return objects[0] < objects[1]

class LessThanEqual(Condition):
    def operation(self, objects: list) -> bool:
        return objects[0] <= objects[1]

class GreaterThan(Condition):
    def operation(self, objects: list) -> bool:
        return objects[0] > objects[1]

class GreaterThanEqual(Condition):
    def operation(self, objects: list) -> bool:
        return objects[0] >= objects[1]

        
class AndOperator(Condition):
    def operation(self, objects: list) -> bool:
        return objects[0] & objects[1]

class XorOperator(Condition):
    def operation(self, objects: list) -> bool:
        return objects[0] ^ objects[1]

class OrOperator(Condition):
    def operation(self, objects: list) -> bool:
        return objects[0] | objects[1]
