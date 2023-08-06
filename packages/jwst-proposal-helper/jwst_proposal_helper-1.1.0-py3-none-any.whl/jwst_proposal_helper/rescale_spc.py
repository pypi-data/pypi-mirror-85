# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

import numpy as np
import pandas as pd

def rescale_spc(wavelength,flux,bound,rescale_value=1.):
    """
    rescale_spc is a function to rescale a spectrum. Given a spectrum (wavelength,flux), the function will compute a mean (wavelength,flux) given the bound. And, rescale the spectrum by setting the mean flux to the rescale_value by using a multiplicative factor: rescale_flux = flux * rescale_factor.
    #####
    + Inputs:
      - wavelength = 1D array of wavelength (any unit). Must be sorted.
      - flux = 1D array of flux, parallel to wavelength (any unit)
      - bound = a tuple of two wavelength elements (bound_min_wavelength, bound_max_wavelength). The function rescales using values within the bound (inclusive for both sides)
        > after subsetting wavelength with bound, at least two elements of wavelengths must be contained within.
      - rescale_value = a scalar to rescale the spectrum to. Given rescale_value, the function computes rescale_factor = rescale_value / mean_flux. And, rescale_flux = flux * rescale_factor.
    #####
    + Outputs:
      - returns rescale_factor, mean_flux = scalar, scalar
        > rescale_factor = rescale_value / mean_flux
        > mean_flux = np.sum(flux_bound * weigth_bound) / np.sum(weigth_bound)
    #####
    + Computation:
      - We compute weighted average. The weights used are the bin size of the spectrum, i.e., weigth = np.diff(wavelength).
      - Since weigth has one less element compared to wavelength, we concatenate weigth with zero as for the last element will get zero weight. Therefore, at least two elements must be included after subsetting with bound.
    """
    m = np.argwhere((wavelength >= bound[0])&(wavelength <= bound[1])).flatten()
    wavelength_bound = wavelength[m]
    flux_bound = flux[m]
    wavelength_bound_diff = np.abs(np.diff(wavelength_bound))
    weight_bound = np.concatenate([wavelength_bound_diff,np.array([0.])])
    mean_flux = np.sum(flux_bound * weight_bound) / np.sum(weight_bound)
    rescale_factor = rescale_value / mean_flux
    return rescale_factor, mean_flux   
