# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

import pandas as pd
import numpy as np

def read_spc_at2017gfo(dat_file):
    """
    read_spc_at2017gfo is a specific function to read .dat files of AT2017gfo's spectra prepared for JWST ETC.
    #####
    + Input:
      - dat_file = string as filepath
    #####
    + Outputs:
      - return phase, micron, mjy = float, 1D array, 1D array
    """
    phase = '.'.join(dat_file.split('/')[-1].split('_')[6].split('.')[0:2])
    spc = pd.read_csv(dat_file,sep=' ')
    micron = spc.micron.values
    mjy = spc.mjy.values
    return float(phase),micron,mjy
