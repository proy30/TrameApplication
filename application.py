from trame.app import get_server
from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import vuetify, router
from trame.ui.router import RouterViewLayout

from simulation import run_simulation
from impactx import distribution, elements
# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

# Specify the client type as "vue2"
server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# Default values (Simulation test)
# -----------------------------------------------------------------------------

def read_file(file_name):
    file_list = []
    try:
        with open(file_name,'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    file_list.append({"text": line, "value": line})
    except FileNotFoundError:
        print(f"{file_name} file was not found")
    return file_list


state.selected_lattice = None
state.selected_lattices = []
state.lattice_dropdown_options = read_file("latticeList.txt")

def find_all_classes(module):
    class_list = []
    for classes in dir(module):
        if isinstance(getattr(module, classes), type):
            class_list.append(classes)
    return class_list

state.selected_distribution = None
state.distribution_dropdown_options = find_all_classes(distribution)
state.lattice_dropdown_options = find_all_classes(elements)


#Sections
state.expand_section = True
state.expand_section2 = True
state.expand_section3 = True

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------

def create_section(title, content, expand_section_index):
    with vuetify.VExpansionPanels(v_model=(expand_section_index,), accordion=True):
        with vuetify.VExpansionPanel():
            with vuetify.VExpansionPanelHeader():
                vuetify.VCardText(title)
            with vuetify.VExpansionPanelContent():
                vuetify.VCardText(content)

def create_slider(label_input, v_model, min_value, max_value, step_value):
    with vuetify.VCardText():
        vuetify.VSlider(
            v_model=(v_model, state),
            thumb_label=True,
            min=min_value,
            max=max_value,
            step=step_value,
            label=label_input,
        )
def create_comboBox(label_input, v_model, items):
    with vuetify.VCardText():
        vuetify.VCombobox(
                label=label_input,
                v_model=(v_model,state),
                items=(items,state),
                clearable=True,
                solo=True
            )
def create_Button(label_input, action_call_on_click):
     vuetify.VBtn(label_input, click=action_call_on_click)

def create_route(label_input, mdi_icon, click_action_name, show_route):
    to = f"/{label_input}"
    click =  f"{click_action_name} = {str(show_route).lower()}"
    with vuetify.VListItem(to=to, click=click):
        with vuetify.VListItemIcon():
            vuetify.VIcon(mdi_icon)
        with vuetify.VListItemContent():
            vuetify.VListItemTitle(label_input)


@ctrl.add("add_lattice_to_list")
def add_lattice_to_list():
    selected_lattice = state.selected_lattice
    if selected_lattice:
        state.selected_lattices = state.selected_lattices + [selected_lattice]
        state.selected_lattice = None


@state.change("selectedRoute")
def on_route_change(**kwargs):
    selected_route = kwargs.get('selectedRoute')
    if selected_route !=  "/Settings":
        state.showSettingsDrawer = False

def reset_parameters():
    state.particle_shape = 1
    state.space_charge = False
    state.slice_step_diagnostics = False
    state.npart = 10000
    state.kin_energy_MeV = 2.0e3
    state.bunch_charge_C = 1.0e-9
    state.image_data=None
# -----------------------------------------------------------------------------
# Layout
# -----------------------------------------------------------------------------
state.trame__title="impactX Visualizer"

with SinglePageWithDrawerLayout(server) as layout:
    layout.title.set_text("impactX Visualization Tool")

    with layout.drawer as drawer:
        drawer.width = 300
        router.RouterView()
        
        with vuetify.VList(shaped=True, v_model=("selectedRoute", 0)):
            vuetify.VSubheader("Directories")
            create_route("Settings","mdi-cogs","showSettingsDrawer","true")
            # create_route("Status", "mdi-list-status")

    with layout.content:
        with vuetify.VRow():
            with vuetify.VCol(cols=4):
                with vuetify.VNavigationDrawer(v_model=("showSettingsDrawer",False),width=500):
                    vuetify.VCardTitle("Settings")
                    
                    with vuetify.VCardText():
                        # create_slider("Particle Shape", "particle_shape", 1, 3, 1)
                        create_slider("[WORKS] Number of Particles", "npart", 1, 10000, 99)
                        create_slider("Kinetic Energy (MeV)", "kin_energy_MeV", 1, 4000, 99)
                        create_slider("Bunch_ Charge (C)", "bunch_charge_C", .000000001, 1, .000000001)
                        create_slider("Particle Shape", "particle_shape", 1, 3, 1)

                        with vuetify.VRow():
                            with vuetify.VCol(cols=7): create_comboBox("Select Accelerator Lattice", "selected_lattice", "lattice_dropdown_options")
                            with vuetify.VCol(cols=2): create_Button("Add", add_lattice_to_list)

                        with vuetify.VList():
                            with vuetify.VListItem(v_for="(item, index) in selected_lattices", key="index"):
                                vuetify.VListItemContent('{{ item.text }}')

                            create_comboBox("Select a Distribution", "selected_distribution", "distribution_dropdown_options")
                            with vuetify.VCol(cols=10): create_Button("Run Simulation", run_simulation)
                            
            with vuetify.VCol(cols=7):
                vuetify.VImg(v_if=("image_data",), src=("image_data",))

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
                        with vuetify.VRow():
                            vuetify.VCardTitle("Settings")
                            vuetify.VSpacer()
                            vuetify.VIcon("mdi-refresh", click=reset_parameters)    
