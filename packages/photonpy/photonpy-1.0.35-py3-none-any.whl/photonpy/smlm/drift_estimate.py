import matplotlib.pyplot as plt
import numpy as np
from photonpy.cpp.lib import SMLM
from photonpy.cpp.context import Context
from photonpy.cpp.gaussian import Gaussian
import os
import tqdm
from scipy.interpolate import InterpolatedUnivariateSpline
from photonpy.cpp.postprocess import PostProcessMethods

from photonpy.gaussian.fitters import fit_sigma_2d

# https://aip.scitation.org/doi/full/10.1063/1.5005899
def phasor_localize(roi):
    fx = np.sum(np.sum(roi,0)*np.exp(-2j*np.pi*np.arange(roi.shape[1])/roi.shape[1]))
    fy = np.sum(np.sum(roi,1)*np.exp(-2j*np.pi*np.arange(roi.shape[0])/roi.shape[0]))
            
    #Get the size of the matrix
    WindowPixelSize = roi.shape[1]
    #Calculate the angle of the X-phasor from the first Fourier coefficient in X
    angX = np.angle(fx)
    if angX>0: angX=angX-2*np.pi
    #Normalize the angle by 2pi and the amount of pixels of the ROI
    PositionX = np.abs(angX)/(2*np.pi/WindowPixelSize)
    #Calculate the angle of the Y-phasor from the first Fourier coefficient in Y
    angY = np.angle(fy)
    #Correct the angle
    if angY>0: angY=angY-2*np.pi
    #Normalize the angle by 2pi and the amount of pixels of the ROI
    PositionY = np.abs(angY)/(2*np.pi/WindowPixelSize)
    
    return PositionX,PositionY


def crosscorrelation(A, B):
    A_fft = np.fft.fft2(A)
    B_fft = np.fft.fft2(B)
    return np.fft.ifft2(A_fft * np.conj(B_fft))

def crosscorrelation_cuda(A, B, smlm: SMLM):
    return smlm.IFFT2(np.conj(smlm.FFT2(A)) * smlm.FFT2(B))



def findshift(cc, smlm:SMLM, plot=False):
    # look for the peak in a small subsection
    r = 6
    hw = 20
    cc_middle = cc[cc.shape[0] // 2 - hw : cc.shape[0] // 2 + hw, cc.shape[1] // 2 - hw : cc.shape[1] // 2 + hw]
    peak = np.array(np.unravel_index(np.argmax(cc_middle), cc_middle.shape))
    peak += [cc.shape[0] // 2 - hw, cc.shape[1] // 2 - hw]
    
    peak = np.clip(peak, r, np.array(cc.shape) - r)
    roi = cc[peak[0] - r + 1 : peak[0] + r, peak[1] - r + 1 : peak[1] + r]
    if plot:
        plt.figure()
        plt.imshow(cc_middle)
        plt.figure()
        plt.imshow(roi)

    #with Context(smlm) as ctx:
        #psf=Gaussian(ctx).CreatePSF_XYIBgSigma(len(roi), 1, False)
        #e = psf.Estimate([roi])
        #print(e[0])
#    px,py=phasor_localize(roi)
        #px,py = e[0][0][:2]
    px,py = fit_sigma_2d(roi, initial_sigma=2)[[0, 1]]
    #            roi_top = lsqfit.lsqfitmax(roi)
    return (peak[1] + px - r + 1 - cc.shape[1] / 2), (peak[0] + py - r + 1 - cc.shape[0] / 2) 


def findshift_pairs(images, pairs, smlm:SMLM, useCuda=True):
    fft2 = smlm.FFT2 if useCuda else np.fft.fft2
    ifft2 = smlm.IFFT2 if useCuda else np.fft.ifft2
    
    print("FFT'ing")
    w = images.shape[-1]
    fft_images = fft2(images)
    fft_conv = np.zeros((len(pairs), w, w),dtype=np.complex64)
    for i, (a,b) in enumerate(pairs):
        fft_conv[i] = np.conj(fft_images[a]) * fft_images[b]
        
    print("IFFT'ing")
    cc =  ifft2(fft_conv)
    cc = np.abs(np.fft.fftshift(cc, (-2, -1)))

    print("Finding cc peaks..")
    shift = np.zeros((len(pairs),2))
    for i in tqdm.trange(len(pairs)):
        shift[i] = findshift(cc[i], smlm)
    
    return shift

def rcc(xyI, framenum, timebins, rendersize, maxdrift=3, wrapfov=1, zoom=1, sigma=1, maxpairs=1000,RCC=True,smlm:SMLM=None):
#    area = np.ceil(np.max(xyI[:,[0,1]],0)).astype(int)
 #   area = np.array([area[0],area[0]])
    
    area = np.array([rendersize,rendersize])
    
    nframes = np.max(framenum)+1
    framesperbin = nframes//timebins
        
    with Context(smlm) as ctx:
        g = Gaussian(ctx)
        
        imgshape = area*zoom//wrapfov
        images = np.zeros((timebins, *imgshape))
            
        for k in range(timebins):
            img = np.zeros(imgshape,dtype=np.float32)
            
            indices = np.nonzero(framenum//framesperbin==k)[0]

            spots = np.zeros((len(indices), 5), dtype=np.float32)
            spots[:, 0] = (xyI[indices,0] * zoom) % imgshape[1]
            spots[:, 1] = (xyI[indices,1] * zoom) % imgshape[0]
            spots[:, 2] = sigma
            spots[:, 3] = sigma
            spots[:, 4] = xyI[indices,2]
            
            if len(spots) == 0:
                raise ValueError(f'no spots in bin {k}')

            images[k] = g.Draw(img, spots)
            
        print(f"RCC pairs: {timebins*(timebins-1)//2}. Bins={timebins}")
            
        if RCC:
            pairs = np.array(np.triu_indices(timebins,1)).T
            if len(pairs)>maxpairs:
                pairs = pairs[np.random.choice(len(pairs),maxpairs)]
            pair_shifts = findshift_pairs(images, pairs, ctx.smlm, useCuda=False)
            
            A = np.zeros((len(pairs),timebins))
            A[np.arange(len(pairs)),pairs[:,0]] = 1
            A[np.arange(len(pairs)),pairs[:,1]] = -1
            
            inv = np.linalg.pinv(A)
            shift_x = inv @ pair_shifts[:,0]
            shift_y = inv @ pair_shifts[:,1]
            shift_y -= shift_y[0]
            shift_x -= shift_x[0]
            shift = -np.vstack((shift_x,shift_y)).T / zoom
        else:
            pairs = np.vstack((np.arange(timebins-1)*0,np.arange(timebins-1)+1)).T
            shift = np.zeros((timebins,2))
            shift[1:] = findshift_pairs(images, pairs, ctx.smlm)
            shift /= zoom
            #shift = np.cumsum(shift,0)
            
        t = (0.5+np.arange(timebins))*framesperbin

        shift_estim = np.zeros((len(shift),3))
        shift_estim[:,[0,1]] = shift
        shift_estim[:,2] = t

        if timebins != nframes:
            spl_x = InterpolatedUnivariateSpline(t, shift[:,0], k=2)
            spl_y = InterpolatedUnivariateSpline(t, shift[:,1], k=2)
        
            shift_interp = np.zeros((nframes,2))
            shift_interp[:,0] = spl_x(np.arange(nframes))
            shift_interp[:,1] = spl_y(np.arange(nframes))
        else:
            shift_interp = shift
                
            
    return shift_interp, shift_estim, images
        

def interp_shift_xy(shift,framesperbin,nframes):

    t = (np.arange(len(shift))+0.5)*framesperbin,
    spl_x = InterpolatedUnivariateSpline(t, shift[:,0], k=2)
    spl_y = InterpolatedUnivariateSpline(t, shift[:,1], k=2)
    
    shift_interp = np.zeros((nframes,2))
    shift_interp[:,0] = spl_x(np.arange(nframes))
    shift_interp[:,1] = spl_y(np.arange(nframes))
    
    return shift_interp


def minEntropy(positions, framenum, crlb, framesperbin, imgshape, 
          sigma, maxdrift=3, dataname=None, outputfn=None,debugMode=False,
          useCuda=True,display=True,pixelsize=None,coarseFramesPerBin=None,
          maxspots=None, initializeWithRCC=False):
    """
    Maximize localization correlation
    """
    
    ndims = positions.shape[1]
    numframes = np.max(framenum)+1
    if np.isscalar(sigma):
        sigstr=f"{sigma:.1f}"
    else:
        with np.printoptions(precision=3):
            sigstr=f"{sigma}"

    if maxspots is not None and maxspots < len(positions):
        print(f"Drift correction: Limiting spot count to {maxspots}/{len(positions)} spots.")
        bestspots = np.argsort(np.prod(crlb,1))
        indices = bestspots[-maxspots:]
        crlb = crlb[indices]
        positions = positions[indices]
        framenum = framenum[indices]
            
    with Context(debugMode=debugMode) as ctx:
        numIterations = 10000
        step = 0.000001

        splitAxis = np.argmax( np.var(positions,0) )
        splitValue = np.median(positions[:,splitAxis])
        
        set1 = positions[:,splitAxis] > splitValue
        set2 = np.logical_not(set1)
        
        if False:
            print(f"Using drift correction with per-spot CRLB")
            crlb_set1 = crlb[set1]
            crlb_set2 = crlb[set2]
        else:
            crlb_set1 = sigma
            crlb_set2 = sigma
        
        ppm = PostProcessMethods(ctx)
                
        initial_drift = np.zeros((numframes,ndims))
        if initializeWithRCC:
            xyI = np.ones((len(positions),3)) 
            xyI[:,:2] = positions[:,:2]
            initial_drift[:,:2] = rcc(xyI, framenum, 10, np.max(imgshape), maxdrift)[0]
        
        if coarseFramesPerBin is not None:
            print(f"Computing initial coarse drift estimate... sigma:{sigstr}",flush=True)
            with tqdm.tqdm() as pbar:
                def update_pbar(i,info): 
                    pbar.set_description(info.decode("utf-8")); pbar.update(1)
                    return 1
    
                fpbCoarse=framesperbin*5
                initial_drift,score = ppm.MinEntropyDriftEstimate(
                    positions, framenum, initial_drift*1, sigma, numIterations, step, maxdrift, 
                    framesPerBin=fpbCoarse, cuda=useCuda,progcb=update_pbar)
                
        print(f"Estimating drift... Splitting axis={splitAxis}",flush=True)
        with tqdm.tqdm() as pbar:
            def update_pbar(i,info): 
                pbar.set_description(info.decode("utf-8"));pbar.update(1)
                return 1
            drift,score = ppm.MinEntropyDriftEstimate(
                positions, framenum, initial_drift*1, crlb, numIterations, step, maxdrift, framesPerBin=framesperbin, 
                cuda=useCuda, progcb=update_pbar)
                
        print("\nComputing drift estimation precision...",flush=True)
        with tqdm.tqdm() as pbar:
            def update_pbar(i,info): 
                pbar.set_description(info.decode("utf-8"));pbar.update(1)
                return 1
            drift_set1,score_set1 = ppm.MinEntropyDriftEstimate(
                positions[set1], framenum[set1], initial_drift*1, crlb_set1, numIterations, step, maxdrift, 
                framesPerBin=framesperbin,cuda=useCuda, progcb=update_pbar)

            drift_set2,score_set2 = ppm.MinEntropyDriftEstimate(
                positions[set2], framenum[set2], initial_drift*1, crlb_set2, numIterations, step, maxdrift, 
                framesPerBin=framesperbin,cuda=useCuda,progcb=update_pbar)

        n = f" for {dataname}" if dataname is not None else ""
        if False:#display:
            plt.figure()
            plt.plot(score,label='Score (full set)')
            plt.plot(score_set1,label='Score (subset 1)')
            plt.plot(score_set2,label='Score (subset 2)')
            plt.title(f'Optimization score progress{n}')
            plt.xlabel('Iteration')
            plt.legend()

        drift_set1 -= np.mean(drift_set1,0)
        drift_set2 -= np.mean(drift_set2,0)
        drift -= np.mean(drift,0)

        # both of these use half the data (so assuming precision scales with sqrt(N)), 2x variance
        # subtracting two 2x variance signals gives a 4x variance estimation of precision
        L = min(len(drift_set1),len(drift_set2))
        diff = drift_set1[:L] - drift_set2[:L]
        est_precision = np.std(diff,0)/2
        print(f"Estimated precision: {est_precision}")

        #hf = drift-drift_smoothed
        #vibration_std = np.sqrt(np.var(hf,0) - est_precision**2)
        #print(f'Vibration estimate: X={vibration_std[0]*pixelsize:.1f} nm, Y={vibration_std[1]*pixelsize:.1f} nm')

        if display:
            
            def plotwnd(L):
    
                fig,ax=plt.subplots(ndims,1,sharex=True,figsize=(10,8),dpi=150)
                
                axnames = ['X', 'Y', 'Z']
                axunits = ['px', 'px', 'um']
                for i in range(ndims):
                    axname=axnames[i]
                    axunit = axunits[i]
                    ax[i].plot(drift_set1[:L,i], '--', label=f'{axname} - set1, sigma={sigstr}')
                    ax[i].plot(drift_set2[:L,i], '--', label=f'{axname} - set2, sigma={sigstr}')
                    ax[i].plot(drift[:L,i], label=f'{axname} - full, sigma={sigstr}')
                    ax[i].plot(initial_drift[:L,i], label=f'Initial value {axname}')
                    ax[i].set_ylabel(f'Drift {axname} [{axunit}]')
                    ax[i].set_xlabel('Frame number')
                    if i==0: ax[i].legend(fontsize=12)
                
                if pixelsize is not None:
                    p=est_precision
                    scale = [pixelsize, pixelsize, 1000]
                    info = ';'.join([ f'{axnames[i]}: {p[i]*scale[i]:.1f} nm ({p[i]:.3f} {axunits[i]})' for i in range(ndims)])
                    
                    plt.suptitle(f'Drift trace. Approx. precision of drift estimate: {info}')
                else:
                    plt.suptitle(f'Drift trace{n}. Est. Precision: X/Y={est_precision[1]:.3f}/{est_precision[1]:.3f} pixels')
                if outputfn is not None:
                    plt.savefig(os.path.splitext(outputfn)[0] + ".png")
                    plt.savefig(os.path.splitext(outputfn)[0] + ".svg")
            
            #plotwnd(np.minimum(len(drift), 200))
            plotwnd(len(drift))
            
        D=ndims
        r = np.zeros((len(drift),4*D))
        r[:,:D] = drift
        r[:,3*D:4*D] = initial_drift

        # subset drift might have less frames in edge cases
        r[:,D:D*2] = drift; r[:len(drift_set1),D:D*2] = drift_set1
        r[:,D*2:D*3] = drift; r[:len(drift_set2),D*2:D*3] = drift_set2
        
        return drift, r, est_precision

