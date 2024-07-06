
import webbrowser
import subprocess
import os

import inspect
import re

from impactx import distribution, elements
# -----------------------------------------------------------------------------
# Code
# -----------------------------------------------------------------------------

class functions:
    
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

    def find_all_classes(module):    
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

        init_params = []
        params = param_str.group(1)
        param_list = params.split(',')

        for param in param_list:
            stripped_param = param.strip()
            if not stripped_param.startswith('self'):
                init_params.append(stripped_param)

        # init_params = [param.strip() for param in param_str.group(1).split(',') if not param.strip().startswith('self')] if param_str else []
        
        return {
            "name": cls.__name__,
            "init_doc": init_documentation,
            "init_params": init_params
        }


    def find_classes(module):
        class_info_list = []

        for name in dir(module):
            obj = getattr(module, name)

            if isinstance(obj, type):
                class_info = functions.get_class_info(obj)
                class_info_list.append(class_info)
        return class_info_list
        # return [get_class_info(getattr(module, name)) for name in dir(module) if isinstance(getattr(module, name), type)]

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


    def class_with_Parameter_DefaultValue_Type_dictionary(module_name):
        classes = functions.findAllClasses(module_name)
        docstrings = functions.findInitDocstringForClasses(classes)

        result = {}

        for class_name, docstring in docstrings.items():
            parameters = functions.extractParameters(docstring)
            result[class_name] = parameters

        return result
    
    def KeysOnly(module_name):
        dictionary = functions.class_with_Parameter_DefaultValue_Type_dictionary(distribution)
        return list(dictionary.keys())
    
    def ParametersOnly(module_name):
        dictionary = functions.class_with_Parameter_DefaultValue_Type_dictionary(elements)
        
        lattice_parameters = {}

        for element_name, parameters in dictionary.items():
            parameter_list = []

            for param, default, _type in parameters:
                parameter_tuple = (param, default)
                
                parameter_list.append(parameter_tuple)
            
            lattice_parameters[element_name] = parameter_list

        return lattice_parameters

    def determine_input_type(value):
        try:
            return int(value), int
        except ValueError:
            try:
                return float(value), float
            except ValueError:
                return value, str
        
    def validate_value(input_value, value_type):
        if value_type == "int":
            try:
                value = int(input_value)
                if value <= 0:
                    return ["Must be a positive integer"]
                return []
            except ValueError:
                return ["Must be an integer"]

        elif value_type == "float":
            try:
                value = float(input_value)
                if value <= 0:
                    return ["Must be a positive float"]
                return []
            except ValueError:
                return ["Must be a float"]

        elif value_type == "string":
            return []

        else:
            return ["Unknown type specified"]
