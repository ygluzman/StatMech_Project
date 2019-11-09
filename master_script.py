from PIL import Image
import numpy as np
import os
import glob

#Import functions 
import imaging
from Pivot_algorithm import pivot

img_number = 0

def save_img(img):
    global img_number
    directory = "generated_images"
    img_number += 1
    img.save(directory + "/polymer_" + str(img_number) + ".jpg")
    

def main():
    #Remove images from previous runs
    for image in glob.glob("generated_images/*"):
        os.remove(image)

    np.random.seed(34)

    #Initialize array
    poly=np.array([0,0])
    length=25
    for i in range(1,int(length/2+1)):
        poly = np.vstack((poly,[i,0]))
    for i in [i for i in range(-(int(length/2)),0)][::-1]: #from -5 to zero backwards
        poly = np.vstack(([i,0],poly))

    #Initialize grid
    grid = imaging.grid(poly)
    img = grid.plot_poly(poly)

    #Do some pivot moves!
    for i in range(0,1001):
        poly = pivot(poly,len(poly))
        img = grid.plot_poly(poly)
        save_img(img)


if __name__ == "__main__":
    main()





