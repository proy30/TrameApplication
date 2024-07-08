
import webbrowser
import subprocess
import os

import inspect
import re

from impactx import distribution, elements

# -----------------------------------------------------------------------------
# Code
# -----------------------------------------------------------------------------

class generalFunctions:
    
    def documentation(section_name):
        if section_name == "LatticeElements":
            url = "https://impactx.readthedocs.io/en/latest/usage/python.html#lattice-elements"
        elif section_name == "BeamDistributions":
            url = "https://impactx.readthedocs.io/en/latest/usage/python.html#initial-beam-distributions"
        elif section_name == "pythonParameters":
            url = "https://impactx.readthedocs.io/en/latest/usage/python.html#general"
        else:
            raise ValueError(f"Invalid section name: {section_name}")
        
        if 'WSL_DISTRO_NAME' in os.environ:
            subprocess.run(['explorer.exe', url])
        else:
            webbrowser.open_new_tab(url)

    def validate(value, validation_type):
        error_messages = []

        if value is None:
            error_messages.append("Field is required")
        else:
            try:
                num_value = float(value)
                if num_value < 0:
                    error_messages.append("Must be positive")
                else:
                    if validation_type == "int":
                        if not float(value).is_integer():
                            error_messages.append("Must be an integer")
                    elif validation_type == "float":
                        try:
                            float(value)
                        except ValueError:
                            error_messages.append("Must be a float")
            except ValueError:
                error_messages.append("Must be a number")

        return error_messages
    
# -----------------------------------------------------------------------------
# Validation functions
# -----------------------------------------------------------------------------

    def determine_input_type(value):
        try:
            return int(value), int
        except ValueError:
            try:
                return float(value), float
            except ValueError:
                return value, str
        
    def validate_against(input_value, value_type):
        if input_value is None or str(input_value).strip() == "":
            if value_type == "str":
                return [f"Must be a string"]
            else:
                return [f"Must be a {value_type}"]

        if value_type == "int":
            try:
                value = int(input_value)
                if value <= 0:
                    return ["Must be positive"]
                return []
            except ValueError:
                return ["Must be an integer"]

        elif value_type == "float":
            try:
                value = float(input_value)
                if value <= 0:
                    return ["Must be positive"]
                return []
            except ValueError:
                return ["Must be a float"]

        elif value_type == "str":
            return []

        else:
            return ["Unknown type"]

# -----------------------------------------------------------------------------
# Class, parameter, default value, and default type retrievals
# -----------------------------------------------------------------------------

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
                    if (default.startswith("'") and default.endswith("'")):
                        default = default[1:-1]
                else:
                    parameter_type = type_and_default

            parameters.append((name, default, parameter_type))

        return parameters

    def classAndParametersAndDefaultValueAndType(module_name):
        classes = generalFunctions.findAllClasses(module_name)
        docstrings = generalFunctions.findInitDocstringForClasses(classes)

        result = {}

        for class_name, docstring in docstrings.items():
            parameters = generalFunctions.extractParameters(docstring)
            result[class_name] = parameters

        return result

    def selectClasses(module_name):
        return list(generalFunctions.classAndParametersAndDefaultValueAndType(module_name))

    def parametersAndDefaults(module_name):
        parameters = {}
        for key, params in generalFunctions.classAndParametersAndDefaultValueAndType(module_name).items():
            param_list = []
            for param, default, _type in params:
                param_list.append((param, default))
            parameters[key] = param_list
        return parameters

    def convert_to_correct_type(value, desired_type):
        if value is None:
            raise ValueError("Cannot convert to desired type")
        if desired_type == "int":
            return int(value)
        elif desired_type == "float":
            return float(value)
        elif desired_type == "str":
            return str(value)
        else:
            raise ValueError("Unknown type")