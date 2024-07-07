from trame.app import get_server
from trame.widgets  import vuetify

from Input.generalFunctions import functions
from impactx import distribution

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# Helpful
# -----------------------------------------------------------------------------

DISTRIBUTIONS_MODULE_NAME = distribution

state.listOfDistributions = functions.selectClasses(DISTRIBUTIONS_MODULE_NAME)
state.listOfDistributionsAndParametersAndDefault = functions.classAndParametersAndDefaultValueAndType(DISTRIBUTIONS_MODULE_NAME)

# -----------------------------------------------------------------------------
# Default
# -----------------------------------------------------------------------------

state.selectedDistribution = "Waterbag" #  Selected distribution is Empty by default
state.selectedDistributionParameters = [] 

# -----------------------------------------------------------------------------
# Main Functions
# -----------------------------------------------------------------------------

def populate_distribution_parameters(selectedDistribution):
    selectedDistributionParameters = state.listOfDistributionsAndParametersAndDefault.get(selectedDistribution, [])

    state.selectedDistributionParameters = [
        {"parameter_name" : parameter[0],
         "parameter_default_value" : parameter[1],
         "parameter_type" : parameter[2],
         "parameter_error_message": [],
         }
        for parameter in selectedDistributionParameters
    ]
    
    save_distribution_parameters_to_file()
    return selectedDistributionParameters


def update_distribution_parameters(parameterName, parameterValue, parameterErrorMessage):
    """
    Updates parameter value and then includes error message if user input is not valid
    """
    for param in state.selectedDistributionParameters:
        if param["parameter_name"] == parameterName:
            param["parameter_default_value"] = parameterValue
            param["parameter_error_message"] = parameterErrorMessage
    
    state.dirty("selectedDistributionParameters")
    save_distribution_parameters_to_file()

# -----------------------------------------------------------------------------
# Write to file functions
# -----------------------------------------------------------------------------

def parameter_input_checker():
    """
    Helper function to check if user input is valid, if yes, then will update with value, if not then set to None.
    """
    parameter_input = {}
    for param in state.selectedDistributionParameters:
        if param["parameter_error_message"] == []:
            parameter_input[param["parameter_name"]] = param["parameter_default_value"]
        else:
            parameter_input[param["parameter_name"]] = None

    return parameter_input

def save_distribution_parameters_to_file():
    """
    Writes users input for distribution parameters into file in simulation code format
    """
    distribution_name = state.selectedDistribution
    parameters = parameter_input_checker()

    with open("output_distribution_parameters.txt", "w") as file:
        file.write(f"distr = distribution.{distribution_name}(\n")
        for param, value in parameters.items():
            file.write(f"    {param}={value},\n")
        file.write(")\n")
# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------

@state.change("selectedDistribution")
def on_lattice_element_name_change(selectedDistribution, **kwargs):
    populate_distribution_parameters(selectedDistribution)
    # print(f"Current list of selected lattice elements: {state.selectedDistributionParameters}")

@ctrl.add("updateDistributionParameters")
def on_distribution_parameter_change(parameter_name, parameter_value, parameter_type):
    parameter_value, input_type = functions.determine_input_type(parameter_value)
    error_message = functions.validate_against(parameter_value, parameter_type)
    
    update_distribution_parameters(parameter_name, parameter_value, error_message)
    print(f"Parameter {parameter_name} was changed to {parameter_value} (type: {input_type})")

# -----------------------------------------------------------------------------
# Content
# -----------------------------------------------------------------------------

class distributionParameters:
    def card():
        with vuetify.VCard(style="width: 340px; height: 300px"):
            with vuetify.VCardTitle("Distribution Parameters"):
                vuetify.VSpacer()
                vuetify.VIcon(
                    "mdi-information",
                    style="color: #00313C;",
                    click=lambda: functions.documentation("BeamDistributions"),
                )
            vuetify.VDivider()
            with vuetify.VCardText():
                vuetify.VCombobox(
                    label="Select Distribution",
                    v_model=("selectedDistribution",),
                    items=("listOfDistributions",),
                    dense=True,
                )
                with vuetify.VRow(classes="my-2"):
                    for i in range(3):
                        with vuetify.VCol(cols=4, classes="py-0"):
                            with vuetify.VRow(v_for="(parameter, index) in selectedDistributionParameters"):
                                with vuetify.VCol(v_if=f"index % 3 == {i}", classes="py-1"):
                                    vuetify.VTextField(
                                        label=("parameter.parameter_name",),
                                        v_model=("parameter.parameter_default_value",),
                                        change=(ctrl.updateDistributionParameters, "[parameter.parameter_name, $event, parameter.parameter_type]"),
                                        error_messages=("parameter.parameter_error_message",),
                                        type="number",
                                        dense=True,
                                    )