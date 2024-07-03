from trame.app import get_server
from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import vuetify

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# UI Classes
# -----------------------------------------------------------------------------

class plots:
    
    def phaseSpacePlots():
        with vuetify.VContainer():
            vuetify.VSpacer()
            vuetify.VBtn(
                "Run Simulation",
                style="background-color: #00313C; color: white;",
            )
