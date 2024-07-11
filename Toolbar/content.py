
from trame.app import get_server
from trame.widgets  import vuetify
from Toolbar.exportTemplate import retrieve_state_content
# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# Trigger
# -----------------------------------------------------------------------------

@ctrl.trigger("export")
def on_export_click():
    return retrieve_state_content()

# -----------------------------------------------------------------------------
# Content
# -----------------------------------------------------------------------------

class toolbars:
    def latticeToolbar():
        vuetify.VSpacer()
        vuetify.VFileInput(
            #Allows users to upload file, but nothing more than that.
            label="Upload Input File",
            clearable=True,
            chips=True,
            show_size=True,
            dense=True,
            hide_details=True,
            style="max-width: 300px;",
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