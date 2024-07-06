from trame.app import get_server
from trame.widgets  import vuetify

from Input.generalFunctions import functions
# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# Content
# -----------------------------------------------------------------------------
def format_to_scientific():
    try:
        value = float(state.npart)
        state.npart = f"{value:.2e}"
    except ValueError:
        state.npart = "Invalid input"

@state.change("particle_shape")
def on_particle_shape_change(particle_shape, **kwargs):
    print(f"Particle Shape changed to: {particle_shape}")

@state.change("npart")
def on_npart_change(npart, **kwargs):
    # inputParameters.format_to_scientific()
    state.npart_validation = functions.validate(npart, "int")
    print(f"# of Particles changed to: {npart}")

@state.change("kin_energy_MeV")
def on_kin_energy_change(kin_energy_MeV, **kwargs):
    state.kin_energy_MeV_validation = functions.validate(kin_energy_MeV, "float")
    print(f"Kinetic Energy changed to: {kin_energy_MeV}")

@state.change("bunch_charge_C")
def on_bunch_charge_C_change(bunch_charge_C, **kwargs):
    state.bunch_charge_C_validation = functions.validate(bunch_charge_C, "float")
    print(f"Bunch Charge (C) changed to: {bunch_charge_C}")

@state.change("kin_energy_unit")
def on_kin_energy_unit_change(kin_energy_unit, **kwargs):
    # inputParameters.convert_kin_energy()
    print(f"Kinetic Energy unit changed to: {kin_energy_unit}")

def convert_kin_energy():
    conversion_factors = {
        "meV": 1.0e-9,
        "eV": 1.0e-6,
        "keV": 1.0e-3,
        "MeV": 1.0,
        "GeV": 1.0e3,
        "TeV": 1.0e6,
    }
    state.kin_energy_MeV = float(state.kin_energy_MeV)
    state.kin_energy_MeV /= conversion_factors["MeV"]
    state.kin_energy_MeV *= conversion_factors[state.kin_energy_unit]

class inputParameters:
    def __init__ (self):
        state.particle_shape = 1
        state.npart = 100
        state.kin_energy_MeV = 2.0e3
        state.bunch_charge_C = 1.0e-9
        state.kin_energy_unit = "MeV"

    def card(self):
        with vuetify.VCard(style="width: 340px; height: 300px"):
            with vuetify.VCardTitle("Input Parameters"):
                vuetify.VSpacer()
                vuetify.VIcon(
                    "mdi-information",
                    style="color: #00313C;",
                    click=lambda: functions.documentation("pythonParameters"),
                )
            vuetify.VDivider()
            with vuetify.VCardText():
                vuetify.VCombobox(
                    v_model=("particle_shape",),
                    label="Particle Shape",
                    items=([1, 2, 3],),
                    dense=True,
                )
                with vuetify.VRow(classes="my-0"):
                    with vuetify.VCol(cols=12, classes="py-0"):
                        vuetify.VTextField(
                            v_model=("npart",),
                            label="Number of Particles",
                            error_messages=("npart_validation",),
                            type="number",
                            dense=True,
                        )
                with vuetify.VRow(classes="my-2"):
                    with vuetify.VCol(cols=8, classes="py-0"):
                        vuetify.VTextField(
                            v_model=("kin_energy_MeV",),
                            label="Kinetic Energy",
                            error_messages=("kin_energy_MeV_validation",),
                            type="number",
                            dense=True,
                            classes="mr-2",
                        )
                    with vuetify.VCol(cols=4, classes="py-0"):
                        vuetify.VSelect(
                            v_model=("kin_energy_unit",),
                            label="Unit",
                            items=(["meV", "eV", "MeV", "GeV", "TeV"],),
                            dense=True,
                        )
                with vuetify.VRow(classes="my-2"):
                    with vuetify.VCol(cols=8, classes="py-0"):
                        vuetify.VTextField(
                            label="Bunch Charge",
                            v_model=("bunch_charge_C",),
                            error_messages=("bunch_charge_C_validation",),
                            type="number",
                            dense=True,
                        )
                    with vuetify.VCol(cols=4, classes="py-0"):
                        vuetify.VTextField(
                            label="Unit",
                            value="C",
                            dense=True,
                            disabled=True,
                        )