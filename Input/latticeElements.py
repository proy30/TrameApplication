import inspect
import re
from impactx import elements

def find_classes_and_parameters(module):
    results = {}
    for name in dir(module):
        attr = getattr(module, name)
        if isinstance(attr, type):
            init = attr.__init__
            try:
                sig = inspect.signature(init)
                params = [(param.name, 
                           param.default if param.default != param.empty else None,
                           param.annotation.__name__ if param.annotation != param.empty else 'Unknown') 
                          for param in sig.parameters.values() if param.name != 'self']
            except ValueError:
                params = parse_docstring(init.__doc__)
            results[name] = params
    return results

def parse_docstring(docstring):
    params = []
    if docstring:
        match = re.search(r'__init__\(self(?:, )?(.*?)\)', docstring)
        if match:
            for param in match.group(1).split(', '):
                parts = param.split(':')
                name = parts[0].strip()
                type_ = parts[1].split('=')[0].strip() if len(parts) > 1 else 'Unknown'
                default = parts[1].split('=')[1].strip() if '=' in parts[1] else None
                if name:
                    params.append((name, default, type_))
    return params

def get_lattice_elements(module):
    # Get class parameters
    results = find_classes_and_parameters(module)

    # Format the results
    formatted_results = {k: [(name, default, type_) for name, default, type_ in v] for k, v in results.items()}

    return formatted_results

# Example usage

