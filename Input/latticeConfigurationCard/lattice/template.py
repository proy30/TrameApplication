from trame.app import get_server
from trame.widgets  import vuetify

import utilities

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

        state.LATTICE_ELEMENTS = latticeElementsList(elements)
        state.lattice_elements = list(state.LATTICE_ELEMENTS.keys())
        state.lattice_parameters = {
            key: [(param, default) for param, default, _type in params]
            for key, params in state.LATTICE_ELEMENTS.items()
        }

        ctrl.on_add_lattice_click = latticeConfiguration.on_add_lattice_click
        ctrl.on_update_latticeParameter_change = latticeConfiguration.on_update_latticeParameter_change
    

    def on_add_lattice_click():
        lattice_element = state.selected_lattice
        if lattice_element:
            lattice_param = state.lattice_parameters.get(lattice_element, [])
            new_item = {
                "name": lattice_element,
                "params": lattice_param,
                "values": {param: default for param, default in lattice_param}
            }
            state.lattice_list = state.lattice_list + [new_item]
            state.selected_lattice = None
                

    def on_clear_lattice_click():
        state.lattice_list = []
    
    def on_update_latticeParameter_change(item_index, param, value):
        # Find the type of the parameter
        lattice_element = state.lattice_list[item_index]['name']
        param_type = next(_type for p, d, _type in state.LATTICE_ELEMENTS[lattice_element] if p == param)
        converted_value = latticeConfiguration.validate_and_convert(value, param_type)
        if converted_value is not None:
            state.lattice_list[item_index]['values'][param] = converted_value
            print(f"Value changed for item {item_index}, param '{param}': {converted_value}")
            # write_lattice_elements_to_file()

    def validate_and_convert(value, desired_type):
        if desired_type == "int":
            return int(value)
        elif desired_type == "float":
            return float(value)
        elif desired_type == "str":
            return str(value)
        else:
            raise ValueError(f"Unsupported type: {desired_type}")
        

    def dialog_lattice_elementList():
        with vuetify.VCard(style="padding: 10px;"):
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
                    with vuetify.VRow(v_for="(latticeElement, i) in lattice_list", key="i", align="center", classes="my-2", no_gutters=True, style="min-width: 1200px;"):
                        with vuetify.VCol(cols="auto"):
                            vuetify.VChip(
                                style="width: 150px; justify-content: center; margin-right: 10px",
                                dense=True,
                                v_text=("latticeElement.name",),
                            )
                        with vuetify.VCol(v_for="(param, j) in latticeElement.params", key="j", cols="auto", style="margin-right: 10px;"):
                            vuetify.VTextField(
                                label=("param[0]",),
                                v_model=(f"latticeElement.values[param[0]]", ""),
                                change=(ctrl.on_update_latticeParameter_change, "[i, param[0], $event]"),
                                dense=True,
                                hide_details=True,
                                style="width: 70px; margin-top: 5px; margin-right: 10px;"
                        )       


    def card(self):
        with vuetify.VDialog(v_model=("showDialog", False), width="1200px"):
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
                                    with vuetify.VRow(v_for="(latticeElement, i) in lattice_list", key="i", align="center", classes="my-2", no_gutters=True, style="min-width: 1200px;"):
                                        with vuetify.VCol(cols="auto"):
                                            vuetify.VChip(
                                                style="width: 150px; justify-content: center; margin-right: 10px",
                                                dense=True,
                                                v_text=("latticeElement.name",),
                                            )
                                        with vuetify.VCol(v_for="(param, j) in latticeElement.params", key="j", cols="auto", style="margin-right: 10px;"):
                                            vuetify.VTextField(
                                                label=("param[0]",),
                                                v_model=(f"latticeElement.values[param[0]]", ""),
                                                change=(ctrl.on_update_latticeParameter_change, "[i, param[0], $event]"),
                                                dense=True,
                                                hide_details=True,
                                                style="width: 70px; margin-top: 5px; margin-right: 10px;"
                                        )                          
