from trame.app import get_server
from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import vuetify

from simulation import run_simulation

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

# Specify the client type as "vue2"
server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# Default values (Simulation test)
# -----------------------------------------------------------------------------

# Lattice
state.selected_lattice = None
state.selected_lattices = []
def read_lattices():
    lattices = []
    try:
        with open('latticeList.txt', 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    lattices.append({"text": line, "value": line})
    except FileNotFoundError:
        print("lattice.txt file is not found")
    return lattices

state.lattice_dropdown_options = read_lattices()

# Distributions
state.selected_distribution = None
distributions = [
    {"text": "Waterbag", "value": "Waterbag"},
    {"text": "Distribution2", "value": "Distribution2"},
    {"text": "Distribution3", "value": "Distribution3"},
    {"text": "Distribution4", "value": "Distribution4"},
]
state.distributions_dropdown_options = distributions

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

def create_slider(label_input, v_model, state, min_value, max_value, step_value):
    with vuetify.VCardText():
        vuetify.VSlider(
            v_model=(v_model, state),
            thumb_label=True,
            min=min_value,
            max=max_value,
            step=step_value,
            label=label_input,
        )


@ctrl.add("add_lattice_to_list")
def add_lattice_to_list():
    selected_lattice = state.selected_lattice
    if selected_lattice:
        state.selected_lattices = state.selected_lattices + [selected_lattice]
        state.selected_lattice = None

@state.change("npart")
def on_npart_change(npart, **kwargs):
    state.npart = npart
    print(f"npart changed to {npart}")
# -----------------------------------------------------------------------------
# Layout
# -----------------------------------------------------------------------------

with SinglePageWithDrawerLayout(server) as layout:
    layout.title.set_text("impactX Visualization Tool")

    with layout.drawer as drawer:
        drawer.width = 500
        with vuetify.VCard():
            vuetify.VCardTitle("Settings")

            # Test section
            # create_section("Section1", "Content for section 1", "expand_section")
            
            with vuetify.VCardText():

                create_slider("Number of Particles", "npart", state, 1, 10000, 99)
                # create_slider("Knetic Energy (MeV)", "kin_energy_MeV", state.kin_energy_MeV, 5,10,1)
                # create_slider("Bunch Charge C", "bunch_charge_C", state.bunch_charge_C, 5, 10, 1)

                with vuetify.VRow():
                    with vuetify.VCol(cols=7):
                        vuetify.VCombobox(
                            label="Select Accelerator Lattice",
                            v_model=("selected_lattice",state.selected_lattice),
                            items=("selected_lattice_dropdown_options",state.lattice_dropdown_options),
                            clearable=True,
                            solo=True
                        )
                    with vuetify.VCol(cols=2):
                        vuetify.VBtn(
                            "Add",
                            click=add_lattice_to_list,
                        )
                with vuetify.VList():
                    with vuetify.VListItem(v_for="(item, index) in selected_lattices", key="index"):
                        vuetify.VListItemContent('{{ item.text }}')
                
                with vuetify.VCol(cols=10):
                    vuetify.VBtn(
                        "Run Simulation",
                        click=run_simulation,
                    )
  
                # vuetify.VSelect(
                #     v_model=("selected_simulations",state.selected_simulations),
                #     items=("simulations_dropdown_options",state.simulations_dropdown_options),
                #     label="Select type of simulation",
                #     outlined=True,
                #     dense=True,
                #     style="width: 300px; background: transparent; border: none;",
                #     classes="custom-select"
                # )
               
                # vuetify.VSelect(
                #     v_model=("selected_option",state.selected_distribution),
                #     items=("dropdown_options",state.distributions_dropdown_options),
                #     label="Select a distribution",
                #     outlined=True,
                #     dense=True,
                #     style="width: 300px; background: transparent; border: none;",
                #     classes="custom-select"
                # )

    with layout.content:
        with vuetify.VContainer(
            fluid=True,
            classes="pa-0 fill-height",
        ):
            # Add your UI components here
            vuetify.VImg(v_if=("image_data",), src=("image_data",))

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
