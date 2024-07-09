from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
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

state.alpha = 0.5  # Twiss parameter alpha
state.beta = 2.0   # Twiss parameter beta
state.epsilon = 1.0  # Beam emittance

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------

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

    # Create the plot
    fig, ax = plt.subplots()
    ax.plot(q, p, label=f'Ellipse: ε={epsilon}, α={alpha}, β={beta}, γ={gamma}')
    ax.set_xlabel('Position (q)')
    ax.set_ylabel('Momentum (p)')
    ax.set_title('Phase Space Ellipse with Twiss Parameters')
    ax.legend()
    ax.grid(True)
    ax.axis('equal')  # Ensure the aspect ratio is equal

    # Annotate axis intercepts and ellipse extents
    intercept_q = np.sqrt(epsilon / gamma)
    intercept_p = np.sqrt(epsilon /beta)
    extent_q = np.sqrt(epsilon * beta)
    extent_p = np.sqrt(epsilon * gamma)

    ax.axvline(x=intercept_q,c='C1',ls="--",alpha=0.5)
    ax.axhline(y=intercept_p,c='C1',ls="--",alpha=0.5)
    
    ax.axvline(x=extent_q,c='C2',ls="--",alpha=0.5)
    ax.axhline(y=extent_p,c='C2',ls="--",alpha=0.5) 
    
    ax.axvline(x=0,c='k',lw=2)
    ax.axhline(y=0,c='k',lw=2)

    # Show the plot
    # plt.show()

    return fig


def update_plot(**kwargs):
    alpha = state.alpha
    beta = state.beta
    epsilon = state.epsilon
    fig = draw_phase_space_ellipse(alpha, beta, epsilon)
    ctrl.matplotlib_figure_update(fig)

# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------

@state.change("alpha", "beta", "epsilon")
def on_params_change(**kwargs):
    update_plot()

# -----------------------------------------------------------------------------
# Layout
# -----------------------------------------------------------------------------

with SinglePageLayout(server) as layout:

    with layout.content:
        with vuetify.VRow():
            with vuetify.VCol(cols="4"):
                vuetify.VSlider(v_model=("alpha", 0.5), min=-2, max=2, step=0.1, label="Alpha")
            with vuetify.VCol(cols="4"):
                vuetify.VSlider(v_model=("beta", 2.0), min=0.1, max=5, step=0.1, label="Beta")
            with vuetify.VCol(cols="4"):
                vuetify.VSlider(v_model=("epsilon", 1.0), min=0.1, max=5, step=0.1, label="Epsilon")
        with vuetify.VRow():
            matplotlib_figure = matplotlib.Figure(style="position: absolute")
            ctrl.matplotlib_figure_update = matplotlib_figure.update

# -----------------------------------------------------------------------------
# Startup
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    update_plot()
    server.start()
