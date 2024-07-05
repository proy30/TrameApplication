import inspect
import re
from impactx import elements, distribution

def findAllClasses(module_name):
    results = []
    for name in dir(module_name):
        attr = getattr(module_name, name)
        if inspect.isclass(attr):
            results.append((name, attr))
    return results


def findInitDocstringForClasses(classes):
    docstrings = {}
    for name, cls in classes:
        init_method = getattr(cls, '__init__', None)
        if init_method:
            docstring = cls.__init__.__doc__
            docstrings[name] = docstring
    return docstrings


def extractParameters(docstring):
    parameters = []
    docstring = re.search(r'\((.*?)\)', docstring).group(1)  # Return class name and init signature
    docstring = docstring.split(',')

    for parameter in docstring:
        if parameter.startswith('self'):
            continue
        
        name = parameter
        default = None
        parameter_type = 'Any' 

        if ':' in parameter:
            split_by_semicolon = parameter.split(':', 1)
            name = split_by_semicolon[0].strip()
            type_and_default = split_by_semicolon[1].strip()
            if '=' in type_and_default:
                split_by_equals = type_and_default.split('=', 1)
                parameter_type = split_by_equals[0].strip()
                default = split_by_equals[1].strip()
                if default.isalpha():
                    default = f"'{default}'"
            else:
                parameter_type = type_and_default

        parameters.append((name, default, parameter_type))

    return parameters


def latticeElementsList(module_name):
    classes = findAllClasses(module_name)
    docstrings = findInitDocstringForClasses(classes)

    result = {}

    for class_name, docstring in docstrings.items():
        parameters = extractParameters(docstring)
        result[class_name] = parameters

    return result

def selectClasses(module_name):
    return list(latticeElementsList(module_name))

def parametersAndDefaults(module_name):
    parameters = {}
    for key, params in latticeElementsList(module_name).items():
        param_list = []
        for param, default, _type in params:
            param_list.append((param, default))
        parameters[key] = param_list
    return parameters

# print(selectClasses(distribution))
# print(parametersAndDefaults(distribution))
