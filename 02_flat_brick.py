#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 17:46:13 2021

@author: amartinez
"""

import numpy as np
from astropy.io import fits
band='H'
py_pruebas='/Users/amartinez/Desktop/PhD/HAWKI/The_Brick/py_pruebas/'
#im='/Users/amartinez/Desktop/PhD/HAWK/The_Brick/py_pruebas/'
# raw='/Users/amartinez/Desktop/PhD/HAWKI/The_Brick/02_Flats/054_'+band+'/'
raw='/Users/alvaromartinez/Desktop/Phd/HAWKI/The_Brick/raw/058_H/dit_10/from_gasgano/'
im ='/Users/alvaromartinez/Desktop/PhD/HAWKI/The_Brick/02_Flats/058_'+band+'/dit_10/im/'
name='58_'+band

flat_dic={}
bpm_dic={}
st=1 # 1 for H september 2019

flat_chip1=fits.getdata(raw+'hawki_cal_flat_set0'+str(st)+'_0000.fits',1)
bpm_chip1=fits.getdata(raw+'hawki_cal_flat_bpmflat_set0'+str(st)+'_0000.fits',1)
flat_dic['flat_chip1']=flat_chip1
bpm_dic['bpm_chip1']=bpm_chip1

flat_chip2=fits.getdata(raw+'hawki_cal_flat_set0'+str(st)+'_0000.fits',2)
bpm_chip2=fits.getdata(raw+'hawki_cal_flat_bpmflat_set0'+str(st)+'_0000.fits',2)
flat_dic['flat_chip2']=flat_chip2
bpm_dic['bpm_chip2']=bpm_chip2

flat_chip3=fits.getdata(raw+'hawki_cal_flat_set0'+str(st)+'_0000.fits',4)
bpm_chip3=fits.getdata(raw+'hawki_cal_flat_bpmflat_set0'+str(st)+'_0000.fits',4)
flat_dic['flat_chip3']=flat_chip3
bpm_dic['bpm_chip3']=bpm_chip3


flat_chip4=fits.getdata(raw+'hawki_cal_flat_set0'+str(st)+'_0000.fits',3)
bpm_chip4=fits.getdata(raw+'hawki_cal_flat_bpmflat_set0'+str(st)+'_0000.fits',3)
flat_dic['flat_chip4']=flat_chip4
bpm_dic['bpm_chip4']=bpm_chip4

for i in range(1,5):
    flat=flat_dic['flat_chip'+str(i)]
    bpm=bpm_dic['bpm_chip'+str(i)]
    bad=np.where((flat<0.8)|(flat>1.2))
    bpm[bad]=1
    good=np.where(bpm<1)
    flat_n=flat/np.median(flat[good])
    print(np.median(flat[good]))
    fits.writeto(im+'bpm'+str(i)+'_'+name+'.fits',bpm,overwrite=True)
    fits.writeto(im+'flat'+str(i)+'_'+name+'.fits',flat_n,overwrite=True)
    print(i)
    
print('Flant and bpm ended for %s' %(name))