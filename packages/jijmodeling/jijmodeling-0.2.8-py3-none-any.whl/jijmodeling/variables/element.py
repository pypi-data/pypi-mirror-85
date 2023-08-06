from typing import Union
from jijmodeling.variables.variable import Variable
from jijmodeling.expression.from_serializable import from_serializable, _cls_serializable_validation
from jijmodeling.variables.array import Array

class Element(Variable):
    def __init__(self, label: str, array: Union[str, Array, tuple]):
        super().__init__(label)
        self.range = None
        if isinstance(array, Array):
            self.array_label = array.var_label
        elif isinstance(array, tuple):
            self.array_label = None
            self.range = array
        elif isinstance(array, str):
            self.array_label = array
        else:
            raise TypeError('array type is `str` or `Array` or `tuple` not {}'.format(array.__class__.__name__))


    @classmethod
    def from_serializable(cls, serializable: dict):
        _cls_serializable_validation(serializable, cls)
        array_label = from_serializable(serializable['attributes']['array_label'])
        if array_label is None:
            array = from_serializable(serializable['attributes']['range'])
        else:
            array = array_label
        init_args_values = {
            'label': from_serializable(serializable['attributes']['label']),
            'array': array,
        }
        return cls(**init_args_values)
