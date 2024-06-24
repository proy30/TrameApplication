from trame.app import get_server
from trame.widgets  import vuetify

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------
server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# Code
# -----------------------------------------------------------------------------

# class appContent:
#     def toolbar(self):
#             vuetify.VSpacer()
#             # vuetify.VBtn(
#             #     "Configure",
#             #     color="primary",
#             #     classes="mr-2"
#             # )
#             vuetify.VSwitch(
#                 v_model="$vuetify.theme.dark",
#                 hide_details=True,
#             )

# class analyzeOptions:
#     def __init__ (self):
#         pass

#     # def card(self):
#     #     with vuetify.VCard(classes="ma-2", style="max-width: 340px; height: 320px"):
#     #         with vuetify.VCardTitle("Distribution Parameters"):
#     #             vuetify.VSpacer()
#     #             vuetify.VIcon(
#     #                 "mdi-information",
#     #                 classes="ml-2",
#     #                 style="color: #00313C;"
#     #                 # color="primary",
#     #                 # click=distributionParameters.reset_parameters
#     #             )
#     #         vuetify.VDivider(classes="my-0")
#     #         with vuetify.VCardText():
#     #             vuetify.VSimpleCheckbox(
#     #                 label="Phase Space Plots",
#     #             )
#     #             vuetify.VDataTable(
                    
#     #             )



