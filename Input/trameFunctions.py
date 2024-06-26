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

class trameFunctions():

    def create_route(route_title, mdi_icon):
        state[route_title] = False # Does not display route by default

        to = f"/{route_title}"
        click =  f"{route_title} = true"

        with vuetify.VListItem(to=to, click=click):
            with vuetify.VListItemIcon():
                vuetify.VIcon(mdi_icon)
            with vuetify.VListItemContent():
                vuetify.VListItemTitle(route_title)
                
    def create_section(title, content, expand_section_index):
        with vuetify.VExpansionPanels(v_model=(expand_section_index,), accordion=True):
            with vuetify.VExpansionPanel():
                with vuetify.VExpansionPanelHeader():
                    vuetify.VCardText(title)
                with vuetify.VExpansionPanelContent():
                    vuetify.VCardText(content)

    def create_slider(label_input, v_model, min_value, max_value, step_value):
                vuetify.VSlider(
                    label=label_input,
                    v_model=(v_model, state),
                    thumb_label=True,
                    min=min_value,
                    max=max_value,
                    step=step_value,
                )
    def lattice_list_dialog():
        with vuetify.VDialog(v_model=("showDialog", False), width="250px"):
            with vuetify.VCard():
                vuetify.VCardTitle("Input Parameters")
                vuetify.VDivider()
                with vuetify.VContainer(fluid=True):
                    with vuetify.VRow(no_gutters=True, v_for="(item, i) in lattice_list", key="i", classes="mb-2"):
                        with vuetify.VCol():
                            vuetify.VChip(
                                    style="width: 150px; justify-content: center",
                                    dense=True,
                                    v_text="item"
                                )