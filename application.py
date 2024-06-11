from trame.app import get_server
from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import vuetify

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

# Specify the client type as "vue2"
server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller


# -----------------------------------------------------------------------------
# Default values
# -----------------------------------------------------------------------------

# Lattice
state.selected_lattice = None
state.selected_lattices = []
lattices = [
    {"text": "FODO", "value": "FODO"},
    {"text": "Chicane", "value": "Chicane"},
    {"text": "Cyclotron", "value": "Cyclotron"},
    {"text": "Quadrupole", "value": "Quadrupole"},
    {"text": "Solenoid", "value": "Solenoid"},
    {"text": "...", "value": "..."},
]
state.lattice_dropdown_options = lattices

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

# def create_slider(label_input, v_model, state, min_value, max_value, step_value):
#     with vuetify.VCardText():
#         vuetify.VSlider(
#             v_model=(v_model, state),
#             thumb_label=True,
#             min=min_value,
#             max=max_value,
#             step=step_value,
#             label=label_input,
#         )


@ctrl.add("add_lattice_to_list")
def add_lattice_to_list():
    selected_lattice = state.selected_lattice
    if selected_lattice:
        state.selected_lattices = state.selected_lattices + [selected_lattice]
        state.selected_lattice = None
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
                vuetify.VSlider(
                    v_model=("kin_energy_MeV", state.kin_energy_MeV),
                    thumb_label=True,
                    min=500,
                    max=5000,
                    step=100,
                    label="Kinetic Energy (MeV)",
                )
                
                vuetify.VSlider(
                    v_model=("bunch_charge_C", state.bunch_charge_C),
                    thumb_label=True,
                    min=500,
                    max=5000,
                    step=100,
                    label="Bunch Charge C",
                )

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
                        vuetify.VListItemContent('{{ item }}')
  

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
            vuetify.VBtn("Click Me", click=ctrl.your_function_name)

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
