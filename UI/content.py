from trame.app import get_server
from trame.widgets  import vuetify
from UI.utilities import find_all_classes, find_classes
from impactx import distribution, elements

# from distributionCard import reset_parameters_distributionParameters

# -----------------------------------------------------------------------   ------
# Trame setup
# -----------------------------------------------------------------------------
server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# Code
# -----------------------------------------------------------------------------

class appContent:
    def toolbar(self):
            vuetify.VSpacer()
            vuetify.VBtn(
                "Configure",
                color="primary",
                classes="mr-2"
            )
            vuetify.VSwitch(
                v_model="$vuetify.theme.dark",
                hide_details=True,
            )

    def card_container_template(self, title, reset_parameters_name):
        with vuetify.VCard(classes="ma-4", style="max-width: 340px; max-hight: 320px"):
            with vuetify.VCardTitle(title):
                vuetify.VSpacer()
                vuetify.VIcon(
                    "mdi-refresh",
                    classes="ml-2",
                    color="primary",
                    click=reset_parameters_name
                )
            vuetify.VDivider(classes="my-0")


class distributionParameters:
    def __init__ (self):
        state.selected_distribution = "Waterbag"
        state.distributions = find_classes(distribution)
        state.distribution_dropdown_options = find_all_classes(distribution)
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

    def reset_parameters():
        state.select_distribution = "Waterbag"
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

    @state.change("parameters")
    def split_parameters(parameters, **kwargs):
        third = len(parameters) // 3
        state.left_parameters = parameters[:third]
        state.middle_parameters = parameters[third:2*third]
        state.right_parameters = parameters[2*third:]

    @ctrl.add("clearDistributionBtn")
    def on_clearDistribution_click():
        resetParameters.reset_DistributionParameters()
    

    def card(self):
        with vuetify.VCard(classes="ma-2", style="max-width: 340px; height: 320px"):
            with vuetify.VCardTitle("Distribution Parameters"):
                vuetify.VSpacer()
                vuetify.VIcon(
                    "mdi-refresh",
                    classes="ml-2",
                    color="primary",
                    # click=distributionParameters.reset_parameters
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
                            style="width: 200px;"
                        )
                    with vuetify.VCol(cols="auto"):
                        vuetify.VBtn(
                            "SELECT",
                            classes="mr-2",
                            color="primary",
                            click=ctrl.selectDistributionBtn,
                            dense=True,
                            style="min-width: 80px;"
                        )
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
                                style="max-width: 90px",
                            )
                    with vuetify.VCol(cols=4):
                        with vuetify.VRow(v_for="(item, i) in right_parameters", key="i", align="center", justify="center"):
                            vuetify.VTextField(
                                v_model=("parameter_values[item]",),
                                label=("item",),
                                dense=True,
                                style="max-width: 90px",
                            )

class inputParameters:
    def __init__ (self):
        pass

    def reset_parameters():
            state.particle_shape = 1
            state.npart = 10000
            state.kin_energy_MeV = 2.0e3
            state.bunch_charge_C = 1.0e-9

    def card(self):
        with vuetify.VCard(classes="ma-2", style="max-width: 340px; height: 320px"):
            with vuetify.VCardTitle("Input Parameters", classes="d-flex justify-space-between align-center"):
                vuetify.VIcon(
                    "mdi-refresh",
                    classes="ml-2",
                    color="primary",
                    click=inputParameters.reset_parameters
                )
            vuetify.VDivider()

            with vuetify.VCardText():
                vuetify.VSelect(
                    label="Particle Shape",
                    v_model="particle_shape",
                    items=["1", "2", "3"],
                    dense=True,
                    classes="mb-2"
                )
                vuetify.VTextField(
                    label="Number of Particles",
                    v_model=("npart",),
                    type="number",
                    dense=True,
                    classes="mb-2"
                )
                with vuetify.VRow(classes="mb-2"):
                    with vuetify.VCol(cols=8):
                        vuetify.VTextField(
                            label="Kinetic Energy",
                            v_model=("kin_energy_MeV",),
                            type="number",
                            dense=True,
                            classes="mr-2"
                        )
                    with vuetify.VCol(cols=4):
                        vuetify.VSelect(
                            label="Unit",
                            items=(["eV", "meV", "MeV", "GeV", "TeV"],),
                            dense=True,
                        )
                vuetify.VTextField(
                    label="Bunch Charge (C)",
                    v_model=("bunch_charge_C",),
                    type="number",
                    dense=True,
                    classes="mb-2"
                )

class latticeConfiguration:
    def __init__(self):
        state.lattice_list = []
        state.selected_lattice =  None
        state.lattice_dropdown_options = find_all_classes(elements)
        

    def card(self):
        with vuetify.VCard(classes="ma-2", style="max-width: 712px;"):
            with vuetify.VCardTitle("Lattice Configuration", classes="d-flex justify-space-between align-center"):
                vuetify.VIcon(
                    "mdi-refresh",
                    classes="ml-2",
                    color="primary",
                    # click=reset_parameters
                )
            vuetify.VDivider()
            with vuetify.VCardText():
                with vuetify.VRow(classes="mb-2 align-center", no_gutters=True):
                    with vuetify.VCol(cols=8):
                        vuetify.VSelect(
                            label="Select Accelerator Lattice",
                            items=("lattice_dropdown_options",),
                            dense=True,
                            classes="mr-2 mt-6"
                        )
                    with vuetify.VCol(cols="auto"):
                        vuetify.VBtn(
                            "ADD",
                            classes="mr-2",
                            color="primary",
                            # click=on_add_lattice_click,
                            dense=True
                        )
                    with vuetify.VCol(cols="auto"):
                        vuetify.VBtn(
                            "CLEAR",
                            color="secondary",
                            dense=True
                        )
class resetParameters:
    def __init__(self) -> None:
        pass

    def reset_DistributionParameters():
        state.select_distribution = "Waterbag"
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
    def reset_parameters():
        state.particle_shape = 1
        state.npart = 10000
        state.kin_energy_MeV = 2.0e3
        state.bunch_charge_C = 1.0e-9
        state.image_data = None
        state.slice_step_diagnostics = False   
        state.space_charge = False
        state.selected_lattice = None
        state.selected_distribution = "waterbag"

