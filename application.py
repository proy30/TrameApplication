from trame.app import get_server
from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import vuetify, router
from trame.ui.router import RouterViewLayout

from simulation import run_impactX_simulation
from impactx import distribution, elements

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

@ctrl.add("add_lattice_to_list")
def on_add_lattice_click():
    if state.selected_lattice:
        state.selected_lattices = state.selected_lattices + [state.selected_lattice]
        state.selected_lattice = None

@ctrl.add("clear_lattices")
def on_clear_lattice_click():
    state.selected_lattices = []

#Drawer statices
state.showInputDrawer = False
state.showRunDrawer = False
state.showAnalyzeDrawer = False

state.selected_lattice = None
state.selected_distribution = None
state.lattice_dropdown_options = find_all_classes(elements)
state.distribution_dropdown_options = find_all_classes(distribution)

state.selected_lattices = []

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
                create_comboBox("Select Accelerator Lattice", "selected_lattice", "lattice_dropdown_options")
                vuetify.VCol(cols="auto")
                create_Button("Add", on_add_lattice_click)
                vuetify.VCol(cols="auto")
                create_Button("Clear",on_clear_lattice_click)
            with vuetify.VRow():
                vuetify.VCol(cols=1)
                # for item,index in selected_lattices:
                #     print {{ item}}
                #     vuetify.VTextField(
                #         placeholder="0.5",
                #         style="width: 25px;"
                #     )
            with vuetify.VRow():
                vuetify.VCol(cols=1)
                create_comboBox("Select a Distribution", "selected_distribution", "distribution_dropdown_options")
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
