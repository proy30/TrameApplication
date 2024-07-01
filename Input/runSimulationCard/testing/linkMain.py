import matplotlib.pyplot as plt
import link  # Ensure this module is correctly imported and accessible

from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify, trame, matplotlib

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

DEFAULT_FIG_SIZE = (6.4, 4.8)  # Adjusted figure size
DEFAULT_DPI = 100
DEFAULT_NUM_POINTS = 100
DEFAULT_NPART = 100

state.setdefault("num_points", DEFAULT_NUM_POINTS)
state.setdefault("npart", DEFAULT_NPART)
state.setdefault("figure_size", None)  # Ensure figure_size is initialized

def figure_size():
    if not state.figure_size:
        return {
            "figsize": DEFAULT_FIG_SIZE,
            "dpi": DEFAULT_DPI,
        }

    dpi = state.figure_size.get("dpi", DEFAULT_DPI)
    rect = state.figure_size.get("size", {})
    if 'width' not in rect or 'height' not in rect:
        return {
            "figsize": DEFAULT_FIG_SIZE,
            "dpi": dpi,
        }

    w_inch = rect["width"] / dpi
    h_inch = rect["height"] / dpi

    return {
        "figsize": (w_inch, h_inch),
        "dpi": dpi,
    }

def create_figure():
    plt.close("all")
    fig = link.run_simulation(npart=state.npart)
    return fig

# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------

@state.change("figure_size", "num_points", "npart")
def update_chart(npart, **kwargs):
    ctrl.update_figure(create_figure())
    print(f"npart being changed to {npart}")

# -----------------------------------------------------------------------------
# UI Classes
# -----------------------------------------------------------------------------

class Toolbar:
    @staticmethod
    def toolbar():
        vuetify.VSpacer()
        vuetify.VSlider(v_model=("num_points", DEFAULT_NUM_POINTS), min=10, max=1000, step=10, label="Number of Points")
        vuetify.VSlider(v_model=("npart", DEFAULT_NPART), min=100, max=10000, step=100, label="Number of Particles")

class runSimulation:
    def __init__(self, server, state, ctrl):
        self.server = server
        self.state = state
        self.ctrl = ctrl
        

    def selectionCard(self):
        with vuetify.VCard(classes="ma-2"):
            with vuetify.VCardTitle(classes="d-flex justify-space-between align-center"):
                vuetify.VIcon("mdi-information")
                vuetify.VSpacer()
                vuetify.VBtn(
                    "Run Simulation",
                    style="background-color: #00313C; color: white;",
                    # click=self.display_simulation
                )

    def simulationPlot(self):
        with vuetify.VContainer(fluid=True, classes="fill-height pa-0 ma-0"):
            with trame.SizeObserver("figure_size"):
                html_figure = matplotlib.Figure()
                self.ctrl.update_figure = html_figure.update

# -----------------------------------------------------------------------------
# Layout Setup
# -----------------------------------------------------------------------------

runSimulation = runSimulation(server, state, ctrl)

with SinglePageLayout(server) as layout:
    layout.title.set_text("Interactive Matplotlib with Trame")
    with layout.toolbar:
        Toolbar.toolbar()

    with layout.content:
        with vuetify.VContainer(fluid=True):
            with vuetify.VRow(no_gutters=True):
                with vuetify.VCol(cols="auto", classes="pa-2"):
                    runSimulation.selectionCard()
                with vuetify.VCol(cols="auto", classes="pa-2"):
                    runSimulation.simulationPlot()

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
