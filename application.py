from trame.app import get_server
from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import vuetify, router
from trame.ui.router import RouterViewLayout

from simulation import run_impactX_simulation
from impactx import distribution, elements
import json

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# Retrieve necessary default values (distirbutions, lattices)
# -----------------------------------------------------------------------------
def reset_parameters():
    state.particle_shape = 1
    state.npart = 10000
    state.kin_energy_MeV = 2.0e3
    state.bunch_charge_C = 1.0e-9
    state.image_data = None
    state.slice_step_diagnostics = False   
    state.space_charge = False

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------
def find_all_classes(module):
    class_list = []
    for classes in dir(module):
        if isinstance(getattr(module, classes), type):
            class_list.append(classes)
    return class_list
# return [cls for cls in dir(module) if isinstance(getattr(module, cls), type)]

def create_section(title, content, expand_section_index):
    with vuetify.VExpansionPanels(v_model=(expand_section_index,), accordion=True):
        with vuetify.VExpansionPanel():
            with vuetify.VExpansionPanelHeader():
                vuetify.VCardText(title)
            with vuetify.VExpansionPanelContent():
                vuetify.VCardText(content)
# create_section("Section1", "Content for section 1", "expand_section")

def create_slider(label_input, v_model, min_value, max_value, step_value):
            vuetify.VSlider(
                label=label_input,
                v_model=(v_model, state),
                thumb_label=True,
                min=min_value,
                max=max_value,
                step=step_value,
            )
def create_comboBox(label_input, v_model, items):
        vuetify.VCombobox(
                label=label_input,
                v_model=(v_model,state),
                items=(items,state),
                clearable=True,
                solo=True,
            )
def create_checkbox(label_input, v_model):
        vuetify.VCheckbox(
                label=label_input,
                v_model=(v_model,state),
                style="padding: 0; margin: 0;",
            )
def create_Button(label_input, action_call_on_click):
     vuetify.VBtn(label_input, click=action_call_on_click)

def create_route(label_input, mdi_icon, click_action_name):
    to = f"/{label_input}"
    click =  f"{click_action_name} = true"
    with vuetify.VListItem(to=to, click=click):
        with vuetify.VListItemIcon():
            vuetify.VIcon(mdi_icon)
        with vuetify.VListItemContent():
            vuetify.VListItemTitle(label_input)

def on_add_lattice_click():
    if state.selected_lattice:
        state.lattice_list = state.lattice_list + [state.selected_lattice]
        state.selected_lattice = None

def on_clear_lattice_click():
    state.lattice_list = []

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------
state.parameters = []
state.parameter_values = {}  # Initialize an empty dictionary for parameter values

def load_distributions_from_file(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Load distributions from output.txt
distributions_data = load_distributions_from_file('output.txt')


@ctrl.add("on_selectDistribution_click")
def selected_distribution(*args):
    if state.selected_distribution:
        for dist in distributions_data:
            if dist['name'] == state.selected_distribution:
                state.parameters = [param.split(':')[0] for param in dist['init_params']]
                state.parameter_values = {param: None for param in state.parameters}  # Reset parameter values
                break
@ctrl.add("on_clearParameters_click")
def reset_distribution_values(*args):
    state.parameters = []

#Drawer statices
state.showInputDrawer = False
state.showRunDrawer = False
state.showAnalyzeDrawer = False

state.selected_lattice = None
state.selected_distribution = None
state.lattice_dropdown_options = find_all_classes(elements)
state.distribution_dropdown_options = find_all_classes(distribution)

state.lattice_list = []

#Sections
state.expand_section = True
# -----------------------------------------------------------------------------
# Content
# -----------------------------------------------------------------------------
with RouterViewLayout(server, "/Input"):
    with vuetify.VRow():
        with vuetify.VCol(cols=4.5):
            
            with vuetify.VRow():
                    vuetify.VCardTitle("Inputs", class_="pa-0")
                    vuetify.VSpacer()
                    vuetify.VIcon("mdi-refresh", click=reset_parameters)

            with vuetify.VRow():
                vuetify.VCol(cols=1)
                vuetify.VSelect(
                    label="Particle Shape",
                    items=("Options",["1","2","3"]),
                )

            with vuetify.VRow():
                vuetify.VCol(cols=1)
                vuetify.VTextField(
                        label="Number of Particles",
                        v_model=("npart",state),
                        underlined = True,
                        type="number",
                )
            with vuetify.VRow():
                vuetify.VCol(cols=1)
                vuetify.VTextField(
                    label="Kinetic Energy",
                    v_model=("kin_energy_MeV","kin_energy_MeV"),
                    underlined = True,
                    clearable=True,
                )
                vuetify.VCol(cols="auto")
                vuetify.VSelect(
                    compact=True,
                    items=("Units",["eV","meV","MeV","GeV","TeV"]),
                    placeholder="MeV",
                    style="width: 25px;"
                )
            with vuetify.VRow():
                vuetify.VCol(cols=1)
                vuetify.VTextField(
                    label="Bunch Charge (C)",
                    v_model=("bunch_charge_C","bunch_charge_C"),
                    underlined = True,
                    clearable=True,
                    type="number",
                )
                        
            with vuetify.VRow(justify="center",style="padding: 0; margin: 0;"):
                with vuetify.VCol(cols="auto"):
                    create_checkbox("Space charge", "space_charge")
                with vuetify.VCol(cols="auto"):
                    create_checkbox("Slice Step Diagnostics", "slice_step_diagnostics")

            with vuetify.VRow():
                vuetify.VCol(cols=1)
                with vuetify.VCol(cols="auto", style="margin-right: 8px; width: 250px; height: 40px"):
                    vuetify.VCombobox(
                        label="Select Accelerator Lattice",
                        items=("lattice_dropdown_options", state),
                        v_model=("selected_lattice", state),
                        clearable=True,
                        solo=True,
                        dense=True,
                    )
                with vuetify.VCol(cols="auto", style="display: flex; align-items: center; margin-right: 8px"):
                    vuetify.VBtn(
                        "ADD",
                        click=on_add_lattice_click,
                        style="padding: 10px;"
                    )
                with vuetify.VCol(cols="auto", style="display: flex; align-items: center"):
                    vuetify.VBtn(
                        "CLEAR",
                        click=on_clear_lattice_click,
                        style="padding: 10px;"
                    )
            with vuetify.VRow():
                vuetify.VCol(cols=1)
                with vuetify.VList():
                    with vuetify.VListItem(v_for="(item, i) in lattice_list", key="i", v_bind="item"):
                        vuetify.VListItemContent("{{ item }}", style="padding-left: 5px; margin: 5px; border: 1px solid black; width: 175px;")
                        with vuetify.VCol(cols="auto",style="display: flex; align-items: center"):
                            vuetify.VIcon("mdi-plus", style="margin-right: 5px; cursor: pointer;")
                            vuetify.VIcon("mdi-delete", style="cursor: pointer;")
            with vuetify.VRow(no_gutters=True):
                vuetify.VCol(cols=1)
                with vuetify.VCol(cols="auto", style="margin-right: 8px; width: 250px; height: 40px"):
                    vuetify.VCombobox(
                        label="Select Distribution",
                        v_model=("selected_distribution",),
                        items=("distribution_dropdown_options",),
                        clearable=True,
                        solo=True,
                        dense=True,
                        color="primary",
                    )
                with vuetify.VCol(cols="auto", style="display: flex; align-items: center; margin-right: 8px"):
                    vuetify.VBtn(
                        "SELECT",
                        click=ctrl.on_select_click,
                        style="padding: 5px;"
                    )
                with vuetify.VCol(cols="auto", style="display: flex; align-items: center"):
                    vuetify.VBtn(
                        "CLEAR",
                        click=ctrl.on_clearParameters_click,
                        style="padding: 10px;"
                    )
            with vuetify.VRow():
                vuetify.VCol(cols=1)
                with vuetify.VList(): 
                    with vuetify.VListItem(v_for="(item, i) in parameters", key="i", style=""):
                        with vuetify.VListItemContent(style="padding: 0;  margin: 0"):
                            with vuetify.VRow():
                                vuetify.VCol(cols=1)
                                with vuetify.VCol(cols=13):
                                    vuetify.VListItemTitle("{{item}}", style="padding: 0; margin: 5px")
                                with vuetify.VCol(style="padding: 5px; margin:0"):
                                    vuetify.VTextField(
                                        label="Value",
                                        type="number",
                                        style="width: 100px; margin:0; padding:0px",
                                    )
            with vuetify.VRow():
                vuetify.VSpacer()
                create_Button("Run Simulation", run_impactX_simulation)
        
        with vuetify.VCol(cols=7):
            with vuetify.VContainer():
                with vuetify.VCard(elevation=2):
                    vuetify.VTextField(label="Hello")
            #             vuetify.VImg(v_if=("image_data",), src=("image_data",))

with RouterViewLayout(server, "/Run"):
    with vuetify.VContainer():
        with vuetify.VCard(elevation=2):
                vuetify.VImg(v_if=("image_data",), src=("image_data",))
# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------
state.trame__title="impactX Visualizer"
with SinglePageWithDrawerLayout(server) as layout:
    layout.title.set_text("🚀 impactX Visualization Tool")

    with layout.toolbar as toolbar:
        vuetify.VSpacer()
        vuetify.VSwitch(
            v_model="$vuetify.theme.dark",
            hide_details=True,
        )

    with layout.drawer as drawer:
        drawer.width = 200
        # with vuetify.VList():
            # vuetify.VSubheader("Simulation")
        create_route("Input","mdi-file-edit","showInputDrawer")
        create_route("Run", "mdi-play","showRunDrawer")
        create_route("Analyze", "mdi-chart-box-multiple","showAnalyzeDrawer")


    with layout.content:
        router.RouterView()

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
