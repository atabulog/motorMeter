"""
Model script for (C_d + Rd) || (L_m + R_o + C_m) || Ll
"""

#imports
import numpy as np

# List of parameter dictionaries with names, initial values,
# and min/max bounds. Set 'vary': False to hold a param constant.
PARAMS = [
	{"name": "Cd", "init":  200e-12, "vary": True, "min": 1e-12, "max": None},
	{"name": "Rd", "init":     10, "vary": True, "min": 1e-12, "max": None},
	{"name": "Lm", "init":   100e-6, "vary": True, "min": 1e-12, "max": None},
	{"name": "Ro", "init":      400, "vary": True, "min": 1e-12, "max": None},
	{"name": "Cm", "init": 20.0e-12, "vary": True, "min": 1e-12, "max": None},
	]

j = 1j

def model(w, params, **kws):
	"""
	Calculate impedance using equations here for all frequencies w.
	:param w: radian frequency array
	:param params: list of component values to apply to the model equations
	:param kws: dict of optional args (eg load, fsf, zsf)
	:return: complex impedance array corresponding to freqs w
	"""
	# Extract individual component values from params list
	Cd = params["Cd"]
	Rd = params["Rd"]
	Ro = params["Ro"]
	Cm = params["Cm"]
	Lm = params["Lm"]

	# impedances in each branch
	Zm = Ro + j*w*Lm + 1/(j*w*Cm)
	Zd = Rd + 1/(j*w*Cd)

	#total impedance equation
	return 1/(1/Zd + 1/Zm)
