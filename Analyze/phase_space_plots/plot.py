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

class phaseSpacePlot:
    
    def toolbar():
        vuetify.VSpacer()
        vuetify.VBtn(
            "Run Simulation",
            style="background-color: #00313C; color: white;",
        )

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

with SinglePageWithDrawerLayout(server) as layout:
    with layout.toolbar:
        phaseSpacePlot.toolbar()

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
