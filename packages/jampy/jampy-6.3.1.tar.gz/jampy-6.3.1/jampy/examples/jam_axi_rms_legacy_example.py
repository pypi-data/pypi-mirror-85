#!/usr/bin/env python

"""
V1.0.0: Michele Cappellari, Oxford, 17 April 2018

"""

import numpy as np
import matplotlib.pyplot as plt

from jampy.legacy.jam_axi_rms import jam_axi_rms

def jam_axi_rms_example():
    """
    Usage example for jam_axi_rms.
    It takes about 1s on a 2.5 GHz computer

    """
    np.random.seed(123)
    xbin, ybin = np.random.uniform(low=[-55, -40], high=[55, 40], size=[1000, 2]).T

    inc = 60.                                                # Assumed galaxy inclination
    r = np.sqrt(xbin**2 + (ybin/np.cos(np.radians(inc)))**2) # Radius in the plane of the disk
    a = 40                                                   # Scale length in arcsec
    vr = 2000*np.sqrt(r)/(r+a)                               # Assumed velocity profile (v_c of Hernquist 1990)
    vel = vr * np.sin(np.radians(inc))*xbin/r                # Projected velocity field
    sig = 8700/(r+a)                                         # Assumed velocity dispersion profile
    rms = np.sqrt(vel**2 + sig**2)                           # Vrms field in km/s

    surf = np.array([39483., 37158., 30646., 17759., 5955.1, 1203.5, 174.36, 21.105, 2.3599, 0.25493])
    sigma = np.array([0.153, 0.515, 1.58, 4.22, 10, 22.4, 48.8, 105, 227, 525])
    qObs = np.full_like(sigma, 0.57)

    distance = 16.5   # Assume Virgo distance in Mpc (Mei et al. 2007)
    mbh = 1e8 # Black hole mass in solar masses
    beta = np.full_like(surf, 0.3)

    surf_lum = surf # Assume self-consistency
    sigma_lum = sigma
    qobs_lum = qObs
    surf_pot = surf
    sigma_pot = sigma
    qobs_pot = qObs

    sigmapsf = [0.6, 1.2]
    normpsf = [0.7, 0.3]
    pixsize = 0.8
    goodbins = r > 10  # Arbitrarily exclude the center to illustrate how to use goodbins

    # The model is similar but not identical to the adopted kinematics!
    rmsModel, ml, chi2, flux = jam_axi_rms(
        surf_lum, sigma_lum, qobs_lum, surf_pot, sigma_pot, qobs_pot,
        inc, mbh, distance, xbin, ybin, plot=True, rms=rms, sigmapsf=sigmapsf,
        normpsf=normpsf, beta=beta, pixsize=pixsize, tensor='zz', goodbins=goodbins)
    plt.pause(1)

##############################################################################

if __name__ == '__main__':

    jam_axi_rms_example()
