# -*- coding: utf-8 -*-

import ctypes
import numpy as np
import numpy.ctypeslib as ctl

from .estimator import Estimator
from .context import Context


class MultiEmitterEstimator(Estimator):
    def __init__(self, ctx, inst, psf:Estimator):
        super().__init__(ctx, inst)
        
        self.psf = psf
        K_psf = self.psf.numparams-1
        self.numEmitters = self.numparams//K_psf
        
    def GetEmitterParams(self, fullParams, emitterIndex):
        """
        Extracts the parameters for a single emitter from the full parameter matrix/vector
        """
        K_psf = self.psf.numparams-1
        
        r = np.zeros((*fullParams.shape[:-1], self.psf.numparams))
        r[...,-1] = fullParams[...,0]
        r[...,0:K_psf] = fullParams[...,(np.arange(K_psf)+1) + emitterIndex*K_psf]
        return r

def CreateEstimator(psf:Estimator, numEmitters, ctx:Context=None, minParam=None, maxParam=None, debugMode=False):
    """
    Create a multi-emitter estimator by creating a single estimation problem for a fixed number
    of a single-emitter estimators. Background is shared between all emitters.
    
    Parameter format if psf is a 3D estimator (x,y,z,I,bg):
        b,X0,Y0,Z0,I0,X1,Y1,Z1,I1....
    Parameter format if psf is a 2D estimator (x,y,I,bg):
        b,X0,Y0,I0,X1,Y1,I1....
        
    b is the background in photons/pixel.
    
    minParam/maxParam can be set to fix the range of each parameter. 
    If none, these are copied from the PSF parameter limits
    """
    
    if ctx is None:
        ctx = psf.ctx
    
    smlmlib = ctx.smlm.lib
        
    InstancePtrType = ctypes.c_void_p

    fn = smlmlib.MultiEmitter_CreateEstimator
    fn.argtypes = [
        InstancePtrType,
        ctypes.c_int32,
        ctl.ndpointer(np.float32, flags="aligned, c_contiguous"),  # minmax
        ctypes.c_bool,
        ctypes.c_void_p
        ]
    fn.restype = ctypes.c_void_p
    
    emitterParams = psf.numparams-1
    totalParams = emitterParams*numEmitters + 1

    if minParam is None:
        minParam = psf.ParamLimits()[0]
    if maxParam is None:
        maxParam = psf.ParamLimits()[1]

    # Copy the individual psf limits into limits for the multi-emitter parameter vector
    totalMin = np.zeros(totalParams, dtype=np.float32)
    totalMax = np.zeros(totalParams, dtype=np.float32)
    totalMin[0] = minParam[-1]   #bg
    totalMax[0] = maxParam[-1]
    
    for k in range(numEmitters):
        totalMin[ (1+np.arange(emitterParams)) + emitterParams*k] = minParam[:emitterParams]
        totalMax[ (1+np.arange(emitterParams)) + emitterParams*k] = maxParam[:emitterParams]
        
    inst = fn(psf.inst, numEmitters, np.ascontiguousarray([totalMin, totalMax]), debugMode, ctx.inst)
    
    return MultiEmitterEstimator(ctx, inst, psf)
    
