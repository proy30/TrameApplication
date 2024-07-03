from trame.app import get_server
from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import vuetify, plotly, matplotlib

from Analyze.widgets import Functions

from Analyze.plot_phase_space.phaseSpace import run_simulation
from Analyze.plot_over_s.overS import line_plot
# -----------------------------------------------------------------------------
# Start server
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# Plotting
# -----------------------------------------------------------------------------

# Call plot_over_s
def plot_over_s():
    fig = line_plot(state.selected_headers, state.filtered_data)
    ctrl.plotly_figure_update(fig)

# Matplotlib features
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

PLOTS = {
    "1D plots over s": plot_over_s,
    "Phase Space Plots": run_simulation,
}

# -----------------------------------------------------------------------------
# Defaults
# -----------------------------------------------------------------------------

reducedBeam_data = '/mnt/c/Users/parth/Downloads/vsCode/fixBugs/diags/reduced_beam_characteristics.0.0'
refParticle_data = '/mnt/c/Users/parth/Downloads/vsCode/fixBugs/diags/ref_particle.0.0'
default_headers = ["step", "s", "sig_x"]
state.plot_options = list(PLOTS.keys())
state.show_table = False

firstPlotOption = state.plot_options[0]
state.active_plot = firstPlotOption

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

@ctrl.add("update_plot")
def update_plot():
    if state.active_plot == "1D plots over s":
        ctrl.plotly_figure_update(plot_over_s())
    else:
        ctrl.matplotlib_figure_update(run_simulation())

ctrl.update_plot = update_plot

# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------
class Table:
    def card():
        vuetify.VSpacer()
        with vuetify.VRow():
            with vuetify.VCol():
                vuetify.VSelect(
                    v_model=("active_plot","1D plots over s"),
                    items=("plot_options",),
                    label="Select plot to view",
                    dense=True,
                    style="width: 500px"
                )
            with vuetify.VCol():
                vuetify.VBtn(
                    "Run Simulation",
                    style="background-color: #00313C; color: white;",
                )
        with vuetify.VRow():
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
