from trame.app import get_server
from trame.widgets  import vuetify

from Input.functions import functions
from Input.latticeConfigurationCard.functions import selectClasses, classAndParametersAndDefaultValueAndType
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

state.listOfDistributions = selectClasses(DISTRIBUTIONS_MODULE_NAME)
state.listOfDistributionsAndParametersAndDefault = classAndParametersAndDefaultValueAndType(DISTRIBUTIONS_MODULE_NAME)

# -----------------------------------------------------------------------------
# Default
# -----------------------------------------------------------------------------
state.selectedDistribution = "Waterbag" #  Selected distribution is Empty by default
state.selectedDistributionParameters = [] 


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

    return selectedDistributionParameters

def save_distribution_parameters_to_file():
    distribution_name = state.selectedDistribution
    parameters = {param["parameter_name"]: param["parameter_default_value"] for param in state.selectedDistributionParameters}

    with open("output_distribution_parameters.txt", "w") as file:
        file.write(f"distr = distribution.{distribution_name}(\n")
        for param, value in parameters.items():
            file.write(f"    {param}={value},\n")
        file.write(")\n")

def validate_float_test(value):
    try:
        float(value)
        return True, []
    except ValueError:
        return False, ["Must be a float"]
# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------

@state.change("selectedDistribution")
def on_lattice_element_name_change(selectedDistribution, **kwargs):
    populate_distribution_parameters(selectedDistribution)
    save_distribution_parameters_to_file()

@ctrl.add("updateDistributionParameters")
def on_distribution_parameter_change(parameter_name, parameter_value):
    parameter_value, input_type = functions.determine_input_type(parameter_value)
    print(f"Parameter {parameter_name} was changed to {parameter_value} (type: {input_type})")
    
    for param in state.selectedDistributionParameters:
        if param["parameter_name"] == parameter_name:
            param["parameter_default_value"] = parameter_value
            isValid, error_message = validate_float_test(parameter_value)
            param["parameter_error_message"] = error_message
            break
    state.dirty("selectedDistributionParameters")
    save_distribution_parameters_to_file()
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
            vuetify.VDivider(classes="my-0")
            with vuetify.VCardText():
                with vuetify.VRow():
                    with vuetify.VCol():
                        vuetify.VSelect(
                            label="Select Distribution",
                            v_model=("selectedDistribution",),
                            items=("listOfDistributions",),
                            dense=True,
                            hide_details=True,
                        )
                with vuetify.VRow():
                    with vuetify.VCol(cols=4):
                        with vuetify.VRow(v_for="(parameter, index) in selectedDistributionParameters", no_gutters=True):
                            with vuetify.VCol(v_if="index % 3 == 0"):
                                vuetify.VTextField(
                                    label=("parameter.parameter_name",),
                                    v_model=("parameter.parameter_default_value",),
                                    change=(ctrl.updateDistributionParameters,  "[parameter.parameter_name, $event]"),
                                    error_messages=("parameter.parameter_error_message",),
                                    dense=True,
                                    style="max-width: 90px",
                                )
                    with vuetify.VCol(cols=4): 
                        with vuetify.VRow(v_for="(parameter, index) in selectedDistributionParameters", no_gutters=True):
                            with vuetify.VCol(v_if="index % 3 == 1"):
                                vuetify.VTextField(
                                    label=("parameter.parameter_name",),
                                    v_model=("parameter.parameter_default_value",),
                                    change=(ctrl.updateDistributionParameters,  "[parameter.parameter_name, $event]"),
                                    error_messages=("parameter.parameter_error_message",),
                                    dense=True,
                                    style="max-width: 90px",
                                )
                    with vuetify.VCol(cols=4):
                        with vuetify.VRow(v_for="(parameter, index) in selectedDistributionParameters", no_gutters=True):
                            with vuetify.VCol(v_if="index % 3 == 2"):
                                vuetify.VTextField(
                                    label=("parameter.parameter_name",),
                                    v_model=("parameter.parameter_default_value",),
                                    change=(ctrl.updateDistributionParameters,  "[parameter.parameter_name, $event]"),
                                    error_messages=("parameter.parameter_error_message",),
                                    dense=True,
                                    style="max-width: 90px",
                                )


