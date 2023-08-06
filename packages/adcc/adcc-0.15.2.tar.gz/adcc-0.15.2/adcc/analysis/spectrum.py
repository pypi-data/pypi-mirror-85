import numpy as np
import matplotlib.pyplot as plt


def plot_spectrum(energies, strengths):
    energies = np.array(energies).flatten()
    strengths = np.array(strengths).flatten()

    def ngauss(en, osc, x, w):
        """A normalised Gaussian"""
        fac = osc / np.sqrt(2 * np.pi * w**2)
        return fac * np.exp((x - en)**2 / (2 * w**2))

    xval = np.arange(np.min(np.min(energies) - 1, 0),
                     np.max(energies) + 1, 0.01)
    yval = np.zeros(xval.size)
    for exc in zip(energies, strengths):
        yval += ngauss(exc[0], exc[1], xval, 0.045)
    plt.plot(xval, yval)
