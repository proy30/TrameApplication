from trame.app import get_server
from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import vuetify

# Create a new server with the correct client type
server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# Initialize the state values
state.int_value = 2
state.int_error_messages = []
state.float_value = 2.0
state.float_error_messages = []

# Define the main page content
def ui_layout(server):
    with SinglePageWithDrawerLayout(server) as layout:
        layout.title.set_text("Validate on Blur Example")

        with layout.content:
            vuetify.VTextField(
                v_model=("int_value",),
                label="Enter integer",
                error_messages=("int_error_messages", []),
                clearable=True,
                type="number"
            )
            vuetify.VTextField(
                v_model=("float_value",),
                label="Enter float",
                error_messages=("float_error_messages", []),
                validate_on_blur=True,
                clearable=True,
                type="number"
            )

# Define the validation functions
def validate_text(value, validation_type):
    error_messages = []

    # Check if the field is required
    if value is None:
        error_messages.append("Field is required")
    else:
        try:
            num_value = float(value)
            # Check if the value is positive
            if num_value <= 0:
                error_messages.append("Must be positive")
            else:
                # Check if the value is an integer or a float
                if validation_type == "int":
                    if not float(value).is_integer():
                        error_messages.append("Must be an integer")
                elif validation_type == "float":
                    # Check if value is a valid float
                    try:
                        float(value)
                    except ValueError:
                        error_messages.append("Must be a float")
        except ValueError:
            error_messages.append("Must be a number")

    return error_messages

# Define the data and validation rules
@state.change("int_value")
def update_int_validation(int_value, **kwargs):
    state.int_error_messages = validate_text(int_value, "int")
    print(f"Integer value changed to: {int_value}")

@state.change("float_value")
def update_float_validation(float_value, **kwargs):
    state.float_error_messages = validate_text(float_value, "float")
    print(f"Float value changed to: {float_value}")

# Set up the server and initialize the layout
ui_layout(server)
server.start()
