# -*- coding: utf-8 -*-

import os
import pickle
import tifffile
import numpy as np
from photonpy.cpp.gaussian import Gaussian
from photonpy.cpp.postprocess import PostProcessMethods
import photonpy.cpp.spotdetect as spotdetect
import time
import sys
import photonpy.cpp.postprocess as postprocess
import matplotlib.pyplot as plt
from photonpy.smlm import drift_estimate
import scipy.spatial.ckdtree

from photonpy.cpp.estimator import Estimator
from photonpy.cpp.estim_queue import EstimQueue_Results
from photonpy.cpp.lib import SMLM
from photonpy.cpp.context import Context

from enum import IntEnum

class DataColumns(IntEnum):
    FRAME = 0
    X = 1
    Y = 2
    I = 3
    BG = 4
    CRLB_X = 5
    CRLB_Y = 6
    CRLB_I = 7
    CRLB_BG = 8
    ITERATIONS = 9
    SCORE = 10
    CHISQ = 11
    ROIX = 12
    ROIY = 13
    SIGMA = 14
    NUMCOL = 15


class LocResultList:
    # 2D result array, with
    data = np.zeros((0, DataColumns.NUMCOL), dtype=np.float)
    # list of indices into the data array
    frames = []
    roisize = 0
    cfg = None
    raw_image_sum = None
    spot_drift = None
    drift = None
    area = None # x,y,w,h
    filename = None
    extraColumns = None
        
    def __init__(self, data=None, cfg=None, area=None, filename=None, extraColumns=None, src_indices=None):
        if data is not None:
            self.data = data * 1
            self._reset_frames()
            self.cfg = dict(cfg)
            self.area = area
            self.imgshape = [area[3],area[2]]
            self.filename = filename
            self.extraColumns = extraColumns
            self.src_indices = src_indices

    def __len__(self):
        return len(self.frames)

    def get_area(self):
        if self.area is not None:
            return np.array(self.area)
        return np.array([0, 0, self.raw_image_sum.shape[1], self.raw_image_sum.shape[0]])
    
    def get_image_size(self):
        return self.get_area()[[2,3]]
    
    def get_positions(self):
        positions = []
        for f, indices in enumerate(self.frames):
            positions.append(self.data[indices, 1:5])
        return positions
    
    def get_frame_spot_indices(self, framelist):
        return np.concatenate([self.frames[f] for f in framelist])
    
    # Regenerate self.frames
    def _reset_frames(self):
        frame_indices = self.data[:,DataColumns.FRAME].astype(int)
        if len(frame_indices) == 0: 
            numFrames = 0
        else:
            numFrames = np.max(frame_indices)+1
        self.frames = [[] for i in range(numFrames)]
        for k in range(len(self.data)):
            self.frames[frame_indices[k]].append(k)
        for f in range(numFrames):
            self.frames[f] = np.array(self.frames[f], dtype=int)
    
    # Remove all spots not in indices
    def filter_indices(self, indices):
        self.data = self.data[indices]
        if self.src_indices is not None:
            self.src_indices = self.src_indices[indices]
        self._reset_frames()

    def filter(self, fn):
        newdata = []
        spotcount = 0
        frames = []
        selindices = []
        for f, indices in enumerate(self.frames):
            ok = fn(indices, self.data[indices, :])
            okcount = np.sum(ok)
            selindices.append(indices[ok])
            frames.append(np.arange(okcount) + spotcount)
            newdata.append(self.data[indices[ok], :])
            spotcount += okcount
        filtered_count = len(self.data)-spotcount
        self.frames = frames
        self.data = np.concatenate(newdata)
        selindices = np.concatenate(selindices)
        if self.src_indices is not None:
            self.src_indices = self.src_indices[selindices]
        if self.extraColumns is not None:
            for k in self.extraColumns.keys():
                print(f"filtering {k} len(seli)={len(selindices)} len(data)={len(self.data)} len(col)={len(self.extraColumns[k])}")
                self.extraColumns[k] = self.extraColumns[k][selindices]
        return filtered_count, selindices

    def filter_nan(self):
        return self.filter(lambda i,d: ~np.isnan(np.sum(d[:, 1:5], 1)))
    
    def filter_inroi(self, minX, minY, maxX, maxY):
        return self.filter(lambda i,d: 
            np.logical_and(
                np.logical_and(d[:,DataColumns.X] - d[:,DataColumns.ROIX]>minX, 
                               d[:,DataColumns.Y] - d[:,DataColumns.ROIY]>minY),
                np.logical_and(d[:,DataColumns.X] - d[:,DataColumns.ROIX]<maxX, 
                               d[:,DataColumns.Y] - d[:,DataColumns.ROIY]<maxY)))

    def draw(self, scale, ctx:Context, area=None, fixedSigma=None):
        if area == None:
            area = self.get_area()
        image = np.zeros((np.array([area[3], area[2]]) * scale).astype(int), dtype=np.float64)
        pts = 1 * self.data[:, [DataColumns.X, DataColumns.Y, DataColumns.CRLB_X, DataColumns.CRLB_Y, DataColumns.I]]
        pts[:, [0, 1]] -= [area[0], area[1]]
        pts *= np.tile([scale, scale, scale, scale, 1], (len(pts), 1))
        if fixedSigma is not None:
            pts[:, [2, 3]] = fixedSigma
        image = Gaussian(ctx).Draw(image, pts)
        return image


    def spot_counts(self):
        return np.array([len(f) for f in self.frames])

    def roisize(self):
        return self.cfg["roisize"]

    def frame_data(self, framenumbers):
        fd = []
        for f in framenumbers:
            fd.append(self.data[self.frames[f], :])
        return fd

    def drift_estimate_rcc(self, smlm, framebinning=1000, scale=6, useIntensities=False, maxdrift=2):
        xyI = self.get_xyI() * 1
        if not useIntensities:
            xyI[:, 2] = 1

        frame_num = self.get_frame_numbers()
        timebins = np.max(frame_num)//framebinning
#def rcc(xyI, framenum, timebins, rendersize, wrapfov=1, zoom=1, sigma=1, RCC=True):
        drift_interp,drift_estim,images = drift_estimate.rcc(xyI, frame_num, timebins, 
                                   self.imgshape[0], smlm, maxdrift=maxdrift,
                                   wrapfov=1,zoom=scale,sigma=0.5)
        
        self.drift = drift_interp
        self.drift_estim= drift_estim
		
        return self.drift
    
    def drift_correct_from_file(self,drift_fn, drift_frames_per_frame):
        drift = np.loadtxt(drift_fn)
        print(f"drift file {drift_fn} as {len(drift)} frames")
        drift_indices = (np.arange(len(self.frames)) * drift_frames_per_frame).astype(int)
        drift_indices = np.clip(drift_indices, 0, len(drift)-1)
        self.drift = drift[drift_indices]
        self.spot_drift = self.drift[self.get_frame_numbers()]
        self.data[:, [DataColumns.X, DataColumns.Y]] -= self.spot_drift
        self.raw_drift = None
        return drift
        
    def apply_drift_correction(self, drift=None):
        frame_num = self.get_frame_numbers()
        self.drift = drift
        self.spot_drift = self.drift[frame_num]
        self.data[:, [DataColumns.X, DataColumns.Y]] -= self.spot_drift

    def plot_drift(self, title):
        fig = plt.figure()
        plt.plot(self.drift[:, 0], label="X drift (interpolated)")
        plt.plot(self.drift[:, 1], label="Y drift (interpolated)")
        
        if hasattr(self, "drift_estim"):
            plt.plot(self.drift_estim[:, 2], self.drift_estim[:, 0], 'o',label="X drift (estim)")
            plt.plot(self.drift_estim[:, 2], self.drift_estim[:, 1], 'o', label="Y drift (estim)")

        plt.xlabel("Timebins")
        plt.ylabel("Pixels")
        plt.legend()
        plt.title(title)

        if hasattr(self, "drift_mr"):
            plt.figure()
            plt.plot(self.drift_mr, label="Point match counts")
            plt.legend()
            plt.title(title)
        return fig

    def get_crlb(self):
        return self.data[:, [DataColumns.CRLB_X, DataColumns.CRLB_Y, DataColumns.CRLB_I, DataColumns.CRLB_BG]]

    def get_xy(self):
        return self.data[:, [DataColumns.X, DataColumns.Y]]

    def get_xyI(self):
        return self.data[:, [DataColumns.X, DataColumns.Y, DataColumns.I]]

    def get_bg(self):
        return self.data[:, DataColumns.BG]

    def get_xyIBg(self):
        return self.data[:, [DataColumns.X, DataColumns.Y, DataColumns.I, DataColumns.BG]]
    
    def get_estim(self):
        e = self.get_xyIBg()*1
        e[:,:2] -= self.get_roipos()
        return e

    def get_roipos(self):
        return self.data[:, [DataColumns.ROIX, DataColumns.ROIY]].astype(np.int32)

    def get_frame_numbers(self):
        return self.data[:, DataColumns.FRAME].astype(np.int32)

    def get_scores(self):
        return self.data[:, DataColumns.SCORE]

    def save_csv(self, filename):
        [e.name for e in DataColumns]
        np.savetxt(filename, self.data, delimiter="\t", fmt="%10.5f")

    def view(self):
        import pptk

        def cloud(xyI, col):
            xyz = np.zeros((len(xyI), 3))
            xyz[:, [0, 1]] = xyI[:, 0:2]
            rgb = np.zeros((len(xyI), 3))
            rgb[:, col] = 1
            return xyz, rgb

        a = cloud(self.get_xyI(), 0)

        v = pptk.viewer(a[0], a[1])
        return v

    def in_roi(self, roi_xy, roi_size=10):
        roi_xy = np.array(roi_xy)
        x = self.data[:, DataColumns.X]
        y = self.data[:, DataColumns.Y]

        indices = np.where(
                (x >= roi_xy[0] - roi_size/2) & (x <= roi_xy[0] + roi_size/2) & 
                (y >= roi_xy[1] - roi_size/2) & (y <= roi_xy[1] + roi_size/2))[0]

        area = [roi_xy[0]-roi_size/2, roi_xy[1]-roi_size/2, roi_size, roi_size]
        r = LocResultList(self.data[indices,:], self.cfg, area)
        return r
    
    def count_neighbors(self, searchdist):
        """
        Return the number of neighbors for each localization
        """
        kdtree = scipy.spatial.ckdtree.cKDTree(self.get_xy())
        pairs = kdtree.query_pairs(searchdist) # output_type='ndarray')
        
        counts = np.zeros((len(self.data)),dtype=np.int)
        for p in pairs:
            counts[p[0]] += 1
        
        return counts
   
    def save_txt(self, fn):
        cols = [DataColumns.FRAME,
                DataColumns.X,
                DataColumns.Y,
                DataColumns.I,
                DataColumns.BG,
                DataColumns.CRLB_X,
                DataColumns.CRLB_Y,
                DataColumns.CRLB_I,
                DataColumns.CRLB_BG]
        
        data = np.zeros((len(self.data), len(cols)))
        h = ''
        for k in range(len(cols)):
            data[:,k]=self.data[:,cols[k].value]
            h += cols[k].name + '\t'
        
        np.savetxt(fn, data, delimiter='\t', header=h,fmt= "%10.8f")
   
    def link_locs(self, ctx:Context, maxdist=None, frameskip=1):
        crlb = self.get_crlb()
        if maxdist is None:
            maxdist = 3*np.sqrt(np.sum(np.mean(crlb[:,[0,1]],0)**2))
        
        pp = PostProcessMethods(ctx)
        xyI = self.get_xyI()
        framenum = self.get_frame_numbers()
        linked, framecounts, startframes, linkedXYI, linkedCRLB = pp.LinkLocalizations(
                xyI,crlb[:,0:3],framenum,maxdist,10,frameskip)
        
        data = np.zeros((len(linkedXYI), DataColumns.NUMCOL),dtype=np.float32)
        data[:,[DataColumns.X,DataColumns.Y,DataColumns.I]] = linkedXYI
        data[:,[DataColumns.CRLB_X,DataColumns.CRLB_Y,DataColumns.CRLB_I]] = linkedCRLB

        data[:,DataColumns.SIGMA] = np.mean(self.data[:,DataColumns.SIGMA])
        data[:,DataColumns.FRAME] = startframes
        data[:,DataColumns.BG] = np.mean(self.get_xyIBg()[:,3])
        
        lr = LocResultList(data, self.cfg, self.area, self.filename)
        return lr
    
    def clone(self):
        return LocResultList(self.data*1, dict(self.cfg), self.area*1, str(self.filename))
    
    def save_picasso_hdf5(self, fn=None, extra_columns=False):
        import h5py 
        import yaml
        
        if fn is None:
            fn = os.path.splitext(self.filename)[0] + "_g2d.hdf5"
        
        print(f"Saving hdf5 to {fn}")
        with h5py.File(fn, 'w') as f:
            dtype = [('frame', '<u4'), 
                     ('x', '<f4'), ('y', '<f4'), 
                     ('photons', '<f4'), 
                     ('sx', '<f4'), ('sy', '<f4'), 
                     ('bg', '<f4'), 
                     ('lpx', '<f4'), ('lpy', '<f4'), 
                     ('lI', '<f4'), ('lbg', '<f4'), 
                     ('ellipticity', '<f4'), 
                     ('net_gradient', '<f4')]
            
            if self.src_indices is not None:
                dtype.append( ('src_index', '<u4'))
            
            if extra_columns and self.extraColumns is not None:
                for k in self.extraColumns.keys():
                    dtype.append((k,self.extraColumns[k].dtype,self.extraColumns[k].shape[1:]))
            
            locs = f.create_dataset('locs', shape=(len(self.data),), dtype=dtype)
            locs['frame'] = self.get_frame_numbers()
            locs['x'] = self.get_xyI()[:,0]
            locs['y'] = self.get_xyI()[:,1]
            locs['photons'] = self.get_xyI()[:,2]
            print(f"Mean photon count: {np.mean(self.get_xyI()[:,2]):.1f}")
            sigma = self.cfg['sigma']
            if np.isscalar(sigma):
                locs['sx'] = sigma
                locs['sy'] = sigma
            else:
                locs['sx'] = sigma[0]
                locs['sy'] = sigma[1]
            locs['bg'] = self.data[:, DataColumns.BG]
            locs['lpx'] = self.data[:, DataColumns.CRLB_X]
            locs['lpy'] = self.data[:, DataColumns.CRLB_Y]
            locs['lI'] = self.data[:, DataColumns.CRLB_I]
            locs['lbg'] = self.data[:, DataColumns.CRLB_BG]
            locs['net_gradient'] = self.data[:, DataColumns.SCORE]
            
            if self.src_indices is not None:
                locs['src_index'] = self.src_indices
            
#            locs['ellipticity']
            
            if extra_columns and self.extraColumns is not None:
                for k in self.extraColumns.keys():
                    locs[k] = self.extraColumns[k] 
                    
            info =  {'Byte Order': '<',
                     'Camera': 'Dont know' ,
                     'Data Type': 'uint16',
                     'File': self.filename,
                     'Frames': len(self.frames),
                     'Width': self.get_area()[2],
                     'Height': self.get_area()[3]}

            info_fn = os.path.splitext(fn)[0] + ".yaml" 
            with open(info_fn, "w") as file:
                yaml.dump(info, file, default_flow_style=False) 

        return fn
    # def export_rois(peaklist)
    #   , width=6, zoom=20, outdir=os.path.split(fn)[0]+'aois/')

    
def from_estim(cfg, area, filename, estim, crlb, roipos, framenum):
    data = np.zeros((len(estim), DataColumns.NUMCOL),dtype=np.float32)
    data[:,[DataColumns.CRLB_X,DataColumns.CRLB_Y,DataColumns.CRLB_I,DataColumns.CRLB_BG]] = crlb
    data[:,DataColumns.FRAME] = framenum
    data[:,[DataColumns.ROIX,DataColumns.ROIY]] = roipos[:,[-1,-2]]

    estim = estim*1
    estim[:, 0] += roipos[:,-1]
    estim[:, 1] += roipos[:,-2]

    data[:,[DataColumns.X,DataColumns.Y,DataColumns.I,DataColumns.BG]] = estim

    lr = LocResultList(data, cfg, area, filename)
    return lr

    

def from_psf_queue_results(results : EstimQueue_Results, cfg, area, filename, divideFrameNum=1):
    crlb = results.CRLB()
    estim,roipos,framenums = results.estim,results.roipos,results.ids
    framenums //= divideFrameNum
    fmt = results.colnames
    xyIBg = [fmt.index('x'), fmt.index('y'), fmt.index('I'), fmt.index('bg')]
   # print(f'Found x,y,I,bg indices: {xyIBg}')

    estim[:,xyIBg[0]] += roipos[:,-1]
    estim[:,xyIBg[1]] += roipos[:,-2]

    data = np.zeros((len(estim), DataColumns.NUMCOL),dtype=np.float32)
    data[:,[DataColumns.X,DataColumns.Y,DataColumns.I,DataColumns.BG]] = estim[:, xyIBg]
    data[:,[DataColumns.CRLB_X,DataColumns.CRLB_Y,DataColumns.CRLB_I,DataColumns.CRLB_BG]] = crlb[:,xyIBg]
    data[:,DataColumns.FRAME] = framenums
    data[:,[DataColumns.ROIX,DataColumns.ROIY]] = roipos[:,[-1,-2]]

    lr = LocResultList(data, cfg, area, filename)
    return lr
        
def load(path, cfg, smlm, rebuild=False, tag="g2d_result") -> LocResultList:
    dir, file = os.path.split(path)
    ext = f".{tag}.pickle"
    if path.endswith(ext):
        with open(path, "rb") as f:
            result, loaded_cfg = pickle.load(f)
            return result

    file, _ = os.path.splitext(file)
    path_noext, _ = os.path.splitext(path)

    resultsfn = path_noext + ext
    if not rebuild and os.path.exists(resultsfn):
        with open(resultsfn, "rb") as f:
            result, loaded_cfg = pickle.load(f)
            if loaded_cfg == cfg:
                print(f"{path} contains {len(result.data)} spots.")
                result.filename = path
                return result

    result = LocResultList()
    with Context(smlm) as ctx:
        result.read_tiff(path, cfg, ctx)

    with open(resultsfn, "wb") as f:
        pickle.dump((result, cfg), f)

    return result



def draw_spots(img, x, y, I, sigmaX, sigmaY, scale, ctx:Context):
    # Spots is an array with rows: [ x,y, sigmaX, sigmaY, intensity ]
    img = np.ascontiguousarray(img, dtype=np.float32)

    spots = np.zeros((len(x), 5), dtype=np.float32)
    spots[:, 0] = x * scale
    spots[:, 1] = y * scale
    spots[:, 2] = sigmaX * scale
    spots[:, 3] = sigmaY * scale
    spots[:, 4] = I

    return Gaussian(ctx).Draw(img, spots)


def binlocalizations(imgshape, xyI, scale=4):
    image = np.zeros((imgshape[0] * scale, imgshape[1] * scale), dtype=np.float32)
    shape = image.shape

    x = (xyI[:, 0] * scale + 0.5).astype(int)
    y = (xyI[:, 1] * scale + 0.5).astype(int)
    x = np.clip(x, 0, shape[1] - 1)
    y = np.clip(y, 0, shape[0] - 1)
    image[y, x] += xyI[:, 2]

    return image

