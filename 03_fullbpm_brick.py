#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 10:46:16 2021

@author: amartinez
"""

import numpy as np
from astropy.io import fits
import glob
from astropy import stats
exptime=10
band='H'
py_pruebas='/Users/amartinez/Desktop/PhD/HAWK/The_Brick/py_pruebas/'
#raw='/Users/amartinez/Desktop/PhD/HAWK/The_Brick/raw/NPL054_Ks/flat_NPL054/'
im ='/Users/alvaromartinez/Desktop/PhD/HAWKI/The_Brick/03_Fullbpm/058_'+band+'/dit_'+str(exptime)+'/im/'
dark_path='/Users/alvaromartinez/Desktop/PhD/HAWKI/The_Brick/01_Dark/058_'+band+'/dit_'+str(exptime)+'/im/'
bpm_path='/Users/alvaromartinez/Desktop/PhD/HAWKI/The_Brick/02_Flats/058_'+band+'/dit_10/im/'
name='58_'+band
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
    mean, median, std=stats.sigma_clipped_stats(dark, sigma=3)
    print(mean, median, std)
    bad= np.where(abs(dark-mean)>sigma_dev_dark*std)
    dark[:,:]=0
    dark[bad]=1
    new = np.where(dark>0)
    bpm[new]=1
    fits.writeto(im+'dark_bpm'+str(i)+'_dit'+str(exptime)+'.fits',dark,overwrite=True)
    fits.writeto(im+'bpm'+str(i)+'_dit'+str(exptime)+'.fits',bpm,overwrite=True)
    
    
print('###### Fullbpm done ######')