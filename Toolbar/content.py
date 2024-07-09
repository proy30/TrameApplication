
from trame.app import get_server
from trame.widgets  import vuetify

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

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
            "Run Simulation",
            style="background-color: #00313C; color: white; margin: 0 20px;",
            # click=ctrl.run_simulation,
        )
        vuetify.VSwitch(
                v_model="$vuetify.theme.dark",
                hide_details=True,
            )

    