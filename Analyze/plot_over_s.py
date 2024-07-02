from trame.app import get_server
from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import vuetify, plotly

from widgets import Functions
import plotly.graph_objects as go


# -----------------------------------------------------------------------------
# Start server
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# 1D Plot
# -----------------------------------------------------------------------------

def line_plot():
    x_axis = [1,2,3,4]
    y_axis =[2,3,4,5,7,12]

    return go.Figure(
        data=go.Scatter(
            x = x_axis,
            y = y_axis,
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
    

PLOTS = {
    "Line": line_plot
}

# -----------------------------------------------------------------------------
# Defaults
# -----------------------------------------------------------------------------

reducedBeam_data = '/mnt/c/Users/parth/Downloads/vsCode/fixBugs/diags/reduced_beam_characteristics.0.0'
refParticle_data = '/mnt/c/Users/parth/Downloads/vsCode/fixBugs/diags/ref_particle.0.0'
default_headers = ["step", "s", "z"]

combined_files= Functions.combine_files(reducedBeam_data, refParticle_data)
combined_files_data_converted_to_dictionary_format = Functions.convert_to_dict(combined_files)

data, headers = combined_files_data_converted_to_dictionary_format
state.all_data = data
state.all_headers = headers
state.selected_headers = default_headers

# -----------------------------------------------------------------------------
# State changes
# -----------------------------------------------------------------------------

@state.change("selected_headers")
def on_header_selection_change(selected_headers, **kwargs):
    state.filtered_headers = Functions.filter_headers(state.all_headers, selected_headers)
    state.filtered_data = Functions.filter_data(state.all_data, selected_headers)

@state.change("filtered_data")
def on_filtered_data_change(filtered_data, **kwargs):
    ctrl.figure_update(line_plot())

@state.change("active_plot")
def on_plot_selection_change(active_plot, **kwargs):
    ctrl.figure.update(PLOTS[active_plot]())


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------
class Table:
    def card():
        with vuetify.VCard():
            with vuetify.VRow():
                vuetify.VCardTitle("Table")
                with vuetify.VCol(style="max-width: 500px;"):
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
        figure = plotly.Figure(display_mode_bar="true")
        ctrl.figure_update = figure.update
        ctrl.figure_update(line_plot())

# -----------------------------------------------------------------------------
# Main Layout
# -----------------------------------------------------------------------------
with SinglePageWithDrawerLayout(server) as layout:
    with layout.content:
        with vuetify.VContainer(fluid=True):
            with vuetify.VRow(no_gutters=True, classes="fill-height"):
                with vuetify.VCol(cols="auto", classes="pa-2 fill-height"):
                    Table.card()
                with vuetify.VCol(classes="pa-2 d-flex align-center justify-center fill-height"):
                    Table.plot()

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    server.start()