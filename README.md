# Zoccalli_reduction
Reduction of Zoccali´s data
in : /Users/amartinez/Desktop/PhD/HAWK/The_Brick/scripts_git/Zoccalli_reduction

Pipeline The Brick for regular reduction. The sky has been computed as the lowest value of the jittered images and substracted directly from the images. 

1. Los flats y dark se hacen con gasgano
2. Del 01 al 06 se hace con python con los correspondientes scrips in la carpeta scrips
3. 07 se hace con IDL con los scrips que se indican abajo.

01_DarK
02_Flats
03_Fullbpm
04_Makemask
05_Sky
06_Reduce
07_Cleancubes( con clean_cubes_headers_thebrick.pro)

