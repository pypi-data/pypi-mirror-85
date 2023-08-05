import ctypes
import numpy as np
import numpy.ctypeslib as ctl

from photonpy import Context, CSplineMethods,CSplinePSF,CSplineCalibration

class DSplineMethods:
    def __init__(self, ctx:Context):
        self.lib = ctx.smlm.lib
        self.ctx = ctx

        #void DSpline_LLWeightsGradient(Vector3f* emitterPos, const float* emitterIntensities,
    	#int emitterCount, int roisize, Int3& splineDims, 
    	#const float* weights, float* weightsGradient, float* partialWeightGradients, const float* pixels, 
        #const float* pixelBackgrounds, const float* expval, bool cuda)

        self._DSpline_LLWeightsGradient = self.lib.DSpline_LLWeightsGradient
        self._DSpline_LLWeightsGradient.argtypes = [
            ctl.ndpointer(np.float32, flags="aligned, c_contiguous"),  # pos
            ctl.ndpointer(np.float32, flags="aligned, c_contiguous"),  # intensities
            ctypes.c_int32,  # count
            ctypes.c_int32,  # roisize
            ctl.ndpointer(np.int32, flags="aligned, c_contiguous"),  # splinedims
            ctl.ndpointer(np.float32, flags="aligned, c_contiguous"),  # weights
            ctl.ndpointer(np.float32, flags="aligned, c_contiguous"),  # weightsgradient
            ctl.ndpointer(np.float32, flags="aligned, c_contiguous"),  # pixels
            ctl.ndpointer(np.float32, flags="aligned, c_contiguous"),  # bg
            ctl.ndpointer(np.float32, flags="aligned, c_contiguous"),  # roi_ll
            ctl.ndpointer(np.float32, flags="aligned, c_contiguous"),  # expval
            ctypes.c_bool  # cuda
        ]


        #void DSpline_Eval(Vector3f* pos, int count, int roisize, const Int3& splineDims, 
            #float* weights, float* output)
        self._DSpline_Eval = self.lib.DSpline_Eval
        self._DSpline_Eval.argtypes = [
            ctl.ndpointer(np.float32, flags="aligned, c_contiguous"),  # pos
            ctypes.c_int32,  # count
            ctypes.c_int32,  # roisize
            ctl.ndpointer(np.int32, flags="aligned, c_contiguous"),  # splinedims
            ctl.ndpointer(np.float32, flags="aligned, c_contiguous"),  # weights
            ctl.ndpointer(np.float32, flags="aligned, c_contiguous"),  # output
        ]

        #Estimator* DSpline_CreatePSF(int roisize, Int3& splineDims, 
        #const float* weights, int csplineMode, bool cuda, Context* ctx)
        self._DSpline_CreatePSF = self.lib.DSpline_CreatePSF
        self._DSpline_CreatePSF.argtypes = [
            ctypes.c_int32,  # roisize
            ctl.ndpointer(np.int32, flags="aligned, c_contiguous"),  # splinedims
            ctypes.POINTER(CSplineCalibration),
            ctl.ndpointer(np.float32, flags="aligned, c_contiguous"), # weights
            ctypes.c_int32,  # csplinemode
            ctypes.c_bool,  # cuda
            ctypes.c_void_p
        ]
        self._DSpline_CreatePSF.restype = ctypes.c_void_p


    def Eval(self, pos, roisize, weights):
        assert(len(weights.shape)==3)
        pos = np.ascontiguousarray(pos,dtype=np.float32)
        assert pos.shape[1] == 3
        splinedims = np.array(weights.shape,dtype=np.int32)
        weights = np.ascontiguousarray(weights, dtype=np.float32)
        output = np.zeros((len(pos),roisize,roisize),dtype=np.float32)
        self._DSpline_Eval(pos, len(pos), roisize, splinedims, weights, output)
        return output
    
    def CreatePSF(self, weights, roisize, csplineMode=CSplineMethods.FlatBg, zrange=None, cuda=True):
        splinedims = np.array(weights.shape,dtype=np.int32)
        weights = np.ascontiguousarray(weights, dtype=np.float32)
        if zrange is None:
            zrange = [0,splinedims[0]//2]
            
        coefs=np.zeros( (*((splinedims//2)-1),64))
        print(f"Shape: {coefs.shape}. size: {coefs.size}")
        calib = CSplineCalibration(zrange[0],zrange[1], coefs)

        psf = self._DSpline_CreatePSF(roisize, splinedims, calib, weights, 
                                      csplineMode, cuda, self.ctx.inst)
        

        return CSplinePSF(self.ctx, psf, calib)
    
    def ComputeWeightsGradient(self, pos, intensities, splineWeights, pixels, pixelBg, cuda=False):
        #void DSpline_LLWeightsGradient2(Vector3f* emitterPos, const float* emitterIntensities,
        #int emitterCount, int roisize, Int3& splineDims,
        #const float* weights, float* weightsGradient, float* partialWeightGradients, const float* pixels, 
        #const float* pixelBackgrounds, float* psf_, bool cuda)

        pos = np.ascontiguousarray(pos, dtype=np.float32)
        intensities = np.ascontiguousarray(intensities, dtype=np.float32)
        assert(len(pos) == len(intensities))
        
        splineWeights = np.ascontiguousarray(splineWeights, dtype=np.float32)
        weightsGradient = splineWeights*0
        pixels = np.ascontiguousarray(pixels, dtype=np.float32)
        pixelBg = np.ascontiguousarray(pixelBg, dtype=np.float32)

        roisize = pixels.shape[-1]
        
        # for debugging
        psf = np.zeros((len(pos), roisize,roisize),dtype=np.float32)
        splineDims = np.array(splineWeights.shape,dtype=np.int32)
        
        roi_ll = np.zeros(len(pos), dtype=np.float32)

        #pwg = np.zeros((len(pos),roisize,roisize,64),dtype=np.float32)
        self._DSpline_LLWeightsGradient(pos, intensities, len(pos), roisize, splineDims, splineWeights,
                                         weightsGradient, pixels, pixelBg, roi_ll, psf, cuda)
        
        return weightsGradient,psf,roi_ll
    
    def RenderSection(self, yaxis, xaxis, slicePos, weights, stepsize=0.2):
        """
        Creates a view of the PSF in dimension axis1,axis2, with pos being the slice position in the remaining axis
        """
        splinedims = np.array(weights.shape,dtype=np.int32)
        gridsize = splinedims//2
        xrange = np.arange(-gridsize[xaxis]/2,gridsize[xaxis]/2,stepsize)[::-1]
        yrange = np.arange(-gridsize[xaxis]/2,gridsize[yaxis]/2,stepsize)[::-1]
        X,Y = np.meshgrid(xrange, yrange)
        X=X.flatten()
        Y=Y.flatten()
        pts = np.zeros((len(X),3))
        pts[:,0] = X
        pts[:,1] = Y
        pts[:,2] = slicePos
        
        return self.Eval(pts, 1, weights).reshape((len(yrange),len(xrange)))
        
    
if __name__ == "__main__":
    with Context() as ctx:
        dsm = DSplineMethods(ctx)
        
        roisize = 10
        D = 4
        pos = [[roisize*0.5,roisize*0.5,D*0.5]]
        
        weights = np.zeros((D,W,W,8),dtype=np.float32)
        
        output = dsm.Eval(pos, roisize, weights)


