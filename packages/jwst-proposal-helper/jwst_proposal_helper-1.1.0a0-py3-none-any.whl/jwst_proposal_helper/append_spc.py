# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

from scipy.signal import savgol_filter
from jwst_proposal_helper.rescale_spc import rescale_spc
import numpy as np

def append_spc(in_spc,ap_spc,bound,direction='greater',do_smoothing=True,window_length=11,polyorder=1):
    """
    append_spc is a function to append a spectral profile from one dataset (ap_spc) to another (in_spc). By append, it means ap_spc would be rescaled to in_spc. The function returns values by appending rescaled ap_spc to in_spc using only the wavelength from ap_spc that is greater than in_spc.
    #####
    + Packages:
      - numpy
      - scipy.signal.savgol_filter
      - jwst_proposal_helper.rescale_spc.rescale_spc (pip install jwst_proposal_helper)
    #####
    + Inputs:
      - in_spc = a dict with key as {'wavelength','flux'} with values as 1D array for each key running parallelly. Wavelength must be sort ascending.
      - ap_spc = a dict with similar construct as in_spc.
      - bound = a tuple of (wavelength_min,wavelength_max) defining a range to be computed for rescaling factor.
      - direction = string {'greater','lesser'} specifying direction of appending. If 'greater', this will append longer wavelength of ap_spc. And vice versa for 'lesser'.
      - do_smoothing = True if scipy.signal.savgol_filter would be applied to in_spc before computing the rescaling factor.
      - window_length = odd integer as a parameter for scipy.signal.savgol_filter.
      - polyorder = integer as a parameter for scipy.signal.svagol_filter.
    #####
    + Outputs:
      - return w_out, f_out, note_out
        > w_out = 1D array of wavelength after appending
        > f_out = 1D array of flux after appending, parallel to w_out
        > note_out = 1D array of string {'in','ap'} parallel to w_out specifying which element coming from in_spc or append_spc.
    """
    ##### 1. use in_spc to compute the scale
    ########## apply smoothing if specified
    w_in,f_in = in_spc['wavelength'],in_spc['flux']
    w_ap,f_ap = ap_spc['wavelength'],ap_spc['flux']
    if do_smoothing:
        f_in = savgol_filter(f_in,window_length=window_length,polyorder=polyorder)
    _,mean_flux_in = rescale_spc(wavelength=w_in,flux=f_in,bound=bound,rescale_value=1.)
    ##### 2. use mean_flux_in as the rescale_value for append_spc
    rescale_factor_ap,_ = rescale_spc(wavelength=w_ap,flux=f_ap,bound=bound,rescale_value=mean_flux_in)
    ##### 3. append f_ap * rescale_factor_ap to in_spc
    if direction == 'greater':
        w_in_max = w_in.max()
        m = np.argwhere(w_ap > w_in_max).flatten()
        w_out = np.concatenate([w_in,w_ap[m]])
        f_out = np.concatenate([f_in,f_ap[m]*rescale_factor_ap])
        tz_in = np.full_like(w_in,'in',dtype='object')
        tz_ap = np.full_like(w_ap[m],'ap',dtype='object')
        note_out = np.concatenate([tz_in,tz_ap])
        return w_out,f_out,note_out
    if direction == 'lesser':
        w_in_min = w_in.min()
        m = np.argwhere(w_ap < w_in_min).flatten()
        w_out = np.concatenate([w_ap[m],w_in])
        f_out = np.concatenate([f_ap[m]*rescale_factor_ap,f_in])
        tz_in = np.full_like(w_in,'in',dtype='object')
        tz_ap = np.full_like(w_ap[m],'ap',dtype='object')
        note_out = np.concatenate([tz_ap,tz_in])
        return w_out,f_out,note_out
