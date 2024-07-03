from trame.app import get_server
from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import vuetify, plotly, matplotlib

from Analyze.plot_over_s.widgets import Functions
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
# -----------------------------------------------------------------------------
# Start server
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# 1D Plot
# -----------------------------------------------------------------------------

def line_plot():
    x_axis = state.selected_headers[1] if len(state.selected_headers) > 1 else None
    y_axis = state.selected_headers[2] if len(state.selected_headers) > 2 else None

    x = [row[x_axis] for row in state.filtered_data] if x_axis else []
    y = [row[y_axis] for row in state.filtered_data] if y_axis else []

    return go.Figure(
        data=go.Scatter(
            x = x,
            y = y,
            mode='lines+markers',
            line = dict(color='blue', width=2),
            marker=dict(size=8)
        ),
        layout=go.Layout(
            title="Interactive 1D plot over s",
            xaxis=dict(title="s"),
            yaxis=dict(title="Y axis"),
            margin=dict(l=20, r=20, t=25, b=30)
        )
    )
    
# Phase Space Plotting
def figure_size():
    if state.figure_size is None:
        return {}

    dpi = state.figure_size.get("dpi")
    rect = state.figure_size.get("size")
    w_inch = rect.get("width") / dpi
    h_inch = rect.get("height") / dpi

    return {
        "figsize": (w_inch, h_inch),
        "dpi": dpi,
    }

def phase_space_plot():
    plt.close("all")
    fig, ax = plt.subplots(**figure_size())
    np.random.seed(0)
    ax.plot(
        np.random.normal(size=100), np.random.normal(size=100), "or", ms=10, alpha=0.3
    )
    ax.plot(
        np.random.normal(size=100), np.random.normal(size=100), "ob", ms=20, alpha=0.1
    )

    ax.set_xlabel("this is x")
    ax.set_ylabel("this is y")
    ax.set_title("Matplotlib Plot Rendered in D3!", size=14)
    ax.grid(color="lightgray", alpha=0.7)

    return fig

PLOTS = {
    "1D plots over s": line_plot,
    "Phase Space Plots": phase_space_plot,
}
# -----------------------------------------------------------------------------
# Defaults
# -----------------------------------------------------------------------------

reducedBeam_data = '/mnt/c/Users/parth/Downloads/vsCode/fixBugs/diags/reduced_beam_characteristics.0.0'
refParticle_data = '/mnt/c/Users/parth/Downloads/vsCode/fixBugs/diags/ref_particle.0.0'
default_headers = ["step", "s", "sig_x"]
state.plot_options = ["1D plots over s", "Phase Space Plots"]
state.show_table = False
state.active_plot = "1D plots over s"  

combined_files= Functions.combine_files(reducedBeam_data, refParticle_data)
combined_files_data_converted_to_dictionary_format = Functions.convert_to_dict(combined_files)

data, headers = combined_files_data_converted_to_dictionary_format
state.all_data = data
state.all_headers = headers
state.selected_headers = default_headers
state.filtered_data = []

# -----------------------------------------------------------------------------
# State changes
# -----------------------------------------------------------------------------

@state.change("selected_headers")
def on_header_selection_change(selected_headers, **kwargs):
    state.filtered_headers = Functions.filter_headers(state.all_headers, selected_headers)
    state.filtered_data = Functions.filter_data(state.all_data, selected_headers)

@state.change("filtered_data")
def on_filtered_data_change(filtered_data, **kwargs):
    ctrl.update_plot() 

@state.change("active_plot")
def on_plot_selection_change(active_plot, **kwargs):
    if active_plot == "1D plots over s":
        state.show_table = True
    else:
        state.show_table = False
    ctrl.update_plot()


def update_plot():
    if state.active_plot == "1D plots over s":
        ctrl.plotly_figure_update(line_plot())
    else:
        ctrl.matplotlib_figure_update(phase_space_plot())

ctrl.update_plot = update_plot

# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------
class Table:
    def card():
        vuetify.VSpacer()
        vuetify.VSelect(
            v_model=("active_plot","1D plots over s"),
            items=("plot_options",),
            label="Select plot to view",
            dense=True,
            style="width: 500px"
        )
        with vuetify.VCard(v_if=("show_table")):
            with vuetify.VCol(style="width: 500px;"):
                vuetify.VSelect(
                    v_model=("selected_headers",),
                    items=("all_headers",),
                    label="Select data to view",
                    multiple=True,
                )
                vuetify.VDivider()
                vuetify.VDataTable(
                    headers=("filtered_headers",),
                    items=("filtered_data",),
                    header_class="centered-header",
                    dense=True,
                    height="250px",
                )
    def plot():
        with vuetify.VContainer():
            with vuetify.VContainer(v_if="active_plot === '1D plots over s'"):
                plotly_figure = plotly.Figure(display_mode_bar="true")
                ctrl.plotly_figure_update = plotly_figure.update
            with vuetify.VContainer(v_if="active_plot === 'Phase Space Plots'"):
                matplotlib_figure = matplotlib.Figure(style="position: absolute")
                ctrl.matplotlib_figure_update = matplotlib_figure.update
