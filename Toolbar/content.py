
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
    def toolbar():
        vuetify.VSpacer()
        vuetify.VBtn(
            "Run Simulation",
            style="background-color: #00313C; color: white; margin: 0 20px;",
            # click=ctrl.run_simulation,
        )
        vuetify.VSwitch(
                v_model="$vuetify.theme.dark",
                hide_details=True,
            )
    def analyzeToolbar():
            vuetify.VSpacer()
            vuetify.VSelect(
                # v_model=("active_plot", "1D plots over s"),
                # items=("plot_options",),
                label="Select plot to view",
                hide_details=True,
                dense=True,
                style="width: 100px;"
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

    