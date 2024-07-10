
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

INPUT_CONTENTS = """a,b,c
1,2,3
4,5,6
7,8,9
"""
state.inputFile_export = INPUT_CONTENTS


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
            "Export Inputs",
            style="margin: 0 20px; width: 150px",
            click="utils.download('input.in', inputFile_export, 'text/plain')",
        )
        vuetify.VBtn(
            "Run Simulation",
            style="background-color: #00313C; color: white; margin: 0 20px; width: 150px",
            # click=ctrl.run_simulation,
        )
        vuetify.VSwitch(
                v_model="$vuetify.theme.dark",
                hide_details=True,
            )

    