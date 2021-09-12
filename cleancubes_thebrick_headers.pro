PRO CLEANCUBES_thebrick_headers;, common_path, in_path, out_path, tmp_path, mask_name, N_SIGMA = n_sigma, DEBUG = debug


   ;field = '10'
   band = 'Ks'
   exptime =10
   
   ;files='/im_dark'
   files='/im_jitter_NOgains'
   ;files='/im_jitter_gains'
   ;files='/im_sky_ESOReflex'
   
   ;common_path = '/data/GNS/2015/' + band + '/' + field + '/ims/'
   ;in_path = '/data/GNS/2015/' + band + '/' + field + '/cubes/'
   in_path ='/Users/amartinez/Desktop/PhD/HAWK/The_Brick/06_Reduce/054_'+band+'/dit_'+strn(exptime)+files+'/'
   ;out_path = '/data/GNS/2015/' + band + '/' + field + '/cleaned/'
   out_path='/Users/amartinez/Desktop/PhD/HAWK/The_Brick/07_Cleancubes/054_'+band+'/dit_'+strn(exptime)+files+'/'
   
   
   ;tmp_path = '/data/GNS/2015/' + band + '/' + field + '/tmp/'
   tmp_path='/Users/amartinez/Desktop/PhD/HAWK/The_Brick/tmp/'
   mask_path='/Users/amartinez/Desktop/PhD/HAWK/The_Brick/04_Makemask/054_'+band+'/dit_'+strn(exptime)+'/im/'
   mask_name = 'mask.fits'
   py_pruebas='/Users/amartinez/Desktop/PhD/HAWK/The_Brick/py_pruebas/'
   
   n_sigma = 7. ; value must be high, otherwise valid pixels of bright stars will be corrected (PSF varies between frames)!
   debug = 0; 
   filt_box = 5 ; width of box for sigma filtering



if not(KEYWORD_SET(n_sigma)) then n_sigma = 5.
if not(KEYWORD_SET(box_width)) then box_width = 5
if not(KEYWORD_SET(debug)) then debug = 0
if not(KEYWORD_SET(sigma_dev)) then sigma_dev = 5.



nam = ''

;inlist = 'cubelist.txt'
;outlist = 'cubelist.txt'

in_list='reduced_dit'+strn(exptime)+'.txt'
out_list='reduced_dit'+strn(exptime)+'_cleand.txt'

;mask = readfits(common_path + mask_name)


openw, lun, (out_path + out_list), /get_lun, lun ; open output file to write
openr, inp, (in_path + in_list), /get_lun  ; open input file for reading
cn = 0L
while (not (EOF(inp))) do begin
   ;nlines = FILE_LINES('mydata.dat')
   ;readf, inp, nam
   readf,inp,nam
   ;cube = readfits(in_path + nam, header)'im1_NOsky_chip1_dit2'
   datos= readfits(in_path+nam, EXTEN_NO=strn(0),header0)
   cube = readfits(in_path+nam, EXTEN_NO=strn(1),header)
   sz = size(cube)
   print,'tamaño del cubo',sz
   ;stop
   ;mask = readfits(mask_path + mask_name)
   ;n3 = sz[3]

   ;  Fid and interpolate bad pixels
   ;for j = 0, n3 -1 do begin
   im = cube
   if debug then writefits, tmp_path + 'im_raw.fits', im
   filtered_im = sigma_filter(im, filt_box, N_SIGMA=n_sigma, /ITERATE)
   bad = where((im - filtered_im) ne 0, n_bad)
   if (n_bad gt 0) then begin
      print, 'Found ' + strn(n_bad) + ' bad pixels in image ' + nam + ' of cube ' + nam
      xy = array_indices(im,bad)
      xbad = xy[0,*]
      ybad = xy[1,*]
      im = replace_pix(im,xbad,ybad)
      nok = im
      nok[*,*] = 0
      nok[bad] = 1
      if debug then begin
         ;writefits, tmp_path + 'clean.fits', im
         writefits, tmp_path + 'nok'+nam+'.fits', nok
         STOP
      endif
   endif
   cube= im ;* mask ;no multiplico por las mascaras porque las imagenes ya estan con la mascara. Parece que sigmafilter no altera la mascara.
 cn = cn + 1
writefits, out_path + nam, datos, header0
writefits, out_path + nam, cube, header,/app ;, /COMPRESS
 
printf, lun,  nam 
print, nam
endwhile

free_lun, inp
free_lun, lun

print, "cleancubes.pro ended"

END
