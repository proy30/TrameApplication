from trame.app import get_server
from trame.widgets import vuetify

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
state.selectedDistribution = None  # Selected distribution is Empty by default
state.selectedDistributionParameters = []  # Initialize selectedDistributionParameters in state
state.left_selectedDistributionParameters = []
state.middle_selectedDistributionParameters = []
state.right_selectedDistributionParameters = []

def populate_distribution_parameters(selectedDistribution):
    selectedDistributionParameters = state.listOfDistributionParametersAndDefault.get(selectedDistribution, [])
    state.selectedDistributionParameters = [
        {"name": parameter_name}
        for parameter_name in selectedDistributionParameters
    ]
    return selectedDistributionParameters

def split_parameters(parameters):
    third = len(parameters) // 3
    state.left_selectedDistributionParameters = parameters[:third]
    state.middle_selectedDistributionParameters = parameters[third:2*third]
    state.right_selectedDistributionParameters = parameters[2*third:]

# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------
@state.change("selectedDistribution")
def on_lattice_element_name_change(selectedDistribution, **kwargs):
    split_parameters(populate_distribution_parameters(selectedDistribution))

# -----------------------------------------------------------------------------
# Content
# -----------------------------------------------------------------------------
class distributionParameters:
    def card():
        with vuetify.VCard(style="width: 340px; height: 320px"):
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
                            hide_details=True
                        )
                vuetify.VDivider()
                with vuetify.VRow():
                    with vuetify.VCol():
                        with vuetify.VRow(v_for="(parameter, index) in left_selectedDistributionParameters"):
                            vuetify.VTextField(
                                label=("parameter",),
                                dense=True,
                                hide_details=True,
                                style="width: 45px",
                            )
                    with vuetify.VCol():
                        with vuetify.VRow(v_for="(parameter, index) in middle_selectedDistributionParameters"):
                            vuetify.VTextField(
                                label=("parameter",),
                                dense=True,
                                hide_details=True,
                                style="width: 45px",
                            )
                    with vuetify.VCol():
                        with vuetify.VRow(v_for="(parameter, index) in right_selectedDistributionParameters"):
                            vuetify.VTextField(
                                label=("parameter.name[0]",),
                                 v_model=("parameter.name[1]",),
                                dense=True,
                                hide_details=True,
                                style="width: 45px",
                            )

# -----------------------------------------------------------------------------
# Start server
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    server.start()
