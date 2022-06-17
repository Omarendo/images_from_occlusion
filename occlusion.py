from solid import *
from solid.utils import *
import cv2 as cv
import numpy as np
from stl import mesh

class cylinders:
    #Takes in the pixel value
    def __init__(self, pix):
        self.pix = pix
        #The size of this vector will change if you change the height of the cube that contains the cylinder
        #If you change it and get an error, print(len(my_mesh) and use that number here.
        self.vects = np.zeros(72, dtype=mesh.Mesh.dtype)

    def call_cylinder_linear(self, x, y):
        #imports the stl related to the pixel value
        doc_name = "linear_5mm/" + str(self.pix) + ".stl"
        #Reads the binary stl file
        my_mesh = mesh.Mesh.from_file(doc_name)
        #Moves the stl file by x, y
        my_mesh.translate([x, y, 0])
        # print(my_mesh.data)
        # print(len(my_mesh))
        #Stores the values of the edges of the triangles
        for i in range(my_mesh.data.shape[0]):
            self.vects['vectors'][i] = np.array(my_mesh.data[i][1])

    def call_cylinder_exp(self, x, y):
        #imports the stl related to the pixel value
        doc_name = "expo_5mm/" + str(self.pix) + ".stl"
        #Reads the binary stl file
        my_mesh = mesh.Mesh.from_file(doc_name)
        #Moves the stl file by x, y
        my_mesh.translate([x, y, 0])
        #Stores the values of the edges of the triangles
        for i in range(my_mesh.data.shape[0]):
            self.vects['vectors'][i] = np.array(my_mesh.data[i][1])

class input_image:
    #Imports the image
    def __init__(self, img):
        self.img = img

    #Reads the image
    def read_img(self):
        return cv.imread(self.img, 0)

    #Returns the values of the values of the pixels as matrix
    def matrices_values(self, x, y):
        if x == 0 and y == 0:
            return self.read_img()

    #Prints the image in a window
    def show_img(self):
        cv.imshow("w", self.read_img())
        cv.waitKey(0)
        cv.destroyAllWindows()

# Call this function to create a linar occlusion
def create_linear():
    for i in range(0, int(h / f_h), 5):
        for j in range(0, int(w / f_w), 5):
            # print(i, j)
            # try:
            cube1 = cylinders(avg_img[i][j])
            cube1.call_cylinder_linear(i, j)

            if i == 0:
                final = cube1.vects
            else:
                # Concatenates the previous iteration with the current one.
                final = (np.concatenate([final, cube1.vects]))
                # final = mesh.Mesh(np.concatenate([final, cube1.vects]))
            # except IndexError:
            #     pass
    final_final = mesh.Mesh(final)
    final_final.save("file_output_linear.stl")
    print("Created file_output_linear.stl")

# Call this function to create an exponential occlusion
def create_expo():
    for i in range(0, int(h / f_h), 5):
        for j in range(0, int(w / f_w), 5):
            # print(i, j)
            try:
                cube1 = cylinders(avg_img[i][j])
                cube1.call_cylinder_exp(i, j)

                if i == 0:
                    final = cube1.vects
                else:
                    # Concatenates the previous iteration with the current one.
                    final = (np.concatenate([final, cube1.vects]))
                    # final = mesh.Mesh(np.concatenate([final, cube1.vects]))
            except IndexError:
                pass
    final_final = mesh.Mesh(final)
    final_final.save("file_output_expo.stl")
    print("Created file_output_expo.stl")

#Creates Linear Depth Cylinders as .scad files
def create_linear_cylinders():
    print("Creating 256 cyliders of linear depth increase.")
    for i in range(0, 256):
        with open(str(i)+".scad", "a") as o:
            d = cube([5, 5, 15]) - right(2.5)(forward(2.5)(cylinder(h = np.around(-(14/255)*i + 14, decimals=2) ,  r = 2, segments=15)))
            o.write(scad_render(d))

#Creates Exponential Depth Cylinders as .scad files
def create_expo_cylidners():
    print("Creating 256 cyliders of exponential depth increase.")
    for i in range(0, 256):
        with open(str(i) + ".scad", "a") as o:
            d = cube([5, 5, 15]) - right(2.5)(forward(2.5)(cylinder(h=np.around(14*np.exp(-i/255) - 14*np.exp(-1)*(i/255), decimals=2), r=2, segments=15)))
            o.write(scad_render(d))

if __name__ == '__main__':
    # create_linear_cylinders()
    # create_expo_cylidners()
    #Input image
    a = input_image(str(input("Input input image: ")))
    #Reads the image
    a.read_img()
    #pixel values matrix
    img = a.matrices_values(0, 0)

    #Size of the image (original)
    h = img.shape[1]
    w = img.shape[0]
    print("Original size of image {0} x {1}".format(h, w))
    ans = True
    #Define the factors to make it smaller
    while ans:
        factor_h = float(input("Input height factor to resize smaller: "))
        factor_w = float(input("Input width factor to resize smaller: "))
        f_h = factor_h
        f_w = factor_w
        #Radius of cylinders
        r = 2

        avg_img = cv.resize(img, (int(h/f_h), int(w/f_w)), interpolation=cv.INTER_NEAREST)

        #Shows the re-sized image
        print("Showing re-sized image")
        print("The print will be of these same dimensions")
        print("{0} x {1} in mm".format(avg_img.shape[0], avg_img.shape[1]))
        print()
        print("Press any keyboard key to close window and continue")
        cv.imshow("b", avg_img)
        cv.waitKey(0)
        cv.destroyAllWindows()

        ans = str(input("Would you like to resize?:(y/n): "))
        if ans == 'y':
            ans = True
        else:
            ans = False

    ans2 = str(input("What kind of occlusion? Linear, exponential or both?(l/e/b): "))
    if ans2 == "l":
        create_linear()
    elif ans2 == 'e':
        create_expo()
    elif ans2 == 'b':
        create_linear()
        create_expo()

