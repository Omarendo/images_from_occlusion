# images_from_occlusion
Creates an .stl file(s) which purpose is to show an image only using occlusions. The implementation follows the ideas from the following paper: https://dl.acm.org/doi/10.1145/2030441.2030445. 

The main part of the python implementation builds an .stl file composed of many cylinders of varying height that creates an image from self occlusion. 
Self occlusion means that the object itself creates shadows and highlights by the way it interacts with incoming light. 
In the python code you can input any image, it will be transformed into gray-scale values, re-sized and then from this it will create the .stl files which you can input in a renderer of your choice to understand how it looks and then to a 3d printer. In my case, I tested my results in blender using uniform light source (sun) with 5 watts of power and at a 45 degree with respect to the .stl surface. 

The code also includes a small section that actually builds the cylinder primitives with the dimensions of your choice. These primitives are build using a python library that basically translates the pyhton code for the geometry into OpenScad language. Therefore, this files are all .scad files. Then this files have to be converted to .stl files using OpenScad software. What I did in this step of the code was to create 255 cylinders, each of a different height, that corresponds to the different 255 pixel values. Then when the code is buiilding the final .stl files all it does is to read the pixel image, correlate it to the correct cylinder. Changing the paramters of the primitive cylinders will greatly affect how your final self-occluded is rendered. Take into consideration the limits of the printing capabilites of your printer when tweaking these parameters like too small edges, too small space between cylinders, etc.  

As of now, me code implements a linear pixel-to-cylinder depth ratio and an exponential pixel-to-cylinder depth ratio. There are many other functions to explore. One example that comes to mind is a type of sigmoid or tangential function. 

Current Limitations:There are many. Feel free to do whatever you want to improve/change. There are other parts of the paper I linked above that I did not implement, and that could be a good starting point to improve. 

