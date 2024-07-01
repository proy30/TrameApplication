import numpy as np
import plotly.graph_objects as go

from trame.app import get_server
from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import vuetify, plotly

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

DEFAULT_NUM_POINTS = 100
state.setdefault("num_points", DEFAULT_NUM_POINTS)

def generate_fodo_data(num_points):
    length_f = 1.0  # Length of focusing quadrupole
    length_d = 1.0  # Length of defocusing quadrupole
    length_o = 2.0  # Length of drift space

    segment_length = length_f + length_o + length_d + length_o
    t = np.linspace(0, num_points * segment_length, num_points)
    x, y, z = np.zeros(num_points), np.zeros(num_points), t

    for i in range(num_points):
        segment = (i % 4)
        if segment == 0:  # Focusing section
            x[i] = np.sin(i * np.pi / 10) * 0.1
            y[i] = np.cos(i * np.pi / 10) * 0.1
        elif segment == 1 or segment == 3:  # Drift sections
            x[i] = x[i - 1]
            y[i] = y[i - 1]
        elif segment == 2:  # Defocusing section
            x[i] = np.sin(i * np.pi / 10) * -0.1
            y[i] = np.cos(i * np.pi / 10) * -0.1

    return x, y, z

def create_plotly_figure(num_points):
    x, y, z = generate_fodo_data(num_points)
    fig = go.Figure()

    # Add FODO lattice trace
    fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines', name='FODO Lattice'))

    return fig

# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------

@state.change("num_points")
def update_chart(num_points, **kwargs):
    fig = create_plotly_figure(num_points)
    ctrl.update_figure(fig)
    print(f"Number of points changed to {num_points}")

# -----------------------------------------------------------------------------
# UI Classes
# -----------------------------------------------------------------------------

class Toolbar:
    @staticmethod
    def toolbar():
        vuetify.VSpacer()
        vuetify.VSlider(
            v_model=("num_points", DEFAULT_NUM_POINTS), 
            min=10, 
            max=1000, 
            step=10, 
            label="Number of Points"
        )

class UI:
    def __init__(self, server, state, ctrl):
        self.server = server
        self.state = state
        self.ctrl = ctrl

    def card(self):
        with vuetify.VContainer(fluid=True, classes="fill-height pa-0 ma-0"):
            plot_figure = plotly.Figure(
                figure=create_plotly_figure(state.num_points), display=True
            )
            self.ctrl.update_figure = plot_figure.update

# -----------------------------------------------------------------------------
# Layout Setup
# -----------------------------------------------------------------------------

ui = UI(server, state, ctrl)

with SinglePageWithDrawerLayout(server) as layout:
    layout.title.set_text("Interactive Plotly with Trame")
    with layout.toolbar:
        Toolbar.toolbar()

    with layout.content:
        ui.card()

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
