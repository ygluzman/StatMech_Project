from PIL import Image
import numpy as np

#Import test
# import double_func_test
# from double_func_test import double
# print(double_func_test.double(2),double(2))

class grid:
    
    """
    Grid Class
    Initializes with a polymer. E.g. x=grid(poly)
    Makes a grid centered on the CoM with height and width 4x the distance of the furthest point from the CoM
    
    Plot polymers with method self.plot_poly
    Ex. img=self.plot_poly(poly)
    
    Instance variables:
    self.size_of_pixel_array -- size of square pixel array (1000)
    self.blank_grid -- image of blank grid
    self.pixels_between_gridpoints -- number of pixels from one gridpoint to another
    self.CoM -- previous center of mass (used for continuity between images)
    self.CoIm -- center of image, where the CoM lies in the pixel array
    """
    
    def make_grid(self,polymer):
        """
        Initializes with a polymer. E.g. x=grid(poly)
        Makes a grid centered on the CoM
        with height and width 4x the distance of the furthest point from the CoM
        """

        poly = polymer

        #Settings for image:
        self.size_of_pixel_array=1000
        white=(255,255,255)
        greyval=205
        grey=(greyval,greyval,greyval)
        black=(0,0,0)

        #Make a RGB white image:
        img=Image.new('RGB',(self.size_of_pixel_array,self.size_of_pixel_array))
        pixels=img.load()
        for i in range(0,img.size[0]):
            for j in range(0,img.size[1]):
                pixels[i,j] = white

        #Calculate CoM of polymer:
        CoM = np.sum(poly,axis=0)//len(poly) #Calculate centroid/center of mass
        #Floor dividing :)

        #Calculate distances from CoM to make appropriate gridding
        distances_from_CoM = np.sqrt(np.sum(((poly - CoM)**2),axis=1))
        max_dist = distances_from_CoM.max()
        size_of_grid = 4*max_dist
        periodicity = self.size_of_pixel_array//size_of_grid
        for i in range(0,img.size[0]):
            for j in range(0,img.size[1]):
                if (i%periodicity == 0) or (j%periodicity == 0):
                    pixels[i,j] = grey
        self.pixels_between_gridpoints = periodicity

        #Assign blank grid, CoM, and CoIm
        self.blank_grid = img
        self.CoM = CoM
        self.pixels_between_gridpoints = periodicity
        self.CoIm = [int(size_of_grid//2*self.pixels_between_gridpoints),int(size_of_grid//2*self.pixels_between_gridpoints)]
        
    def plot_poly(self,polymer):
        """
        Takes a polymer array, returns the polymer plotted onto a grid as an image
        """
    
        #Settings
        black=(0,0,0)
        img = self.blank_grid.copy()
        pixels = img.load()
#         point_width = [-1,0,1]
        
        if self.pixels_between_gridpoints >= 20: 
            point_width = [-3,-2,-1,0,1,2,3]
        else:
            point_width = [-1,0,1]

        #Center the polymer around the CoM in order to plot
        poly = polymer-self.CoM
        pixel_locations = np.ones([len(poly),2])
        pixel_locations[:,0] = self.CoIm[0]
        pixel_locations[:,1] = self.CoIm[1]
        pixel_locations = pixel_locations + poly*self.pixels_between_gridpoints

        #Check if any lie out of range and re-center if so:
        test = pixel_locations + self.pixels_between_gridpoints
        check = test >= self.size_of_pixel_array
        if check.any():
            print("Re-centering, hit max!")
            self.CoM = np.sum(polymer,axis=0)//len(polymer)
            poly = polymer-self.CoM
            # print(polymer)
            # print(self.CoM)
            # print(poly)
            pixel_locations = np.ones([len(poly),2])
            pixel_locations[:,0] = self.CoIm[0]
            pixel_locations[:,1] = self.CoIm[1]
            pixel_locations = pixel_locations + poly*self.pixels_between_gridpoints
            # print(pixel_locations)

        test = pixel_locations - self.pixels_between_gridpoints
        check = test <= 0
        if check.any():
            print("Re-centering, hit 0!")
            self.CoM = np.sum(polymer,axis=0)//len(polymer)
            # print(polymer)
            # print(self.CoM)
            # print(poly)
            poly = polymer-self.CoM
            pixel_locations = np.ones([len(poly),2])
            pixel_locations[:,0] = self.CoIm[0]
            pixel_locations[:,1] = self.CoIm[1]
            pixel_locations = pixel_locations + poly*self.pixels_between_gridpoints
            # print(pixel_locations)          
                
        #Draw the Polymer!
        for atom_number in range(0,len(poly)):
            
            #Set-up
            atom = poly[atom_number]
            try:
                next_atom = poly[atom_number + 1]
            except IndexError:
                pass

            loc_x = pixel_locations[atom_number][0]
            loc_y = pixel_locations[atom_number][1]

            # print(loc_x,loc_y)
            
            #Fill in the point
            for i in point_width:
                for j in point_width:
#                     print(loc_x+i,loc_y+j)
                    pixels[loc_x + i, loc_y + j] = black
             
            #Conenect the dots! lol
            if atom_number != len(poly)-1:
                #The next point will either be to the left, right, up, or down
                #We want to fill in the pixels in-between
                diff = next_atom - atom
                
                if (diff[0] == 0) and (diff[1] == 1):
#                     print("Up!")
                    for i in range(1,int(self.pixels_between_gridpoints)):
                        pixels[loc_x, loc_y + i] = black
                elif (diff[0] == 0) and (diff[1] == -1):
#                     print("Down!")
                    for i in range(1,int(self.pixels_between_gridpoints)):
                        pixels[loc_x, loc_y - i] = black
                elif (diff[0] == 1) and (diff[1] == 0):
#                     print("Right!")
                    for i in range(1,int(self.pixels_between_gridpoints)):
                        pixels[loc_x + i, loc_y] = black
                elif (diff[0] == -1) and (diff[1] == 0):
#                     print("Left!")
                    for i in range(1,int(self.pixels_between_gridpoints)):
                        pixels[loc_x - i, loc_y] = black
                else:
                    print("Error! Polymer array is non-continuous.")
            
        return img
        
    def __init__(self,polymer):
        self.make_grid(polymer)
        
#Testing

def main():
    poly=np.array([0,0])
    length=25
    for i in range(1,int(length/2+1)):
        poly = np.vstack((poly,[i,0]))
    for i in [i for i in range(-(int(length/2)),0)][::-1]: #from -5 to zero backwards
        poly = np.vstack(([i,0],poly))

    test_grid = grid(poly)
    img = test_grid.plot_poly(poly)
    img.show()


if __name__ == "__main__":
    main()





