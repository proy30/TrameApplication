from trame.app import get_server
from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import vuetify, router
from trame.ui.router import RouterViewLayout

from Input.trameFunctions import trameFunctions

from Toolbar.content import toolbar

from Input.inputParametersCard.inputMain import inputParameters
from Input.distributionParametersCard.distributionMain import distributionParameters
from Input.latticeConfigurationCard.latticeMain import latticeConfiguration
from Input.runSimulationCard.content import runSimulation
from Analyze.plotsMain import AnalyzeSimulation

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# ContentSetup
# -----------------------------------------------------------------------------
inputParameters = inputParameters()
latticeConfiguration = latticeConfiguration()
runSimulation = runSimulation()

with RouterViewLayout(server, "/Input"):
    with vuetify.VContainer(fluid=True):
        with vuetify.VRow(no_gutters=True):
            with vuetify.VCol(cols="auto", classes="pa-2"):
                inputParameters.card()
            with vuetify.VCol(cols="auto", classes="pa-2"):
                distributionParameters.card()
            # with vuetify.VCol(cols="auto", classes="pa-2"):
                # runSimulation.simulationPlot()
        with vuetify.VCol(cols="auto", classes="pa-2"):
            latticeConfiguration.card() 

with RouterViewLayout(server, "/Analyze"):
        with vuetify.VContainer(fluid=True):
            with vuetify.VRow(no_gutters=True, classes="fill-height"):
                with vuetify.VCol(cols="auto", classes="pa-2 fill-height"):
                    AnalyzeSimulation.card()
                with vuetify.VCol(classes="pa-2 d-flex align-center justify-center fill-height"):
                    AnalyzeSimulation.plot()

# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------
with SinglePageWithDrawerLayout(server) as layout:
    with layout.toolbar:
        with vuetify.Template(v_if="$route.path == '/Input'"):
            toolbar.toolbar()
        with vuetify.Template(v_if="$route.path == '/Analyze'"):
            AnalyzeSimulation.toolbar()
        
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