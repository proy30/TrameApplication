## Add any lattice specific functions here

def convert_kin_energy(old_unit, new_unit, kin_energy_MeV):
    conversion_factors = {
        "meV": 1.0e-9,
        "eV":  1.0e-6,
        "keV": 1.0e-3,
        "MeV": 1.0,
        "GeV": 1.0e3,
        "TeV": 1.0e6,
    }
    value_in_mev = kin_energy_MeV * conversion_factors[old_unit] / conversion_factors["MeV"]
    return value_in_mev * conversion_factors["MeV"] / conversion_factors[new_unit]
