# Polygon Label Tool
This is a label tool for croping objects and polygons. 
Since it is for a private project, you should contact guangyuzhonghikari@gmail.com first if you want to use it for any reason.
## Usage
* Set input folder path and press "OK". The default input path is "../test/".
* Select one file in the list widget. You can also use "<<" and ">>" to check forward and backward.
* Crop the object in the left window.
* Press left mouse button to select polygon. If one polygon is done, press "Z" to save it. If not satisfied, press "X" to delete it.
* Press "Star Poly" to save the result. The default save path is '../test/save/'
## Dependence
This code is written with PySide. It has not been released, thus you have to compile it.

# grab_add.py
##usage
* Set input path use terminal. Example, './grab_add.py' ' ' './test/'.
* Use right button to crop candidate region, then use left button to draw foreground region (press 0: backward, press 1: foreground).
* Press 'z': start grabcut
* Press 'a': save current results
* Press 'j': goto last image
* Press 'k': goto next image
* Press 'r': reset all the parameters for this image
* Press 's': imwrite current results into input_path/grab/imagename_label.png

	   
	   
	   