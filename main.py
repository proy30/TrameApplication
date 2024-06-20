from trame.app import get_server
from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import vuetify, router
from trame.ui.router import RouterViewLayout

from simulation import run_impactX_simulation

from UI.trameFunctions import trameFunctions
from UI.content import appContent, inputParameters, distributionParameters, latticeConfiguration
from UI.utilities import find_all_classes, find_classes
# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# ContentSetup
# -----------------------------------------------------------------------------
appContent = appContent()
inputParameters = inputParameters()
distributionParameters = distributionParameters()
latticeConfiguration = latticeConfiguration()


with RouterViewLayout(server, "/Input"):
    with vuetify.VContainer(fluid=True):
        with vuetify.VRow(no_gutters=True):
            with vuetify.VCol(cols="auto", classes="pa-2"):
                inputParameters.card()
            with vuetify.VCol(cols="auto", classes="pa-2"):
                distributionParameters.card()
        with vuetify.VCol(cols="auto", classes="pa-2"):
            latticeConfiguration.card() 

# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------
with SinglePageWithDrawerLayout(server) as layout:
    with layout.toolbar:
        appContent.toolbar()

    with layout.drawer as drawer:
        drawer.width = 200
        with vuetify.VList():
            vuetify.VSubheader("Simulation")
        trameFunctions.create_route("Input","mdi-file-edit")
        trameFunctions.create_route("Run", "mdi-play")
        trameFunctions.create_route("Analyze", "mdi-chart-box-multiple")


    with layout.content:
        router.RouterView()
# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()