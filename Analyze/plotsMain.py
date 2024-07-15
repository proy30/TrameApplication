import os
from trame.app import get_server
from trame.widgets import vuetify, plotly, matplotlib

from Analyze.analyzeFunctions import analyzeFunctions
from Analyze.plot_phase_space.phaseSpace import run_simulation
from Analyze.plot_over_s.overS import line_plot
from Run.optimize_triplet.run_triplet import run_optimize_triplet

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

PLOTS = {
    "Plot Over S": plot_over_s,
    "Phase Space Plots": None,
}

def validPlotOptions(simulationClicked):
    if simulationClicked:
        return list(PLOTS.keys())
    else:
        return ["Run Simulation To See Options"]
    
# -----------------------------------------------------------------------------
# Defaults
# -----------------------------------------------------------------------------

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

reducedBeam_data = os.path.join(base_path, 'diags', 'reduced_beam_characteristics.0.0')
refParticle_data = os.path.join(base_path, 'diags', 'ref_particle.0.0')

default_headers = ["step", "s", "x_mean"]
state.plot_options = validPlotOptions(simulationClicked=False)
state.show_table = False
state.active_plot = None

combined_files= analyzeFunctions.combine_files(reducedBeam_data, refParticle_data)
combined_files_data_converted_to_dictionary_format = analyzeFunctions.convert_to_dict(combined_files)

data, headers = combined_files_data_converted_to_dictionary_format
state.all_data = data
state.all_headers = headers
state.selected_headers = default_headers
state.filtered_data = []

# -----------------------------------------------------------------------------
# Functions to update table/plot
# -----------------------------------------------------------------------------

def update_data_table():
    """
    Combines reducedBeam and refParticle files
    and updates upon column selection by user
    """
    combined_files= analyzeFunctions.combine_files(reducedBeam_data, refParticle_data)
    combined_files_data_converted_to_dictionary_format = analyzeFunctions.convert_to_dict(combined_files)
    data, headers = combined_files_data_converted_to_dictionary_format
    
    state.all_data = data
    state.all_headers = headers
    state.filtered_data = analyzeFunctions.filter_data(state.all_data, state.selected_headers)

def update_plot():
    """
    Performs actions to display correct information,
    based on the plot optin selected by the user
    """
    if state.active_plot == "Plot Over S":
        update_data_table()
        ctrl.plotly_figure_update(plot_over_s())
        state.show_table = True
    elif state.active_plot == "Phase Space Plots":
        state.show_table = False
        # ctrl.matplotlib_figure_update(state.simulation_data) 

# -----------------------------------------------------------------------------
# State changes
# -----------------------------------------------------------------------------

@state.change("selected_headers")
def on_header_selection_change(selected_headers, **kwargs):
    state.filtered_headers = analyzeFunctions.filter_headers(state.all_headers, selected_headers)
    state.filtered_data = analyzeFunctions.filter_data(state.all_data, selected_headers)
 
@state.change("filtered_data", "active_plot")
def on_filtered_data_change(**kwargs):
    update_plot() 

@ctrl.add("run_simulation")
def run_simulation_and_store():
    workflow = state.selectedWorkflow
    state.plot_options = validPlotOptions(simulationClicked=True)
    if workflow == "DataFrameTest":
        state.simulation_data = run_simulation()
        update_plot()
    elif workflow == "Optimize Triplet":
        run_optimize_triplet()

# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

class AnalyzeSimulation:
        
    def card():
        with vuetify.VContainer():
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
        with vuetify.VContainer(v_if="active_plot === 'Plot Over S'"):
            plotly_figure = plotly.Figure(display_mode_bar="true")
            ctrl.plotly_figure_update = plotly_figure.update
        # with vuetify.VLayout(v_if="active_plot === 'Phase Space Plots'"):
            # matplotlib_figure = matplotlib.Figure(style="position: absolute")
            # ctrl.matplotlib_figure_update = matplotlib_figure.update
