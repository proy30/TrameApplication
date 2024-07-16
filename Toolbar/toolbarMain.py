
from trame.app import get_server
from trame.widgets  import vuetify
from Toolbar.exportTemplate import retrieve_state_content
# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

state.selectedWorkflow = "Optimize Triplet"
state.isSelectedWorkflow = ""
state.selectedVisualization = ""
# -----------------------------------------------------------------------------
# Trigger
# -----------------------------------------------------------------------------

@ctrl.trigger("export")
def on_export_click():
    return retrieve_state_content()

@state.change("selectedWorkflow")
def on_selectedWorkflow_change(selectedWorkflow, **kwargs):
    print(f"Selected workflow is {selectedWorkflow}")
    if selectedWorkflow == None:
        state.isSelectedWorkflow = "Please select a workflow"

# -----------------------------------------------------------------------------
# Common toolbar elements
# -----------------------------------------------------------------------------

class toolbarElements:
    
    def select_workflow():
        vuetify.VCombobox(
        placeholder="Select Workflow",
        v_model=("selectedWorkflow",),
        items=(["DataFrameTest", "Optimize Triplet"],),
        clearable=True,
        error_messages=("isSelectedWorkflow",),
        dense=True,
        hide_details=True,
        style="max-width: 175px",
        classes="mr-2",
    )
    
    def select_visualization():
        vuetify.VCombobox(
            placeholder="Select Visualization",
            v_model=("selectedVisualization",),
            items=(["Twiss Phase Space Ellipses", "Lattice Visualization"],),
            clearable=True,
            dense=True,
            hide_details=True,
            style="max-width: 250px",
        )

    def plot_options():
        vuetify.VSelect(
            v_model=("active_plot", "1D plots over s"),
            items=("plot_options",),
            label="Select plot to view",
            hide_details=True,
            dense=True,
            style="max-width: 250px",
            disabled=("disableRunSimulationButton",True),
        )

    def run_simulation_button():
        vuetify.VBtn(
            "Run Simulation",
            style="background-color: #00313C; color: white; margin: 0 20px;",
            click=ctrl.run_simulation,
            disabled=("disableRunSimulationButton",True),
        )
    
    def export_input_data():
        vuetify.VIcon(
            "mdi-download",
            style="color: #00313C; margin: 0 10px;",
            click="utils.download('input.in', trigger('export'), 'text/plain')",
            disabled=("disableRunSimulationButton",True),
        )

    def switch_theme():
        vuetify.VSwitch(
            v_model="$vuetify.theme.dark",
            hide_details=True,
        )

    def file_upload():
        vuetify.VFileInput(
            #Allows users to upload file, but nothing more than that.
            label="Upload Input File",
            clearable=True,
            chips=True,
            show_size=True,
            dense=True,
            hide_details=True,
            style="max-width: 175px;",
        )
    
# -----------------------------------------------------------------------------
# Content
# -----------------------------------------------------------------------------

class toolbars:
    
    def analyzeToolbar():
        vuetify.VSpacer()
        toolbarElements.select_workflow()
        toolbarElements.plot_options()
        toolbarElements.run_simulation_button()
        toolbarElements.export_input_data()
        toolbarElements.switch_theme()
        
    def latticeToolbar():
        toolbarElements.file_upload()
        vuetify.VSpacer()
        toolbarElements.select_workflow()
        toolbarElements.select_visualization()
        toolbarElements.run_simulation_button()
        toolbarElements.export_input_data()
        toolbarElements.switch_theme()
