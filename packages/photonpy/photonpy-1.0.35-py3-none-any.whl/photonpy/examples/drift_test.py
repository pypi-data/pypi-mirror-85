# Drift estimation example using Minimum Entropy
# use pip install photonpy==1.0.34

from photonpy import Dataset
import os

fn = 'C:/dev/drift/figures/simulated_data/tubules8.hdf5'
ds = Dataset.load(fn, pixelsize=100)

ds.estimateDriftMinEntropy(initializeWithRCC=True, framesPerBin=0, maxdrift=5, 
                           apply=True, useCuda=True)

ds.save(os.path.splitext(fn)[0]+"_undrifted_dme.hdf5")
