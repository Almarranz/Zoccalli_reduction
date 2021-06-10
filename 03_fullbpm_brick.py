#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 10:46:16 2021

@author: amartinez
"""

import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table # para leer cualquier tabla
from astropy.table import Table, Column
from astropy.io import fits
import glob
from matplotlib.colors import LogNorm
import random
import statistics
from scipy.stats import mode
from astropy import stats
import random
import idlwrap
exptime=10
band='Ks'
py_pruebas='/Users/amartinez/Desktop/PhD/HAWK/The_Brick/py_pruebas/'
#raw='/Users/amartinez/Desktop/PhD/HAWK/The_Brick/raw/NPL054_Ks/flat_NPL054/'
im ='/Users/amartinez/Desktop/PhD/HAWK/The_Brick/03_Fullbpm/054_'+band+'/dit_'+str(exptime)+'/im/'
dark_path='/Users/amartinez/Desktop/PhD/HAWK/The_Brick/01_Dark/054_'+band+'/dit_'+str(exptime)+'/im/'
bpm_path='/Users/amartinez/Desktop/PhD/HAWK/The_Brick/02_Flats/054_'+band+'/im/'
name='54_'+band
sigma_dev_dark = 20

dfiles=sorted(glob.glob(dark_path+'*.fits'))
print(len(dfiles))

bpmfiles=sorted(glob.glob(bpm_path+'bpm*.fits'))
bpmfiles

dfiles=sorted(glob.glob(dark_path+'*.fits'))
i=0
for f in dfiles:
    i+=1
    dark=fits.getdata(f)
    bpm=fits.getdata(bpm_path+'bpm'+str(i)+'_'+name+'.fits')
    print(bpm.shape)
    mean, median, std=stats.sigma_clipped_stats(dark, sigma=6)
    print(mean, median, std)
    bad= np.where(abs(dark-mean)>sigma_dev_dark*std)
    dark[:,:]=0
    dark[bad]=1
    new = np.where(dark>0)
    bpm[new]=1
    fits.writeto(im+'dark_bpm'+str(i)+'_dit'+str(exptime)+'.fits',dark,overwrite=True)
    fits.writeto(im+'bpm'+str(i)+'_dit'+str(exptime)+'.fits',bpm,overwrite=True)
    
    
print('###### Fullbpm done ######')