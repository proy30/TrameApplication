
from trame.app import get_server
from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import vuetify

from functions  import selectClasses, parametersAndDefaults
from impactx import elements

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# Helpful
# -----------------------------------------------------------------------------
LATTICE_ELEMENTS_MODULE_NAME = elements

state.listOfLatticeElements = selectClasses(LATTICE_ELEMENTS_MODULE_NAME)
state.listOfLatticeElementParametersAndDefault = parametersAndDefaults(LATTICE_ELEMENTS_MODULE_NAME)

# -----------------------------------------------------------------------------
# Default
# -----------------------------------------------------------------------------
state.selectedLattice = None #  Selected lattice is Empty by default
state.selectedLatticeList = [] # Selected lattice list is Empty by default

# state.listOfLatticeElementParametersAndDefault = {'Alignment': [], 'Aperture': [('xmax', None), ('ymax', None), ('shape', "'rectangular'"), ('dx', '0'), ('dy', '0'), ('rotation', '0')], 
#                                             'BeamMonitor': [('name', None), ('backend', "'default'"), ('encoding', "'g'")],
#                                             'Buncher': [('V', None), ('k', None), ('dx', '0'), ('dy', '0'), ('rotation', '0')],
#                                             'CFbend': [('ds', None), ('rc', None), ('k', None), ('dx', '0'), ('dy', '0'), ('rotation', '0'), ('nslice', '1')]
#                                             }  


def add_lattice_element():
    selectedLattice = state.selectedLattice
    selectedLatticeParameters = state.listOfLatticeElementParametersAndDefault.get(selectedLattice, [])

    selectedLatticeElementWithParameters = {
        "name": selectedLattice,
        "parameters_with_default_value": selectedLatticeParameters,
    }
    return selectedLatticeElementWithParameters
# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------
@state.change("selectedLattice")
def on_lattice_element_changed(selectedLattice, **kwargs):
    print (f"Lattice Selection Changed to: {selectedLattice}")

@ctrl.add("add_latticeElement")
def on_add_lattice_click():
    selectedLattice = state.selectedLattice
    if selectedLattice:
        selectedLatticeElementWithParameters = add_lattice_element()
        state.selectedLatticeList.append(selectedLatticeElementWithParameters)
        state.dirty("selectedLatticeList")
        # print(f"ADD button clicked, added: {selectedLattice}")
        # print(f"Current list of selected lattice elements: {state.selectedLatticeList}")

# -----------------------------------------------------------------------------
# ContentSetup
# -----------------------------------------------------------------------------
class latticeConfiguration:
    def card(self):
        with vuetify.VCard(classes="ma-2", style="width: 712px;"):
            with vuetify.VCardTitle("Lattice Configuration"):
                vuetify.VIcon(
                    "mdi-information",
                    classes="ml-2",
                    style="color: #00313C;",
                )
            vuetify.VDivider()
            with vuetify.VCardText():
                with vuetify.VRow(align="center"):
                    with vuetify.VCol(cols=8):
                        vuetify.VSelect(
                            label="Select Accelerator Lattice",
                            v_model=("selectedLattice", None),
                            items=("listOfLatticeElements",),
                            dense=True,
                            classes="mr-2"
                        )
                    with vuetify.VCol(cols="auto"):
                        vuetify.VBtn(
                            "ADD",
                            color="primary",
                            dense=True,
                            classes="mr-2",
                            click=ctrl.add_latticeElement,
                        )
                    with vuetify.VCol(cols="auto"):
                        vuetify.VBtn(
                            "CLEAR",
                            color="secondary",
                            dense=True
                        )
                with vuetify.VRow():
                    with vuetify.VCol():       
                        with vuetify.VCard(style="height: 300px; width: 700px; overflow-y: auto;"):
                            with vuetify.VCardTitle("Elements", classes="text-subtitle-2 pa-2"):
                                vuetify.VSpacer()
                                vuetify.VIcon(
                                    "mdi-arrow-expand",
                                    color="primary",
                                )
                            vuetify.VDivider()
                            with vuetify.VContainer(fluid=True):
                                with vuetify.VRow(v_for="(latticeElement, index) in selectedLatticeList", align="center"):
                                    with vuetify.VCol():
                                        vuetify.VChip(
                                            style="width: 150px; justify-content: center;",
                                            v_text=("latticeElement.name",),
                                            dense=True,
                                        )
                                    with vuetify.VCol(v_for="(value, parameterIndex) in latticeElement.parameters_with_default_value"):
                                            vuetify.VTextField(
                                                label=("value[0]",), # value[0] = parameter name
                                                v_model=("value[1]",), #  value[1] =  parameter default value 
                                            )

latticeConfiguration =  latticeConfiguration()
with SinglePageWithDrawerLayout(server) as layout:
    with layout.content:
        with vuetify.VContainer(fluid=True):
            with vuetify.VRow(no_gutters=True):
                with vuetify.VCol(cols="auto", classes="pa-2"):
                    latticeConfiguration.card()

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
