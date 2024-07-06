from trame.app import get_server
from trame.widgets import vuetify

import Input.runSimulationCard.simulation as simulation

import numpy as np
import matplotlib.pyplot as plt
from trame.widgets import vuetify, trame, matplotlib

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# Content
# -----------------------------------------------------------------------------
DEFAULT_FIG_SIZE = (2.4, 2.8)  # 6.4 inches by 4.8 inches
DEFAULT_DPI = 20
DEFAULT_NUM_POINTS = 100
DEFAULT_NPART = 100

state.setdefault("num_points", DEFAULT_NUM_POINTS)
state.setdefault("npart", DEFAULT_NPART)
state.setdefault("kin_energy_MeV", 2000)
state.setdefault("bunch_charge_C", 1e-9)

def figure_size():
    if not state.figure_size:
        return {
            "figsize": DEFAULT_FIG_SIZE,
            "dpi": DEFAULT_DPI,
        }

    dpi = state.figure_size.get("dpi", DEFAULT_DPI)
    rect = state.figure_size.get("size", {})
    if 'width' not in rect or 'height' not in rect:
        return {
            "figsize": DEFAULT_FIG_SIZE,
            "dpi": dpi,
        }

    w_inch = rect["width"] / dpi
    h_inch = rect["height"] / dpi

    return {
        "figsize": (w_inch, h_inch),
        "dpi": dpi,
    }

def create_figure():
    plt.close("all")
    npart_int = int(state.npart)
    kin_energy_MeV_int = int(state.kin_energy_MeV)
    bunch_charge_C_int = float(state.bunch_charge_C)
    fig = simulation.run_simulation(npart=npart_int, kin_energy_MeV=kin_energy_MeV_int, bunch_charge_C=bunch_charge_C_int)
    return fig

# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------

def validate_npart(npart):
    try:
        npart_int = int(npart)
        if npart_int < 1 or npart_int > 10000:  # Adjust bounds as needed
            state.npart_validation = "Number of particles must be between 1 and 10000."
            return False
        state.npart = npart_int
        state.npart_validation = ""
        return True
    except ValueError:
        state.npart_validation = "Invalid input for number of particles."
        return False

def validate_kin_energy(kin_energy):
    try:
        kin_energy_float = float(kin_energy)
        if kin_energy_float < 0:  # Adjust bounds as needed
            state.kin_energy_MeV_validation = "Kinetic energy must be positive."
            return False
        state.kin_energy_MeV = kin_energy_float
        state.kin_energy_MeV_validation = ""
        return True
    except ValueError:
        state.kin_energy_MeV_validation = "Invalid input for kinetic energy."
        return False

def validate_bunch_charge(bunch_charge):
    try:
        bunch_charge_float = float(bunch_charge)
        if bunch_charge_float < 0:  # Adjust bounds as needed
            state.bunch_charge_C_validation = "Bunch charge must be positive."
            return False
        state.bunch_charge_C = bunch_charge_float
        state.bunch_charge_C_validation = ""
        return True
    except ValueError:
        state.bunch_charge_C_validation = "Invalid input for bunch charge."
        return False

# @state.change("npart")
# def on_npart_change(npart, **kwargs):
#     if validate_npart(npart):
#         print(f"# of Particles changed to: {npart} (type: {type(state.npart)})")

# @state.change("kin_energy_MeV")
# def on_kin_energy_change(kin_energy_MeV, **kwargs):
#     if validate_kin_energy(kin_energy_MeV):
#         print(f"Kinetic Energy changed to: {kin_energy_MeV}")

# @state.change("bunch_charge_C")
# def on_bunch_charge_C_change(bunch_charge_C, **kwargs):
#     if validate_bunch_charge(bunch_charge_C):
#         print(f"Bunch Charge (C) changed to: {bunch_charge_C}")

# @state.change("figure_size", "num_points", "npart", "kin_energy_MeV", "bunch_charge_C")
# def update_chart(**kwargs):
#     # ctrl.update_figure(create_figure())
#     print(f"Figure updated with npart: {state.npart}, kin_energy_MeV: {state.kin_energy_MeV}, bunch_charge_C: {state.bunch_charge_C}")

# -----------------------------------------------------------------------------
# UI Classes
# -----------------------------------------------------------------------------

class runSimulation:

    def selectionCard(self):
        with vuetify.VCard(classes="ma-2", width="150px"):
            with vuetify.VCardTitle("Run", classes="d-flex justify-space-between align-center"):
                vuetify.VIcon("mdi-information")
            vuetify.VDivider()
            with vuetify.VContainer(fluid=True):
                with vuetify.VRow():
                    with vuetify.VCol():
                        vuetify.VBtn(
                            "Run Simulation",
                            style="background-color: #00313C; color: white;",
                            click=lambda: update_chart()
                        )

    # def simulationPlot(self):
    #     with vuetify.VContainer(fluid=True, classes="fill-height pa-0 ma-0", style="width: 500px"):
    #         with trame.SizeObserver("figure_size"):
    #             html_figure = matplotlib.Figure()
    #             ctrl.update_figure = html_figure.update

