from numbers import Number
from jijmodeling.variables.array import ArraySizePlaceholder, Tensor
from jijmodeling.variables.variable import Placeholder
import warnings
import numpy as np


def array_size(s, placeholder):
    if isinstance(s, (int, np.int)):
        return s
    elif isinstance(s, ArraySizePlaceholder):
        return np.array(placeholder[s.array_label]).shape[s.dimension]
    elif isinstance(s, Placeholder):
        return placeholder[s.label]
    else:
        raise TypeError('Array shape should be int or ArraySizePlaceholder or Placeholder, not {}'.format(type(s)))
    

def variables_validation(placeholder: dict, variables: dict):
    array = variables['array']
    ph_values = variables['placeholders']
    for label, var in placeholder.items():
        if isinstance(var, Number):
            pass
        elif isinstance(var, (list, np.ndarray)):
            if label not in ph_values and label not in array:
                warnings.warn('"{}" is not found in your model.'.format(label))
                continue
            if label not in ph_values:
                continue
            var_obj = ph_values[label]
            if isinstance(var_obj, Tensor):
                var_shape = tuple([array_size(s, placeholder) for s in var_obj.shape])
                var = np.array(var)
                if var.shape != var_shape:
                    raise TypeError('The shape of "{}" should be {}, not {}'.format(label, var_shape, var.shape))
            else:
                raise TypeError('{} is scalar value ({}). So set it to an int or a float value.'.format(label, type(variables[label])))
                