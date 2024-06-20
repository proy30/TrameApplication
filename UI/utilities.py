import re
from impactx import distribution, elements


def find_all_classes(module):
    # list_of_classes = [name for name in dir(module) if isinstance(getattr(module, name), type)]
    
    list_of_classes = []
    for name in dir(module):
        if isinstance(getattr(module, name), type):
            list_of_classes.append(name)
            
    return list_of_classes

def get_class_info(cls):
    init_documentation = getattr(cls, '__init__', None).__doc__
    if not init_documentation:
        raise ValueError(f"__init__ documentation not found")
    
    param_str = re.search(r'\((.*?)\)', init_documentation)
    init_params = [param.strip() for param in param_str.group(1).split(',') if not param.strip().startswith('self')] if param_str else []
    
    return {
        "name": cls.__name__,
        "init_doc": init_documentation,
        "init_params": init_params
    }

def find_classes(module):
    return [get_class_info(getattr(module, name)) for name in dir(module) if isinstance(getattr(module, name), type)]

