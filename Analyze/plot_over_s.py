import pandas as pd
from trame.app import get_server
from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import vuetify

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

def load_data(file_path):
    df = pd.read_csv(file_path, sep=' ')
    dictionary = df.to_dict(orient='records')

    columns = df.columns
    list = []
    for column in columns:
        clean = column.strip()

        convert_to_dictionary = {"text": clean, "value": clean}
        list.append(convert_to_dictionary)

    return dictionary, list

data, headers = load_data('/mnt/c/Users/parth/Downloads/vsCode/fixBugs/diags/reduced_beam_characteristics.0.0')

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
