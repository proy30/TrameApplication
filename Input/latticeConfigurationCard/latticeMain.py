from trame.app import get_server
from trame.widgets import vuetify

from Input.generalFunctions import functions
from impactx import elements

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# Helpful
# -----------------------------------------------------------------------------

LATTICE_ELEMENTS_MODULE_NAME = elements

state.listOfLatticeElements = functions.selectClasses(LATTICE_ELEMENTS_MODULE_NAME)
state.listOfLatticeElementParametersAndDefault = functions.classAndParametersAndDefaultValueAndType(LATTICE_ELEMENTS_MODULE_NAME)

# -----------------------------------------------------------------------------
# Default
# -----------------------------------------------------------------------------
state.selectedLattice = None #  Selected lattice is Empty by default
state.selectedLatticeList = [] # Selected lattice list is Empty by default

# state.listOfLatticeElementParametersAndDefault = {'Alignment': [], 'Aperture': [('xmax', None), ('ymax', None), ('shape', "'rectangular'"), ('dx', '0'), ('dy', '0'), ('rotation', '0')], 
#                                             'BeamMonitor': [('name', None), ('backend', "'default'"), ('encoding', "'g'")],
#                                             'Buncher': [('V', None), ('k', None), ('dx', '0'), ('dy', '0'), ('rotation', '0')],
#                                             'CFbend': [('ds', None), ('rc', None), ('k', None), ('dx', '0'), ('dy', '0'), ('rotation', '0'), ('nslice', '1')]
#                                             }  

# -----------------------------------------------------------------------------
# Main Functions
# -----------------------------------------------------------------------------

def add_lattice_element():
    selectedLattice = state.selectedLattice
    selectedLatticeParameters = state.listOfLatticeElementParametersAndDefault.get(selectedLattice, [])

    selectedLatticeElement = {
        "name": selectedLattice,
        "parameters": [
            {"parameter_name": parameter[0], 
             "parameter_default_value": parameter[1], 
             "parameter_type": parameter[2], 
             "parameter_error_message": []
            }
            for parameter in selectedLatticeParameters
        ]
    }

    state.selectedLatticeParaameters = selectedLatticeElement["parameters"]
    state.selectedLatticeList.append(selectedLatticeElement)
    return selectedLatticeElement
 
def update_latticeElement_parameters(index, parameterName, parameterValue, parameterErrorMessage):
    """
    Updates parameter value
    """
    for param in state.selectedLatticeList[index]["parameters"]:
        if param["parameter_name"] == parameterName:
            param["parameter_default_value"] = parameterValue
            param["parameter_error_message"] = parameterErrorMessage


    state.dirty("selectedLatticeList")
    print(state.selectedLatticeList)
    save_elements_to_file()
# -----------------------------------------------------------------------------
# Write to file functions
# -----------------------------------------------------------------------------

def save_elements_to_file():
    with open("output_latticeElements_parameters.txt", "w") as file:
        file.write("latticeElements = [\n")
        for element in state.selectedLatticeList:
            element_name = element["name"]
            parameters = ", ".join(
                f"{param['parameter_default_value']}" for param in element["parameters"]
            )
            file.write(f"    elements.{element_name}({parameters}),\n")
        file.write("]\n")   

# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------

@state.change("selectedLattice")
def on_lattice_element_name_change(selectedLattice, **kwargs):
    return
    # print (f"Lattice Selection Changed to: {selectedLattice}")

@ctrl.add("add_latticeElement")
def on_add_lattice_element_click():
    selectedLattice = state.selectedLattice
    if selectedLattice:
        add_lattice_element()
        save_elements_to_file()
        state.dirty("selectedLatticeList")
        # print(f"ADD button clicked, added: {selectedLattice}")
        # print(f"Current list of selected lattice elements: {state.selectedLatticeList}")

@ctrl.add("updateLatticeElementParameters")
def on_lattice_element_parameter_change(index, parameter_name, parameter_value, parameter_type):
    parameter_value, input_type = functions.determine_input_type(parameter_value)
    error_message = functions.validate_against(parameter_value, parameter_type)

    update_latticeElement_parameters(index, parameter_name, parameter_value, error_message)
    print(f"Lattice element {index}, {parameter_name} changed to {parameter_value} (type: {input_type})")


@ctrl.add("clear_latticeElements")
def on_clear_lattice_element_click():
    state.selectedLatticeList = []
    save_elements_to_file()

@ctrl.add("deleteLatticeElement")
def on_delete_LatticeElement_click(index):
    state.selectedLatticeList.pop(index)
    state.dirty("selectedLatticeList")
    save_elements_to_file()

# -----------------------------------------------------------------------------
# ContentSetup
# -----------------------------------------------------------------------------

class latticeConfiguration:
    def card(self):
        with vuetify.VDialog(v_model=("showDialog", False), width="1200px"):
            latticeConfiguration.dialog_lattice_elementList()
            
        with vuetify.VCard(style="width: 696px;"):
            with vuetify.VCardTitle("Lattice Configuration"):
                vuetify.VSpacer()
                vuetify.VIcon(
                    "mdi-information",
                    classes="ml-2",
                    click=lambda: functions.documentation("LatticeElements"),
                    style="color: #00313C;",
                )
            vuetify.VDivider()
            with vuetify.VCardText():
                with vuetify.VRow(align="center", no_gutters=True):
                    with vuetify.VCol(cols=8):
                        vuetify.VCombobox(
                            label="Select Accelerator Lattice",
                            v_model=("selectedLattice", None),
                            items=("listOfLatticeElements",),
                            dense=True,
                            classes="mr-2 pt-6"
                        )
                    with vuetify.VCol(cols="auto"):
                        vuetify.VBtn(
                            "ADD",
                            color="primary",
                            dense=True,
                            classes="mr-2",
                            click=ctrl.add_latticeElement,
                        )
                    with vuetify.VCol(cols="auto"):
                        vuetify.VBtn(
                            "CLEAR",
                            color="secondary",
                            dense=True,
                            click=ctrl.clear_latticeElements,
                        )
                with vuetify.VRow():
                    with vuetify.VCol():       
                        with vuetify.VCard(style="height: 300px; width: 700px; overflow-y: auto;"):
                            with vuetify.VCardTitle("Elements", classes="text-subtitle-2 pa-3"):
                                vuetify.VSpacer()
                                vuetify.VIcon(
                                    "mdi-arrow-expand",
                                    color="primary",
                                    click="showDialog = true",
                                )
                            vuetify.VDivider()
                            with vuetify.VContainer(fluid=True):
                                with vuetify.VRow(v_for="(latticeElement, index) in selectedLatticeList", align="center", no_gutters=True, style="min-width: 1500px;"):
                                    with vuetify.VCol(cols="auto", classes="pa-2"):
                                        vuetify.VIcon(
                                            "mdi-delete",
                                            click=(ctrl.deleteLatticeElement,"[index]"),
                                        )
                                        vuetify.VChip(
                                            v_text=("latticeElement.name",),
                                            dense=True,
                                            classes="mr-2",
                                            style="justify-content: center"
                                        )
                                    with vuetify.VCol(v_for="(parameter, parameterIndex) in latticeElement.parameters", cols="auto", classes="pa-2"):
                                        vuetify.VTextField(
                                            label=("parameter.parameter_name",),
                                            v_model=("parameter.parameter_default_value",),
                                            change=(ctrl.updateLatticeElementParameters, "[index, parameter.parameter_name, $event, parameter.parameter_type]"),
                                            error_messages=("parameter.parameter_error_message",),
                                            dense=True,
                                            style="width: 75px;"
                                        )


    def dialog_lattice_elementList():
        with vuetify.VCard():
            with vuetify.VCardTitle("Elements", classes="text-subtitle-2 pa-3"):
                vuetify.VSpacer()
            vuetify.VDivider()
            with vuetify.VContainer(fluid=True):
                with vuetify.VRow(v_for="(latticeElement, index) in selectedLatticeList", align="center", no_gutters=True, style="min-width: 1500px;"):
                    with vuetify.VCol(cols="auto", classes="pa-2"):
                        vuetify.VIcon(
                            "mdi-delete",
                            click=(ctrl.deleteLatticeElement,"[index]"),
                        )
                        vuetify.VChip(
                            v_text=("latticeElement.name",),
                            dense=True,
                            classes="mr-2",
                            style="justify-content: center"
                        )
                    with vuetify.VCol(v_for="(parameter, parameterIndex) in latticeElement.parameters", cols="auto", classes="pa-2"):
                        vuetify.VTextField(
                            label=("parameter.parameter_name",),
                            v_model=("parameter.parameter_default_value",),
                            change=(ctrl.updateLatticeElementParameters, "[index, parameter.parameter_name, $event, parameter.parameter_type]"),
                            error_messages=("parameter.parameter_error_message",),
                            dense=True,
                            style="width: 75px;"
                        )
