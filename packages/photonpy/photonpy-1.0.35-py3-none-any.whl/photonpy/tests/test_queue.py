# -*- coding: utf-8 -*-

from photonpy import GaussianPSFMethods, Context, EstimQueue

import numpy as np
import matplotlib.pyplot as plt

with Context(debugMode=True) as ctx:
    np.random.seed(0)
    sigma = 2
    roisize=10
    
    psf = GaussianPSFMethods(ctx).CreatePSF_XYIBg(roisize, sigma, cuda=True)
    
    n=20
    params= np.repeat( [[roisize/2,roisize/2,500,50]], n, 0)
    smp = psf.GenerateSample(params)
    #plt.figure()
    #plt.imshow(smp[0])
    estim = psf.Estimate(smp)[0]
    chisq = psf.ChiSquare(estim, smp)
    mu = psf.ExpectedValue(estim)
    
    chisq2 = np.sum( (smp-mu)**2/mu,(1,2))
    print(f"numpy eval: {chisq2}")
    
    print(f"psf.ChiSq: {chisq}")
    
    with EstimQueue(psf,batchSize=10) as q:
        q.Schedule(smp,ids=np.arange(n))
        q.Flush()
        q.WaitUntilDone()
        qr = q.GetResults()
        qr.SortByID()
        print(f"Queue eval: {qr.chisq}")
        