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

# -----------------------------------------------------------------------------
# Retrieve necessary default values (distirbutions, lattices)
# -----------------------------------------------------------------------------
def find_all_classes(module):
    class_list = []
    for classes in dir(module):
        if isinstance(getattr(module, classes), type):
            class_list.append(classes)
    return class_list
    # return [cls for cls in dir(module) if isinstance(getattr(module, cls), type)]



state.selected_lattice = None
state.selected_distribution = None
state.lattice_dropdown_options = find_all_classes(elements)
state.distribution_dropdown_options = find_all_classes(distribution)

state.selected_lattices = []

#Sections
state.expand_section = True

#Drawer statices
state.showSettingsDrawer = False
state.showStatusDrawer = False

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
                solo=True
            )
def create_checkbox(label_input, v_model):
        vuetify.VCheckbox(
                label=label_input,
                v_model=(v_model,state),
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
    layout.title.set_text("🚀 impactX Visualization Tool")

    with layout.drawer as drawer:
        drawer.width = 200
        router.RouterView()
    
        with vuetify.VList():
            vuetify.VSubheader("Directories")
            create_route("Settings","mdi-cogs","showSettingsDrawer")
            create_route("Status", "mdi-list-status","showStatusDrawer")

    with layout.content:
            with vuetify.VRow():
                with vuetify.VCol(cols=4):
                    with vuetify.VNavigationDrawer(v_model=("showSettingsDrawer"),width=500):
                        with vuetify.VCardText():
                            with vuetify.VRow():
                                vuetify.VCardTitle("Settings")
                                vuetify.VSpacer()
                                vuetify.VIcon("mdi-refresh", click=reset_parameters)    
                        
                            create_slider("Particle Shape", "particle_shape", 1, 3, 1)
                            create_slider("[WORKS] Number of Particles", "npart", 1, 10000, 99)
                            create_slider("Kinetic Energy (MeV)", "kin_energy_MeV", 1, 4000, 99)
                            create_slider("Bunch Charge (C)", "bunch_charge_C", .000000001, 1, .000000001)
                            
                            # create_slider("Particle Shape", "particle_shape", 1, 3, 1)
                            with vuetify.VCardText():
                                with vuetify.VRow(justify="center"):
                                    vuetify.VCol(cols="auto")
                                    create_checkbox("Space charge","space_charge")
                                    vuetify.VCol(cols="auto")
                                    create_checkbox("Slice Step Diagnostics","slice_step_diagnostics")
                                with vuetify.VRow():
                                    with vuetify.VCol(cols=7): 
                                        create_comboBox("Select Accelerator Lattice", "selected_lattice", "lattice_dropdown_options")
                                    with vuetify.VCol(cols=2): 
                                        create_Button("Add", add_lattice_to_list)
                                    with vuetify.VCol(cols=2): 
                                        create_Button("Clear",clear_lattices)
                                with vuetify.VRow():
                                        with vuetify.VListItem(v_for="(item, index) in selected_lattices", key="index"):
                                            vuetify.VListItemContent('{{ item }}')
                                            with vuetify.VCol(cols=4):  # Adjust column width as needed
                                                vuetify.VTextField(
                                                    label="Enter value",
                                                    dense=True,
                                                    outlined=True,
                                            )
                                with vuetify.VRow():
                                    create_comboBox("Select a Distribution", "selected_distribution", "distribution_dropdown_options")
                                with vuetify.VRow():
                                    vuetify.VSpacer()
                                    create_Button("Run Simulation", run_impactX_simulation)
                    
                with vuetify.VCol(cols=8):
                    with vuetify.VContainer():
                        with vuetify.VCard(elevation=2):
                                vuetify.VImg(v_if=("image_data",), src=("image_data",))
                                        # with trame.SizeObserver("figure_size"):
                                        #     html_figure = matplotlib.Figure(style="position: absolute",v_if="show_plot")
                                        #     ctrl.update_figure = html_figure.update


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
