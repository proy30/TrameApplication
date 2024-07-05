from trame.app import get_server
from trame.widgets  import vuetify

from Input.functions import functions
from impactx import distribution
# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# Content
# -----------------------------------------------------------------------------

class distributionParameters:
    def __init__ (self):
        state.selected_distribution = "Waterbag"
        state.distributions = functions.find_classes(distribution)
        state.distribution_dropdown_options = functions.find_all_classes(distribution)
        state.parameters = []


        ctrl.selectDistributionBtn()
        state.parameter_values = {
            "lambdaX": 3.9984884770e-5,
            "lambdaY": 3.9984884770e-5,
            "lambdaT": 1.0e-3,
            "lambdaPx": 2.6623538760e-5,
            "lambdaPy": 2.6623538760e-5,
            "lambdaPt": 2.0e-3,
            "muxpx": -0.846574929020762,
            "muypy": 0.846574929020762,
            "mutpt": 0.0
        }


    @ctrl.add("selectDistributionBtn")
    def on_selectDistribution_click():
        if state.selected_distribution:
            distribution_info = None
            for distribution in state.distributions:
                if distribution['name'] == state.selected_distribution:
                    distribution_info = distribution
                    break
            if distribution_info:
                state.parameters = [param.split(':')[0] for param in distribution_info['init_params']]
        print(f"Distribution has been selected to: {state.selected_distribution}")

    @state.change("parameters")
    def split_parameters(parameters, **kwargs):
        third = len(parameters) // 3
        state.left_parameters = parameters[:third]
        state.middle_parameters = parameters[third:2*third]
        state.right_parameters = parameters[2*third:]
        print(f"Distribution parameters have been changed to {state.parameters}")

    @state.change("selected_distribution")
    def on_selected_distribution_change(selected_distribution, **kwargs):
        distributionParameters.on_selectDistribution_click
        print(f"Distribution changed to: {selected_distribution}")
        
    def card(self):
        with vuetify.VCard(classes="ma-2", style="max-width: 360px; height: 320px"):
            with vuetify.VCardTitle("Distribution Parameters"):
                vuetify.VSpacer()
                vuetify.VIcon(
                    "mdi-information",
                    classes="ml-2",
                    style="color: #00313C;",
                    click=lambda: functions.documentation("BeamDistributions"),
                )
            vuetify.VDivider(classes="my-0")
            with vuetify.VCardText():
                with vuetify.VRow(no_gutters=True):
                    with vuetify.VCol(cols="auto"):
                        vuetify.VSelect(
                            label="Select Distribution",
                            items=("distribution_dropdown_options",),
                            v_model=("selected_distribution",),
                            dense=True,
                            classes="mr-2",
                            style="width: 200px;",
                            # change=ctrl.selectDistributionBtn,
                        )
                    # with vuetify.VCol(cols="auto"):
                    #     vuetify.VBtn(
                    #         "SELECT",
                    #         classes="mr-2",
                    #         color="primary",
                    #         click=ctrl.selectDistributionBtn,
                    #         dense=True,
                    #         style="min-width: 80px;"
                    #     )
                vuetify.VDivider(classes="mb-7")

                with vuetify.VRow(no_gutters=True):
                    with vuetify.VCol(cols=4):
                        with vuetify.VRow(v_for="(item, i) in left_parameters", key="i", align="center", justify="center"):
                            vuetify.VTextField(
                                v_model=("parameter_values[item]",),
                                label=("item",),
                                dense=True,
                                style="max-width: 90px",
                                type="number",
                            )
                    with vuetify.VCol(cols=4):
                        with vuetify.VRow(v_for="(item, i) in middle_parameters", key="i", align="center", justify="center"):
                            vuetify.VTextField(
                                v_model=("parameter_values[item]",),
                                label=("item",),
                                dense=True,
                                style="max-width: 45px",
                            )
                    with vuetify.VCol(cols=4):
                        with vuetify.VRow(v_for="(item, i) in right_parameters", key="i", align="center", justify="center"):
                            vuetify.VTextField(
                                v_model=("parameter_values[item]",),
                                label=("item",),
                                dense=True,
                                style="max-width: 90px",
                            )
