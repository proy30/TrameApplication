
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
# Content
# -----------------------------------------------------------------------------

class toolbars:
    def latticeToolbar():
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
        vuetify.VSpacer()
        vuetify.VCombobox(
            placeholder="Select Workflow",
            v_model=("selectedWorkflow",),
            items=(["DataFrameTest", "Optimize Triplet"],),
            clearable=True,
            error_messages=("isSelectedWorkflow",),
            dense=True,
            hide_details=True,
            style="max-width: 175px",
        )
        vuetify.VBtn(
            "Export",
            style="margin: 0 10px;",
            click="utils.download('input.in', trigger('export'), 'text/plain')",
            disabled=("disableRunSimulationButton",True),
        )
        vuetify.VBtn(
            "Run Simulation",
            style="background-color: #00313C; color: white; margin: 0 10px;",
            click=ctrl.run_simulation,
            disabled=("disableRunSimulationButton",True),
        )
        vuetify.VSwitch(
                v_model="$vuetify.theme.dark",
                hide_details=True,
            )