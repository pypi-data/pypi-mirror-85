# JWST Proposal Helper
This package provides helpers for JWST proposal preparation. (pip install jwst_proposal_helper)

## 2020 JWST Cycle 1
- read_spc_at2017gfo is a specific function to read .dat files of AT2017gfo's spectra prepared for JWST ETC. (from jwst_proposal_helper.read_spc_at2017gfo import read_spc_at2017gfo)
- read_spc_even2020 is a specific function to read .dat files of Even et al. 2020's spectra of KN with Lanthanide, prepared for JWST ETC. (from jwst_proposal_helper.read_spc_even2020 import read_spc_even2020)
- rescale_spc is a function to rescale a spectrum. Given a spectrum (wavelength,flux), the function will compute a mean (wavelength,flux) given the bound. And, rescale the spectrum by setting the mean flux to the rescale_value by using a multiplicative factor: rescale_flux = flux * rescale_factor. (from jwst_proposal_helper.rescale_spc import rescale_spc)
