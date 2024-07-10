
from trame.app import get_server

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# Content
# -----------------------------------------------------------------------------

def retrieve_state_content():
    content = f"""###############################################################################
# Particle Beam(s)
###############################################################################
beam.npart = {state.npart}
beam.units = static
beam.kin_energy = {state.kin_energy_MeV}
beam.charge = {state.charge}
beam.particle = electron
beam.distribution = {state.selectedDistribution}
beam.lambdaX = {state.lambdaX} 
beam.lambdaY = {state.lambdaY} 
beam.lambdaT = {state.lambdaT} 
beam.lambdaPx = {state.lambdaPx}
beam.lambdaPy = {state.lambdaPy}
beam.lambdaPt = {state.lambdaPt}
beam.muxpx = 0.0
beam.muypy = 0.0
beam.mutpt = 0.0
""" 
    return content
