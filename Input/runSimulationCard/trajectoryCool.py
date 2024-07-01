
#from trame.app import get_server
from trame.widgets import vuetify, plotly
from trame.ui.vuetify import SinglePageLayout
import pandas as pd
import plotly.express as px
from  trame.app import get_server

# Initialize server
server = get_server(client_type="vue2")
state = server.state

ref_particle_path = "/mnt/c/Users/parth/Downloads/vsCode/TrameApplication/diags/ref_particle.0.0"
reduced_beam_characteristics_path = "/mnt/c/Users/parth/Downloads/vsCode/TrameApplication/diags/reduced_beam_characteristics.0.0"

ref_particle_df = pd.read_csv(ref_particle_path)
reduced_beam_characteristics_df = pd.read_csv(reduced_beam_characteristics_path)

# Define callback for plotting
@state.change("step")
def update_plot(step, **kwargs):
    filtered_data = ref_particle_df[ref_particle_df['step'] == step]
    fig = px.scatter(filtered_data, x='x', y='y', color='beta_gamma')
    state.fig = fig

# Initialize with the first step plot
state.step = 0
update_plot(0)

# Set up UI
with SinglePageLayout(server) as layout:
    layout.title.set_text("Particle and Beam Visualization")

    with layout.content:
        with vuetify.VContainer(fluid=True):
            vuetify.VSlider(v_model=("step", 0), min=0, max=ref_particle_df['step'].max(), step=1, hide_details=True, key="step_slider")
            plotly.Figure(fig=("fig",), key="particle_plot")

# Run server
if __name__ == "__main__":
    server.start()
