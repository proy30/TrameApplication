#!/usr/bin/env python3
#
# Copyright 2022-2023 The ImpactX Community
#
# Authors: Axel Huebl
# License: BSD-3-Clause-LBNL
#
# -*- coding: utf-8 -*-

import importlib

import matplotlib.pyplot as plt
import pytest

from impactx import ImpactX, amr, distribution, elements

# -----------------------------------------------------------------------------
# New Code - Parthib
# -----------------------------------------------------------------------------
from trame.app import get_server
import base64, io
from mpi4py import MPI

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# Default values
# -----------------------------------------------------------------------------
state.particle_shape = 1
state.space_charge = False
state.slice_step_diagnostics = False
state.npart = 10000
state.kin_energy_MeV = 2.0e3
state.bunch_charge_C = 1.0e-9
state.image_data=None

# Functions
# -----------------------------------------------------------------------------

def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

# -----------------------------------------------------------------------------
# Simulation code (variables now reference state and figure is not converted to base64)
# -----------------------------------------------------------------------------
@pytest.mark.skipif(
    importlib.util.find_spec("pandas") is None, reason="pandas is not available"
)
def run_impactX_simulation(save_png=True):
    """
    This tests using ImpactX and Pandas Dataframes
    """
    sim = ImpactX()

    sim.particle_shape = state.particle_shape
    sim.space_charge = state.space_charge
    sim.slice_step_diagnostics = state.slice_step_diagnostics
    sim.init_grids()
    npart  = int(state.npart)

    # init particle beam
    kin_energy_MeV = int(state.kin_energy_MeV)
    bunch_charge_C = int(state.bunch_charge_C)

    #   reference particle
    pc = sim.particle_container()
    ref = pc.ref_particle()
    ref.set_charge_qe(-1.0).set_mass_MeV(0.510998950).set_kin_energy_MeV(kin_energy_MeV)

    #   particle bunch
    distr = distribution.Waterbag(
        lambdaX=3.9984884770e-5,
        lambdaY=3.9984884770e-5,
        lambdaT=1.0e-3,
        lambdaPx=2.6623538760e-5,
        lambdaPy=2.6623538760e-5,
        lambdaPt=2.0e-3,
        muxpx=-0.846574929020762,
        muypy=0.846574929020762,
        mutpt=0.0,
    )
    sim.add_particles(bunch_charge_C, distr, npart)

    assert pc.total_number_of_particles() == npart

    # init accelerator lattice
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

    # compare number of global particles
    # FIXME
    # df = pc.to_df(local=False)
    # if df is not None:
    #    assert npart == len(df)
    #    assert df.columns.tolist() == ['idcpu', 'position_x', 'position_y', 'position_t', 'momentum_x', 'momentum_y', 'momentum_t', 'qm', 'weighting']

    # plot
    fig = pc.plot_phasespace()

    #   note: figure data available on MPI rank zero
    if fig is not None:
        # fig.savefig("phase_space.png")
        image_base64 = fig_to_base64(fig)
        state.image_data =  f"data:image/png;base64, {image_base64}"
        # if save_png:
        #     fig.savefig("phase_space.png")
        # else:
        #     plt.show()

    # finalize simulation
    sim.finalize()
    # return fig


if __name__ == "__main__":
    test_df_pandas(save_png=False)

    # clean simulation shutdown
    amr.finalize()