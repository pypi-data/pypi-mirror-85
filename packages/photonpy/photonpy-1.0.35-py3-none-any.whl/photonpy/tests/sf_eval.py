# To run this first do
# pip install photonpy=1.0.24

import numpy as np
import matplotlib.pyplot as plt

import photonpy.smlm.util as su
from photonpy import Context, GaussianPSFMethods

from photonpy.cpp.simflux import SIMFLUX

mod = np.array([
    # kx,ky,kz, depth, phase, relative intensity
    [0, 1.8, 0,  0.95, 0, 1/6],
    [1.9, 0, 0,0.95, 0, 1/6],
    [0, 1.8, 0,  0.95, 2*np.pi/3, 1/6],
    [1.9, 0, 0,0.95, 2*np.pi/3, 1/6],
    [0, 1.8,0,   0.95, 4*np.pi/3, 1/6],
    [1.9, 0, 0,0.95, 4*np.pi/3, 1/6]
])

with Context() as ctx:
    sigma=1.5
    roisize=10
    n = 10000
    # Create an array with bunch of different emitter positions
    theta = [[roisize//2, roisize//2, 1000, 1.0]]
    theta = np.repeat(theta,n,0)
    theta[:,:2] += np.random.uniform(-2,2,size=(n,2))
    
    # Create some variation in modulation pattern
    mod_per_spot = np.repeat([mod],n,0)
    mod_per_spot[:, 4] += np.random.uniform(0,0.02, size=(n,6)) # add some random phase jitter
    
        
    # Create a uniform-illumination 2D Gaussian PSF:
    #psf = g.CreatePSF_XYIBg(roisize, sigma, True)
    
    sf_psf = SIMFLUX(ctx).CreateEstimator_Gauss2D(sigma, len(mod), roisize, len(mod), True)
    
    print(f"Expected value...")
    ev = sf_psf.ExpectedValue(theta,constants=mod_per_spot)
    print(f"CRLB...")
    crlb = sf_psf.CRLBAndChiSquare(theta,constants=mod_per_spot)
    print(f"FI...")
    fi = sf_psf.FisherMatrix(theta,constants=mod_per_spot)
    print(f"Simflux CRLB: {crlb}")
    smp = np.random.poisson(ev)
    su.imshow_hstack(smp[0])

    print(f"Derivatives...")
    deriv, mu = sf_psf.Derivatives(theta,constants=mod_per_spot)
    for k in range(deriv.shape[1]):
         plt.figure()
         su.imshow_hstack(deriv[0,k])
         plt.title(f"Simflux psf derivative {sf_psf.colnames[k]}")
    
