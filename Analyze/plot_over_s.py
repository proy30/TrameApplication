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

combined_data = Functions.combine_files(reducedBeam_data, refParticle_data)
dictionary_data = Functions.convert_to_dict(combined_data)
data, headers = dictionary_data

state.data = data
state.headers = headers

default_columns = ["step", "s"]
state.selected_columns = default_columns
state.all_columns = [header['value'] for header in headers]

@state.change("selected_columns")
def update_table(selected_columns, **kwargs):
    state.data = Functions.filter_data_by_columns(data, selected_columns)
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
                        v_model=("selected_columns",),
                        items=("all_columns",),
                        label="Select data to view",
                        multiple=True,
                    )
            vuetify.VDivider()
            vuetify.VDataTable(
                headers=("headers",),
                items=("data",),
                header_class="centered-header"
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
