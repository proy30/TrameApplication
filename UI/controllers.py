from trame.app import get_server
from trame.widgets  import vuetify
from UI.utilities import find_classes
from impactx import distribution

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# Code
# -----------------------------------------------------------------------------

class controllers:

    def __init__ (self):
        state.selected_distribution = "Waterbag"
        self.distributions = find_classes(distribution)

    def register_callbacks(self):
        ctrl.select_distribution = self.selected_distribution


    @ctrl.add("select_distribution")
    def on_selectDistribution_click(self):
        if state.selected_distribution:
            distribution_info = None
            for distribution in self.distributions:
                if distribution['name'] == state.selected_distribution:
                    distribution_info = distribution
                    break
            if distribution_info:
                state.parameters = [param.split(':')[0] for param in distribution_info['init_params']]
    
    
