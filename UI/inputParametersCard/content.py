from trame.app import get_server
from trame.widgets  import vuetify

from UI.functions import functions
# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# Content
# -----------------------------------------------------------------------------

class inputParameters:
    def __init__ (self):
        state.particle_shape = 1
        state.npart = 10000
        state.kin_energy_MeV = 2.0e3
        state.bunch_charge_C = 1.0e-9
        state.kin_energy_unit = "MeV"

    def format_to_scientific():
        try:
            value = float(state.npart)
            state.npart = f"{value:.2e}"
        except ValueError:
            state.npart = "Invalid input"

    @state.change("particle_shape")
    def a(particle_shape, **kwargs):
        print(f"Particle Shape changed to: {particle_shape}")

    @state.change("npart")
    def on_npart_change(npart, **kwargs):
        # inputParameters.format_to_scientific()
        print(f"# of Particles changed to: {npart}")

    @state.change("kin_energy_MeV")
    def on_kin_energy_change(kin_energy_MeV, **kwargs):
        print(f"Kinetic Energy changed to: {kin_energy_MeV}")

    @state.change("bunch_charge_C")
    def on_bunch_charge_C_change(bunch_charge_C, **kwargs):
        print(f"Bunch Charge (C) changed to: {bunch_charge_C}")

    @state.change("kin_energy_unit")
    def b(kin_energy_unit, **kwargs):
        # inputParameters.convert_kin_energy()
        print(f"Kinetic Energy unit changed to: {kin_energy_unit}")

    # def convert_kin_energy():
    #     conversion_factors = {
    #         "meV": 1.0e-9,
    #         "eV": 1.0e-6,
    #         "keV": 1.0e-3,
    #         "MeV": 1.0,
    #         "GeV": 1.0e3,
    #         "TeV": 1.0e6,
    #     }
    #     state.kin_energy_MeV = float(state.kin_energy_MeV)
    #     state.kin_energy_MeV /= conversion_factors["MeV"]
    #     state.kin_energy_MeV *= conversion_factors[state.kin_energy_unit]

    def card(self):
        with vuetify.VCard(classes="ma-2", style="max-width: 340px; height: 320px"):
            with vuetify.VCardTitle("Input Parameters", classes="d-flex justify-space-between align-center"):
                vuetify.VIcon(
                    "mdi-information",
                    classes="ml-2",
                    style="color: #00313C;",
                    click=lambda: functions.documentation("pythonParameters"),
                )
            vuetify.VDivider()

            with vuetify.VCardText():
                vuetify.VSelect(
                    label="Particle Shape",
                    v_model=("particle_shape",),
                    items=([1, 2, 3],),
                    dense=True,
                    classes="mb-2"
                )
                vuetify.VTextField(
                    label="Number of Particles",
                    v_model=("npart",),
                    classes="mb-2",
                    dense=True,
                )
                with vuetify.VRow(classes="mb-2"):
                    with vuetify.VCol(cols=8):
                        vuetify.VTextField(
                            label="Kinetic Energy",
                            v_model=("kin_energy_MeV",),
                            type="number",
                            dense=True,
                            classes="mr-2",
                        )
                    with vuetify.VCol(cols=4):
                        vuetify.VSelect(
                            label="Unit",
                            v_model=("kin_energy_unit",),
                            items=(["meV", "eV", "MeV", "GeV", "TeV"],),
                            dense=True,
                        )
                vuetify.VTextField(
                    label="Bunch Charge (C)",
                    v_model=("bunch_charge_C",),
                    type="number",
                    dense=True,
                    classes="mb-2"
                )