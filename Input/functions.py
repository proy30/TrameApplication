
import webbrowser
import subprocess
import os

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