#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 11:18:12 2021

@author: amartinez
"""

import numpy as np
import matplotlib.pyplot as plt
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
from astropy.io.fits import getheader
import os



band='H'
exptime=10
py_pruebas='/Users/amartinez/Desktop/PhD/HAWK/The_Brick/py_pruebas/'
raws='/Users/amartinez/Desktop/PhD/HAWK/The_Brick/raw/NPL054_'+band+'/raw_sci_only/'
raw='/Users/amartinez/Desktop/PhD/HAWK/The_Brick/raw/NPL054_'+band+'/raw_sci_only/HAWKI.2019-07-12T06:25:31.454.fits'
bpm_path ='/Users/amartinez/Desktop/PhD/HAWK/The_Brick/03_Fullbpm/054_'+band+'/dit_'+str(exptime)+'/im/'
mask_path='/Users/amartinez/Desktop/PhD/HAWK/The_Brick/04_Makemask/054_'+band+'/dit_'+str(exptime)+'/im/'
flat_path='/Users/amartinez/Desktop/PhD/HAWK/The_Brick/02_Flats/054_'+band+'/im/'
sky_path='/Users/amartinez/Desktop/PhD/HAWK/The_Brick/01_Dark/054_'+band+'/im/' #Sky is the dark in this one.
dark_path='/Users/amartinez/Desktop/PhD/HAWK/The_Brick/01_Dark/054_'+band+'/dit_'+str(exptime)+'/im/'
imag='/Users/amartinez/Desktop/PhD/HAWK/The_Brick/06_Reduce/054_'+band+'/im/'
red_im = '/Users/amartinez/Desktop/PhD/HAWK/The_Brick/06_Reduce/054_'+band+'/dit_'+str(exptime)+'/im_jitter_NOgains/'
sky_sto='/Users/amartinez/Desktop/PhD/HAWK/The_Brick/05_Sky/054_'+band+'/dit_'+str(exptime)+'/im/sky_jitter/'

name='54_'+band

imf=sorted(glob.glob(raws+'*fits'))#,key=os.path.getmtime)
dim=0
dic_im={}
for f in imf:
    #print (f)
    header=fits.open(f)[0].header
    if header['EXPTIME'] == exptime:
        dim+=1
        dic_im['im'+str(dim)+'_expt'+str(exptime)]=f
        print(f)
len(dic_im)

count=0
for v in dic_im:
    count+=1
    print(v)
    for c in range(1,5):
        if c<3:
            j=c
        elif c==3:
            j=4
        elif c==4:
            j=3
        print(2,c,j)
        hdu0 = fits.open(dic_im[v])[0]
        hdu2= fits.ImageHDU()
        new_hdul = fits.HDUList([hdu0, hdu2])
        ima,header=fits.getdata(dic_im[v],j,header=True)
        
        
        #ima,header=fits.getdata(dic_im[v],j,header=True)
        #big_header=fits.getheader(dic_im[v],0)
        flat=fits.getdata(flat_path+'flat'+str(c)+'_'+name+'.fits')
        bpm=fits.getdata(bpm_path+'bpm'+str(c)+'_dit'+str(exptime)+'.fits')
        masc=fits.getdata(mask_path+'mask'+str(c)+'_dit'+str(exptime)+'.fits') 
        sky = fits.getdata(sky_sto+'sky_jitter_chip'+str(c)+'_dit'+str(exptime)+'.fits')
        #sky = fits.getdata(sky_sto+'sky_jitter_chip'+str(c)+'_dit'+str(exptime)+'.fits')
        good = np.where((bpm<1)&(masc>0))
        bad = np.where((bpm>0)&(masc>0))
        #good = np.where((dic_bpm['bpm'+str(c)]<1)&(dic_mask['mask'+str(c)]>0))
        #bad = np.where((dic_bpm['bpm'+str(c)]>0)&(dic_mask['mask'+str(c)]>0))
        dark = fits.getdata(dark_path+'dark_chip'+str(c)+'_dit'+str(exptime)+'.fits')
        
        im=ima-dark
        #im=im1
        im[good]=im[good]/flat[good]
        for x, y in zip(bad[0], bad[1]) : # sustituye cada bad pixel por la mediana en una caja de 3X3 alrededor
            cacho = im[max(0,x-2):x+3, max(0,y-2):y+3] 
            im[x,y] = np.median([cacho])
        sky[good]=sky[good]/flat[good]
        fits.writeto(py_pruebas+'sky_flat_im%s_chip%s.fits'%(count,c),sky,overwrite=True)
        im=im-sky
        #im_a=im-sky
        '''
        im_a[good]=im_a[good]/flat[good]
        '''
        for x, y in zip(bad[0], bad[1]) : # sustituye cada bad pixel por la mediana en una caja de 3X3 alrededor
            cacho = im[max(0,x-2):x+3, max(0,y-2):y+3]
            im[x,y] = np.median([cacho])
        new_hdul.writeto(red_im+'im'+str(count)+'_NOgains_chip'+str(c)+'_dit'+str(exptime)+'.fits',overwrite=True)
        fits.update(red_im+'im'+str(count)+'_NOgains_chip'+str(c)+'_dit'+str(exptime)+'.fits',im*masc,header,1,overwrite=True)
        #fits.writeto(py_pruebas+'reduc_im_'+str(count)+'_NOgains_chip'+str(c)+'_dit'+str(exptime)+'.fits',im*masc,header+big_header,overwrite=True)
print('#### Done with reducction No Gains of %s sec DIT images ####'%(exptime))
        