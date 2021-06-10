#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 22:47:58 2021

@author: amartinez
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 09:25:53 2021

@author: amartinez
"""

import numpy as np
from astropy.io import fits
import glob
import random
import statistics

from astropy import stats as sta
#%%
band='H'
exptime=10
py_pruebas='/Users/amartinez/Desktop/PhD/HAWK/The_Brick/py_pruebas/'
raws='/Users/amartinez/Desktop/PhD/HAWK/The_Brick/raw/NPL054_'+band+'/raw_sci_only/'
raw='/Users/amartinez/Desktop/PhD/HAWK/The_Brick/raw/NPL054_'+band+'/raw_sci_only/HAWKI.2019-07-12T06:25:31.454.fits'
bpm_path ='/Users/amartinez/Desktop/PhD/HAWK/The_Brick/03_Fullbpm/054_'+band+'/dit_'+str(exptime)+'/im/'
mask_path='/Users/amartinez/Desktop/PhD/HAWK/The_Brick/04_Makemask/054_'+band+'/dit_'+str(exptime)+'/im/'
flat_path='/Users/amartinez/Desktop/PhD/HAWK/The_Brick/02_Flats/054_'+band+'/im/'
sky_path='/Users/amartinez/Desktop/PhD/HAWK/The_Brick/01_Dark/054_'+band+'/dit_'+str(exptime)+'/im/' #Sky is the dark in this one.
dark_path='/Users/amartinez/Desktop/PhD/HAWK/The_Brick/01_Dark/054_'+band+'/dit_'+str(exptime)+'/im/'
im_sto='/Users/amartinez/Desktop/PhD/HAWK/The_Brick/05_Sky/054_'+band+'/dit_'+str(exptime)+'/im/sky_jitter/'
#imag='/Users/amartinez/Desktop/PhD/HAWK/The_Brick/06_Reduce/054_'+band+'/im/'
name='54_'+band
sigma_dev=20


dic_mask={}
dic_bpm={}
dic_good={}
dic_bad={}
dic_dark={}
dic_flat={}
for m in range(1,5):
    dic_mask['mask'+str(m)]=fits.getdata(mask_path+'mask'+str(m)+'_dit'+str(exptime)+'.fits') 
    dic_bpm['bpm'+str(m)]=fits.getdata(bpm_path+'bpm'+str(m)+'_dit'+str(exptime)+'.fits')
    dic_dark['dark'+str(m)]=fits.getdata(dark_path+'dark_chip'+str(m)+'_dit'+str(exptime)+'.fits')
    dic_good['good'+str(m)]=np.where((dic_bpm['bpm'+str(m)]<1)&(dic_mask['mask'+str(m)]>0))
    dic_bad['bad'+str(m)]=np.where((dic_bpm['bpm'+str(m)]>0)&(dic_mask['mask'+str(m)]>0))
    #dic_bad['bad'+str(m)]=np.where((dic_bpm['bpm'+str(m)]>0)&(dic_mask['mask'+str(m)]<1))
    dic_flat['flat'+str(m)]=fits.getdata(flat_path+'flat'+str(m)+'_'+name+'.fits')
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
#%%
dic_chip={}
t=0
for ch in range(1,5):
    dic_chip['chip'+str(ch)]=np.zeros(shape=(len(dic_im),2048,2048))
for c in dic_im:
    print(c)
    for j in range(0,4):
        chip_cube=dic_chip['chip1']
        chip=fits.getdata(dic_im[c],1)
        header1=fits.getheader(dic_im[c],1)
        chip_cube[t,:,:]=chip
        fits.writeto(im_sto +'im_chip_1_dit'+str(exptime)+'.fits',chip_cube,header1,overwrite=True)
        
        chip_cube=dic_chip['chip2']
        chip=fits.getdata(dic_im[c],2)
        header2=fits.getheader(dic_im[c],2)
        chip_cube[t,:,:]=chip
        fits.writeto(im_sto+'im_chip_2_dit'+str(exptime)+'.fits',chip_cube,header2,overwrite=True)
        
        chip_cube=dic_chip['chip3']
        chip=fits.getdata(dic_im[c],4)
        header3=fits.getheader(dic_im[c],4)
        chip_cube[t,:,:]=chip
        fits.writeto(im_sto+'im_chip_3_dit'+str(exptime)+'.fits',chip_cube,header3,overwrite=True)
        
        chip_cube=dic_chip['chip4']
        chip=fits.getdata(dic_im[c],3)
        header4=fits.getheader(dic_im[c],3)
        chip_cube[t,:,:]=chip
        fits.writeto(im_sto+'im_chip_4_dit'+str(exptime)+'.fits',chip_cube,header4,overwrite=True)
    t+=1
        
gains=np.zeros(shape=(4,1))
for chip in range(1,5):
    im_chip,header=fits.getdata(im_sto+'im_chip_'+str(chip)+'_dit'+str(exptime)+'.fits',header=True)
    dark=dic_dark['dark'+str(chip)]
    im_chip=im_chip-dark
    
    prueba_dark=im_chip[0,:,:]-dark
    p_dark=im_chip-dark
    fits.writeto(py_pruebas+'prueba_dark.fits',prueba_dark,overwrite=True)
    fits.writeto(py_pruebas+'p_dark.fits',p_dark,overwrite=True)
    
    good=dic_good['good'+str(chip)]
    flat=dic_flat['flat'+str(chip)]
    masc=dic_mask['mask'+str(chip)]
    sky_chip=np.amin(im_chip,axis=0)
    sky_vector=sky_chip[good]
    a=sta.sigma_clipped_stats(sky_vector, sigma=3, maxiters=5) 
    b=sta.sigma_clipped_stats(sky_chip, sigma=3, maxiters=5) 
    skysigma=a[2]
    skymod=statistics.mode(sky_vector)
    
    #malos =np.where(sky_chip>(abs(a[0]-skysigma*sigma_dev))&(masc>0))
    #malos=np.where((sky_vector<(skymod+skysigma*sigma_dev))&(masc>0))
    #malos_p=np.where((sky_chip<skymod-skysigma*sigma_dev)&(masc>0))
    #malos_g=np.where((sky_chip>skymod+skysigma*sigma_dev)&(masc>0))
    #malos_p=np.where((sky_chip<15*a[2])&(masc>0))
    malos_p=np.where(((sky_chip<a[0]-5*a[2])|(sky_chip>a[0]+5*a[2]))&(masc>0))
    join=zip(malos_p[0],malos_p[1])
    for m in join:
        sky_chip[m]=a[1]+skysigma*random.random()
    print(len(malos_p[0]))
    sky_chip[malos_p]=a[0]+skysigma*random.random()
    #sky_chip[malos_g]=a[0]+skysigma*random.random()
    skymed=np.median(sky_chip[good])
    print('Esto es la mediana %.2f'%(skymed))
    skymod=statistics.mode(sky_vector)
    print('esto es la moda......', skymod)
    print ('esto es sigma........',skysigma)
    gains[chip-1]=skymod
    #sky_chip[good]=sky_chip[good]/flat[good] #no dividimos aún por el flat. Lo hacemos con reduce
    print(sky_chip.shape)
    fits.writeto(im_sto+'sky_jitter_chip'+str(chip)+'_dit'+str(exptime)+'.fits',sky_chip*masc,header,overwrite=True)
    fits.writeto(im_sto+'sky_jitter_norm_chip'+str(chip)+'_dit'+str(exptime)+'.fits',(sky_chip/skymed)*masc,header,overwrite=True)
media =np.mean(gains)
gains = (gains/media)
print(gains)
gan = open(im_sto+'gains_dit'+str(exptime)+'.txt', "w")
for i in gains:
     np.savetxt(gan, i)
gan.close()    

print('##### Sky jitter band %s DIT %s ended #####'%(band, exptime))