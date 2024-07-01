def adjusted_settings_plot_2nd(pc, num_bins=50, root_rank=0):
    """
    Plot the x-px phase space projection with matplotlib.

    Parameters
    ----------
    pc : ImpactXParticleContainer_*
        The particle container class in ImpactX
    num_bins : int, default=50
        The number of bins for spatial and momentum directions per plot axis.
    root_rank : int, default=0
        MPI root rank to reduce to in parallel runs.

    Returns
    -------
    A matplotlib figure containing the plot.
    For MPI-parallel ranks, the figure is only created on the root_rank.
    """
    import matplotlib.pyplot as plt
    import numpy as np
    from quantiphy import Quantity

    # Beam Characteristics
    rbc = pc.reduced_beam_characteristics()

    # update for plot unit system
    m2mm = 1.0e3
    rad2mrad = 1.0e3

    # Data Histogramming
    df = pc.to_df(local=True)

    # calculate local histograms
    if df is None:
        xpx = np.zeros((num_bins, num_bins))
        x_edges = np.linspace(rbc["x_min"] * m2mm, rbc["x_max"] * m2mm, num_bins + 1)
        px_edges = np.linspace(
            rbc["px_min"] * rad2mrad, rbc["px_max"] * rad2mrad, num_bins + 1
        )
    else:
        # update for plot unit system
        df.position_x = df.position_x.multiply(m2mm)
        df.position_y = df.position_y.multiply(m2mm)
        df.position_t = df.position_t.multiply(m2mm)
        df.momentum_x = df.momentum_x.multiply(rad2mrad)
        df.momentum_y = df.momentum_y.multiply(rad2mrad)
        df.momentum_t = df.momentum_t.multiply(rad2mrad)

        xpx, x_edges, px_edges = np.histogram2d(
            df["position_x"],
            df["momentum_x"],
            bins=num_bins,
            range=[
                [rbc["x_min"] * m2mm, rbc["x_max"] * m2mm],
                [rbc["px_min"] * rad2mrad, rbc["px_max"] * rad2mrad],
            ],
        )

    # MPI reduce
    from inspect import getmodule

    ix = getmodule(pc)
    if ix.Config.have_mpi:
        from mpi4py import MPI

        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()

        # MPI_Reduce the node-local histogram data
        combined_data = xpx
        summed_data = comm.reduce(
            combined_data,
            op=MPI.SUM,
            root=root_rank,
        )

        if rank != root_rank:
            return None

        xpx = summed_data

    # histograms per axis
    x = np.sum(xpx, axis=1)
    px = np.sum(xpx, axis=0)

    # Matplotlib canvas: figure and plottable axes areas
    fig, ax_xpx = plt.subplots(figsize=(8, 4), constrained_layout=True)

    #   projected axes
    ax_x, ax_px = ax_xpx.twinx(), ax_xpx.twiny()

    # Plotting
    def plot_2d(hist, r, p, r_edges, p_edges, ax_r, ax_p, ax_rp):
        hist = np.ma.masked_where(hist == 0, hist)
        im = ax_rp.imshow(
            hist.T,
            origin="lower",
            aspect="auto",
            extent=[r_edges[0], r_edges[-1], p_edges[0], p_edges[-1]],
        )
        cbar = fig.colorbar(im, ax=ax_rp)

        r_mids = (r_edges[:-1] + r_edges[1:]) / 2
        p_mids = (p_edges[:-1] + p_edges[1:]) / 2
        ax_r.plot(r_mids, r, c="w", lw=0.8, alpha=0.7)
        ax_r.plot(r_mids, r, c="k", lw=0.5, alpha=0.7)
        ax_r.fill_between(r_mids, r, facecolor="k", alpha=0.2)
        ax_p.plot(p, p_mids, c="w", lw=0.8, alpha=0.7)
        ax_p.plot(p, p_mids, c="k", lw=0.5, alpha=0.7)
        ax_p.fill_betweenx(p_mids, p, facecolor="k", alpha=0.2)

        return cbar

    cbar_xpx = plot_2d(xpx, x, px, x_edges, px_edges, ax_x, ax_px, ax_xpx)

    # Limits
    def set_limits(r, p, r_edges, p_edges, ax_r, ax_p, ax_rp):
        pad = 0.1
        len_r = r_edges[-1] - r_edges[0]
        len_p = p_edges[-1] - p_edges[0]
        ax_rp.set_xlim(r_edges[0] - len_r * pad, r_edges[-1] + len_r * pad)
        ax_rp.set_ylim(p_edges[0] - len_p * pad, p_edges[-1] + len_p * pad)

        # ensure zoom does not change value axis for projections
        def on_xlims_change(axes):
            if not axes.xlim_reset_in_progress:
                pad = 6.0
                axes.xlim_reset_in_progress = True
                axes.set_xlim(0, np.max(p) * pad)
                axes.xlim_reset_in_progress = False

        ax_p.xlim_reset_in_progress = False
        ax_p.callbacks.connect("xlim_changed", on_xlims_change)
        on_xlims_change(ax_p)

        def on_ylims_change(axes):
            if not axes.ylim_reset_in_progress:
                pad = 6.0
                axes.ylim_reset_in_progress = True
                axes.set_ylim(0, np.max(r) * pad)
                axes.ylim_reset_in_progress = False

        ax_r.ylim_reset_in_progress = False
        ax_r.callbacks.connect("ylim_changed", on_ylims_change)
        on_ylims_change(ax_r)

    set_limits(x, px, x_edges, px_edges, ax_x, ax_px, ax_xpx)

    # Annotations
    fig.canvas.manager.set_window_title("Phase Space")
    ax_xpx.set_xlabel(r"$\Delta x$ [mm]")
    ax_xpx.set_ylabel(r"$\Delta p_x$ [mrad]")
    cbar_xpx.set_label(r"$Q$ [C/bin]")
    ax_x.set_yticks([])
    ax_px.set_xticks([])

    leg = ax_xpx.legend(
        title=r"$\epsilon_{n,x}=$"
        f"{Quantity(rbc['emittance_x'], 'm'):.3}\n"
        rf"$\sigma_x=${Quantity(rbc['sig_x'], 'm'):.3}"
        "\n"
        rf"$\beta_x=${Quantity(rbc['beta_x'], 'm'):.3}"
        "\n"
        rf"$\alpha_x=${rbc['alpha_x']:.3g}",
        loc="upper right",
        framealpha=0.8,
        handles=[],
    )
    leg._legend_box.sep = 0

    return fig
