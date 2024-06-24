from trame.app import get_server
from trame.widgets  import vuetify

from Input.functions import functions
from impactx import elements
# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# Content
# -----------------------------------------------------------------------------
class latticeConfiguration:
    def __init__(self):
        state.lattice_list = []
        state.selected_lattice =  None
        state.lattice_elements = functions.find_all_classes(elements)
        # print(state.lattice_elements)
        # state.latticeParameters = {
        #     "Quad": ["ds", "k","ds", "k","ds", "k"],
        #     "Drift": ["ds"]
        # }

    def on_add_lattice_click():
        if state.selected_lattice:
            state.lattice_list = state.lattice_list + [state.selected_lattice]
            state.selected_lattice = None
            

    def on_clear_lattice_click():
        state.lattice_list = []
    
    def dialog_lattice_elementList():
        with vuetify.VCard(style="padding: 10px;"):
            vuetify.VCardTitle("Elements")
            vuetify.VDivider()
            with vuetify.VContainer(fluid=True):
                with vuetify.VRow(no_gutters=True, v_for="(item, i) in lattice_list", key="i", classes="mb-2"):
                    with vuetify.VCol():
                        vuetify.VChip(
                                style="width: 150px; justify-content: center",
                                dense=True,
                                v_text="item"
                            )

    def card(self):
        with vuetify.VDialog(v_model=("showDialog", False), width="700px"):
            latticeConfiguration.dialog_lattice_elementList()

        with vuetify.VCard(classes="ma-2", style="max-width: 712px;"):
            with vuetify.VCardTitle("Lattice Configuration", classes="d-flex justify-space-between align-center"):
                vuetify.VIcon(
                    "mdi-information",
                    classes="ml-2",
                    click=lambda: functions.documentation("LatticeElements"),
                    style="color: #00313C;",
                )
            vuetify.VDivider()
            with vuetify.VCardText():
                with vuetify.VRow(classes="mb-1 align-center", no_gutters=True):
                    with vuetify.VCol(cols=8):
                        vuetify.VSelect(
                            label="Select Accelerator Lattice",
                            items=("lattice_elements",),
                            v_model=("selected_lattice", None),
                            dense=True,
                            classes="mr-2 mt-6"
                        )
                    with vuetify.VCol(cols="auto"):
                        vuetify.VBtn(
                            "ADD",
                            classes="mr-2",
                            color="primary",
                            click=latticeConfiguration.on_add_lattice_click,
                            dense=True
                        )
                    with vuetify.VCol(cols="auto"):
                        vuetify.VBtn(
                            "CLEAR",
                            color="secondary",
                            click=latticeConfiguration.on_clear_lattice_click,
                            dense=True
                        )
                with vuetify.VRow():
                    with vuetify.VCol():       
                        with vuetify.VCard(style="height: 300px; overflow-y: auto; width: 700px; padding: 10px;"):
                            with vuetify.VCardTitle("Elements", classes="text-subtitle-2 pa-2"):
                                vuetify.VSpacer()
                                vuetify.VIcon(
                                    "mdi-arrow-expand",
                                    classes="ml-2",
                                    color="primary",
                                    click="showDialog = true",
                                )
                            vuetify.VDivider()
                            with vuetify.VContainer(fluid=True):
                                    with vuetify.VRow(no_gutters=True, v_for="(item, i) in lattice_list", key="i", classes="mb-2", align_center=True):
                                        with vuetify.VCol(cols="auto"):
                                            vuetify.VChip(
                                                style="width: 150px; justify-content: center",
                                                dense=True,
                                                v_text="item"
                                            )
                          

                    # with vuetify.VCol(): 
                    #     with vuetify.VCard(style="height: 220px; overflow-y: auto; width: 400px; padding: 10px;"):
                    #         with vuetify.VCardTitle("Values", classes="text-subtitle-2 pa-2"):
                    #             vuetify.VSpacer()
                    #             vuetify.VIcon(
                    #                 "mdi-arrow-expand",
                    #                 classes="ml-2",
                    #                 color="primary",
                    #                 click="showVa = true",
                    #             )
                    #         vuetify.VDivider()
                    #         with vuetify.VContainer(fluid=True):
                    #             with vuetify.VRow(no_gutters=True, v_for="(item, i) in lattice_list", key="i", classes="mb-2"):
                    #                 with vuetify.VCol():
                    #                     vuetify.VChip(
                    #                             style="width: 150px; justify-content: center",
                    #                             dense=True,
                    #                             v_text="item"
                    #                         )