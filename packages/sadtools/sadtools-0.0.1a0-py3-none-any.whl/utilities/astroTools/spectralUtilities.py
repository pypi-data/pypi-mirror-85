import numpy as np


# -------------------------------------------------------------------------
# Functions for spectroscopy
# -------------------------------------------------------------------------
def fwhm_to_std_dev(fwhm):
    return fwhm / (np.sqrt(8 * np.log(2)))


def std_dev_to_fwhm(std_dev):
    return np.sqrt(8 * np.log(2)) * std_dev


def velocities_to_wavelengths(velocities, line_centre):
    wavelengths = line_centre * ((np.array(velocities) / 2.99792458e5) + 1.)
    return wavelengths


def wavelengths_to_velocities(wavelengths, line_centre):
    velocities = ((np.array(wavelengths) / line_centre) - 1.) * 2.99792458e5
    return velocities