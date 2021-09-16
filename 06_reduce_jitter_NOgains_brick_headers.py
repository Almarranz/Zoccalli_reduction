#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 11:18:12 2021

@author: amartinez
"""
#%%
import numpy as np
from astropy.io import fits
import glob
import os



band='H'
exptime=10
py_pruebas='/Users/alvaromartinez/Desktop/PhD/HAWKI/The_Brick/py_pruebas/'
raws='/Users/alvaromartinez/Desktop/PhD/HAWKI/The_Brick/raw/058_'+band+'/dit_10/jitter_obs/'
#raws='/Users/alvaromartinez/Desktop/PhD/HAWKI/The_Brick/raw/NPL058_'+band+'/raw_sci_only/HAWKII.2019-07-12T06:25:31.458.fits'
bpm_path ='/Users/alvaromartinez/Desktop/PhD/HAWKI/The_Brick/03_Fullbpm/058_'+band+'/dit_'+str(exptime)+'/im/'
mask_path='/Users/alvaromartinez/Desktop/PhD/HAWKI/The_Brick/04_Makemask/058_'+band+'/dit_'+str(exptime)+'/im/'
flat_path='/Users/alvaromartinez/Desktop/PhD/HAWKI/The_Brick/02_Flats/058_'+band+'/dit_10/im/'
sky_path='/Users/alvaromartinez/Desktop/PhD/HAWKI/The_Brick/01_Dark/058_'+band+'/im/' #Sky is the dark in this one.
dark_path='/Users/alvaromartinez/Desktop/PhD/HAWKI/The_Brick/01_Dark/058_'+band+'/dit_'+str(exptime)+'/im/'
imag='/Users/alvaromartinez/Desktop/PhD/HAWKI/The_Brick/06_Reduce/058_'+band+'/im/'
red_im = '/Users/alvaromartinez/Desktop/PhD/HAWKI/The_Brick/06_Reduce/058_'+band+'/dit_'+str(exptime)+'/im_jitter_NOgains/'
sky_sto='/Users/alvaromartinez/Desktop/PhD/HAWKI/The_Brick/05_Sky/058_'+band+'/dit_'+str(exptime)+'/im/'

name='58_'+band

#%%
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
        print('DIT %s,ext %s, chip %s'%(exptime,c,j))
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
        
        im=ima-sky
        #im=im1
        im[good]=im[good]/flat[good]
        for x, y in zip(bad[0], bad[1]) : # sustituye cada bad pixel por la mediana en una caja de 3X3 alrededor
            cacho = im[max(0,x-2):x+3, max(0,y-2):y+3] 
            im[x,y] = np.median([cacho])
        
        new_hdul.writeto(red_im+'im'+str(count)+'_NOgains_chip'+str(c)+'_dit'+str(exptime)+'.fits',overwrite=True)
        fits.update(red_im+'im'+str(count)+'_NOgains_chip'+str(c)+'_dit'+str(exptime)+'.fits',im*masc,header,1,overwrite=True)
        #fits.writeto(py_pruebas+'reduc_im_'+str(count)+'_NOgains_chip'+str(c)+'_dit'+str(exptime)+'.fits',im*masc,header+big_header,overwrite=True)
print('#### Done with reducction No Gains of %s sec DIT images ####'%(exptime))
#%%
files = sorted(glob.glob(red_im+'*.fits'),key=os.path.getmtime)
files =[os.path.basename(files[i]) for i in range(len(files))]
with open (red_im+'reduced_dit10.txt', 'w') as in_files:
    for eachfile in files: in_files.write(eachfile+'\n')




