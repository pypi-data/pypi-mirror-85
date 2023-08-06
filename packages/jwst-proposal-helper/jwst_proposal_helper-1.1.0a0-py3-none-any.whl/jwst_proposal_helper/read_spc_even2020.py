# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

import pandas as pd
import numpy as np

def read_spc_even2020(dat_file):
    """
    read_spc_even2020 is a specific function to read .dat files of Even et al. 2020's spectra of KN with Lanthanide, prepared for JWST ETC.
    #####
    + Input:
      - dat_file = string as filepath
    #####
    + Outputs:
      - return mass_fraction, phase, micron, mjy = float, float, 1D array, 1D array
    """
    mass_fraction = dat_file.split('/')[-1].split('_')[2]
    if mass_fraction == 'unscaled':
        mass_fraction = 0.032
    else:
        base,sign,power = float(mass_fraction[1]),mass_fraction[3],float(mass_fraction[4:])
        if sign=='p':
            mass_fraction = base * np.power(10.,power)
        elif sign=='m':
            mass_fraction = base * np.power(10.,-power)
    phase = dat_file.split('/')[-1].split('_')[-1].split('d.dat')[0]
    spc = pd.read_csv(dat_file,sep=' ')
    micron = spc.microns.values
    mjy = spc.mJy.values
    return mass_fraction,float(phase),micron,mjy
