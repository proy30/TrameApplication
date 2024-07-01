from trame.app import get_server
from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import vuetify

from widgets import Functions


# -----------------------------------------------------------------------------
# Start server
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# Defaults
# -----------------------------------------------------------------------------

reducedBeam_data = '/mnt/c/Users/parth/Downloads/vsCode/fixBugs/diags/reduced_beam_characteristics.0.0'
refParticle_data = '/mnt/c/Users/parth/Downloads/vsCode/fixBugs/diags/ref_particle.0.0'
default_headers = ["step", "s", "z"]

combined_files= Functions.combine_files(reducedBeam_data, refParticle_data)
combined_files_data_converted_to_dictionary_format = Functions.convert_to_dict(combined_files)


data, headers = combined_files_data_converted_to_dictionary_format
state.all_data = data
state.all_headers = headers
state.selected_headers = default_headers

@state.change("selected_headers")
def on_header_selection_change(selected_headers, **kwargs):
    state.filtered_headers = Functions.filter_headers(state.all_headers, selected_headers)
    state.filtered_data = Functions.filter_data(state.all_data, selected_headers)

# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------
class Table:
    def card():
        with vuetify.VCard():
            with vuetify.VRow():
                vuetify.VCardTitle("Table")
                with vuetify.VCol(style="max-width: 500px;"):
                    vuetify.VSelect(
                        v_model=("selected_headers",),
                        items=("all_headers",),
                        label="Select data to view",
                        multiple=True,
                    )
            vuetify.VDivider()
            vuetify.VDataTable(
                headers=("filtered_headers",),
                items=("filtered_data",),
                header_class="centered-header",
                dense=True
            )

# -----------------------------------------------------------------------------
# Main Layout
# -----------------------------------------------------------------------------
with SinglePageWithDrawerLayout(server) as layout:
    with layout.content:
        with vuetify.VContainer(fluid=True):
            with vuetify.VRow(no_gutters=True):
                with vuetify.VCol(cols="auto", classes="pa-2"):
                    Table.card()

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    server.start()