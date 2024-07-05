#!/usr/bin/env python3
#
# Copyright 2022-2023 The ImpactX Community
#
# Authors: Axel Huebl
# License: BSD-3-Clause-LBNL
#
# -*- coding: utf-8 -*-

from trame.app import get_server


server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller


import importlib

import matplotlib.pyplot as plt
import pytest

from impactx import ImpactX, amr, distribution, elements
from Analyze.plot_phase_space.phaseSpaceSettings import adjusted_settings_plot

from mpi4py import MPI

import os

###
distribution_parameters_file_path = "output_distribution_parameters.txt"

def read_elements_from_file(file_path):
    elements_list = []
    with open(file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith("elements."):
                element_code = line.replace("elements.", "").rstrip(",")
                elements_list.append(eval(f"elements.{element_code}"))
    return elements_list

def load_distribution_from_file(file_path):
    # Define a safe environment for exec
    safe_env = {
        "distribution": distribution,
        "distr": None
    }

    with open(file_path, "r") as file:
        exec(file.read(), safe_env)
    
    return safe_env["distr"]
###

@pytest.mark.skipif(
    importlib.util.find_spec("pandas") is None, reason="pandas is not available"
)
def run_simulation(save_png=True):
    """
    This tests using ImpactX and Pandas Dataframes
    """
    sim = ImpactX()

    sim.particle_shape = 2
    sim.space_charge = False
    sim.slice_step_diagnostics = False
    sim.init_grids()

    # init particle beam
    kin_energy_MeV = 2.0e3
    bunch_charge_C = 1.0e-9
    npart = state.npart

    #   reference particle
    pc = sim.particle_container()
    ref = pc.ref_particle()
    ref.set_charge_qe(-1.0).set_mass_MeV(0.510998950).set_kin_energy_MeV(kin_energy_MeV)

    #   particle bunch
    # distr = distribution.Waterbag(
    #     lambdaX=3.9984884770e-5,
    #     lambdaY=3.9984884770e-5,
    #     lambdaT=1.0e-3,
    #     lambdaPx=2.6623538760e-5,
    #     lambdaPy=2.6623538760e-5,
    #     lambdaPt=2.0e-3,
    #     muxpx=-0.846574929020762,
    #     muypy=0.846574929020762,
    #     mutpt=0.0,
    # )
    distr = load_distribution_from_file(distribution_parameters_file_path)
    sim.add_particles(bunch_charge_C, distr, npart)

    assert pc.total_number_of_particles() == npart

    # init accelerator lattice
    # fodo = [
    #     elements.Drift(0.25),
    #     elements.Quad(1.0, 1.0),
    #     elements.Drift(0.5),
    #     elements.Quad(1.0, -1.0),
    #     elements.Drift(0.25),
    # ]
    file_path = "output_latticeElements_parameters.txt"
    if os.path.exists(file_path):
        fodo = read_elements_from_file(file_path)
    else:
        fodo = [
            elements.Drift(0.25),
            elements.Quad(1.0, 1.0),
            elements.Drift(0.5),
            elements.Quad(1.0, -1.0),
            elements.Drift(0.25),
        ]

    sim.lattice.extend(fodo)

    # simulate
    sim.evolve()

    # check local particles
    df = pc.to_df(local=True)
    print(df)

    # ensure the column heads are correctly labeled
    assert df.columns.tolist() == [
        "idcpu",
        "position_x",
        "position_y",
        "position_t",
        "momentum_x",
        "momentum_y",
        "momentum_t",
        "qm",
        "weighting",
    ]

    # fig = pc.plot_phasespace()
    fig = adjusted_settings_plot(pc)

    return fig