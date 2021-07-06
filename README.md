# Zoccalli_reduction
Reduction of Zoccali´s data
in : /Users/amartinez/Desktop/PhD/HAWK/The_Brick/scripts_git/Zoccalli_reduction

Pipeline The Brick for regular reduction. The sky has been computed as the lowest value of the jittered images and substracted directly from the images. 

1. Flats and Dark with GASGANO
2. 01 to 06 with python.

01._DarK
02._Flats
03._Fullbpm
04._Makemask
05._Sky
06._Reduce.IMPORTANT: go to folder and make a list of reduced files 'reduced_dit10.txt'.
          NOTE to myself:change the script so you don have to make the list, you dull bastard
07._Cleancubes( con clean_cubes_headers_thebrick.pro)#TRY USING lacosmic 'python'#

