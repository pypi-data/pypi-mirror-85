# -*- coding: utf-8 -*-

import ctypes
import numpy as np
import numpy.ctypeslib as ctl

from photonpy.cpp.estimator import Estimator
from photonpy.cpp.context import Context


def CreateEstimator(psf:Estimator, offsets, ctx:Context=None):
    """
    Create a multiplane PSF from a 3D PSF with parameters (x,y,z,I,bg).
    offsets: xyz offsets. If just one-dimensional, the values are interpreted as Z-shifts
    """
    
    offsets = np.ascontiguousarray(offsets,dtype=np.float32)

    if len(offsets.shape) == 1:
        offsets_ = np.zeros((len(offsets),3),dtype=np.float32)
        offsets_[:,2] = offsets
        offsets = offsets_
    
    if ctx is None:
        ctx = psf.ctx
    
    smlmlib = ctx.smlm.lib

    InstancePtrType = ctypes.c_void_p

    fn = smlmlib.MultiplaneEstimator_Create
    fn.argtypes = [
        ctypes.c_int32,
        ctl.ndpointer(np.float32, flags="aligned, c_contiguous"),  # offsets
        InstancePtrType,
        ctypes.c_void_p
        ]
    fn.restype = ctypes.c_void_p
    
    inst = fn(len(offsets), offsets, psf.inst, ctx.inst)
   
    return Estimator(ctx, inst)


    
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    from photonpy.cpp.gaussian import Gauss3D_Calibration, Gaussian
    from photonpy.smlm.util import imshow_hstack

    calib = Gauss3D_Calibration()
    
    with Context() as ctx:
        sigma=1.5
        roisize=12
        theta = np.array([[roisize//2, roisize//2, 0.5, 10000, 5]])
        g_api = Gaussian(ctx)
        psf = g_api.CreatePSF_XYZIBg(roisize, calib, True)
        
        mp_psf = CreateEstimator(psf, np.linspace(-5,5,5))
    
        imgs = mp_psf.ExpectedValue(theta)
        
        sample = np.random.poisson(imgs)
        
        theta_ = theta*1
        theta_[0,2]=0
    
        # Run localization on the sample
        estimated,diag,traces = mp_psf.Estimate(sample, initial=theta_)
        print(f"Estimated position: {estimated[0]}")
        
        imshow_hstack(sample[0])
