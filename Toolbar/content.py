
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
class toolbar:
    def toolbar(self):
            vuetify.VSpacer()
            vuetify.VSwitch(
                v_model="$vuetify.theme.dark",
                hide_details=True,
            )