#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 13:10:44 2021

@author: amartinez
"""

from astropy.io import fits
import os
import numpy as np
import glob

exptime=10
band='H'
py_pruebas='/Users/alvaromartinez/Desktop/PhD/HAWK/The_Brick/py_pruebas/'
raw_dark='/Users/alvaromartinez/Desktop/PhD/HAWKI/The_Brick/raw/058_H/dit_10/darks/'
im ='/Users/alvaromartinez/Desktop/PhD/HAWKI/The_Brick/01_Dark/058_'+band+'/dit_'+str(exptime)+'/im/'

imf=sorted(glob.glob(raw_dark+'*fits'),key=os.path.getmtime)
dim=0
darks={}
for f in imf:
    #print (f)
    header=fits.open(f)[0].header
    if header['OBJECT']=='DARK' and header['EXPTIME'] == exptime:
        dim+=1
        darks[f]=f
        print(f)
print(dim)

chip1=np.zeros(shape=(len(darks),2048,2048))
chip2=np.zeros(shape=(len(darks),2048,2048))
chip3=np.zeros(shape=(len(darks),2048,2048))
chip4=np.zeros(shape=(len(darks),2048,2048))
a=0
for i in darks:
        
    m_d1=fits.getdata(i,4)
    chip3[a,:,:]=m_d1[:,:]

    m_d2=fits.getdata(i,3)
    chip4[a,:,:]=m_d2[:,:]

    m_d3=fits.getdata(i,1)
    chip1[a,:,:]=m_d3[:,:] 

    m_d4=fits.getdata(i,2)
    chip2[a,:,:]=m_d4[:,:] 
    a+=1
    
d1=np.average(chip1,axis=0)
d2=np.average(chip2,axis=0)
d3=np.average(chip3,axis=0)
d4=np.average(chip4,axis=0)


fits.writeto(im+'dark_chip1_dit'+str(exptime)+'.fits',d1,overwrite=True)
fits.writeto(im+'dark_chip2_dit'+str(exptime)+'.fits',d2,overwrite=True)
fits.writeto(im+'dark_chip3_dit'+str(exptime)+'.fits',d3,overwrite=True)
fits.writeto(im+'dark_chip4_dit'+str(exptime)+'.fits',d4,overwrite=True)

print('########### Dark band %s, dit %s ended ##############' %(band,exptime))