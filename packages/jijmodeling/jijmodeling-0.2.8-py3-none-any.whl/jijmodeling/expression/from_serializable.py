import jijmodeling
from typing import Union

def from_serializable(serializable: Union[dict, list])->Union[dict, tuple, list]:
    if isinstance(serializable, dict) and 'class' in serializable:
        modulePath = serializable['class'].split('.')[1:]
        module = jijmodeling
        for m in modulePath:
            module = getattr(module, m)
        _cls_serializable_validation(serializable, module)
        return module.from_serializable(serializable)

    elif isinstance(serializable, dict) and 'iteratable' in serializable:
        if serializable['iteratable'] == 'list':
            return [from_serializable(s) for s in serializable['value']]
        elif serializable['iteratable'] == 'tuple':
            return tuple(from_serializable(s) for s in serializable['value'])
    
    elif isinstance(serializable, list):
        return [from_serializable(s) for s in serializable]
    elif isinstance(serializable, dict):
        return {k: from_serializable(v) for k, v in serializable.items()}

    return serializable


    

def _cls_serializable_validation(serializable: dict, cls):
    if 'class' not in serializable:
        return None
    class_name = serializable['class'].split('.')[-1]
    if cls.__name__ != class_name:
        raise ValueError('Class "{}" is not class "{}"'.format(cls.__name__, class_name))