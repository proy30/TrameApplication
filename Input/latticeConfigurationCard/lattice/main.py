
from trame.app import get_server
from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import vuetify

from functions  import selectClasses
from impactx import elements
# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# Helpful
# -----------------------------------------------------------------------------
state.listOfLatticeElements = selectClasses(elements)
state.selectedLatticeList = []


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
        state.selectedLatticeList.append(selectedLattice)
        print(f"ADD button clicked, added: {selectedLattice}")
        print(f"Current list of selected lattice elements: {state.selectedLatticeList}")

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
                with vuetify.VRow(classes="mb-1 align-center", no_gutters=True):
                    with vuetify.VCol(cols=8):
                        vuetify.VSelect(
                            label="Select Accelerator Lattice",
                            v_model=("selectedLattice", None),
                            items=("listOfLatticeElements",),
                            dense=True,
                            classes="mr-2 mt-6"
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
