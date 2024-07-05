from trame.app import get_server
from trame.widgets  import vuetify

from Input.functions import functions
from Input.latticeConfigurationCard.functions import selectClasses, parametersAndDefaults
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
state.listOfDistributionParametersAndDefault = parametersAndDefaults(DISTRIBUTIONS_MODULE_NAME)

# -----------------------------------------------------------------------------
# Default
# -----------------------------------------------------------------------------
state.selectedDistribution = "Waterbag" #  Selected distribution is Empty by default
state.selectedDistributionParameters = [] 


def populate_distribution_parameters(selectedDistribution):
    selectedDistributionParameters = state.listOfDistributionParametersAndDefault.get(selectedDistribution, [])

    state.selectedDistributionParameters = [
        {"parameter_name": parameter[0],
         "parameter_default_value" : parameter[1]
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

# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------

@state.change("selectedDistribution")
def on_lattice_element_name_change(selectedDistribution, **kwargs):
    populate_distribution_parameters(selectedDistribution)
    save_distribution_parameters_to_file()

@ctrl.add("updateDistributionParameters")
def on_distribution_parameter_change(parameter_name, value):
    for param in state.selectedDistributionParameters:
        if param["parameter_name"] == parameter_name:
            param["parameter_default_value"] = value
            break
    save_distribution_parameters_to_file()
    print(f"Parameter {parameter_name} was changed to {value}")
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
                        with vuetify.VRow(v_for="(parameter, index) in selectedDistributionParameters"):
                            with vuetify.VCol(v_if="index % 3 == 0"):
                                vuetify.VTextField(
                                    label=("parameter.parameter_name",),
                                    v_model=("parameter.parameter_default_value",),
                                    change=(ctrl.updateDistributionParameters,  "[parameter.parameter_name, $event]"),
                                    dense=True,
                                    hide_details=True,
                                    style="max-width: 90px",
                                )
                    with vuetify.VCol(cols=4): 
                        with vuetify.VRow(v_for="(parameter, index) in selectedDistributionParameters"):
                            with vuetify.VCol(v_if="index % 3 == 1"):
                                vuetify.VTextField(
                                    label=("parameter.parameter_name",),
                                    v_model=("parameter.parameter_default_value",),
                                    change=(ctrl.updateDistributionParameters,  "[parameter.parameter_name, $event]"),
                                    dense=True,
                                    hide_details=True,
                                    style="max-width: 90px",
                                )
                    with vuetify.VCol(cols=4):
                        with vuetify.VRow(v_for="(parameter, index) in selectedDistributionParameters"):
                            with vuetify.VCol(v_if="index % 3 == 2"):
                                vuetify.VTextField(
                                    label=("parameter.parameter_name",),
                                    v_model=("parameter.parameter_default_value",),
                                    change=(ctrl.updateDistributionParameters,  "[parameter.parameter_name, $event]"),
                                    dense=True,
                                    hide_details=True,
                                    style="max-width: 90px",
                                )


