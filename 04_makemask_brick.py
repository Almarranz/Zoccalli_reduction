#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 11:26:36 2021

@author: amartinez
"""

import numpy as np
from scipy import ndimage
from astropy.io import fits
import glob

exptime=10

band='H'
py_pruebas='/Users/amartinez/Desktop/PhD/HAWKI/The_Brick/py_pruebas/'
bpm_path ='/Users/alvaromartinez/Desktop/PhD/HAWKI/The_Brick/03_Fullbpm/058_'+band+'/dit_'+str(exptime)+'/im/'
im='/Users/alvaromartinez/Desktop/PhD/HAWKI/The_Brick/04_Makemask/058_'+band+'/dit_'+str(exptime)+'/im/'
name='58_'+band
#second struct doesnt group data by the corners, first one does

#struct=np.ones((3,3))
struct=[[0, 1, 0],
 [1, 1, 1],
 [0, 1, 0]] 

bpmfiles=sorted(glob.glob(bpm_path+'bpm*.fits'))
bpmfiles

a=0
for i in bpmfiles:
    a+=1
    bpm=fits.getdata(i)
    mask=np.ones(shape=(bpm.shape))
    # makes data from FITS usable in scipy.ndimage
    bpm1=bpm.byteswap().newbyteorder()
    #labels the strcutures in bpm, and print the number of structures found
    id_regions, num_ids =ndimage.label(bpm1, structure=struct)
    print(num_ids)
    #sums the values of the pixels in each structres individually
    id_sizes =np.array(ndimage.sum(bpm1,id_regions, range(0,num_ids+1)))
    print(id_sizes)
    #choose regions smaller than 6 pixels and makes them zeros
    area_mask = (id_sizes < 6)
    bpm1[area_mask[id_regions]] = 0
    #makes the mask white with blcks holes
    where_0 = np.where(bpm1 == 0)
    where_1 = np.where(bpm1 == 1)
    bpm1[where_0] = 1
    bpm1[where_1] = 0
    fits.writeto(im+'mask'+str(a)+'_dit'+str(exptime)+'.fits',bpm1*mask,overwrite=True)
    
print('###### Makemask done %s ###### '%(name))