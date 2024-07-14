import warnings

# Ignore mpld3 warning
warnings.filterwarnings("ignore", message="Blended transforms not yet supported. Zoom behavior may not work as expected.", category=UserWarning, module="mpld3.mplexporter.exporter")

from trame.app import get_server
from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import vuetify, matplotlib

import matplotlib.pyplot as plt
import numpy as np

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# Defaults
# -----------------------------------------------------------------------------
state.alpha_x = 1
state.beta_x = 1
state.epsilon_x = 1

@state.change("alpha_x", "beta_x", "epsilon_x")
def on_params_change(**kwargs):
    temporaryClass.update_plot()

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------

class temporaryClass:
    def draw_phase_space_ellipse(alpha, beta, epsilon, n_points=100):
        """
        Draw a phase space ellipse using Twiss parameters and beam emittance.

        Parameters:
        alpha (float): Twiss parameter alpha
        beta (float): Twiss parameter beta
        epsilon (float): Beam emittance
        n_points (int): Number of points used to draw the ellipse
        """
        # Calculate gamma from alpha and beta
        gamma = (1 + alpha**2) / beta

        # Covariance matrix
        sigma = epsilon * np.array([[beta, -alpha], [-alpha, gamma]])

        # Eigenvalues and eigenvectors
        eigvals, eigvecs = np.linalg.eigh(sigma)

        # Semi-major and semi-minor axes
        a = np.sqrt(eigvals[1])
        b = np.sqrt(eigvals[0])

        # Rotation angle
        theta = np.arctan2(eigvecs[1, 1], eigvecs[0, 1])

        # Generate points for the ellipse
        t = np.linspace(0, 2 * np.pi, n_points)
        cos_t = np.cos(t)
        sin_t = np.sin(t)

        # Generate the ellipse points before rotation
        q0 = a * cos_t
        p0 = b * sin_t

        # Apply the rotation
        q = q0 * np.cos(theta) - p0 * np.sin(theta)
        p = q0 * np.sin(theta) + p0 * np.cos(theta)

        # Create the plot with a smaller size
        fig, ax = plt.subplots(figsize=(3.25, 2.25)) 
        ax.plot(q, p, label=f'ε={epsilon}, α={alpha}, β={beta}', linestyle='-', marker='o')
        ax.set_xlabel('Position (q)')
        ax.set_ylabel('Momentum (p)')
        legend = ax.legend(loc='upper right')
        legend.get_frame().set_facecolor('lightgray') 
        legend.get_frame().set_alpha(0.8)
        legend.get_frame().set_edgecolor('black')
        legend.get_frame().set_linewidth(1.5)
        ax.grid(True)
        ax.axis('equal')

        # Fix axis limits
        # ax.set_xlim([-10, 10])
        # ax.set_ylim([-10, 10])

        fig.subplots_adjust(left=0.2, bottom=0.2, right=.97, top=.95)

        return fig

    def update_plot(**kwargs):
        alpha = state.alpha_x
        beta = state.beta_x
        epsilon = state.epsilon_x
        fig = temporaryClass.draw_phase_space_ellipse(alpha, beta, epsilon)
        ctrl.matplotlib_figure_update(fig)
        plt.close(fig)

    def card():
        with vuetify.VCard(style="width: 340px; height: 300px"):
            with vuetify.VCardText():
                with vuetify.VRow(classes="pl-1"):
                    vuetify.VIcon("mdi-chart-arc")
                    vuetify.VCardTitle("Phase Space Ellipse w/Twiss Parameters", classes="text-subtitle-2", style="color: black;")
            vuetify.VDivider()
            matplotlib_figure = matplotlib.Figure()
            ctrl.matplotlib_figure_update = matplotlib_figure.update
        # with vuetify.VContainer():
        #     with vuetify.VRow():
        #         with vuetify.VCol(cols="4"):
        #             vuetify.VSlider(v_model=("alpha_x",), min=-2, max=2, step=0.1, label="Alpha x", hide_details=True)
        #         with vuetify.VCol(cols="4"):
        #             vuetify.VSlider(v_model=("beta_x",), min=0.1, max=5, step=0.1, label="Beta x", hide_details=True)
        #         with vuetify.VCol(cols="4"):
        #             vuetify.VSlider(v_model=("epsilon_x",), min=0.1, max=5, step=0.1, label="Epsilon x", hide_details=True)

# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------

# @state.change("alpha_x", "beta_x", "epsilon_x")
# def on_params_change(**kwargs):
#     temporaryClass.update_plot()

# -----------------------------------------------------------------------------
# Layout
# -----------------------------------------------------------------------------

# with SinglePageWithDrawerLayout(server) as layout:
    # with layout.content:
        # temporaryClass.card()
        # with vuetify.VContainer():
        #     with vuetify.VCard(style="width: 360px; height: 310px"):
        #         with vuetify.VCardText(classes="pt-0 pb-1"):
        #             with vuetify.VRow(classes="pl-1"):
        #                 vuetify.VIcon("mdi-chart-arc")
        #                 vuetify.VCardTitle("Phase Space Ellipse w/Twiss Parameters", classes="text-subtitle-2", style="color: black;")
        #         vuetify.VDivider()
        #         matplotlib_figure = matplotlib.Figure()
        #         ctrl.matplotlib_figure_update = matplotlib_figure.update

# -----------------------------------------------------------------------------
# Startup
# -----------------------------------------------------------------------------

# if __name__ == "__main__":
#     server.start()
