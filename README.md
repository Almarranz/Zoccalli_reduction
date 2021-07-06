# Zoccalli_reduction
Reduction of Zoccali´s data
in : /Users/amartinez/Desktop/PhD/HAWK/The_Brick/scripts_git/Zoccalli_reduction

Pipeline The Brick for regular reduction. The sky has been computed as the lowest value of the jittered images and substracted directly from the images. 

1. Flats and Dark with GASGANO
2. 01 to 06 with python.

01. _dark_brick.py
02. _flat_brick.py
03. _fulbpm_brick.py
04. _makemask_brick.py
05. _sky_jitter_lowest.py
06. _reduce_jitter_NOgains_brick_headers.py
07. _cleancubes_thebrick_headers.pro #TRY USING lacosmic 'python'#

