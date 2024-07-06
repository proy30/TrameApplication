class distributionFunctions:
    
    def validate_value(input_value, value_type):
        if value_type == "int":
            try:
                int(input_value)
                return []
            except ValueError:
                return ["Must be an integer"]

        elif value_type == "float":
            try:
                float(input_value)
                return []
            except ValueError:
                return ["Must be a float"]

        elif value_type == "string":
            return []

        else:
            return ["Unknown type specified"]