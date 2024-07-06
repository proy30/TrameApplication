def validate_value(input_value, value_type):
    if value_type == "int":
        try:
            int(input_value)
            return True, []
        except ValueError:
            return False, ["Must be an integer"]

    elif value_type == "float":
        try:
            float(input_value)
            return True, []
        except ValueError:
            return False, ["Must be a float"]

    elif value_type == "string":
        # Assuming any input is valid for a string
        return True, []

    else:
        return False, ["Unknown type specified"]

# Example usage
print(validate_value("123", "float"))    # Should return (True, [])
print(validate_value("123.45", "int"))  # Should return (True, [])
print(validate_value("abc", "string"))  # Should return (True, [])
print(validate_value("abc", "int"))  # Should return (False, ["Must be an integer"])
print(validate_value("abc", "float"))  # Should return (False, ["Must be a float"])
print(validate_value("123.45", "int"))  # Should return (False, ["Must be an integer"])