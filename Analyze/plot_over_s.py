import pandas as pd
from trame.app import get_server
from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import vuetify

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

def load_data(file_path):
    df = pd.read_csv(file_path, sep=' ')
    return df

def convert_to_dict(combined_data):
    dictionary = combined_data.to_dict(orient='records')

    columns = combined_data.columns
    headers = []
    for column in columns:
        clean = column.strip()

        headers.append({"text": clean, "value": clean})

    return dictionary, headers

reducedBeam_data = load_data('/mnt/c/Users/parth/Downloads/vsCode/fixBugs/diags/reduced_beam_characteristics.0.0')
refParticle_data = load_data('/mnt/c/Users/parth/Downloads/vsCode/fixBugs/diags/ref_particle.0.0')

combined_data = pd.merge(reducedBeam_data, refParticle_data, how='outer')
data, headers = convert_to_dict(combined_data)

state.data = data
state.headers = headers

# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------
class table():
    def card():
        with vuetify.VCard():
            vuetify.VCardTitle("Table"),
            vuetify.VDataTable(
                headers=("headers",),
                items=("data",),
            )
            
# -----------------------------------------------------------------------------
# Main Layout
# -----------------------------------------------------------------------------
with SinglePageWithDrawerLayout(server) as layout:
    with layout.content:
        with vuetify.VContainer(fluid=True):
            with vuetify.VRow(no_gutters=True):
                with vuetify.VCol(cols="auto", classes="pa-2"):
                    table.card()

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    server.start()
